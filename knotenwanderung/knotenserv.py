import configparser
import logging
import pathlib
import sys

from functools import reduce, wraps

from bottle import Bottle, HTTPError, HTTPResponse
from bottle import abort, redirect, request, response, run, static_file, template

from .knotenwanderung import Knotenwanderung


app = Bottle()
nodes = None
logger = logging.getLogger("knotenwanderung")


def load_template(name, **kwargs):
    "Wrapper around bottle's template function for the right template path."
    template_dir = pathlib.PurePath(__file__).parent.joinpath("templates")
    template_file = f"{template_dir}/{name}.tpl"
    return template(template_file, **kwargs)


def serve_template(title, content, search=None):
    "Serve the general template."
    return load_template("general", title=title, content=content, search=search)


@app.get("/")
def greet():
    return serve_template("Main", load_template("main"))


@app.post("/s")
def search_hostname():
    hostname = request.forms.get("hostname")
    if hostname is not None and hostname != "":
        redirect(f"/s/{hostname}")
    else:
        redirect("/")


@app.get("/s/<hostname>")
def show_hostname(hostname):
    if not nodes.valid_hostname(hostname):
        abort(500)

    return serve_template(
            hostname,
            load_template("list", node_data=nodes.nodes_for_hostname(hostname)),
            hostname)


@app.get("/bulk")
def bulk_mask():
    return serve_template("Bulk Search", load_template("bulk_search"))


@app.post("/bulk")
def bulk_search():
    hostnames = request.forms.get("hostnames")
    if hostnames is None or hostnames.strip() == "":
        redirect("/bulk")

    # map each entered hostname to an amount of other hostnames
    # thus: 0 means unknown, 1 means unique, >1 means KNOTENWANDERUNG
    hostname_map = {h.strip(): nodes.nodes_for_hostname(h.strip())
            for h in hostnames.strip().split("\n")
            if nodes.valid_hostname(h.strip())}
    hostname_len = {k: reduce(lambda a, b: a + b, list(map(lambda x: len(x.hosts), v)) + [0])
            for k, v in hostname_map.items()}

    return serve_template("Bulk Search",
            load_template("bulk_result", hostname_len=hostname_len))


@app.error(404)
@app.error(500)
def error_page(err):
    return serve_template("Error", "Something went wrong..")


@app.get("/static/<filepath:path>")
def serve_static(filepath):
    static_dir = pathlib.PurePath(__file__).parent.joinpath("static")
    return static_file(filepath, root=static_dir)


def bottle_logger(fn):
    "Wraps bottle's logger into Python logging."
    @wraps(fn)
    def _bottle_logger(*args, **kwargs):
        try:
            resp = fn(*args, **kwargs)
            logger.info(f"{request.method} {response.status_code} {request.path}")
            return resp
        except HTTPError as e:
            logger.warning(f"{request.method} {e.status_code} {request.path}: {e.body}")
            raise e
        except HTTPResponse as r:
            if r.status_code == 303:
                logger.info(f"{request.method} {r.status_code} {request.path} -> {r._headers}")
            else:
                logger.info(f"{request.method} {r.status_code} {request.path}")
            raise r
        except Exception as e:
            logger.error(f"{request.method} {request.path}: {e}")
            raise e

    return _bottle_logger


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} config.ini")
        return

    conf = configparser.ConfigParser()
    conf.read(sys.argv[1])

    global nodes
    nodes = Knotenwanderung(**conf["influxdb"])

    logHandler = logging.StreamHandler()
    logHandler.setFormatter(logging.Formatter("%(levelname)-5s %(message)s"))

    logger.addHandler(logHandler)
    logger.setLevel(logging.DEBUG)

    app.install(bottle_logger)

    run(**{
        **{"app": app, "server": "bjoern", "quiet": True},
        **conf["bottle"]})


if __name__ == '__main__':
    main()
