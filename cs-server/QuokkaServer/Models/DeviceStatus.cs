namespace QuokkaServer.Db;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;

[BsonIgnoreExtraElements]
public class DeviceStatus : BaseModel
{
    // Note: naming conventions follow that of the mongo and python conventions
    //       used throughout the quokka project

    // public ObjectId _id { get; set; }

    public string name { get; set; }
    public string? time { get; set; }
    public bool? availability { get; set; }
    public string? response_time { get; set; }

    public DeviceStatus(Device device)
    {
        this.name = device.name;
        this.time = device.last_heard;
        this.availability = device.availability;
        this.response_time = device.response_time;
    }

    public static IList<DeviceStatus> GetDeviceStatus(string name, int dataPoints)
    {
        var collectionDevices = GetMongoDB().GetCollection<BsonDocument>("deviceStatus");

        var filter = Builders<BsonDocument>.Filter.Eq("name", name);
        var deviceStatusDataBson = collectionDevices.Find(filter).Sort("{time:-1}").Limit(dataPoints).ToList();

        var deviceStatusData = new List<DeviceStatus>();
        foreach (BsonDocument deviceStatusBson in deviceStatusDataBson)
        {
            Console.WriteLine("--- device ---> " + deviceStatusBson.ToString());
            DeviceStatus deviceStatusItem = BsonSerializer.Deserialize<DeviceStatus>(deviceStatusBson);
            deviceStatusData.Add(deviceStatusItem);
        }
        return deviceStatusData;
    }

    public static void SetDeviceStatus(DeviceStatus deviceStatus)
    {
        Console.WriteLine("---> made it to set deviceStatus\n  ---> " + JsonConvert.SerializeObject(deviceStatus));
    
        var collectionDevices = GetMongoDB().GetCollection<BsonDocument>("deviceStatus");
        collectionDevices.InsertOne(deviceStatus.ToBsonDocument());

        Console.WriteLine("---> successfully updated deviceStatus");
    }
}
