namespace QuokkaServer.Db;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;

[BsonIgnoreExtraElements]
public class DeviceStatusSummary : StatusSummary
{
    public string name { get; set; }

    public DeviceStatusSummary(Device device, int availability, float response_time) : base(availability, response_time)
    {
        this.name = device.name;
    }

    public static IList<DeviceStatusSummary> GetDeviceStatusSummary(string name, int dataPoints)
    {
        var collectionDevices = GetMongoDB().GetCollection<BsonDocument>("deviceStatusSummary");

        var filter = Builders<BsonDocument>.Filter.Eq("name", name);
        var deviceStatusSummaryDataBson = collectionDevices.Find(filter).Sort("{time:-1}").Limit(dataPoints).ToList();

        var deviceStatusSummaryData = new List<DeviceStatusSummary>();
        foreach (BsonDocument deviceStatusSummaryBson in deviceStatusSummaryDataBson)
        {
            Console.WriteLine("--- device status ---> " + deviceStatusSummaryBson.ToString());
            DeviceStatusSummary deviceStatusSummaryItem = BsonSerializer.Deserialize<DeviceStatusSummary>(deviceStatusSummaryBson);
            deviceStatusSummaryData.Add(deviceStatusSummaryItem);
        }
        return deviceStatusSummaryData;
    }

    public static void SetDeviceStatusSummary(DeviceStatusSummary deviceStatusSummary)
    {
        Console.WriteLine("---> made it to set deviceStatusSummary\n  ---> " + JsonConvert.SerializeObject(deviceStatusSummary));
    
        var collectionDevices = GetMongoDB().GetCollection<BsonDocument>("deviceStatusSummary");
        collectionDevices.InsertOne(deviceStatusSummary.ToBsonDocument());

        Console.WriteLine("---> successfully updated deviceStatusSummary");
    }
}
