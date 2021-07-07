package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"os/exec"
	"regexp"
	"sync"
	"time"
)

type hostDef struct {
	Hostname     string
	ip           string
	mac          string
	availability string
	resopnseTime string
	openPorts    string
}

type hostsDef struct {
	hosts map[string]hostDef
}

func getHosts() map[string]map[string]interface{} {

	fmt.Println("getHosts: requesting hosts from quokka server")
	rsp, err := http.Get("http://localhost:5001/hosts")
	if err != nil {
		fmt.Println("getHosts: request to get hosts failed:", err)
		return nil
	}
	defer rsp.Body.Close()

	fmt.Println("rsp:", rsp)
	fmt.Println("body:", rsp.Body)

	bodyBytes, err := ioutil.ReadAll(rsp.Body)
	if err != nil {
		fmt.Println("getHosts: attempt to get JSON body failed:", err)
		return nil
	}
	fmt.Println("body string:", string(bodyBytes))

	mapHosts := make(map[string]map[string]interface{})
	err = json.Unmarshal([]byte(bodyBytes), &mapHosts)
	if err != nil {
		fmt.Println("getHosts: attempt Unmarshal failed:", err)
		return nil
	}
	fmt.Println("mapHosts:", mapHosts)

	return mapHosts
}

func pingHost(waitGroup *sync.WaitGroup, host map[string]interface{}) {

	defer waitGroup.Done()

	fmt.Fprintln(os.Stdout, "---- pinging host:", host["hostname"])
	out, err := exec.Command("ping", "-c3", "-n", "-i0.5", "-W2", host["hostname"].(string)).Output()
	fmt.Fprintln(os.Stdout, host["hostname"], "err:", err)
	fmt.Fprintln(os.Stdout, host["hostname"], "out:", string(out))

	if err != nil {
		host["availability"] = false
		fmt.Fprintln(os.Stdout, "!!! error pinging host:", err)
	} else {
		host["availability"] = true
		host["response_time"] = getResponseTime(string(out))
		host["last_heard"] = time.Now().String()[:23]
	}

	updateHost(host)
}

func getResponseTime(pingOutput string) string {

	m, _ := regexp.Compile("min/avg/max/mdev = ([0-9]*[.][0-9]*)/([0-9]*[.][0-9]*)")
	rspTimeMatch := m.FindStringSubmatch(pingOutput)
	if len(rspTimeMatch) >= 2 {
		return rspTimeMatch[2]
	} else {
		return "0.000"
	}

}

func updateHost(host map[string]interface{}) {

	fmt.Fprintln(os.Stdout, "---> updating host:", host["hostname"])
	for key, value := range host {
		switch value.(type) {
		case bool:
			fmt.Printf("%16s : %t\n", key, value)
		case string:
			fmt.Printf("%16s : %-s\n", key, value)
		}
	}

	jsonHost, err := json.Marshal(host)
	if err != nil {
		fmt.Fprintln(os.Stdout, "!!! error marshalling host:", err)
	}

	client := &http.Client{}
	req, _ := http.NewRequest(http.MethodPut, "http://localhost:5001/hosts?hostname="+host["hostname"].(string), bytes.NewBuffer(jsonHost))

	req.Header.Set("Content-Type", "application/json")
	rsp, err := client.Do(req)
	if err != nil {
		fmt.Fprintln(os.Stdout, "!!! error updating host:", err)
	}
	if rsp.StatusCode != 204 {
		fmt.Fprintln(os.Stdout, "!!! error updating host, unexpected status code:", rsp.Status)
	}

}

func main() {

	for {
		mapHosts := getHosts()
		if mapHosts != nil {

			// for _, host := range mapHosts {
			// 	fmt.Fprintln(os.Stdout, "---- host:", host["hostname"], "--------------------")
			// 	fmt.Fprintln(os.Stdout, "---- host:", host)
			// 	for key, value := range host {
			// 		switch value.(type) {
			// 		case bool:
			// 			fmt.Printf("%16s : %t\n", key, value)
			// 		case string:
			// 			fmt.Printf("%16s : %-s\n", key, value)
			// 		}
			// 	}
			// }

			var waitGroup sync.WaitGroup
			for _, host := range mapHosts {
				waitGroup.Add(1)
				go pingHost(&waitGroup, host)
			}
			waitGroup.Wait()
			fmt.Fprintln(os.Stdout, "---> all pings completed")

		}
		time.Sleep(60 * time.Second)
	}

}
