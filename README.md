grafana
=======

Role to install and configure Grafana - the metrics dashboard and graph editor.
Grafana is installed from RPM package (needs to be built separately, see the
`contrib` directory) and the web application is served via Apache web server.


Example
-------

```
---

# Example of how to use the role with elasticsearch, graphite and InfluxDB
- hosts: myhost
  roles:
    - role: grafana
      grafana_datasources:
        graphite:
          type: graphite
          url: http://my.graphite.server.com:8080
        elasticsearch:
          type: elasticsearch
          url: http://my.elastic.server.com:9200
          index: grafana-dash
          grafanaDB: 'true'
        influxdb:
          type: influxdb
          url: http://my.influxdb.server.com:8086/db/database_name
          username: admin
          password: admin
```


Role variables
--------------

List of variables used by the role:

```
# Default datasources
grafana_datasources:
  graphite:
    type: graphite
    url: http://my.graphite.server.com:8080
  elasticsearch:
    type: elasticsearch
    url: http://my.elastic.server.com:9200
    index: grafana-dash
    grafanaDB: 'true'
# Example of InfluxDB configuration
#  influxdb:
#    type: influxdb
#    url: http://my.influxdb.server.com:8086/db/database_name
#    username: admin
#    password: admin
# Example of OpenTSDB configuration
#  opentsdb:
#    type: opentsdb
#    url: http://my.opentsdb.server.com:4242

# Default max results
grafana_max_results: 100

# Default route
grafana_default_route: /dashboard/file/default.json

# Default behavior on unsaved changes
grafana_unsaved_changes_warning: 'true'

# Default playlist timespan
grafana_playlist_timespan: 1m

# Default admin password
grafana_admin_password: ''

# Default window title prefix
grafana_window_title_prefix: 'Grafana - '

# Whether to use rewrite rules to redirect root queries into the grafana
# directory
grafana_redirect_root: false
```


License
-------

MIT


Author
------

Jiri Tyr
