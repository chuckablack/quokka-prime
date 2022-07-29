namespace QuokkaServer;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using Newtonsoft.Json;

[BsonIgnoreExtraElements]
public class Host : BaseModel
{
    // Note: naming conventions follow that of the mongo and python conventions
    //       used throughout the quokka project

    // public ObjectId _id { get; set; }

    public string? mac_address { get; set; }
    public string? ip_address { get; set; }
    public string hostname { get; set; }

    public string? last_heard { get; set; }
    public bool? availability { get; set; }
    public string? response_time { get; set; }

    public string? open_tcp_ports { get; set; }

    public Host(string hostname)
    {
        this.hostname = hostname;
    }

    public static IDictionary<string, Host> GetHosts()
    {
        var collectionHosts = GetMongoDB().GetCollection<BsonDocument>("hosts");
        var hostsBson = collectionHosts.Find(new BsonDocument()).ToList();

        var hosts = new Dictionary<string, Host>();
        foreach (BsonDocument hostBson in hostsBson)
        {
            // Console.WriteLine("--- host ---> " + hostBson.ToString());
            Host host = BsonSerializer.Deserialize<Host>(hostBson);
            hosts[host.hostname] = host;
        }

        Console.WriteLine("---> successfully got hosts: " + collectionHosts);
        return hosts;
    }

    public static Host? GetHost(string hostname)
    {
        var collectionHosts = GetMongoDB().GetCollection<BsonDocument>("hosts");

        var filter = Builders<BsonDocument>.Filter.Eq("hostname", hostname);
        var hostBson = collectionHosts.Find(filter).FirstOrDefault();

        if (hostBson is null) {
            return null;
        }
        return BsonSerializer.Deserialize<Host>(hostBson);
    }

    public static void SetHost(Host host)
    {
        Console.WriteLine("---> made it to put host\n  ---> " + JsonConvert.SerializeObject(host));

        var collectionHosts = GetMongoDB().GetCollection<BsonDocument>("hosts");
        Console.WriteLine("---> hosts collection: " + collectionHosts);

        var filter = Builders<BsonDocument>.Filter.Eq("hostname", host.hostname);
        var hostBson = collectionHosts.Find(filter).FirstOrDefault();

        if (hostBson is null) {
            collectionHosts.InsertOne(host.ToBsonDocument());
        }
        else {
            // if open_tcp_ports is not present, don't overwrite it
            var current_open_tcp_ports = hostBson.GetValue("open_tcp_ports");
            if ((host.open_tcp_ports == null) && (current_open_tcp_ports is not MongoDB.Bson.BsonNull)) {
                host.open_tcp_ports = (string)hostBson.GetValue("open_tcp_ports");
            }
            collectionHosts.ReplaceOne(filter, host.ToBsonDocument());
        }

        Console.WriteLine("---> successfully inserted/updated host");
    }

}
