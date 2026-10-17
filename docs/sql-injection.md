# Manual SQL injection: establish a reproducible difference

[Home](../README.md) · [Web triage](web.md) · [Local validation exercise](lab-validation.md) · [Historical SQL commands](../README.md#sql-injection)

**Use when:** a request parameter affects a database-backed lookup, or a reproducible response/error suggests SQL processing. Start with a request that already works and one input you can isolate.

**Status:** the method and syntax below were reviewed against primary documentation. All response bodies and measurements on this page are **synthetic illustrations**, not captured target output. The separate [local validation record](lab-validation.md) identifies the bounded exercise actually executed and its limits. No external target, database extraction or OS execution was tested for this page.

## 1. Establish the request and its prerequisites

This worked example assumes a deliberately vulnerable **SQLite lab** with a read-only product lookup:

- A running lab HTTP endpoint `/product?id=1` returns the fixture product `Lab notebook`.
- The lab deliberately concatenates the `id` text into a numeric SQL expression. Its conceptual query is `SELECT id, name FROM products WHERE id = <untrusted_id>`; this is an explanation, not a command to paste into a SQL console.
- A query returning no row is rendered as HTTP 404 with `{"error":"not found"}`. That mapping belongs to this lab, not SQLite generally.
- Only this known product lookup is used. A login, update, delete, quoted string or JSON input can require a different approach.

The repository's [local exercise instructions](lab-validation.md) explain how to start the matching disposable example. Use the printed local port; do not assume a service exists at the placeholder below. For another authorized lab, replace the endpoint, session and context using a captured valid request.

**Host/console:** Kali Bash or another shell with curl, inside a private session directory. Replace `<LAB_PORT>` before executing.

```bash
export APP_URL='http://127.0.0.1:<LAB_PORT>'
mkdir -p evidence/sql
```

**Baseline request**, represented as HTTP for Burp Repeater. Preserve the actual Host, method and session headers when working on an authenticated application.

```http
GET /product?id=1 HTTP/1.1
Host: 127.0.0.1:<LAB_PORT>
Connection: close

```

Send the same baseline more than once before changing it. If it redirects to a login, loses a CSRF token, returns a cache error or alternates between different pages, fix that first. An unstable baseline cannot support a clean comparison.

## 2. Change only the numeric condition

**Kali Bash:** these three requests save headers and bodies separately. `--data-urlencode` performs query encoding; `--get` keeps the request a GET. Do not manually encode the same payload a second time.

```bash
curl -sS --get "$APP_URL/product" --data-urlencode 'id=1' \
  -D evidence/sql/baseline.headers -o evidence/sql/baseline.json \
  -w 'baseline status=%{http_code} seconds=%{time_total}\n'

curl -sS --get "$APP_URL/product" --data-urlencode 'id=1 AND 1=1' \
  -D evidence/sql/true.headers -o evidence/sql/true.json \
  -w 'true status=%{http_code} seconds=%{time_total}\n'

curl -sS --get "$APP_URL/product" --data-urlencode 'id=1 AND 1=2' \
  -D evidence/sql/false.headers -o evidence/sql/false.json \
  -w 'false status=%{http_code} seconds=%{time_total}\n'
```

**Synthetic observations — not a lab transcript:**

| Request | Example status/body | Meaning within the stated lab model |
|---|---|---|
| `id=1` | `200`, `{"id":1,"name":"Lab notebook"}` | Known row and working baseline |
| `id=1 AND 1=1` | `200`, `{"id":1,"name":"Lab notebook"}` | True condition preserves the known row |
| `id=1 AND 1=2` | `404`, `{"error":"not found"}` | False condition removes that row |

**Interpretation:** this pattern is consistent with the supplied text being evaluated as SQL in the deliberately vulnerable lab. On an unknown application it is a strong lead to corroborate, not proof of a specific database engine, privilege level or arbitrary data access. The baseline and true request must match in the relevant application result; simply receiving three HTTP responses is insufficient.

**Next decision:** repeat the three requests in at least a few interleaved rounds, keeping the original records or changing the filenames for each round. For example, send baseline → false → true, then true → baseline → false. Compare the product/error marker, status, redirect target, session state and timing. A stable `true`/`false` split matters more than an arbitrary length threshold. Keep full requests and responses for one reproducible pair plus baseline.

## 3. Separate application behavior from noise

| Result | Conclusion to record | Next smallest test |
|---|---|---|
| Baseline is already 404 | Positive control is missing | Use a known existing lab record before testing a condition |
| True/false both return the same product | This test did not show a boolean distinction | Check whether the parameter is used, normalized to an integer, bound as data or placed in another context |
| True/false both return a validation error | Input handling rejected these values | Preserve the rejection; review the observed context instead of spraying quote variants |
| One value causes HTTP 500 or a SQL-looking error | Parser/error lead only | Replay the unchanged baseline and a controlled comparison; capture the exact error |
| All requests redirect to login | Session invalid or request incomplete | Refresh the lab session and restore the valid request |
| Differences disappear in later rounds | Finding not yet reproducible | Investigate cache, personalized data, load balancing and session expiry |
| All bodies differ only in timestamp/token | Dynamic content, not a useful oracle | Compare a stable application marker instead of complete-body equality |
| One response is slow | Timing alone is inconclusive | Measure unchanged controls repeatedly before considering a database-specific delay test |

Failure of this numeric example does **not** establish that the application is free of SQL injection. It establishes only that these inputs did not produce the expected evidence in this context. Stop when a hypothesis has no new support and record the next justified test.

## 4. Identify context and dialect before expanding the test

The example needs no quote closure, comment syntax, column count or vendor delay function because its fixture uses a final numeric expression. Do not transfer those assumptions to an unknown search or login form.

| Question | Useful evidence | Decision it controls |
|---|---|---|
| Is the input numeric, quoted text, an identifier or another expression? | Known lab source, reproducible parse behavior, or carefully paired tests | Placement of operators, quotes and parentheses |
| Which database/dialect processes it? | A corroborated engine error, application configuration or a matching documented behavior | Comment, concatenation, type and delay syntax |
| Are rows reflected in the response? | An injected condition changes a stable result marker | Whether an in-band approach is appropriate; UNION additionally needs matching column count/types |
| Is there only an indirect signal? | A repeatable boolean/error distinction | Whether a blind test has a usable oracle |
| What can the database account actually do? | Demonstrated permissions or configuration evidence | Further read, write or OS-execution possibilities, each assessed separately |

For a timing hypothesis, first identify the dialect and whether the relevant SQL expression is actually evaluated. Alternate a minimal conditional delay with its false/no-delay control; compare multiple samples under similar conditions. Cache, concurrent requests, retries and network jitter can imitate a delay. A lone three-second response is not confirmation. This page deliberately stops before data extraction or file/OS execution: the next step must answer a specific objective with established prerequisites.

> **Exam Tip:** Save `working request + true control + false control + repeatable response difference`. Twenty payloads without a comparison do not make a finding reproducible. SQLMap is prohibited in the [OSCP exam](exam.md); a failed manual test does not change tool permission.

## Record the finding

In [machine notes](../templates/machine.md), record endpoint and parameter, authenticated role, input context, suspected versus confirmed database, exact requests, stable comparison marker, contradictory results, observed impact and next test. For a pentest report, recommend parameterized queries for data values and explicit allowlists where identifiers cannot be parameterized; verify that the fix preserves valid lookup behavior.

## Primary references

- [PortSwigger: SQL injection detection and query contexts](https://portswigger.net/web-security/sql-injection).
- [PortSwigger: conditional responses and blind SQL injection](https://portswigger.net/web-security/sql-injection/blind).
- [SQLite: SQL expressions](https://www.sqlite.org/lang_expr.html), including comparison and boolean operators.
- [PostgreSQL: SELECT](https://www.postgresql.org/docs/current/sql-select.html), for the meaning of filtering and set operations in that dialect; it is not the engine assumed by the fixture.
- [curl manual](https://curl.se/docs/manpage.html): `--get`, `--data-urlencode`, `--dump-header`, `--output`, and `--write-out`.
- [Burp Repeater documentation](https://portswigger.net/burp/documentation/desktop/tools/repeater) for controlled request replay.
