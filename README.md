# uWSGI Stats Monitoring Extension

##Use Case

This extension pulls data from the [uWSGI Stats Server](http://uwsgi-docs.readthedocs.io/en/latest/StatsServer.html), if enabled, and sends the metrics to your AppDynamics controller instance. 

This extension only works with standalone Machine Agent. 

**Note : By default, the Machine Agent can only send a fixed number of metrics to the controller. To change this limit, please follow the instructions mentioned [here](http://docs.appdynamics.com/display/PRO14S/Metrics+Limits).**

##Installation
1. Clone this repository into your Machine Agent installation directory - \<machine_agent_dir\>/monitors/
2. Restart the Machine Agent.

##Configuration
| Param | Description |
| ----- | ----- |


##Metrics
Metric path is typically: **Application Infrastructure Performance|\<Tier\>|Custom Metrics|Hardware Resources|\<Node\>|Processes|uwsgi|** followed by the metrics below:

###Global uWSGI statistics

| Metric | Description |
| ----- | ----- |
| Active Workers | The total number of active uWSGI processes. (This does not include workers that were started with `cheap`.) |
| Total Workers | The total number uWSGI processes, include processes that were started with `cheap`. |
| Total Harakiri Count | The total number of times that uWSGI processes that were terminated due to a timeout. |


###Individual uWSGI process statistics
**Note: \<process_id\> is replaced with the actual uwsgi process id**

| Metric | Description |
| ----- | ----- |
| \<process_id\>&#124;Harakiri Count | The total number of times that this uwsgi process was terminated due to a timeout. |
| \<process_id\>&#124;Total Requests | The total number of requests this uwsgi process has processed. |
| \<process_id\>&#124;Total Exceptions | The total number of exceptions returned by this uwsgi process. |
| \<process_id\>&#124;Total Running Time (s) | The total time, in seconds, that this uwsgi process has been running. |
| \<process_id\>&#124;Total Transmitted Data (MB) | The total amount of data, in MB, that this uwsgi process has returned. |
| \<process_id\>&#124;Respawn Count | The total number of times that this uwsgi process was restarted. |
| \<process_id\>&#124;Average Response Time (s) | The average response time for this uwsgi process. |


##Platform Tested

| Platform | Version |
| ----- | ----- |
| Ubuntu | 12.04 LTS |


##Agent Compatibility

| Version |
| ----- |
| 3.7.11+ |

##Contributing

Always feel free to fork and contribute any changes directly here on GitHub.

##Community

Find out more in the [AppSphere](http://community.appdynamics.com/t5/eXchange-Community-AppDynamics/Network-Monitoring-Extension/idi-p/9497) community.

##Support

For any questions or feature request, please contact [AppDynamics Support](mailto:help@appdynamics.com).

