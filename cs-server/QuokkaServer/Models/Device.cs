namespace QuokkaServer;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;

[BsonIgnoreExtraElements]
public class Device : BaseModel
{
    // Note: naming conventions follow that of the mongo and python conventions
    //       used throughout the quokka project

    // public ObjectId _id { get; set; }

    public string name { get; set; }
    
    public string? hostname { get; set; }
    public string? ip_address { get; set; }
    public string? vendor { get; set; }
    public string? model { get; set; }
    public string? os { get; set; }
    public string? os_version { get; set; }

    public string? username { get; set; }
    public string? password { get; set; }
    public int? ssh_port { get; set; }

    public string? last_heard { get; set; }

    public bool? availability { get; set; }
    public string? response_time { get; set; }

    public float? sla_response_time { get; set; }
    public float? sla_availability { get; set; }

    public Device(string name)
    {
        this.name = name;
    }

    public static IDictionary<string, Device> GetDevices()
    {
        var collectionDevices = GetMongoDB().GetCollection<BsonDocument>("devices");
        Console.WriteLine("---> successfully got devices: " + collectionDevices);

        var devicesBson = collectionDevices.Find(new BsonDocument()).ToList();

        var devices = new Dictionary<string, Device>();
        foreach (BsonDocument deviceBson in devicesBson)
        {
            Console.WriteLine("--- device ---> " + deviceBson.ToString());
            Device device = BsonSerializer.Deserialize<Device>(deviceBson);
            devices[device.name] = device;
        }
        return devices;
    }

    public static Device? GetDevice(string name)
    {
        var collectionDevices = GetMongoDB().GetCollection<BsonDocument>("devices");

        var filter = Builders<BsonDocument>.Filter.Eq("name", name);
        var deviceBson = collectionDevices.Find(filter).FirstOrDefault();

        if (deviceBson is null) {
            return null;
        }
        return BsonSerializer.Deserialize<Device>(deviceBson);
    }

    public static void SetDevice(Device device)
    {
        Console.WriteLine("---> made it to put device\n  ---> " + JsonConvert.SerializeObject(device));

        var collectionDevices = GetMongoDB().GetCollection<BsonDocument>("devices");
        Console.WriteLine("---> devices collection: " + collectionDevices);

        var filter = Builders<BsonDocument>.Filter.Eq("name", device.name);
        var deviceBson = collectionDevices.Find(filter).FirstOrDefault();

        if (deviceBson is null) {
            collectionDevices.InsertOne(device.ToBsonDocument());
        }
        else {
            collectionDevices.ReplaceOne(filter, device.ToBsonDocument());
        }

        Console.WriteLine("---> successfully inserted/updated device");
    }

}
