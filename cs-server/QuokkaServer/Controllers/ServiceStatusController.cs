namespace QuokkaServer.Controllers;

using Microsoft.AspNetCore.Mvc;
using QuokkaServer.Db;

[ApiController]
[Route("service/status")]
public class ServiceStatusController : ControllerBase
{
    [HttpGet()]
    public IActionResult GetServiceStatus(string name, int dataPoints)
    {
        Console.WriteLine("---> made it to get serviceStatus: " + name + "  num dataPoints: " + dataPoints);
    
        var service = Service.GetService(name);
        if (service is null)
        {
            return NotFound();
        }
    
        Dictionary<string, object> serviceStatusReply = new Dictionary<string, object>();
        serviceStatusReply["service"] = service;
        serviceStatusReply["status"] = ServiceStatus.GetServiceStatus(name, dataPoints);
        serviceStatusReply["summary"] = ServiceStatusSummary.GetServiceStatusSummary(name, dataPoints);
        return Ok(serviceStatusReply);
    }
}
