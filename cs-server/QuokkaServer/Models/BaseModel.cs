namespace QuokkaServer.Db;

using MongoDB.Driver;

public class BaseModel
{
    public static IMongoDatabase GetMongoDB()
    {
        MongoClient dbClient = MongoService.dbClient;
        return dbClient.GetDatabase("quokkadb");

    }
}