using MongoDB.Driver;
using QuokkaServer.Db;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

MongoService mongoService = new MongoService();
mongoService.connect();
MongoClient dbClient = MongoService.dbClient;
// MongoClient dbClient = new MongoClient("mongodb://localhost:27017");

var dbList = dbClient.ListDatabases().ToList();

Console.WriteLine("The list of databases on this server is: ");
foreach (var db in dbList)
{
    Console.WriteLine(db);
}

app.Run();