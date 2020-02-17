import configparser
import sys

from bottle import abort, error, get, post, redirect, request, route, run, template
from functools import reduce
from knotenwanderung.knotenwanderung import Knotenwanderung
from os import path


nodes = None


@route("/")
def greet():
    main_tpl = template("{}/main.tpl".format(path.dirname(__file__)))
    return template("{}/general.tpl".format(path.dirname(__file__)),
            title="Main", content=main_tpl, search=None)


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

    hostname_list = template("{}/list.tpl".format(path.dirname(__file__)),
        node_data=nodes.other_hostnames(hostname))
    return template("{}/general.tpl".format(path.dirname(__file__)),
            title=hostname, content=hostname_list, search=hostname)


@get("/bulk")
def bulk_mask():
    bulk_mask_tpl = template("{}/bulk_search.tpl".format(path.dirname(__file__)))
    return template("{}/general.tpl".format(path.dirname(__file__)),
            title="Bulk Search", content=bulk_mask_tpl, search=None)


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

    hostname_len_tpl = template("{}/bulk_result.tpl".format(path.dirname(__file__)),
        hostname_len=hostname_len)
    return template("{}/general.tpl".format(path.dirname(__file__)),
            title="Bulk Search", content=hostname_len_tpl, search=None)


@error(404)
@error(500)
def error_page(err):
    return template("{}/general.tpl".format(path.dirname(__file__)),
            title="Error", content="Something went wrong..", search=None)


def main():
    if len(sys.argv) != 2:
        print("Usage: {} config.ini".format(sys.argv[0]))
        return

    conf = configparser.ConfigParser()
    conf.read(sys.argv[1])

    global nodes
    nodes = Knotenwanderung(**conf["influxdb"])
    run(**conf["bottle"])


if __name__ == '__main__':
    main()
