import configparser

from bottle import get, post, redirect, request, route, run, template
from knotenwanderung import Knotenwanderung


NODES = None


@route("/")
def greet():
    return template("general.tpl", title="Main", content=template("main.tpl"))


@post("/s")
def search_hostname():
    hostname = request.forms.get("hostname")
    if hostname is not None and hostname != "":
        redirect("/s/{}".format(hostname))
    else:
        redirect("/")


@get("/s/<hostname>")
def show_hostname(hostname):
    hostname_list = template("list.tpl", node_data=NODES.other_hostnames(hostname))
    return template("general.tpl", title=hostname, content=hostname_list)


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read("knotenwanderung.ini")

    NODES = Knotenwanderung(**conf["InfluxDBClient"])
    run(**conf["Bottle"])
