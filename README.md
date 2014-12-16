grafana
=======

Role to install and configure Grafana - the metrics dashboard and graph editor.
Grafana is installed from RPM package (needs to be built separately, see the
`contrib` directory) and the web application is served via Apache web server.


Example
-------

```
---

# Example of how to use the role
- hosts: myhost
  roles:
    - role: grafana
      grafana_elasticsearch_server: 192.168.1.101
      grafana_graphite_server: 192.168.1.101
```


Role variables
--------------

List of variables used by the role:

```
```


License
-------

MIT


Author
------

Jiri Tyr
