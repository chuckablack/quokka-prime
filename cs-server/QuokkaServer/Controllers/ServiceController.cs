namespace QuokkaServer.Controllers;

using Microsoft.AspNetCore.Mvc;
using QuokkaServer.Db;

[ApiController]
[Route("services")]
public class ServiceController : ControllerBase
{
    [HttpGet(Name = "GetAllServices")]
    public IDictionary<string, Service> Get()
    {
        return Service.GetServices();
    }

    [HttpGet("{name}")]
    public ActionResult<Service> Get(string name)
    {
        var service = Service.GetService(name);
        if (service is null)
        {
            return NotFound();
        }
        return service;
    }

    [HttpPut(Name = "UpdateService")]
    public IActionResult Put(Service service)
    {
        Service.SetService(service);
        ServiceStatus.SetServiceStatus(new ServiceStatus(service));
        return NoContent();
    }

}
