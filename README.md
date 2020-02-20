# Knotenwanderung

A web service to check whether [Marburg's Freifunk][ffmr] nodes have potentially
renamed themselves. For this purpose, the same database (InfluxDB) is accessed
as for the [Grafana][grafana]. Allows both querying single nodes and performing
bulk requests.


## Development

1. Install a recent Python 3 together with the dependencies specified in
  `setup.py`: [bjoern], [bottle], [cachetools], and [influxdb-python].
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


## Licenses

This application is released under the GNU Affero General Public License, as
specified in the `LICENSE` file. However, this repository also contains a
compiled version of [Bootstrap][bootstrap] (MIT License) and [jQuery][jquery]
(jQuery License).


[bjoern]: https://github.com/jonashaag/bjoern
[bootstrap]: https://getbootstrap.com/
[bottle]: https://bottlepy.org/docs/dev/
[cachetools]: https://github.com/tkem/cachetools
[ffmr]: https://marburg.freifunk.net/
[grafana]: https://grafana.hsmr.cc/
[influxdb-python]: https://github.com/influxdata/influxdb-python
[jquery]: https://jquery.com/
