package quokka.home;

public class Main {

    public static void main(String[] args) {

        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                System.out.println("Shutting down gracefully...");
            }
        });

        Monitor monitor = new Monitor();
        monitor.monitorHosts();

   }
}
