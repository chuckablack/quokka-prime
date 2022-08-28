namespace QuokkaServer.Db;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Bson.Serialization;
using System.Globalization;

class DoSummaries : BaseModel 
{

    public int interval { get; set; }

    public DoSummaries(int interval)
    {
        this.interval = interval;
    }
  
    // Non-static method
    public void Summarize()
    {
        DateTime lastHour = DateTime.Now.AddHours(-1);
        var lastHourString = lastHour.ToString("yyyy-MM-dd HH");

        while (true) 
        {
            DateTime currentHour = DateTime.Now;
            var currentHourString = currentHour.ToString("yyyy-MM-dd HH");
            if (currentHourString != lastHourString)
            {
                var timeFilter = Builders<BsonDocument>.Filter.Regex("time", new BsonRegularExpression("^"+lastHourString));
                
                var collectionHostStatus = GetMongoDB().GetCollection<BsonDocument>("hostStatus");
                var collectionHosts = GetMongoDB().GetCollection<BsonDocument>("hosts");
                var hostsBson = collectionHosts.Find(new BsonDocument()).ToList();

                foreach (BsonDocument hostBson in hostsBson)
                {
                    Host host = BsonSerializer.Deserialize<Host>(hostBson);

                    var hostFilter = Builders<BsonDocument>.Filter.Eq("hostname", host.hostname);
                    var hostAndTimeFilter = Builders<BsonDocument>.Filter.And(timeFilter, hostFilter);

                    var hostStatusDataBson = collectionHostStatus.Find(hostAndTimeFilter).ToList();

                    int numAvailability = 0, numResponseTime = 0;
                    int availabilityTotal = 0, availability_summary = 0;
                    float responseTimeTotal = 0, response_time_summary = 0;

                    foreach (BsonDocument hostStatusBson in hostStatusDataBson)
                    {
                        HostStatus hostStatusItem = BsonSerializer.Deserialize<HostStatus>(hostStatusBson);

                        numAvailability++;
                        if (hostStatusItem.availability)
                        {
                            availabilityTotal += 100;

                            numResponseTime++;
                            responseTimeTotal += float.Parse(host.response_time, CultureInfo.InvariantCulture.NumberFormat);
                        }

                    }
                    if (numAvailability != 0) {
                        availability_summary = availabilityTotal / numAvailability;
                    }
                    if (numResponseTime != 0) {
                        response_time_summary = responseTimeTotal / numResponseTime;
                    } 
                    HostStatusSummary hostStatusSummary = new HostStatusSummary(host, availability_summary, response_time_summary);
                    HostStatusSummary.SetHostStatusSummary(hostStatusSummary);
                }

                var collectionServiceStatus = GetMongoDB().GetCollection<BsonDocument>("serviceStatus");
                var collectionServices = GetMongoDB().GetCollection<BsonDocument>("services");
                var servicesBson = collectionServices.Find(new BsonDocument()).ToList();

                foreach (BsonDocument serviceBson in servicesBson)
                {
                    Service service = BsonSerializer.Deserialize<Service>(serviceBson);

                    var serviceFilter = Builders<BsonDocument>.Filter.Eq("name", service.name);
                    var serviceAndTimeFilter = Builders<BsonDocument>.Filter.And(timeFilter, serviceFilter);

                    var serviceStatusDataBson = collectionServiceStatus.Find(serviceAndTimeFilter).ToList();

                    int numAvailability = 0, numResponseTime = 0;
                    int availabilityTotal = 0, availability_summary = 0;
                    float responseTimeTotal = 0, response_time_summary = 0;

                    foreach (BsonDocument serviceStatusBson in serviceStatusDataBson)
                    {
                        ServiceStatus serviceStatusItem = BsonSerializer.Deserialize<ServiceStatus>(serviceStatusBson);

                        numAvailability++;
                        if (serviceStatusItem.availability)
                        {
                            availabilityTotal += 100;

                            numResponseTime++;
                            responseTimeTotal += float.Parse(service.response_time, CultureInfo.InvariantCulture.NumberFormat);
                        }

                    }
                    if (numAvailability != 0) {
                        availability_summary = availabilityTotal / numAvailability;
                    }
                    if (numResponseTime != 0) {
                        response_time_summary = responseTimeTotal / numResponseTime;
                    } 
                    ServiceStatusSummary serviceStatusSummary = new ServiceStatusSummary(service, availability_summary, response_time_summary);
                    ServiceStatusSummary.SetServiceStatusSummary(serviceStatusSummary);
                }

                var collectionDeviceStatus = GetMongoDB().GetCollection<BsonDocument>("deviceStatus");
                var collectionDevices = GetMongoDB().GetCollection<BsonDocument>("devices");
                var devicesBson = collectionDevices.Find(new BsonDocument()).ToList();

                foreach (BsonDocument deviceBson in devicesBson)
                {
                    Device device = BsonSerializer.Deserialize<Device>(deviceBson);

                    var deviceFilter = Builders<BsonDocument>.Filter.Eq("name", device.name);
                    var deviceAndTimeFilter = Builders<BsonDocument>.Filter.And(timeFilter, deviceFilter);

                    var deviceStatusDataBson = collectionDeviceStatus.Find(deviceAndTimeFilter).ToList();

                    int numAvailability = 0, numResponseTime = 0;
                    int availabilityTotal = 0, availability_summary = 0;
                    float responseTimeTotal = 0, response_time_summary = 0;

                    foreach (BsonDocument deviceStatusBson in deviceStatusDataBson)
                    {
                        DeviceStatus deviceStatusItem = BsonSerializer.Deserialize<DeviceStatus>(deviceStatusBson);

                        numAvailability++;
                        if (deviceStatusItem.availability)
                        {
                            availabilityTotal += 100;

                            numResponseTime++;
                            responseTimeTotal += float.Parse(device.response_time, CultureInfo.InvariantCulture.NumberFormat);
                        }

                    }
                    if (numAvailability != 0) {
                        availability_summary = availabilityTotal / numAvailability;
                    }
                    if (numResponseTime != 0) {
                        response_time_summary = responseTimeTotal / numResponseTime;
                    } 
                    DeviceStatusSummary deviceStatusSummary = new DeviceStatusSummary(device, availability_summary, response_time_summary);
                    DeviceStatusSummary.SetDeviceStatusSummary(deviceStatusSummary);
                }

                lastHourString = currentHourString;
            }
            Thread.Sleep(1000*interval);
        }
    }
}