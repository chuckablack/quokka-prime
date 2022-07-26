namespace QuokkaServer;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;

[BsonIgnoreExtraElements]
public class Service : BaseModel
{
    // Note: naming conventions follow that of the mongo and python conventions
    //       used throughout the quokka project

    // public ObjectId _id { get; set; }

    public string name { get; set; }
    public string? type { get; set; }
    public string? target { get; set; }
    public string? data { get; set; }

    public string? last_heard { get; set; }

    public bool? availability { get; set; }
    public string? response_time { get; set; }

    public float? sla_response_time { get; set; }
    public float? sla_availability { get; set; }

    public Service(string name)
    {
        this.name = name;
    }

    public static IDictionary<string, Service> GetServices()
    {
        var collectionServices = GetMongoDB().GetCollection<BsonDocument>("services");
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

    public static Service? GetService(string name)
    {
        var collectionServices = GetMongoDB().GetCollection<BsonDocument>("services");

        var filter = Builders<BsonDocument>.Filter.Eq("name", name);
        var serviceBson = collectionServices.Find(filter).FirstOrDefault();

        if (serviceBson is null) {
            return null;
        }
        return BsonSerializer.Deserialize<Service>(serviceBson);
    }

    public static void SetService(Service service)
    {
        Console.WriteLine("---> made it to put service\n  ---> " + JsonConvert.SerializeObject(service));

        var collectionServices = GetMongoDB().GetCollection<BsonDocument>("services");
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
    }
}
