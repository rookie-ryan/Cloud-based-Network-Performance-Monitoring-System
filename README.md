#  Cloud-based Network Performance Monitoring System
This is a monitoring system to periodically measure the inter-datacenter network performance over various public clouds. Currently, the monitored performance includes **end-to-end delay** and **loss rate**.

## Preparation
To clone this repository, run:

```
git clone https://github.com/rookie-ryan/Cloud-based-Network-Performance-Monitoring-System.git
```
## Dependencies
To install required dependencies, run the handy script `tools/install_deps.sh` we provide:

```
./tools/install_deps.sh
```
## Vantage points
To build a monitoring testbed, you can lease VMs as vantage points from public clouds, e.g. AWS, Azure, Aliyun. You need to maintain the list of vantage points `vantage_points.json`
## Start monitoring
To start the monitoring system, run:

```
python src/performance_test.py
```

The monitoring result data are kept in `data/`.
## Monitoring parameters
If needed, you can customize the monitoring parameters at `monitor_parameters.json`. The parameters includes **monitoring interval** (seconds, default is 30), **test package size** (data bytes combined with 8 bytes of header, default is 56) and **the number of packages sent for each test** (default is 4).