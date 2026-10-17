# Troubleshooting without random retries

[Home](../README.md) · [Pivoting](pivoting.md)

Write the exact error, execution host, shell, identity, tool version and timestamp. Compare against one known-working operation. Change one variable per test.

| Symptom | Check first | Next controlled test |
|---|---|---|
| No scan response | Route, VPN interface, target state | A selected TCP connection; compare `ip route get` |
| DNS works on pivot only | Resolver and route to DNS server | Query that server explicitly; verify DC FQDN |
| Kerberos fails, NTLM works | DNS/SPN, clock, realm, ticket selection | Resolve intended service FQDN; inspect time and ticket cache |
| Login succeeds, shell denied | Protocol-specific authorization | Confirm groups and access on that exact service |
| Password rejected | Domain/local scope, quoting, account lockout | One known pair; stop repeated attempts while investigating |
| SMB hash fails | Hash type and username scope | Confirm this is an NT hash, not a captured challenge-response |
| No callback | Destination from the target's viewpoint | Harmless TCP connection or file download along that route |
| File downloaded but cannot run | Architecture, runtime, permissions, file integrity | Compare checksum; inspect file type and exact loader error |
| Web request differs from browser | Host header, cookies, redirects, encoding, CSRF | Replay an unchanged captured request first |
| SQL injection appears intermittent | Baseline, session expiry, network noise | Alternate control/test requests; keep other inputs fixed |
| BloodHound empty/incomplete | Collector edition, import and DNS errors | Confirm one known user, group and computer appear |
| Tool crashes with Python errors | Interpreter, dependencies, bytes/string assumptions | Isolated environment matching upstream requirements |
| Port already in use | Existing server/listener, wrong bind address | Inspect local listeners; choose a distinct port |
| Shell dies on disconnect | Session lifetime, process behavior, transport | Test persistence of a harmless process in the lab |
| Privilege exploit reports success | Identity, trigger, expected side effect | Check `id` or `whoami /all` in the resulting session |

## Start from the actual error

These are illustrative message patterns, not captured results. Commands run in the named console using observed lab values.

| Message/pattern | First controlled check | Decision |
|---|---|---|
| SMB `STATUS_LOGON_FAILURE` | Kali: one known pair with explicit domain or local scope; [SMB examples](smb.md) | Investigate identity/secret/scope before changing execution method |
| SMB `NT_STATUS_ACCESS_DENIED` after login | In smbclient, list a share you know is permitted; compare the denied path under the same identity | Record resource authorization; successful login still stands |
| `Host seems down` in Nmap | Kali: `ip route get <IP>`; for a known live host, a selected `nmap -sT -Pn -n -p <PORT> <IP>` | Discovery failure differs from a tested TCP service result |
| PowerShell `Access is denied` from `sc.exe sdshow` | Target PowerShell: `whoami /all`, confirm service name, record descriptor unavailable | Do not infer service-control rights from a file ACL alone |
| Linux `Exec format error` | Target shell: `uname -m`; with `file <BINARY>` available, inspect executable type | Match architecture/format before debugging a callback |
| SQLi control changes redirect to login | Replay the unchanged saved request with the current session | Restore the baseline; the difference is not yet a database oracle |
| Callback test fails after forward pivot works | Test a harmless download to the pivot listener's internal address; [return mapping](pivoting.md#return-connections-and-file-transfer) | Diagnose the independent return direction |

## Minimum bug note

```text
Observed:
Expected:
Runs on / shell / identity:
Tool version and source:
Route and destination:
Exact command or saved request:
Relevant output:
Single change tested:
Result and next decision:
```

Do not “fix” every failure by disabling a firewall or antivirus. First determine which connection, permission or component failed; broad changes can hide the cause and make the result harder to reproduce.
