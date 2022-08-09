using QuokkaServer.Db;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddCors();
builder.Services.AddMvc();

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

app.UseCors(options => options.WithOrigins("http://localhost:3000").AllowAnyMethod());

MongoService mongoService = new MongoService();
mongoService.connect();

TrimTables tt = new TrimTables(300);  // trim tables every 5 minutes
Thread thr = new Thread(new ThreadStart(tt.Trim));
thr.Start();

app.Run();