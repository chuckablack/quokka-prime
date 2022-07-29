using Microsoft.AspNetCore.Mvc;

namespace QuokkaServer.Controllers;

[ApiController]
[Route("hosts")]
public class HostController : ControllerBase
{

    [HttpGet(Name = "GetAllHosts")]
    public IDictionary<string, Host> Get()
    {
        return Host.GetHosts();
    }

    [HttpGet("{hostname}")]
    public ActionResult<Host> Get(string hostname)
    {
        var host = Host.GetHost(hostname);
        if (host is null)
        {
            return NotFound();
        }
        return host;
    }

    [HttpPut(Name = "UpdateHost")]
    public ActionResult Put(Host host)
    {
        Host.SetHost(host);
        HostStatus.SetHostStatus(new HostStatus(host));

        return NoContent();
    }

}
