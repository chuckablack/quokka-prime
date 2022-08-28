namespace QuokkaServer.Db;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;

[BsonIgnoreExtraElements]
public class ServiceStatusSummary : StatusSummary
{
    public string name { get; set; }

    public ServiceStatusSummary(Service service, int availability, float response_time) : base(availability, response_time)
    {
        this.name = service.name;
    }

    public static IList<ServiceStatusSummary> GetServiceStatusSummary(string name, int dataPoints)
    {
        var collectionServices = GetMongoDB().GetCollection<BsonDocument>("serviceStatusSummary");

        var filter = Builders<BsonDocument>.Filter.Eq("name", name);
        var serviceStatusSummaryDataBson = collectionServices.Find(filter).Sort("{time:-1}").Limit(dataPoints).ToList();

        var serviceStatusSummaryData = new List<ServiceStatusSummary>();
        foreach (BsonDocument serviceStatusSummaryBson in serviceStatusSummaryDataBson)
        {
            Console.WriteLine("--- service status ---> " + serviceStatusSummaryBson.ToString());
            ServiceStatusSummary serviceStatusSummaryItem = BsonSerializer.Deserialize<ServiceStatusSummary>(serviceStatusSummaryBson);
            serviceStatusSummaryData.Add(serviceStatusSummaryItem);
        }
        return serviceStatusSummaryData;
    }

    public static void SetServiceStatusSummary(ServiceStatusSummary serviceStatusSummary)
    {
        Console.WriteLine("---> made it to set serviceStatusSummary\n  ---> " + JsonConvert.SerializeObject(serviceStatusSummary));
    
        var collectionServices = GetMongoDB().GetCollection<BsonDocument>("serviceStatusSummary");
        collectionServices.InsertOne(serviceStatusSummary.ToBsonDocument());

        Console.WriteLine("---> successfully updated serviceStatusSummary");
    }
}
