namespace QuokkaServer;
using MongoDB.Bson.Serialization.Attributes;

[BsonIgnoreExtraElements]
public class Service
{
    // Note: naming conventions follow that of the mongo and python conventions
    //       used throughout the quokka project

    // public ObjectId _id { get; set; }

    public string? name { get; set; }
    public string? type { get; set; }
    public string? target { get; set; }
    public string? data { get; set; }

    public string? last_heard { get; set; }

    public bool? availability { get; set; }
    public string? response_time { get; set; }

    public float? sla_response_time { get; set; }
    public float? sla_availability { get; set; }
}
