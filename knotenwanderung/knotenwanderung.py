import influxdb
import json
import re


class Node:
    "Node represents one Freifunk Node with its different hostnames."

    __slots__ = ["node_id", "hosts"]
    def __init__(self, node_id):
        self.node_id = node_id

    def __repr__(self):
        return self.node_id

    __str__ = __repr__


class Host:
    "Host is a hostname of a Node, together with its first and last appearance."

    __slots__ = ["node_id", "hostname", "first", "last"]
    def __init__(self, node_id, hostname):
        self.node_id = node_id
        self.hostname = hostname

    def __repr__(self):
        return f"{self.node_id} {self.hostname}"

    def __lt__(self, other):
        return self.hostname < other.hostname


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

    def _nodes_for_hostname(self, hostname):
        if not self.valid_hostname(hostname):
            return []

        params = params={"params": json.dumps({"hostname": hostname})}
        result = self._influx.query("""
            SHOW TAG VALUES WITH key = "node_id"
            WHERE "hostname" = $hostname
        """, params=params)
        unique_node_ids = {p["value"] for p in result.get_points()}

        return [Node(node_id) for node_id in unique_node_ids]

    def _populate_node_hosts(self, node):
        params = params={"params": json.dumps({"node_id": node.node_id})}
        result = self._influx.query("""
            SHOW TAG VALUES WITH key = "hostname"
            WHERE "node_id" = $node_id
        """, params=params)
        hostnames = {p["value"] for p in result.get_points()}

        node.hosts = [Host(node, hostname) for hostname in hostnames]

    def _populate_host_values(self, host):
        params = params={"params": json.dumps(
            {"node_id": str(host.node_id), "hostname": host.hostname})}

        result = self._influx.query("""
            SELECT FIRST(*) FROM "clients"
            WHERE "node_id" = $node_id AND "hostname" = $hostname
        """, params=params)
        host.first = result.get_points().__next__()['time']

        result = self._influx.query("""
            SELECT LAST(*) FROM "clients"
            WHERE "node_id" = $node_id AND "hostname" = $hostname
        """, params=params)
        host.last = result.get_points().__next__()['time']

    def _populate_node(self, node):
        self._populate_node_hosts(node)
        for host in node.hosts:
            self._populate_host_values(host)

    def node(self, node_id):
        "Create a populated Node by its node_id."
        node = Node(node_id)
        self._populate_node(node)
        return node

    def nodes_for_hostname(self, hostname):
        "Create a list of populated Nodes identified by a hostname."
        nodes = self._nodes_for_hostname(hostname)
        for node in nodes:
            self._populate_node(node)
        return nodes
