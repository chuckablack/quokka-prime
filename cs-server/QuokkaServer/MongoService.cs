using MongoDB.Driver;

namespace QuokkaServer.Db;

public class MongoService
{
    public static MongoClient? dbClient;
    public void connect()
    {
        dbClient = new MongoClient("mongodb://localhost:27017");
    }
}