using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using QuokkaServer.Db;
using MongoDB.Driver;
using MongoDB.Bson;
using MongoDB.Bson.Serialization;

namespace QuokkaServer;

public class BaseModel
{
    public static IMongoDatabase GetMongoDB()
    {
        MongoClient dbClient = MongoService.dbClient;
        return dbClient.GetDatabase("quokkadb");

    }
}