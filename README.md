# Web monitoring


### Web monitoring

This is a tool which monitors the availability of given websites over the network, produces metrics about these and 
save the metrics into the data storage. 
Now only PostreSQL can be used as a data storage.

### Requirements

 - Python 3.6+
 - Docker
 - Docker compose
 - PosgreSQL

### Using

To run in development mode use:

```
sh run.sh dev
```  

To run in production mode use:

```
sh run.sh prod
```  

Be default it runs in development mode.

To stop services press Ctrl+C or use
```
sh stop.sh
```

All services will be stopped and containers, networks and volumes will be removed

### Configuration

Development configuration:
```
data_handler/configs/development.yaml
web_monitor/configs/development.yaml
```

Production configuration:
```
data_handler/configs/production.yaml
web_monitor/configs/production.yaml
```

### Tests 

Tests run automatically after container build.  

```
pytest data_handler/tests
pytest web_monitor/tests
```




