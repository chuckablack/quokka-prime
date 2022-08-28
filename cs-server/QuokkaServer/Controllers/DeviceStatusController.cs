namespace QuokkaServer.Controllers;

using Microsoft.AspNetCore.Mvc;
using QuokkaServer.Db;

[ApiController]
[Route("device/status")]
public class DeviceStatusController : ControllerBase
{
    [HttpGet()]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IDictionary<string, object>))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public IActionResult GetDeviceStatus(string name, int dataPoints)
    {
        Console.WriteLine("---> made it to get deviceStatus: " + name);
    
        var device = Device.GetDevice(name);
        if (device is null)
        {
            return NotFound();
        }
    
        Dictionary<string, object> deviceStatusReply = new Dictionary<string, object>();
        deviceStatusReply["device"] = device;
        deviceStatusReply["status"] = DeviceStatus.GetDeviceStatus(name, dataPoints);
        deviceStatusReply["summary"] = DeviceStatusSummary.GetDeviceStatusSummary(name, dataPoints);
        return Ok(deviceStatusReply);
    }
}
