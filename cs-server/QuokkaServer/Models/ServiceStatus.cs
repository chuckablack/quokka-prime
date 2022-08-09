namespace QuokkaServer.Db;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;

[BsonIgnoreExtraElements]
public class ServiceStatus : BaseModel
{
    // Note: naming conventions follow that of the mongo and python conventions
    //       used throughout the quokka project

    public string name { get; set; }
    public string? time { get; set; }
    public bool? availability { get; set; }
    public string? response_time { get; set; }

    public ServiceStatus(Service service)
    {
        this.name = service.name;
        this.time = service.last_heard;
        this.availability = service.availability;
        this.response_time = service.response_time;
    }

    public static IList<ServiceStatus> GetServiceStatus(string name, int dataPoints)
    {
        var collectionServices = GetMongoDB().GetCollection<BsonDocument>("serviceStatus");

        var filter = Builders<BsonDocument>.Filter.Eq("name", name);
        var serviceStatusDataBson = collectionServices.Find(filter).Sort("{time: -1}").Limit(dataPoints).ToList();

        var serviceStatusData = new List<ServiceStatus>();
        foreach (BsonDocument serviceStatusBson in serviceStatusDataBson)
        {
            Console.WriteLine("--- service ---> " + serviceStatusBson.ToString());
            ServiceStatus serviceStatusItem = BsonSerializer.Deserialize<ServiceStatus>(serviceStatusBson);
            serviceStatusData.Add(serviceStatusItem);
        }
        return serviceStatusData;
    }

    public static void SetServiceStatus(ServiceStatus serviceStatus)
    {
        Console.WriteLine("---> made it to set serviceStatus\n  ---> " + JsonConvert.SerializeObject(serviceStatus));
    
        var collectionDevices = GetMongoDB().GetCollection<BsonDocument>("serviceStatus");
        collectionDevices.InsertOne(serviceStatus.ToBsonDocument());

        Console.WriteLine("---> successfully updated serviceStatus");
    }

}
