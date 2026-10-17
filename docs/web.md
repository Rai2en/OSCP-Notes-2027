# Web: choose the next test from a saved request

[Home](../README.md) · [Target workflow](methodology.md) · [Manual SQL injection](sql-injection.md) · [Historical web commands](../README.md#web-attacks)

**Use when:** a web port, redirect, hostname, login or API route is discovered. The first goal is a working request and a known negative response. Preserve method, path, Host, cookies, content type and CSRF token; change one variable at a time.

**Status:** documentation-reviewed; no web target or attack chain was executed during this revision. All addresses, accounts, bodies and response tables below are **synthetic illustrations**, not captured findings. Substitute values observed in your lab. The separately recorded [local SQL exercise](lab-validation.md) validates only its stated fixture.

## 1. Reach the intended application

**Clue:** an IP/port responds, but following a redirect fails to resolve a hostname. **Prerequisites:** the address and discovered hostname belong to the target; save the initial response before following redirects.

**Host/console:** Kali Bash, inside your private notes directory.

```bash
mkdir -p evidence/web
curl -sS -D evidence/web/ip.headers -o evidence/web/ip.body http://192.0.2.10:8080/
```

**Synthetic response fragment:**

```http
HTTP/1.1 302 Found
Location: http://inventory.lab.test:8080/
```

**Interpretation/next decision:** the application names a virtual host. Request that name at the observed address; do not replace the name with the IP inside a request that depends on Host routing.

```bash
curl -sS --resolve inventory.lab.test:8080:192.0.2.10 \
  -D evidence/web/home.headers -o evidence/web/home.html \
  http://inventory.lab.test:8080/
```

`--resolve` changes curl's connection mapping while the URL supplies the HTTP Host. For HTTPS, the hostname in the URL also supplies TLS SNI and certificate verification identity; use the actual HTTPS port and lab CA. If another redirect names a different host or port, investigate it explicitly instead of assuming the first mapping covers it.

**If this fails:** distinguish name resolution, TCP reachability, TLS/certificate failure and an application error. An HTTP redirect to an unresolved name is not the same as a closed port. Record the final host/port that served the working request.

## 2. Measure a nonexistent route before directory discovery

**Clue:** an application returns HTTP 200 even for invalid paths. **Prerequisites:** the intended Host works and the two control paths below are absent from the lab.

**Kali Bash:** retain both bodies; a status code or length alone is not a classifier.

```bash
curl -sS --resolve inventory.lab.test:8080:192.0.2.10 \
  -D evidence/web/missing-a.headers -o evidence/web/missing-a.html \
  http://inventory.lab.test:8080/missing-lab-7f29

curl -sS --resolve inventory.lab.test:8080:192.0.2.10 \
  -D evidence/web/missing-b.headers -o evidence/web/missing-b.html \
  http://inventory.lab.test:8080/missing-lab-a841
```

**Synthetic comparison:**

| Request | Status | Stable body marker | Decision |
|---|---|---|---|
| `/` | 200 | `Inventory home` | Known application baseline |
| `/missing-lab-7f29` | 200 | `Route not found` | Negative control despite HTTP 200 |
| `/missing-lab-a841` | 200 | `Route not found` | Supports a wildcard/soft-404 pattern |
| `/admin` (later discovered) | 200 | `Sign in` | Different page to investigate; not administrative access |

**Next decision:** configure allowed directory discovery around the observed negative pattern, then manually replay promising results. If the application echoes the requested path or changes tokens, length can vary on negative pages; inspect structure/markers as well. Avoid filtering all HTTP 200 responses or every page of a common length. A route that differs from the controls is a lead, not a vulnerability.

Inspect the working page's source, linked scripts, `robots.txt`, redirects and referenced API routes. Record a version only with its source and confidence. An HTTP header or scanner guess alone does not establish a matching exploitable component.

## 3. Pick a test that answers the observed question

| Observed feature | Smallest useful check | Evidence needed before the next step |
|---|---|---|
| Numeric lookup/search parameter | Save a working lookup, then paired conditions in the [SQL workflow](sql-injection.md) | Repeated result differences, not one error or delay |
| API object identifier | Compare private fixture objects using two lab accounts, below | Ownership/authorization expectation and the same request under the other session |
| Upload form | Upload a uniquely named harmless lab text marker using a saved valid request | Returned storage/reference, exact retrieval behavior and account permissions |
| File/path parameter | Compare normal behavior with reading a known harmless lab file | File content reached, rather than a reflected path or error |
| Application includes a local file | Establish inclusion/interpreter behavior separately from file reading | Traversal/read does not itself establish execution |
| Utility/command parameter | Compare a benign lab marker or identity result with the baseline | Server-generated result, not merely echoed input |
| A version-specific exploit appears relevant | Match product, feature, auth, platform and fixed/affected versions | Source and prerequisites documented before adaptation |

For uploads, an accepted file and HTTP 200 do not prove a writable executable web directory. Record renaming and retrieval URL. Download the harmless marker and compare its content; if it is served as an attachment or processed into another format, record that result. A separate execution claim requires an executing handler and verified behavior. Remove your marker through the lab's supported mechanism and note the cleanup.

## 4. Worked access-control comparison with two lab accounts

**Clue:** `/api/notes/<id>` returns account data. **Prerequisites:** you control two ordinary lab accounts of the same role, `lab-a` and `lab-b`. Create one private note in each with distinct harmless markers. Verify that `lab-a` owns note `101` and `lab-b` owns note `202`, and that the application does not intentionally share these notes.

**Host/console:** Burp Repeater. Capture a working request for each account first. Keep sessions separate and replace the illustrative session token below with the session of **lab-a**. Replay only the known fixture objects.

```http
GET /api/notes/202 HTTP/1.1
Host: inventory.lab.test:8080
Cookie: session=<LAB_A_SESSION>
Connection: close

```

**Synthetic comparison matrix:**

| Session / object | Expected private-note behavior | Illustrative observed result |
|---|---|---|
| `lab-a` / `101` | Read A's own note | 200 and `LAB-A-MARKER` |
| `lab-b` / `202` | Read B's own note | 200 and `LAB-B-MARKER` |
| `lab-a` / `202` | Deny B's private note, often 403/404 | 200 and `LAB-B-MARKER` — potential access-control failure |
| No session / `202` | Deny unauthenticated access or require login | 401 in this illustration |

**Interpretation:** the third row is meaningful because B's private content, created under a separate account, was returned to A. HTTP 200 by itself, an echoed ID or a login page would not prove this. Preserve the original request and returned marker. Reconfirm the two sessions have not been swapped and repeat the A→B read once.

**Next decision:** when confirmed, record horizontal unauthorized read of that object type and its effect. Test another action only if that action is an authorized objective with a fixture you control; one unauthorized read does not prove unauthorized write/delete or access to every record. If cross-account access is denied, record the negative result and inspect another evidenced route rather than enumerating arbitrary IDs.

**If results are inconsistent:** check session expiry, object sharing, caching and whether a CSRF token or account header is tied to the original session. Use the application's server response, not a hidden button in the browser, to judge authorization.

> **Exam Tip:** Keep one working request and its negative control before changing inputs. A failed replay can be a lost Host, cookie or token rather than a disproved vulnerability.

## 5. From a confirmed behavior to the next objective

When server-side execution is actually established, record the command's identity, OS, available runtime and writable location before choosing a callback. Confirm the destination is reachable **from the target**; an internal host may need a [pivot listener](pivoting.md). Keep the trigger request and resulting identity together in the [machine notes](../templates/machine.md).

For a public PoC, preserve its source and your changes. Review scheme/port, endpoint, auth/CSRF handling, shell and URL/JSON encoding, interpreter and architecture. If a prerequisite is absent, record why the PoC does not currently apply. Use [troubleshooting](troubleshooting.md) to isolate the failed layer.

## Primary references

- [curl manual](https://curl.se/docs/manpage.html): `--resolve`, response headers, output and TLS hostname handling.
- [Burp Repeater](https://portswigger.net/burp/documentation/desktop/tools/repeater): saved request replay and response comparison.
- [PortSwigger: insecure direct object references](https://portswigger.net/web-security/access-control/idor): object references and missing authorization.
- [PortSwigger: file uploads](https://portswigger.net/web-security/file-upload): server-side handling, validation and execution prerequisites.

The sources explain tool behavior and vulnerability models; none is a source of the fictional observations above.
