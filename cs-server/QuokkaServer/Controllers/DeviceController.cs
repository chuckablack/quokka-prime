namespace QuokkaServer.Controllers;

using Microsoft.AspNetCore.Mvc;
using QuokkaServer.Db;

[ApiController]
[Route("devices")]
public class DeviceController : ControllerBase
{
    [HttpGet(Name = "GetAllDevices")]
    public IDictionary<string, Device> Get()
    {
        return Device.GetDevices();
    }

    [HttpGet("{name}")]
    public ActionResult<Device> Get(string name)
    {
        var device = Device.GetDevice(name);
        if (device is null)
        {
            return NotFound();
        }
        return device;
    }

    [HttpPut(Name = "UpdateDevice")]
    public IActionResult Put(Device device)
    {
        Device.SetDevice(device);
        DeviceStatus.SetDeviceStatus(new DeviceStatus(device));
        return NoContent();
    }

}
