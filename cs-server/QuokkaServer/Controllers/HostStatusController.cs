using Microsoft.AspNetCore.Mvc;

namespace QuokkaServer.Controllers;

[ApiController]
[Route("host/status")]
public class HostStatusController : ControllerBase
{
    [HttpGet()]
    public IList<HostStatus>? GetHostStatus(string hostname, string dataPoints)
    {
        Console.WriteLine("---> made it to get hostStatus: " + hostname);
    
        var hostStatus = HostStatus.GetHostStatus(hostname);
        return hostStatus;
    }
}
