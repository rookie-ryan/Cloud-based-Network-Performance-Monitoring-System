#  Live Streaming Delivery Overlay Network
## Preparation
To clone this repository, run:

```
git clone https://github.com/rookie-ryan/Cloud-based-Network-Performance-Monitoring-System.git
```
Then open the folder to run following commands:
```
cd Cloud-based-Network-Performance-Monitoring-System
```
To install required dependencies, run the handy script `tools/install_deps.sh` we provide:

```
bash tools/install_deps.sh
```
To build a monitoring testbed, you can lease VMs as vantage points from public clouds, e.g. AWS, Azure, Aliyun. You need to maintain the list of vantage points `vantage_points.json`

## Network Monitoring Module
Periodically measure the inter-datacenter network performance over various public clouds. Currently, the monitored performance includes **end-to-end delay** and **loss rate**.
### Start monitoring
To start the monitoring system, run:

```
python3 src/parallel_test.py
```
### Result format 
The monitoring result data are kept in `data/`, e.g. `data/2021-08/07.json` save the data monitored in 2021-08-07.

In the result files, each line represents a test. The data format is *time:{ip:{loss rate,rtt}}*, for example:
```
{"07:28:51":
    {"44.192.46.176": {"loss rate": "0% packet loss", "rtt": "min/avg/max/mdev = 0.339/0.349/0.363/0.024 ms"}, 
    "8.8.8.8": {"loss rate": "0% packet loss", "rtt": "min/avg/max/mdev = 0.695/0.781/0.822/0.061 ms"}}
}
{"07:29:24": 
    {"44.192.46.176": {"loss rate": "0% packet loss", "rtt": "min/avg/max/mdev = 0.333/0.353/0.381/0.025 ms"}, 
    "8.8.8.8": {"loss rate": "0% packet loss", "rtt": "min/avg/max/mdev = 0.662/0.689/0.726/0.023 ms"}}
}
```
### Monitoring parameters
If needed, you can customize the monitoring parameters at `monitor_parameters.json`. The parameters includes **monitoring interval** (seconds, default is 30), **test package size** (data bytes combined with 8 bytes of header, default is 56) and **the number of packages sent for each test** (default is 10).

## Live Streaming Module
To be done
