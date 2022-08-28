namespace QuokkaServer.Db;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;

[BsonIgnoreExtraElements]
public class StatusSummary : BaseModel
{
    // Note: naming conventions follow that of the mongo and python conventions
    //       used throughout the quokka project

    // public ObjectId _id { get; set; }

    public string time { get; set; }
    public int availability { get; set; }
    public float response_time { get; set; }

    public StatusSummary(int availability, float response_time)
    {
        this.time = DateTime.Now.ToString("yyyy-MM-dd HH:"+"00:00");
        this.availability = availability;
        this.response_time = response_time;
    }

    public static IList<StatusSummary> GetStatusSummary(string hostname, int dataPoints)
    {
        var collections = GetMongoDB().GetCollection<BsonDocument>("hostStatusSummary");

        var filter = Builders<BsonDocument>.Filter.Eq("hostname", hostname);
        var hostStatusSummaryDataBson = collections.Find(filter).Sort("{time:-1}").Limit(dataPoints).ToList();

        var hostStatusSummaryData = new List<StatusSummary>();
        foreach (BsonDocument hostStatusSummaryBson in hostStatusSummaryDataBson)
        {
            Console.WriteLine("--- host status ---> " + hostStatusSummaryBson.ToString());
            StatusSummary hostStatusSummaryItem = BsonSerializer.Deserialize<StatusSummary>(hostStatusSummaryBson);
            hostStatusSummaryData.Add(hostStatusSummaryItem);
        }
        return hostStatusSummaryData;
    }

    public static void SetStatusSummary(StatusSummary hostStatusSummary)
    {
        Console.WriteLine("---> made it to set hostStatusSummary\n  ---> " + JsonConvert.SerializeObject(hostStatusSummary));
    
        var collections = GetMongoDB().GetCollection<BsonDocument>("hostStatusSummary");
        collections.InsertOne(hostStatusSummary.ToBsonDocument());

        Console.WriteLine("---> successfully updated hostStatusSummary");
    }
}
