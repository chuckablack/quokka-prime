using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using Newtonsoft.Json;
using QuokkaServer.Db;
using MongoDB.Driver;
using MongoDB.Bson;
using MongoDB.Bson.Serialization;
using System.Net;
using System.Web;

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
        MongoClient dbClient = MongoService.dbClient;
        var dbQuokka = dbClient.GetDatabase("quokkadb");

        var collectionServices = dbQuokka.GetCollection<BsonDocument>("services");
        Console.WriteLine("---> successfully got services: " + collectionServices);

        var servicesBson = collectionServices.Find(new BsonDocument()).ToList();

        var services = new Dictionary<string, Service>();
        foreach (BsonDocument serviceBson in servicesBson)
        {
            Console.WriteLine("--- service ---> " + serviceBson.ToString());
            Service service = BsonSerializer.Deserialize<Service>(serviceBson);
            services[service.name] = service;
        }
        return services;
    }

    [HttpGet("{name}")]
    public ActionResult<Service> Get(string name)
    {
        var dbQuokka = MongoService.dbClient.GetDatabase("quokkadb");
        var collectionServices = dbQuokka.GetCollection<BsonDocument>("services");

        var filter = Builders<BsonDocument>.Filter.Eq("name", name);
        var serviceBson = collectionServices.Find(filter).FirstOrDefault();

        if (serviceBson is null) {
            return NotFound();
        }
        return BsonSerializer.Deserialize<Service>(serviceBson);
    }

    [HttpPut(Name = "UpdateService")]
    public IActionResult Put(Service service)
    {
        Console.WriteLine("---> made it to put service\n  ---> " + JsonConvert.SerializeObject(service));

        var dbQuokka = MongoService.dbClient.GetDatabase("quokkadb");
        var collectionServices = dbQuokka.GetCollection<BsonDocument>("services");
        Console.WriteLine("---> services collection: " + collectionServices);

        var filter = Builders<BsonDocument>.Filter.Eq("name", service.name);
        var serviceBson = collectionServices.Find(filter).FirstOrDefault();

        if (serviceBson is null) {
            collectionServices.InsertOne(service.ToBsonDocument());
        }
        else {
            collectionServices.ReplaceOne(filter, service.ToBsonDocument());
        }

        Console.WriteLine("---> successfully inserted/updated service");

        return NoContent();
    }

}
