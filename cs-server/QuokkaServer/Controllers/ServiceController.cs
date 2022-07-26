using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using QuokkaServer.Db;
using MongoDB.Driver;
using MongoDB.Bson;
using MongoDB.Bson.Serialization;

namespace QuokkaServer.Controllers;

[ApiController]
[Route("services")]
public class ServiceController : ControllerBase
{
    private readonly ILogger<ServiceController> _logger;

    public ServiceController(ILogger<ServiceController> logger)
    {
        _logger = logger;
    }

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
        return NoContent();
    }

}
