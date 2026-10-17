"""Run a bounded HTTP/SQLite teaching fixture on loopback, then shut it down.

The deliberately unparameterized SELECT demonstrates true/false request controls.
It uses an in-memory database with one synthetic product, binds 127.0.0.1 only,
accepts no remote target argument, and performs no writes after fixture setup.
This validates the local example, not any third-party target or offensive tool.
"""
import argparse
import json
import platform
import sqlite3
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import ProxyHandler, Request, build_opener


def rehearse(serve=False):
    database = sqlite3.connect(":memory:", check_same_thread=False)
    database.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT)")
    database.execute("INSERT INTO products VALUES (1, 'Lab notebook')")
    database.commit()
    database.execute("PRAGMA query_only = ON")

    class Handler(BaseHTTPRequestHandler):
        # Bound incomplete local requests so shutdown cannot wait indefinitely.
        timeout = 2

        def do_GET(self):
            parsed = urlsplit(self.path)
            status, body = 404, {"error": "not found"}
            if parsed.path == "/product":
                candidate = parse_qs(parsed.query).get("id", [""])[0]
                try:
                    # Intentionally vulnerable, read-only teaching query.
                    row = database.execute(
                        f"SELECT id, name FROM products WHERE id={candidate}"
                    ).fetchone()
                    if row:
                        status, body = 200, {"id": row[0], "name": row[1]}
                except sqlite3.Error:
                    status, body = 400, {"error": "invalid query"}
            payload = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *_args):
            pass

    # The OS selects an unused port; no public-interface or target option exists.
    server = HTTPServer(("127.0.0.1", 0), Handler)
    if serve:
        print(f"Local lab: http://127.0.0.1:{server.server_port} (Ctrl+C to stop)", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
            database.close()
        return []
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    opener = build_opener(ProxyHandler({}))
    records = []
    cases = [("baseline", "1", 200)]
    cases += [(name, value, status) for _ in range(3) for name, value, status in (
        ("true", "1 AND 1=1", 200), ("false", "1 AND 1=2", 404)
    )]
    cases += [("unknown route", None, 404)]
    expected_product = {"id": 1, "name": "Lab notebook"}
    try:
        for name, value, expected_status in cases:
            path = "/product?" + urlencode({"id": value}) if value else "/missing"
            request = Request(f"http://127.0.0.1:{server.server_port}{path}")
            try:
                response = opener.open(request, timeout=3)
            except HTTPError as error:
                response = error
            with response:
                status = response.code
                body = json.loads(response.read())
            expected_body = expected_product if expected_status == 200 else {"error": "not found"}
            if status != expected_status or body != expected_body:
                raise AssertionError(f"{name}: unexpected {status} {body!r}")
            record = f"{name}: GET {path} -> {status} {json.dumps(body)}"
            records.append(record)
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)
        database.close()
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serve", action="store_true", help="keep the loopback fixture open for manual replay until Ctrl+C")
    args = parser.parse_args()
    print(f"Python {platform.python_version()} / SQLite {sqlite3.sqlite_version}")
    for line in rehearse(serve=args.serve):
        print(line)
    if not args.serve:
        print("PASS: 8 bounded loopback requests; server closed; in-memory fixture discarded.")
