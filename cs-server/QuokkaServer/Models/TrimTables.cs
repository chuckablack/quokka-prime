namespace QuokkaServer.Db;

using MongoDB.Bson;
using MongoDB.Driver;

class TrimTables : BaseModel 
{

    public int interval { get; set; }

    public TrimTables(int interval)
    {
        this.interval = interval;
    }
  
    // Non-static method
    public void Trim()
    {
        while (true) {
            DateTime trimTime = DateTime.Now.AddHours(-24);
            var trimTimeStr = trimTime.ToString("yyyy-MM-dd HH:mm:ss");
            var filter = Builders<BsonDocument>.Filter.Lt("time", trimTimeStr);

            var collectionHosts = GetMongoDB().GetCollection<BsonDocument>("hostStatus");
            var collectionDevices = GetMongoDB().GetCollection<BsonDocument>("deviceStatus");
            var collectionServices = GetMongoDB().GetCollection<BsonDocument>("serviceStatus");

            Console.WriteLine("-|-|-|  trimming status data older than: " + trimTimeStr);

            collectionHosts.DeleteMany(filter);
            collectionDevices.DeleteMany(filter);
            collectionServices.DeleteMany(filter);

            Thread.Sleep(1000*interval);
        }
    }
}