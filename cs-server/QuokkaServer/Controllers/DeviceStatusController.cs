using Microsoft.AspNetCore.Mvc;

namespace QuokkaServer.Controllers;

[ApiController]
[Route("device/status")]
public class DeviceStatusController : ControllerBase
{
    [HttpGet()]
    public IList<DeviceStatus>? GetDeviceStatus(string name, string dataPoints)
    {
        Console.WriteLine("---> made it to get deviceStatus: " + name);
    
        var deviceStatus = DeviceStatus.GetDeviceStatus(name);
        return deviceStatus;
    }
}
