# Knotenwanderung

A web service to check whether [Marburg's Freifunk][ffmr] nodes have potentially
renamed themselves. For this purpose, the same database (InfluxDB) is accessed
as for the [Grafana][grafana]. Allows both querying single nodes and performing
bulk requests.


## Development

1. Install a recent Python 3 together with the dependencies specified in
  `setup.py`: [bjoern][], [bottle][], and [influxdb-python][].
2. Copy `knotenwanderung_example.ini` to `knotenwanderung.ini` and edit it.
3. `python -m knotenwanderung.knotenserv knotenwanderung.ini`


## NixOS Deployment

Take a look at the `module.nix` file and adjust it to your needs. After being
included, one might configure its system as follows:

```nix
{
  services.knotenwanderung = {
    enable = true;

    # Values from the ini configuration.
    config = {
      influxdb = {
        host = "influx.example.com"; port = 1312; database = "ff";
      };
      bottle = {
        host = "localhost"; port = 8080;
      };
    };
  };
}
```


[ffmr]: https://marburg.freifunk.net/
[grafana]: https://grafana.hsmr.cc/
[influxdb-python]: https://github.com/influxdata/influxdb-python
[bjoern]: https://github.com/jonashaag/bjoern
[bottle]: https://bottlepy.org/docs/dev/
