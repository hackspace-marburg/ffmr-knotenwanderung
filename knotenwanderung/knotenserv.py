import configparser

from bottle import abort, error, get, post, redirect, request, route, run, template
from functools import reduce
from knotenwanderung.knotenwanderung import Knotenwanderung


nodes = None


@route("/")
def greet():
    return template("knotenwanderung/general.tpl",
            title="Main", content=template("knotenwanderung/main.tpl"), search=None)


@post("/s")
def search_hostname():
    hostname = request.forms.get("hostname")
    if hostname is not None and hostname != "":
        redirect("/s/{}".format(hostname))
    else:
        redirect("/")


@get("/s/<hostname>")
def show_hostname(hostname):
    if not nodes.valid_hostname(hostname):
        abort(500)

    hostname_list = template("knotenwanderung/list.tpl", node_data=nodes.other_hostnames(hostname))
    return template("knotenwanderung/general.tpl",
            title=hostname, content=hostname_list, search=hostname)


@get("/bulk")
def bulk_mask():
    return template("knotenwanderung/general.tpl",
            title="Bulk Search", content=template("knotenwanderung/bulk_search.tpl"), search=None)


@post("/bulk")
def bulk_search():
    hostnames = request.forms.get("hostnames")
    if hostnames is None or hostnames.strip() == "":
        redirect("/bulk")

    # map each entered hostname to an amount of other hostnames
    # thus: 0 means unknown, 1 means unique, >1 means KNOTENWANDERUNG
    hostname_lst = map(lambda x: x.strip(), hostnames.strip().split("\n"))
    hostname_map = {h: nodes.other_hostnames(h)
            for h in hostname_lst if nodes.valid_hostname(h)}
    hostname_len = {k: reduce(lambda a, b: a + b, list(map(len, v.values())) + [0])
            for k, v in hostname_map.items()}

    hostname_len_tpl = template("knotenwanderung/bulk_result.tpl", hostname_len=hostname_len)
    return template("knotenwanderung/general.tpl",
            title="Bulk Search", content=hostname_len_tpl, search=None)


@error(404)
@error(500)
def error_page(err):
    return template("knotenwanderung/general.tpl",
            title="Error", content="Something went wrong..", search=None)


def main():
    conf = configparser.ConfigParser()
    conf.read("knotenwanderung.ini")

    global nodes
    nodes = Knotenwanderung(**conf["InfluxDBClient"])
    run(**conf["Bottle"])


if __name__ == '__main__':
    main()
