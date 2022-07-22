namespace QuokkaServer;
using MongoDB.Bson.Serialization.Attributes;

[BsonIgnoreExtraElements]
public class Host
{
    // Note: naming conventions follow that of the mongo and python conventions
    //       used throughout the quokka project

    // public ObjectId _id { get; set; }

    public string? mac_address { get; set; }
    public string? ip_address { get; set; }
    public string? hostname { get; set; }

    public string? last_heard { get; set; }
    public bool? availability { get; set; }
    public string? response_time { get; set; }

    public string? open_tcp_ports { get; set; }
}
