using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using QuokkaServer.Db;
using MongoDB.Driver;
using MongoDB.Bson;
using MongoDB.Bson.Serialization;

namespace QuokkaServer.Controllers;

[ApiController]
[Route("hosts")]
public class HostController : ControllerBase
{
    private readonly ILogger<HostController> _logger;

    public HostController(ILogger<HostController> logger)
    {
        _logger = logger;
    }

    [HttpGet(Name = "GetAllHosts")]
    public IDictionary<string, Host> Get()
    {
        return Host.GetHosts();
    }

    [HttpGet("{hostname}")]
    public ActionResult<Host> Get(string hostname)
    {
        // var dbQuokka = MongoService.dbClient.GetDatabase("quokkadb");
        // var collectionHosts = dbQuokka.GetCollection<BsonDocument>("hosts");

        // var filter = Builders<BsonDocument>.Filter.Eq("hostname", hostname);
        // var hostBson = collectionHosts.Find(filter).FirstOrDefault();

        // if (hostBson is null) {
        //     return NotFound();
        // }
        // return BsonSerializer.Deserialize<Host>(hostBson);

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
        // Console.WriteLine("---> made it to put host\n  ---> " + JsonConvert.SerializeObject(host));

        // var dbQuokka = MongoService.dbClient.GetDatabase("quokkadb");
        // var collectionHosts = dbQuokka.GetCollection<BsonDocument>("hosts");
        // Console.WriteLine("---> hosts collection: " + collectionHosts);

        // var filter = Builders<BsonDocument>.Filter.Eq("hostname", host.hostname);
        // var hostBson = collectionHosts.Find(filter).FirstOrDefault();

        // if (hostBson is null) {
        //     collectionHosts.InsertOne(host.ToBsonDocument());
        // }
        // else {
        //     // if open_tcp_ports is not present, don't overwrite it
        //     var current_open_tcp_ports = hostBson.GetValue("open_tcp_ports");
        //     if ((host.open_tcp_ports == null) && (current_open_tcp_ports is not MongoDB.Bson.BsonNull)) {
        //         host.open_tcp_ports = (string)hostBson.GetValue("open_tcp_ports");
        //     }
        //     collectionHosts.ReplaceOne(filter, host.ToBsonDocument());
        // }

        // Console.WriteLine("---> successfully inserted/updated host");

        Host.SetHost(host);
        return NoContent();
    }

}
