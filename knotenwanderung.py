import influxdb
import json
import re


class Knotenwanderung:
    "Wrapper class for InfluxDBClient to query the occurrence for some node."

    def __init__(self, **kwargs):
        self._influx = influxdb.InfluxDBClient(**kwargs)

    def __exit__(self, exc_type, exc_value, traceback):
        self._influx.close()

    def __enter__(self):
        return self

    def valid_hostname(self, hostname):
        "Checks if some hostname satisfies the FFMR regex."
        p = re.compile("35\d{3}-[\w-]{1,}")
        return p.fullmatch(hostname) != None

    def hostname_to_node_ids(self, hostname):
        "List all 'node_id's for a 'hostname'."
        if not self.valid_hostname(hostname):
            return {}

        params = params={"params": json.dumps({"hostname": hostname})}
        result = self._influx.query("""
            SHOW TAG VALUES WITH key = "node_id"
            WHERE "hostname" = $hostname
        """, params=params)
        return list({p["value"] for p in result.get_points()})

    def node_id_to_hostnames(self, node_id):
        "List all 'hostname's for a 'node_id'."
        params = params={"params": json.dumps({"node_id": node_id})}
        result = self._influx.query("""
            SHOW TAG VALUES WITH key = "hostname"
            WHERE "node_id" = $node_id
        """, params=params)
        return list({p["value"] for p in result.get_points()})

    def other_hostnames(self, hostname):
        "Return a dict of all 'hostname's sharing the same 'node_id'."
        node_ids = self.hostname_to_node_ids(hostname)
        return {node_id: self.node_id_to_hostnames(node_id) for node_id in node_ids}
