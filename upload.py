import requests, json, os
from pathlib import Path

TOKEN = os.environ["TOKEN"]
DOMAIN = os.environ["DOMAIN"]
FUNC = os.environ["FUNC"]


def upload_templates():
    for path in Path("templates").glob("**/*.html"):
        print(path)
        with open(path, "r") as f:
            r = requests.put(
                f"{DOMAIN}/_data/{path}",
                headers={"Authorization": f"Token {TOKEN}"},
                verify=0,
                data={"data": json.dumps(f.read()), "path": path},
            )


def upload_static():
    for path in Path("static").glob("**/*.*"):
        print(path)
        with open(path, "rb") as f:
            r = requests.put(
                f"{DOMAIN}/_data/{path}",
                headers={"Authorization": f"Token {TOKEN}"},
                verify=0,
                files={"file": f},
                data={"data": 1, "path": path},
            )
            if r.status_code == 500:
                print("ERROR:", r.content.decode())

def upload_code():
    path = 'main.snek'
    print(path)
    with open(path, "rb") as f:
        r = requests.patch(
            f"{FUNC}",
            headers={"Authorization": f"Token {TOKEN}"},
            verify=0,
            data={"code": f.read()},
        )
        print(r.content.decode())

if __name__ == '__main__':
    import argparse
    import urllib3
    urllib3.disable_warnings()
    parser = argparse.ArgumentParser(description='Upload code, templates, or static files')
    parser.add_argument('-c', '--code', action='store_true')
    parser.add_argument('-t', '--templates', action='store_true')
    parser.add_argument('-s', '--static', action='store_true')
    args = parser.parse_args()

    if args.static:
        upload_static()
    if args.templates:
        upload_templates()
    if args.code:
        upload_code()
