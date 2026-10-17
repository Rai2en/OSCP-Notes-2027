# Validation: what was actually exercised

[Home](../README.md) · [Technique record](../templates/technique.md) · [Coverage](coverage.md)

## Status definitions

| Label | Evidence required |
|---|---|
| Illustrative output | A constructed example to explain a decision; never presented as captured target output. |
| Source-reviewed | Options/behavior compared with primary documentation; installed versions and target behavior still need checking. |
| Local fixture tested | A bounded exercise executed locally with recorded runtime/results. Its scope does not include other targets or tools. |
| Target-lab-tested | A dated reproducible run with tool/target versions, configuration, expected/observed results and limitations. |

## Executed record: HTTP true/false controls

**Date:** 2026-10-17. **Status:** local fixture tested. **Runtime observed:** Python 3.12.14, SQLite 3.53.1, Windows host. **Source:** [rehearse_web.py](../scripts/rehearse_web.py).

From the repository root, with Python 3:

```bash
python3 scripts/rehearse_web.py
```

The script creates one synthetic product in an in-memory SQLite database, enables query-only access, binds HTTP to `127.0.0.1` on an unused port, sends a fixed sequence of eight requests and shuts down. It has no target or external-interface argument, does not consult proxy settings and does not download or install anything.

Observed output:

```text
Python 3.12.14 / SQLite 3.53.1
baseline: GET /product?id=1 -> 200 {"id": 1, "name": "Lab notebook"}
true: GET /product?id=1+AND+1%3D1 -> 200 {"id": 1, "name": "Lab notebook"}
false: GET /product?id=1+AND+1%3D2 -> 404 {"error": "not found"}
true: GET /product?id=1+AND+1%3D1 -> 200 {"id": 1, "name": "Lab notebook"}
false: GET /product?id=1+AND+1%3D2 -> 404 {"error": "not found"}
true: GET /product?id=1+AND+1%3D1 -> 200 {"id": 1, "name": "Lab notebook"}
false: GET /product?id=1+AND+1%3D2 -> 404 {"error": "not found"}
unknown route: GET /missing -> 404 {"error": "not found"}
PASS: 8 bounded loopback requests; server closed; in-memory fixture discarded.
```

**Conclusion:** in this deliberately unparameterized local SELECT, the baseline and true expression return the same object; three alternating false expressions return no object. This demonstrates why contrasting controls support a narrower conclusion than one changed/slow response. It does not demonstrate data extraction, file access, OS execution, blind timing behavior or compatibility with MySQL/MSSQL/PostgreSQL. See [the SQL procedure](sql-injection.md).

**Cleanup:** the server closes in `finally`, and the in-memory database is discarded. The exercise creates no target accounts, files or persistent service. The intentionally vulnerable fixture is a teaching aid; it is not application code to reuse in a deployed service.

## Replay manually with curl or Repeater

```bash
python3 scripts/rehearse_web.py --serve
```

This optional mode prints the loopback URL and keeps the same disposable fixture running. Use that printed port in [the SQL procedure](sql-injection.md); replace its `<LAB_PORT>` placeholder. It listens only on this computer, so run the HTTP client on the same machine. Stop with Ctrl+C when finished; the database is discarded. The automatic run above is the recorded validation, not a claim that every client/version was exercised.

An additional local check on 2026-10-17 started this mode, left one HTTP request incomplete, then sent a complete product request. The handler's two-second timeout released the incomplete connection; the complete request returned the expected `200` product in 2.02 seconds. The test process was then stopped. This checks bounded local responsiveness, not browser coverage or a remote application.

## Target-lab repetitions still required

| Procedure | Current status | Minimal record to add before target-lab-tested status |
|---|---|---|
| [Discovery](methodology.md) | Source-reviewed | Installed Nmap version, known listening/filtered ports, route, all-port and selected-service results. |
| [SMB](smb.md) | Source-reviewed; illustrative outputs | Server/client versions; anonymous denial, known scoped login, one readable and one denied resource, resulting decision. |
| [Windows services](windows-services.md) | Source-reviewed; illustrative outputs | OS build; token groups; service/file/directory ACLs; permitted trigger and observed identity. |
| [Linux permissions](linux-permissions.md) | Source-reviewed; illustrative outputs | Distro/sudo/binary versions; run-as/argument constraints, actual owner/mount behavior and resulting identity. |
| [AD](active-directory.md) | Source-reviewed; illustrative outputs | Domain/DC build, collector version, current principal, live object ACL/membership, permission and access actually obtained. |
| [Pivoting](pivoting.md) | Source-reviewed; illustrative outputs | Proxy/agent versions, topology, route, forward TCP result, return file transfer and cleanup; repeat per hop. |
| [NFS](nfs.md) | Source-reviewed; illustrative outputs | Client/server versions, export/source policy, numeric ownership, effective read/write mapping and mount options. |
| [Client workflow](pentest.md) | Illustrative assessment/finding | Agreed scope, two controlled identities, expected versus observed access, bounded evidence, restored state and retest. |

Use the [technique template](../templates/technique.md) for each record. Keep private evidence outside the public repo and replace identifying material with synthetic examples when sharing a generic lesson. A downloaded PoC, successful help command or corrected link does not satisfy this record.

## Repository checks have a different scope

```bash
python3 scripts/check_docs.py
python3 -m unittest discover -s tests -v
git diff --check
```

These check document navigation, notebook behavior and repository consistency. They do not prove that a target is vulnerable, authorize an exam feature or replace a target-lab repetition.
