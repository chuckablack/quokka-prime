SET Q=%1
ECHO %Q%
IF %Q%=="" (SET quokka="localhost:5001") ELSE (SET quokka="%Q%")
ECHO %quokka%
START /B python host_monitor.py --quokka %quokka% &
START /B python host_portscan.py --quokka %quokka% &
START /B python device_monitor.py --quokka %quokka% &
START /B python service_monitor.py --quokka %quokka% &
