# Knotenwanderung

A web service to check whether [Marburg's Freifunk][ffmr] nodes have potentially
renamed themselves. For this purpose, the same database (InfluxDB) is accessed
as for the [Grafana][grafana]. Allows both querying single nodes and performing
bulk requests.


## Deployment

1. Install a recent Python 3 together with [bottle][] and [influxdb-python][].
2. Copy `knotenwanderung_example.ini` to `knotenwanderung.ini` and edit it.
3. `python knotenserv.py`


[ffmr]: https://marburg.freifunk.net/
[grafana]: https://grafana.hsmr.cc/
[influxdb-python]: https://github.com/influxdata/influxdb-python
[bottle]: https://bottlepy.org/docs/dev/
