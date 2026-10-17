# Target workflow

[Home](../README.md) · [Machine notes](../templates/machine.md) · [Troubleshooting](troubleshooting.md)

## 1. Build an evidence inventory

On Kali, inside a private session directory:

```bash
export IP=192.0.2.10
mkdir -p scans
nmap -sT -Pn -n -p- --reason -oA scans/tcp-all "$IP"
# Replace this example list with the ports actually found.
nmap -sT -Pn -n -sV -sC -p 22,80,445 --reason -oA scans/services "$IP"
sudo nmap -sU --top-ports 20 -Pn -n --reason -oA scans/udp-top "$IP"
```

`-Pn` skips discovery, not connectivity requirements. A timeout is not proof that a port is closed. UDP `open|filtered` is inconclusive. Investigate promising UDP services with protocol-specific requests. Review scripts before running them; broad NSE categories include different behaviors. [Nmap scan semantics](https://nmap.org/book/man-port-scanning-techniques.html).

## 2. Turn each service into a question

| Observation | Next question | Evidence to save |
|---|---|---|
| HTTP on any port | Redirect, virtual host, application, parameters, API, source map or backup? | Request/response, hostname, version evidence |
| SMB | Anonymous access? Readable shares? Local versus domain authentication? | Share list, permission result, source of each secret |
| FTP/NFS | What is readable? Does a path correspond to a web directory? | Export/share path, ownership and permissions |
| MSSQL/MySQL | Which identity and privileges? Other databases or linked servers? | Login context, permissions, relevant tables/configuration |
| LDAP/Kerberos | Domain, DC and identity? Object permissions? | DNS records, domain names, collection results |
| SSH/RDP/WinRM | Is the credential valid AND authorized for this service? | Authentication result and resulting identity |
| Unfamiliar service | What does the banner/protocol reveal? | Product, build, port and upstream advisory |

Use [service triage](services.md), the [SMB procedure](smb.md) or the [web procedure](web.md) to interpret a first result. Consult [historical protocol variants](reference/commands.md#recon-and-enumeration) only after choosing the question. Revisit the inventory whenever a new hostname, credential or route is discovered.

## 3. Rank hypotheses

Write `observation → hypothesis → smallest test → expected result → next action` before a long attempt. Prefer a specific exposed credential or verified permission over a version-only exploit guess. Record why a failed hypothesis was rejected. After a timebox with no new evidence, change the hypothesis or service rather than repeating the same scan.

Illustrative decision record, not a target transcript:

| Observation/test | Result | Decision |
|---|---|---|
| HTTP redirects to `portal.lab.example` | Hostname found on a known IP | Resolve that host to the lab IP and preserve the intended Host header |
| Two nonexistent paths return the same login page as `/admin` | HTTP 200 is a generic response, not evidence that every guessed path exists | Calibrate discovery using a stable marker; do not report each 200 as a finding |
| A customer session already verified on its own page receives `403` on an admin route | The known session is denied at this route; `403` alone would not prove authentication | Compare only with an authorized second test role; don't jump to an OS exploit |

The [web procedure](web.md) gives the concrete requests. The note records which interpretation was rejected, rather than only the last command tried.

## 4. Validate an exploit before adapting it

Check target version, architecture, authentication, module/feature configuration and required privileges. Read the source for hardcoded addresses, file paths and side effects. Record upstream URL and commit/hash. Start with a harmless identity or file-read check where practical. Change one variable at a time and save the diff.

## 5. After initial access

Record who/where you are; stabilize the shell; inspect network interfaces and local services; look for targeted configuration/history secrets; then apply the [privilege workflow](privilege-escalation.md). A new credential may lead to another host rather than local escalation. Use the [AD workflow](active-directory.md) when the identity is domain-scoped.

## 6. Close the loop

Capture evidence immediately, track changes needed for reproduction or cleanup, and draft the finding while the reasoning is fresh. Mark access and proof milestones separately. Do not count an unverified tool success message as a completed objective.
