import datetime
import influxdb
import json
import logging
import re

from cachetools import cached, TTLCache


logger = logging.getLogger("knotenwanderung")


class DayCache(TTLCache):
    "A Cache implementation which holds a value untils the day's end."

    def timer(self):
        now = datetime.date.today()
        return now.year * (10 ** 4) + now.month * (10 ** 2) + now.day

    def __init__(self, maxsize, **kwargs):
        super().__init__(maxsize, ttl=0, timer=self.timer, **kwargs)


class Node:
    "Node represents one Freifunk Node with its different hostnames."

    __slots__ = ["node_id", "hosts", "availability"]
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
        return f"{self.node_id}/{self.hostname}"

    def __lt__(self, other):
        return self.last < other.last


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
        p = re.compile("35\d{3}-[\w\.-]+")
        return p.fullmatch(hostname) != None

    @cached(cache=DayCache(1024))
    def _fetch_nodes_for_hostname(self, hostname):
        logger.debug(f"fetch nodes for hostname \"{hostname}\"")

        if not self.valid_hostname(hostname):
            return []

        params = params={"params": json.dumps({"hostname": hostname})}
        result = self._influx.query("""
            SHOW TAG VALUES WITH key = "node_id"
            WHERE "hostname" = $hostname
        """, params=params)
        unique_node_ids = {p["value"] for p in result.get_points()}

        return [Node(node_id) for node_id in unique_node_ids]

    @cached(cache=DayCache(1024))
    def _fetch_availability_for_node_id(self, node_id):
        logger.debug(f"fetch availability for node \"{node_id}\"")

        params = params={"params": json.dumps({"node_id": node_id})}
        result = self._influx.query("""
            SELECT count("value")  / (60 * 24 * 30) FROM "clients"
            WHERE "node_id" = $node_id AND time > now() - 30d
        """, params=params)

        counts = list(result.get_points())
        if len(counts) == 1:
            return counts[0]["count"]
        else:
            return 0.0

    @cached(cache=DayCache(1024))
    def _fetch_hosts_for_node_id(self, node_id):
        logger.debug(f"fetch hosts for node \"{node_id}\"")

        params = params={"params": json.dumps({"node_id": node_id})}
        result = self._influx.query("""
            SHOW TAG VALUES WITH key = "hostname"
            WHERE "node_id" = $node_id
        """, params=params)
        return {p["value"] for p in result.get_points()}

    @cached(cache=DayCache(1024))
    def _fetch_host_values(self, node_id, hostname):
        logger.debug(f"fetch host values for \"{node_id}/{hostname}\"")

        params = params={"params": json.dumps(
            {"node_id": node_id, "hostname": hostname})}

        result = self._influx.query("""
            SELECT FIRST(*) FROM "clients"
            WHERE "node_id" = $node_id AND "hostname" = $hostname
        """, params=params)
        first = result.get_points().__next__()["time"]

        result = self._influx.query("""
            SELECT LAST(*) FROM "clients"
            WHERE "node_id" = $node_id AND "hostname" = $hostname
        """, params=params)
        last = result.get_points().__next__()["time"]

        return {"first": datetime.datetime.strptime(first, "%Y-%m-%dT%H:%M:%SZ"),
                "last": datetime.datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ")}

    def _populate_node(self, node):
        node.availability = self._fetch_availability_for_node_id(node.node_id)

        hostnames = self._fetch_hosts_for_node_id(node.node_id)
        node.hosts = [Host(node, hostname) for hostname in hostnames]

        for host in node.hosts:
            host_data = self._fetch_host_values(str(host.node_id), host.hostname)
            host.first = host_data['first']
            host.last = host_data['last']

        node.hosts.sort()

    def node(self, node_id):
        "Create a populated Node by its node_id."
        node = Node(node_id)
        self._populate_node(node)
        return node

    def nodes_for_hostname(self, hostname):
        "Create a list of populated Nodes identified by a hostname."
        nodes = self._fetch_nodes_for_hostname(hostname)
        for node in nodes:
            self._populate_node(node)
        return nodes
