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
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.concurrent.TimeUnit;

public class Monitor {

    private void discoverHosts() {

        InetAddress localhost;

        try {
            localhost = InetAddress.getLocalHost();
        } catch (java.net.UnknownHostException e) {
            System.out.println("!!! discoverHosts: unable to get my local IP, error: " + e);
            return;
        }

        byte[] ip = localhost.getAddress();

        for (int i = 1; i <= 254; i++) {

            InetAddress address;
            ip[3] = (byte) i;
            try {
                address = InetAddress.getByAddress(ip);
            } catch (java.net.UnknownHostException e) {
                System.out.println("!!! discoverHosts: unable to get IP: " + Arrays.toString(ip) + ", error: " + e);
                continue;
            }

            try {

                long startTime = System.currentTimeMillis();
                if (address.isReachable(3000)) {

                    Host host = new Host();
                    host.hostname = address.getHostName();
                    host.ip_address = address.getHostAddress();

                    host.availability = true;
                    host.response_time = String.valueOf((float) (System.currentTimeMillis() - startTime) / 1000);

                    Date date = new Date();
                    SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS");
                    host.last_heard = formatter.format(date);

                    updateHost(host);
                    System.out.println("discoverHosts: Discovered: " + host.hostname + " RspTime: " + host.response_time);

                }

            } catch (java.io.IOException e) {
                System.out.println("!!! discoverHosts: exception pinging host: " + address.getHostAddress() + ", error: " + e);
            }
        }
    }

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

    private void pingHosts(ArrayList<Host> hosts) {

        for (Host host : hosts) {

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

            updateHost(host);
        }
    }

    private void updateHost(Host host) {

        ObjectMapper mapper = new ObjectMapper();
        String jsonHost;

        try {
            jsonHost = mapper.writeValueAsString(host);
        } catch (java.io.IOException e) {
            System.out.println("!!! Error converting host to JSON: " + host.hostname + " Error: " + e);
            return;
        }

        var client = HttpClient.newHttpClient();
        var url = "http://localhost:5001/hosts?hostname=" + host.hostname;
        var putRequest =  HttpRequest.newBuilder(URI.create(url))
                .header("Content-Type", "application/json")
                .PUT(HttpRequest.BodyPublishers.ofString(jsonHost))
                .build();

        HttpResponse<String> response;

        try {
            response = client.send(putRequest, HttpResponse.BodyHandlers.ofString());
        } catch (java.io.IOException | java.lang.InterruptedException e) {
            System.out.println("!!! updateHost: Error updating host: " + host.hostname + " Error: " + e);
            return;
        }

        if (response.statusCode() != 204) {
            System.out.println("!!! updateHost: Error status code received: " + response.statusCode());
            return;
        }

        System.out.println("updateHost: Host updated: " + host.hostname);
    }

    public void monitorHosts() {

        int discoveryWaitMinutes = 0;
        while (true) {

            if (discoveryWaitMinutes == 0) {
                discoverHosts();
                discoveryWaitMinutes = 60;
            }

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
                discoveryWaitMinutes--;
            } catch (InterruptedException ignored) {
                break;
            }
        }

    }
}
