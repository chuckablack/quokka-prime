using Microsoft.AspNetCore.Mvc;

namespace QuokkaServer.Controllers;

[ApiController]
[Route("service/status")]
public class ServiceStatusController : ControllerBase
{
    [HttpGet()]
    public IList<ServiceStatus>? GetServiceStatus(string name, string dataPoints)
    {
        Console.WriteLine("---> made it to get serviceStatus: " + name);
    
        var serviceStatus = ServiceStatus.GetServiceStatus(name);
        return serviceStatus;
    }
}
