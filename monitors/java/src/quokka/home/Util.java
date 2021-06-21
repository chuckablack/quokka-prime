package quokka.home;

import org.codehaus.jackson.map.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Util {

    public static void updateHost(Host host) {

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
}
