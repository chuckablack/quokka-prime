using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using QuokkaServer.Db;
using MongoDB.Driver;
using MongoDB.Bson;
using MongoDB.Bson.Serialization;

namespace QuokkaServer.Controllers;

[ApiController]
[Route("devices")]
public class DeviceController : ControllerBase
{
    private readonly ILogger<DeviceController> _logger;

    public DeviceController(ILogger<DeviceController> logger)
    {
        _logger = logger;
    }

    [HttpGet(Name = "GetAllDevices")]
    public IDictionary<string, Device> Get()
    {
        // MongoClient dbClient = MongoService.dbClient;
        // var dbQuokka = dbClient.GetDatabase("quokkadb");

        // var collectionDevices = dbQuokka.GetCollection<BsonDocument>("devices");
        // Console.WriteLine("---> successfully got devices: " + collectionDevices);

        // var devicesBson = collectionDevices.Find(new BsonDocument()).ToList();

        // var devices = new Dictionary<string, Device>();
        // foreach (BsonDocument deviceBson in devicesBson)
        // {
        //     Console.WriteLine("--- device ---> " + deviceBson.ToString());
        //     Device device = BsonSerializer.Deserialize<Device>(deviceBson);
        //     devices[device.name] = device;
        // }
        // return devices;

        return Device.GetDevices();
    }

    [HttpGet("{name}")]
    public ActionResult<Device> Get(string name)
    {
        // var dbQuokka = MongoService.dbClient.GetDatabase("quokkadb");
        // var collectionDevices = dbQuokka.GetCollection<BsonDocument>("devices");

        // var filter = Builders<BsonDocument>.Filter.Eq("name", name);
        // var deviceBson = collectionDevices.Find(filter).FirstOrDefault();

        // if (deviceBson is null) {
        //     return NotFound();
        // }
        // return BsonSerializer.Deserialize<Device>(deviceBson);

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
        // Console.WriteLine("---> made it to put device\n  ---> " + JsonConvert.SerializeObject(device));

        // var dbQuokka = MongoService.dbClient.GetDatabase("quokkadb");
        // var collectionDevices = dbQuokka.GetCollection<BsonDocument>("devices");
        // Console.WriteLine("---> devices collection: " + collectionDevices);

        // var filter = Builders<BsonDocument>.Filter.Eq("name", device.name);
        // var deviceBson = collectionDevices.Find(filter).FirstOrDefault();

        // if (deviceBson is null) {
        //     collectionDevices.InsertOne(device.ToBsonDocument());
        // }
        // else {
        //     collectionDevices.ReplaceOne(filter, device.ToBsonDocument());
        // }

        // Console.WriteLine("---> successfully inserted/updated device");

        // return NoContent();

        Device.SetDevice(device);
        return NoContent();
    }

}
