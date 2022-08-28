namespace QuokkaServer.Db;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;

[BsonIgnoreExtraElements]
public class HostStatusSummary : StatusSummary
{
    public string hostname { get; set; }

    public HostStatusSummary(Host host, int availability, float response_time) : base(availability, response_time)
    {
        this.hostname = host.hostname;
        // this.time = DateTime.Now.ToString("yyyy-MM-dd HH:"+"00:00");
        // this.availability = availability;
        // this.response_time = response_time;
    }

    public static IList<HostStatusSummary> GetHostStatusSummary(string hostname, int dataPoints)
    {
        var collectionHosts = GetMongoDB().GetCollection<BsonDocument>("hostStatusSummary");

        var filter = Builders<BsonDocument>.Filter.Eq("hostname", hostname);
        var hostStatusSummaryDataBson = collectionHosts.Find(filter).Sort("{time:-1}").Limit(dataPoints).ToList();

        var hostStatusSummaryData = new List<HostStatusSummary>();
        foreach (BsonDocument hostStatusSummaryBson in hostStatusSummaryDataBson)
        {
            Console.WriteLine("--- host status ---> " + hostStatusSummaryBson.ToString());
            HostStatusSummary hostStatusSummaryItem = BsonSerializer.Deserialize<HostStatusSummary>(hostStatusSummaryBson);
            hostStatusSummaryData.Add(hostStatusSummaryItem);
        }
        return hostStatusSummaryData;
    }

    public static void SetHostStatusSummary(HostStatusSummary hostStatusSummary)
    {
        Console.WriteLine("---> made it to set hostStatusSummary\n  ---> " + JsonConvert.SerializeObject(hostStatusSummary));
    
        var collectionHosts = GetMongoDB().GetCollection<BsonDocument>("hostStatusSummary");
        collectionHosts.InsertOne(hostStatusSummary.ToBsonDocument());

        Console.WriteLine("---> successfully updated hostStatusSummary");
    }
}
