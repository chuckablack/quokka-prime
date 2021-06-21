package quokka.home;

public class Main {

    public static void main(String[] args) {

        Runtime.getRuntime().addShutdownHook(new Thread(() -> System.out.println("Shutting down gracefully...")));

        DiscoveryThread discoveryThread = new DiscoveryThread();
        discoveryThread.start();

        Monitor monitor = new Monitor();
        monitor.monitorHosts();

   }
}
