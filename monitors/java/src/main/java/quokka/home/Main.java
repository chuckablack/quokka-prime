package quokka.home;

public class Main {

    public static void main(String[] args) {

        DiscoveryThread discoveryThread = new DiscoveryThread();
        discoveryThread.start();

        Monitor monitor = new Monitor();
        monitor.monitorHosts();

   }
}
