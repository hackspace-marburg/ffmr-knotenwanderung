import configparser
import pathlib
import sys

from bottle import abort, error, get, post, redirect, request, route, run, template
from functools import reduce
from knotenwanderung.knotenwanderung import Knotenwanderung


nodes = None


def load_template(name, **kwargs):
    "Wrapper around bottle's template function for the right template path."
    template_dir = pathlib.PurePath(__file__).parent.joinpath("templates")
    template_file = f"{template_dir}/{name}.tpl"
    return template(template_file, **kwargs)


def serve_template(title, content, search=None):
    "Serve the general template."
    return load_template("general", title=title, content=content, search=search)


@route("/")
def greet():
    return serve_template("Main", load_template("main"))


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

    return serve_template(
            hostname,
            load_template("list", node_data=nodes.other_hostnames(hostname)),
            hostname)


@get("/bulk")
def bulk_mask():
    return serve_template("Bulk Search", load_template("bulk_search"))


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

    return serve_template("Bulk Search",
            load_template("bulk_result", hostname_len=hostname_len))


@error(404)
@error(500)
def error_page(err):
    return serve_template("Error", "Something went wrong..")


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
