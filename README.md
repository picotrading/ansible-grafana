grafana
=======

Role to install and configure Grafana - the metrics dashboard and graph editor.
It is installed from [RPM package](http://docs.grafana.org/installation/rpm/)
available in the officiall [YUM repo](https://packagecloud.io/grafana/stable).

The configuraton of the role is done in such way that it should not be necessary
to change the role for any kind of configuration. All can be done either by
changing role parameters or by declaring completely new configuration as a
variable. That makes this role absolutely universal. See the examples below for
more details.

Please report any issues or send PR.


Example
-------

```
---

# Example of how to use the role
- hosts: myhost1
  roles:
    - yumrepo:
      # Configure the grafana YUM repo
      grafana:
        name: Grafana repo
        baseurl: https://packagecloud.io/grafana/stable/el/6/x86_64
        gpgcheck: 0
    - grafana

# Example of how to modify the grafana configuration
- hosts: myhost2
  roles:
    - yumrepo:
      # Configure the grafana YUM repo
      grafana:
        name: Grafana repo
        baseurl: https://packagecloud.io/grafana/stable/el/6/x86_64
        gpgcheck: 0
    - role: grafana
      # Allow grafana to bind to TCP port <1024
      grafana_allow_low_port: true
      # Changing port nunmber from the default 3000 to 80
      grafana_server_http_port: 80

# Example how to use only certain blocks of the configuration
- hosts: myhost3
  roles:
    - yumrepo:
      # Configure the grafana YUM repo
      grafana:
        name: Grafana repo
        baseurl: https://packagecloud.io/grafana/stable/el/6/x86_64
        gpgcheck: 0
    - role: grafana
      # Use only paths, server and database sections (the rest of values is
      # inherited from /usr/share/grafana/conf/defaults.ini)
      grafana_config:
        app_mode: "{{ grafana_app_mode }}"
        paths: "{{ grafana_paths }}"
        server: "{{ grafana_server }}"
        database: "{{ grafana_database }}"

# Example of how to create completely new configuration
- hosts: myhost4
  roles:
    - yumrepo:
      # Configure the grafana YUM repo
      grafana:
        name: Grafana repo
        baseurl: https://packagecloud.io/grafana/stable/el/6/x86_64
        gpgcheck: 0
    - role: grafana
      # Very simple configuration (the rest of values is inherited from
      # /usr/share/grafana/conf/defaults.ini)
      grafana_config:
        app_mode: production
        server:
          http_port: 8080
```


Role variables
--------------

List of variables used by the role:

```
# Package to be installed (you can force a specific version here)
grafana_pkg: grafana

# Allow grafana to bind to TCP port <1024
grafana_allow_low_port: false


# Default environment
grafana_app_mode: production


# Default data path
grafana_paths_data: /var/lib/grafana

# Default logs path
grafana_paths_logs: /var/log/grafana

grafana_paths:
  data: "{{ grafana_paths_data }}"
  logs: "{{ grafana_paths_logs }}"


# Protocol (http or https)
grafana_server_protocol: http

# The ip address to bind to, empty will bind to all interfaces
grafana_server_http_addr: ""

# The http port to use
grafana_server_http_port: 3000

# The public facing domain name used to access grafana from a browser
grafana_server_domain: localhost

# The full public facing url
grafana_server_root_url: "%(protocol)s://%(domain)s:%(http_port)s/"
grafana_server_router_logging: "false"

# The path relative to the binary where the static (html/js/css) files are placed
grafana_server_static_root_path: public

# Enable gzip
grafana_server_enable_gzip: "false"

# SSL cert & key file if grafana_server_protocol is https
grafana_server_cert_file: ""
grafana_server_cert_key: ""

grafana_server:
  protocol: "{{ grafana_server_protocol }}"
  http_addr: "{{ grafana_server_http_addr }}"
  http_port: "{{ grafana_server_http_port }}"
  domain: "{{ grafana_server_domain }}"
  root_url: "{{ grafana_server_root_url }}"
  router_logging: "{{ grafana_server_router_logging }}"
  static_root_path: "{{ grafana_server_static_root_path }}"
  enable_gzip: "{{ grafana_server_enable_gzip }}"
  cert_file: "{{ grafana_server_cert_file }}"
  cert_key: "{{ grafana_server_cert_key }}"


# Either "mysql", "postgres" or "sqlite3", it's your choice
grafana_database_type: sqlite3
grafana_database_host: 127.0.0.1:3306
grafana_database_name: grafana
grafana_database_user: root
grafana_database_password: ""

# For "postgres" only, either "disable", "require" or "verify-full"
grafana_database_ssl_mode: disable

# For "sqlite3" only, path relative to data_path setting
grafana_database_path: grafana.db

grafana_database:
  type: "{{ grafana_database_type }}"
  host: "{{ grafana_database_host }}"
  name: "{{ grafana_database_name }}"
  user: "{{ grafana_database_user }}"
  password: "{{ grafana_database_password }}"
  ssl_mode: "{{ grafana_database_ssl_mode }}"
  path: "{{ grafana_database_path }}"


# Either "memory", "file", "redis", "mysql", default is "memory"
grafana_session_provider: file

# Provider config options
# memory: not have any config yet
# file: session dir path, is relative to grafana data_path
# redis: config like redis server addr, poolSize, password, e.g. `127.0.0.1:6379,100,grafana`
# mysql: go-sql-driver/mysql dsn config string, e.g. `user:password@tcp(127.0.0.1)/database_name`
grafana_session_provider_config: sessions

# Session cookie name
grafana_session_cookie_name: grafana_sess

# If you use session in https only, default is false
grafana_session_cookie_secure: "false"

# Session life time, default is 86400
grafana_session_session_life_time: 86400

grafana_session:
  provider: "{{ grafana_session_provider }}"
  provider_config: "{{ grafana_session_provider_config }}"
  cookie_name: "{{ grafana_session_cookie_name }}"
  cookie_secure: "{{ grafana_session_cookie_secure }}"
  session_life_time: "{{ grafana_session_session_life_time }}"


# Server reporting, sends usage counters to stats.grafana.org every 24 hours.
# No ip addresses are being tracked, only simple counters to track
# running instances, dashboard and error counts. It is very helpful to us.

# Change this option to false to disable reporting.
grafana_analytics_reporting_enabled: "true"

# Google Analytics universal tracking code, only enabled if you specify an id here
grafana_analytics_google_analytics_ua_id: ""

grafana_analytics:
  reporting_enabled: "{{ grafana_analytics_reporting_enabled }}"
  google_analytics_ua_id: "{{ grafana_analytics_google_analytics_ua_id }}"


# Default admin user, created on startup
grafana_security_admin_user: admin

# Default admin password, can be changed before first start of grafana,  or in profile settings
grafana_security_admin_password: admin

# Used for signing
grafana_security_secret_key: SW2YcwTIb9zpOOhoPsMm

# Auto-login remember days
grafana_security_login_remember_days: 7
grafana_security_cookie_username: grafana_user
grafana_security_cookie_remember_name: grafana_remember

grafana_security:
  admin_user: "{{ grafana_security_admin_user }}"
  admin_password: "{{ grafana_security_admin_password }}"
  secret_key: "{{ grafana_security_secret_key }}"
  login_remember_days: "{{ grafana_security_login_remember_days }}"
  cookie_username: "{{ grafana_security_cookie_username }}"
  cookie_remember_name: "{{ grafana_security_cookie_remember_name }}"


# Disable user signup / registration
grafana_users_allow_sign_up: "true"

# Allow non admin users to create organizations
grafana_users_allow_org_create: "true"

# Set to true to automatically assign new users to the default organization (id 1)
grafana_users_auto_assign_org: "true"

# Default role new users will be automatically assigned (if disabled above is set to true)
grafana_users_auto_assign_org_role: Viewer

grafana_users:
  allow_sign_up: "{{ grafana_users_allow_sign_up }}"
  allow_org_create: "{{ grafana_users_allow_org_create }}"
  auto_assign_org: "{{ grafana_users_auto_assign_org }}"
  auto_assign_org_role: "{{ grafana_users_auto_assign_org_role }}"


# Enable anonymous access
grafana_auth__anonymous_enabled: "false"

# Specify organization name that should be used for unauthenticated users
grafana_auth__anonymous_org_name: Main Org.

# Specify role for unauthenticated users
grafana_auth__anonymous_org_role: Viewer

grafana_auth__anonymous:
  enabled: "{{ grafana_auth__anonymous_enabled }}"
  org_name: "{{ grafana_auth__anonymous_org_name }}"
  org_role: "{{ grafana_auth__anonymous_org_role }}"


grafana_auth__github_enabled: "false"
grafana_auth__github_client_id: some_id
grafana_auth__github_client_secret: some_secret
grafana_auth__github_scopes: user:email
grafana_auth__github_auth_url: https://github.com/login/oauth/authorize
grafana_auth__github_token_url: https://github.com/login/oauth/access_token
grafana_auth__github_api_url: https://api.github.com/user
grafana_auth__github_allowed_domains: ""
grafana_auth__github_allow_sign_up: "false"

grafana_auth__github:
  enabled: "{{ grafana_auth__github_enabled }}"
  client_id: "{{ grafana_auth__github_client_id }}"
  client_secret: "{{ grafana_auth__github_client_secret }}"
  scopes: "{{ grafana_auth__github_scopes }}"
  auth_url: "{{ grafana_auth__github_auth_url }}"
  token_url: "{{ grafana_auth__github_token_url }}"
  api_url: "{{ grafana_auth__github_api_url }}"
  allowed_domains: "{{ grafana_auth__github_allowed_domains }}"
  allow_sign_up: "{{ grafana_auth__github_allow_sign_up }}"


grafana_auth__google_enabled: "false"
grafana_auth__google_client_id: some_client_id
grafana_auth__google_client_secret: some_client_secret
grafana_auth__google_scopes: https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email
grafana_auth__google_auth_url: https://accounts.google.com/o/oauth2/auth
grafana_auth__google_token_url: https://accounts.google.com/o/oauth2/token
grafana_auth__google_api_url: https://www.googleapis.com/oauth2/v1/userinfo
grafana_auth__google_allowed_domains: ""
grafana_auth__google_allow_sign_up: "false"

grafana_auth__google:
  enabled: "{{ grafana_auth__google_enabled }}"
  client_id: "{{ grafana_auth__google_client_id }}"
  client_secret: "{{ grafana_auth__google_client_secret }}"
  scopes: "{{ grafana_auth__google_scopes }}"
  auth_url: "{{ grafana_auth__google_auth_url }}"
  token_url: "{{ grafana_auth__google_token_url }}"
  api_url: "{{ grafana_auth__google_api_url }}"
  allowed_domains: "{{ grafana_auth__google_allowed_domains }}"
  allow_sign_up: "{{ grafana_auth__google_allow_sign_up }}"


# Either "console", "file", default is "console"
# Use comma to separate multiple modes, e.g. "console, file"
grafana_log_mode: console

# Buffer length of channel, keep it as it is if you don't know what it is.
grafana_log_buffer_len: 10000

# Either "Trace", "Debug", "Info", "Warn", "Error", "Critical", default is "Trace"
grafana_log_level: Info

grafana_log:
  mode: "{{ grafana_log_mode }}"
  buffer_len: "{{ grafana_log_buffer_len }}"
  level: "{{ grafana_log_level }}"


# Log level for "console" mode only
grafana_log__console_level: ""

grafana_log__console:
  level: "{{ grafana_log__console_level }}"


# Log level for "file" mode only
grafana_log__file_level: ""

# This enables automated log rotate(switch of following options), default is true
grafana_log__file_log_rotate: "true"

# Max line number of single file, default is 1000000
grafana_log__file_max_lines: 1000000

# Max size shift of single file, default is 28 means 1 << 28, 256MB
grafana_log__file_max_lines_shift: 28

# Segment log daily, default is true
grafana_log__file_daily_rotate: "true"

# Expired days of log file(delete after max days), default is 7
grafana_log__file_max_days: 7

grafana_log__file:
  level: "{{ grafana_log__file_level }}"
  log_rotate: "{{ grafana_log__file_log_rotate }}"
  max_lines: "{{ grafana_log__file_max_lines }}"
  max_lines_shift: "{{ grafana_log__file_max_lines_shift }}"
  daily_rotate: "{{ grafana_log__file_daily_rotate }}"
  max_days: "{{ grafana_log__file_max_days }}"


grafana_event_publisher_enabled: "false"
grafana_event_publisher_rabbitmq_url: amqp://localhost/
grafana_event_publisher_exchange: grafana_events

grafana_event_publisher:
  enabled: "{{ grafana_event_publisher_enabled }}"
  rabbitmq_url: "{{ grafana_event_publisher_rabbitmq_url }}"
  exchange: "{{ grafana_event_publisher_exchange }}"


grafana_config:
  app_mode: "{{ grafana_app_mode }}"
  paths: "{{ grafana_paths }}"
  server: "{{ grafana_server }}"
  database: "{{ grafana_database }}"
  session: "{{ grafana_session }}"
  analytics: "{{ grafana_analytics }}"
  security: "{{ grafana_security }}"
  users: "{{ grafana_users }}"
  auth.anonymous: "{{ grafana_auth__anonymous }}"
  auth.github: "{{ grafana_auth__github }}"
  auth.google: "{{ grafana_auth__google }}"
  log: "{{ grafana_log }}"
  log.console: "{{ grafana_log__console }}"
  log.file: "{{ grafana_log__file }}"
  event_publisher: "{{ grafana_event_publisher }}"
```


Dependencies
------------

* [`yumrepo`](https://github.com/picotrading/ansible-yumrepo) role


License
-------

MIT


Author
------

Jiri Tyr
