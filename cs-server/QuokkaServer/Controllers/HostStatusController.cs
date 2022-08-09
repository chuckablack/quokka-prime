namespace QuokkaServer.Controllers;

using Microsoft.AspNetCore.Mvc;
using QuokkaServer.Db;


[ApiController]
[Route("host/status")]
public class HostStatusController : ControllerBase
{
    [HttpGet()]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IDictionary<string, object>))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public IActionResult GetHostStatus(string hostname, int dataPoints)
    {
        Console.WriteLine("---> made it to get hostStatus: " + hostname);

        var host = Host.GetHost(hostname);
        if (host is null)
        {
            return NotFound();
        }
    
        Dictionary<string, object> hostStatusReply = new Dictionary<string, object>();
        hostStatusReply["host"] = host;
        hostStatusReply["status"] = HostStatus.GetHostStatus(hostname, dataPoints);
        hostStatusReply["summary"] = new List<HostStatus>();
        return Ok(hostStatusReply);
    }
}
