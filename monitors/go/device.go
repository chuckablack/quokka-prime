package main

import "fmt"

type deviceStruct struct {
	name    string
	vendor  string
	model   string
	os      string
	version string
	ip      string
}

func main() {

	dev := deviceStruct{
		name:    "sbx-n9kv-ao",
		vendor:  "cisco",
		model:   "Nexus9000 C9300v Chassis",
		os:      "nxos",
		version: "9.3(3)",
		ip:      "10.1.1.1",
	}

	fmt.Println()
	fmt.Println("device:", dev)
	fmt.Println("device name:", dev.name)

	device := make(map[string]string)
	device["name"] = "sbx-n9kv-ao"
	device["vendor"] = "cisco"
	device["model"] = "Nexus9000 C9300v Chassis"
	device["os"] = "nxos"
	device["version"] = "9.3(3)"
	device["ip"] = "10.1.1.1"

	fmt.Println()
	fmt.Println("device:", device)
	fmt.Println("device name:", device["name"])

	fmt.Println()
	for key, value := range device {
		fmt.Println(key, ":", value)
	}
	fmt.Println()

	for key, value := range device {
		fmt.Printf("%16s : %-s\n", key, value)
	}
	fmt.Println()

}
