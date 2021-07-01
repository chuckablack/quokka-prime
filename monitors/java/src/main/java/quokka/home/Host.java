package quokka.home;

import org.codehaus.jackson.annotate.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Host {
    public String hostname = "";
    public String ip_address = "";
    public String mac_address = "";
    public Boolean availability = false;
    public String response_time = "";
    public String last_heard = "";
    public String open_tcp_ports = "";
}
