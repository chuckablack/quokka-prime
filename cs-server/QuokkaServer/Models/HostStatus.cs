namespace QuokkaServer.Db;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;

[BsonIgnoreExtraElements]
public class HostStatus : BaseModel
{
    // Note: naming conventions follow that of the mongo and python conventions
    //       used throughout the quokka project

    // public ObjectId _id { get; set; }

    public string hostname { get; set; }
    public string time { get; set; }
    public bool availability { get; set; }
    public string response_time { get; set; }

    public HostStatus(Host host)
    {
        this.hostname = host.hostname;
        this.time = host.last_heard;
        this.availability = host.availability;
        this.response_time = host.response_time;
    }

    public static IList<HostStatus> GetHostStatus(string hostname, int dataPoints)
    {
        var collectionHosts = GetMongoDB().GetCollection<BsonDocument>("hostStatus");

        var filter = Builders<BsonDocument>.Filter.Eq("hostname", hostname);
        var hostStatusDataBson = collectionHosts.Find(filter).Sort("{time:-1}").Limit(dataPoints).ToList();

        var hostStatusData = new List<HostStatus>();
        foreach (BsonDocument hostStatusBson in hostStatusDataBson)
        {
            Console.WriteLine("--- host status ---> " + hostStatusBson.ToString());
            HostStatus hostStatusItem = BsonSerializer.Deserialize<HostStatus>(hostStatusBson);
            hostStatusData.Add(hostStatusItem);
        }
        return hostStatusData;
    }

    public static void SetHostStatus(HostStatus hostStatus)
    {
        Console.WriteLine("---> made it to set hostStatus\n  ---> " + JsonConvert.SerializeObject(hostStatus));
    
        var collectionHosts = GetMongoDB().GetCollection<BsonDocument>("hostStatus");
        collectionHosts.InsertOne(hostStatus.ToBsonDocument());

        Console.WriteLine("---> successfully updated hostStatus");
    }
}
