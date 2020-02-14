import configparser
import json

from bottle import get, post, redirect, request, route, run, template
from knotenwanderung import Knotenwanderung


NODES = None


@route("/")
def greet():
    return template("template.tpl", title="Main", content="nope")


@post("/s")
def search_hostname():
    hostname = request.forms.get("hostname")
    if hostname is not None and hostname != "":
        redirect("/s/{}".format(hostname))
    else:
        redirect("/")


@get("/s/<hostname>")
def show_hostname(hostname):
    nodes = json.dumps(NODES.other_hostnames(hostname))
    return template("template.tpl", title=hostname, content=nodes)


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read("knotenwanderung.ini")

    NODES = Knotenwanderung(**conf["InfluxDBClient"])
    run(**conf["Bottle"])
