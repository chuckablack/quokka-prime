package quokka.home;

import java.net.InetAddress;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;
import java.util.concurrent.TimeUnit;

public class DiscoveryThread extends Thread {

    public DiscoveryThread() {
        System.out.println("Discovery thread created");
    }

    boolean terminate;

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

                    Util.updateHost(host);
                    System.out.println("discoverHosts: Discovered: " + host.hostname + " RspTime: " + host.response_time);

                }

            } catch (java.io.IOException e) {
                System.out.println("!!! discoverHosts: exception pinging host: " + address.getHostAddress() + ", error: " + e);
            }
        }
    }

    public void run() {

        System.out.println("---> Discovery thread running");

        int discoverWaitMinutes;
        while (!terminate) {
            discoverHosts();

            discoverWaitMinutes = 60;
            while (discoverWaitMinutes > 0) {
                try {
                    TimeUnit.MINUTES.sleep(1);
                } catch (java.lang.InterruptedException e) {
                    System.out.println("!!! discoveryThread: interrupted exception: " + e);
                    break;
                }
                --discoverWaitMinutes;
            }
        }
    }
}
