namespace QuokkaServer;
using MongoDB.Bson.Serialization.Attributes;

[BsonIgnoreExtraElements]
public class Device
{
    // Note: naming conventions follow that of the mongo and python conventions
    //       used throughout the quokka project

    // public ObjectId _id { get; set; }

    public string? name { get; set; }
    
    public string? hostname { get; set; }
    public string? ip_address { get; set; }
    public string? vendor { get; set; }
    public string? model { get; set; }
    public string? os { get; set; }
    public string? os_version { get; set; }

    public string? username { get; set; }
    public string? password { get; set; }
    public int? ssh_port { get; set; }

    public string? last_heard { get; set; }

    public bool? availability { get; set; }
    public string? response_time { get; set; }

    public float? sla_response_time { get; set; }
    public float? sla_availability { get; set; }
}
