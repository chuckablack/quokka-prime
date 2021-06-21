package quokka.home;

import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.type.TypeReference;

import java.io.IOException;
import java.net.InetAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.concurrent.TimeUnit;

public class Monitor {

    private HashMap<String, Host> getHosts() {

        var client = HttpClient.newHttpClient();
        var request = HttpRequest.newBuilder(URI.create("http://localhost:5001/hosts"))
                .header("accept", "application/json")
                .build();

        HttpResponse<String> response;
        HashMap<String, Host> hosts = new HashMap<>();

        try {
            response = client.send(request, HttpResponse.BodyHandlers.ofString());
        } catch (java.io.IOException | java.lang.InterruptedException e) {
            System.out.println("!!! getHosts: Error retrieving hosts: " + e);
            return hosts;
        }

        if (response.statusCode() != 200) {
            System.out.println("!!! getHosts: Error status code received: " + response.statusCode());
            return hosts;
        }

        var jsonHosts = response.body();
        ObjectMapper mapper = new ObjectMapper();
        try {
            hosts = mapper.readValue(jsonHosts, new TypeReference<HashMap<String, Host>>(){});
        } catch (java.io.IOException e) {
            System.out.println("!!! getHosts: Error processing JSON output: " + e);
        }
        return hosts;
    }

    private void pingHost(Host host) {

        try {
            InetAddress hostInetAddr = InetAddress.getByName(host.hostname);
            long startTime = System.currentTimeMillis();
            if (hostInetAddr.isReachable(3000)) {
                host.availability = true;
                host.response_time = String.valueOf((float) (System.currentTimeMillis() - startTime) / 1000);

                Date date = new Date();
                SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS");
                host.last_heard = formatter.format(date);

                System.out.println("pingHosts: Result: " + host.hostname + " RspTime: " + host.response_time);
            } else {
                host.availability = false;
                System.out.println("pingHosts: Result: " + host.hostname + " Unavailable");
            }

        } catch (IOException e) {
            host.availability = false;
            System.out.println("!!! pingHosts: Unable to ping host from hostname: " + host.hostname + " Error: " + e);
        }

    }
    private void pingHosts(ArrayList<Host> hosts) {

        for (Host host : hosts) {
            pingHost(host);
            Util.updateHost(host);
        }
    }

   public void monitorHosts() {

        while (true) {

            System.out.println("\n___ Retrieving hosts from quokka-prime server _________________\n");
            var hosts = getHosts();
            for (Host host : hosts.values())
                System.out.println("host: "+host.hostname+", ip: "+host.ip_address+", mac: "+host.mac_address);
            System.out.println();

            System.out.println("\n___ Monitoring hosts _________________\n");
            pingHosts(new ArrayList<>(hosts.values()));

            System.out.println("\nbeginning to monitor " + hosts.size() + " devices");

            try {
                TimeUnit.SECONDS.sleep(60);
            } catch (InterruptedException ignored) {
                break;
            }
        }

    }
}
