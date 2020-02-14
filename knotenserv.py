import configparser

from bottle import error, get, post, redirect, request, route, run, template
from functools import reduce
from knotenwanderung import Knotenwanderung


NODES = None


@route("/")
def greet():
    return template("general.tpl",
            title="Main", content=template("main.tpl"), search=None)


@post("/s")
def search_hostname():
    hostname = request.forms.get("hostname")
    if hostname is not None and hostname != "":
        redirect("/s/{}".format(hostname))
    else:
        redirect("/")


@get("/s/<hostname:re:35\d{3}-[\w-]{1,}>")
def show_hostname(hostname):
    hostname_list = template("list.tpl", node_data=NODES.other_hostnames(hostname))
    return template("general.tpl",
            title=hostname, content=hostname_list, search=hostname)


@get("/bulk")
def bulk_mask():
    return template("general.tpl",
            title="Bulk Search", content=template("bulk_search.tpl"), search=None)


@post("/bulk")
def bulk_search():
    hostnames = request.forms.get("hostnames")
    if hostnames is None or hostnames.strip() == "":
        redirect("/bulk")

    # map each entered hostname to an amount of other hostnames
    # thus: 0 means unknown, 1 means unique, >1 means KNOTENWANDERUNG
    hostname_map = {h.strip(): NODES.other_hostnames(h.strip())
            for h in hostnames.strip().split("\n")}
    hostname_len = {k: reduce(lambda a, b: a + b, list(map(len, v.values())) + [0])
            for k, v in hostname_map.items()}

    hostname_len_tpl = template("bulk_result.tpl", hostname_len=hostname_len)
    return template("general.tpl",
            title="Bulk Search", content=hostname_len_tpl, search=None)


@error(404)
@error(500)
def error_page(err):
    return template("general.tpl",
            title="Error", content="Something went wrong..", search=None)


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read("knotenwanderung.ini")

    NODES = Knotenwanderung(**conf["InfluxDBClient"])
    run(**conf["Bottle"])
