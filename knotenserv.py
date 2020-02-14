import configparser

from bottle import get, route, run
from knotenwanderung import Knotenwanderung


NODES = None


@route("/")
def greet():
    return "uwu"


@get("/s/<hostname>")
def search_hostname(hostname):
    return NODES.other_hostnames(hostname)


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read("knotenwanderung.ini")

    NODES = Knotenwanderung(**conf["InfluxDBClient"])
    run(**conf["Bottle"])
