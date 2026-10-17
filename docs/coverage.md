# Coverage and remaining validation

[Home](../README.md) · [Validation records](lab-validation.md) · [Correction history](command-audit.md)

Updated 2026-10-17 from baseline `09c2c27`. The former 2,529-line README is now a situation index. Its technical topics and attribution remain in [the command archive](reference/commands.md), the [historical path list](reference/file-locations.md) and explicitly [retired snippets](reference/retired-snippets.md). Old README bookmarks have chapter links.

## Current procedures

| Area | Current path | Evidence supplied / remaining work |
|---|---|---|
| Discovery and services | [Methodology](methodology.md), [protocol triage](services.md), [NFS](nfs.md) | Priority decisions and bounded checks; target/tool repetition pending |
| SMB and credential scope | [SMB](smb.md), [private inventory](../templates/credentials.md) | Illustrative allowed/denied results and branch decisions; target-lab repetition pending |
| Web and manual SQL | [Web](web.md), [SQLi](sql-injection.md) | Baseline, contrasting requests and false-positive handling; one [HTTP/SQLite fixture executed](lab-validation.md#executed-record-http-truefalse-controls) |
| Linux permissions | [Interpreted sudo/SUID/capabilities](linux-permissions.md) | Illustrative permission/mount/runtime evidence; target-lab repetition pending |
| Windows escalation | [Triage](privilege-escalation.md), [service interpretation](windows-services.md) | Token, file ACL, service SDDL and trigger distinguished; target-lab repetition pending |
| AD | [Identity and ACL decisions](active-directory.md) | Illustrative login/share denial and live ACL/membership checks; target-lab repetition pending |
| Routing | [Pivoting](pivoting.md) | Host/console separation, route/return path and interpreted example; multi-hop target-lab repetition pending |
| File/secret discovery | [Targeted triage](file-triage.md) | Application-context-first workflow; broad old wordlist moved to appendix |
| Exam | [Rules/proofs](exam.md), [time management](../README.md#exam-mindset--time-management), [report](../templates/report.md) | Objective and evidence tracking; full exported report rehearsal still needed |
| Client mission | [Pentest workflow](pentest.md), [brief](../templates/engagement.md), [client report](../templates/client-report.md) | Illustrative bounded assessment/finding and retest criteria; adapt to actual scope |
| Practice and maintenance | [Training](training.md), [toolkit](toolkit.md), [troubleshooting](troubleshooting.md) | Repeatable drills, error-led checks and notebook helpers |

## Validation levels

The [validation page](lab-validation.md#status-definitions) defines illustrative, source-reviewed, local-fixture-tested and target-lab-tested. Source review, heading checks and passing notebook tests cannot certify an exploit or OSCP tool permission. No Windows, Linux privilege, SMB, AD, NFS or pivot target was exercised in this revision.

The [official body of knowledge](https://help.offsec.com/hc/en-us/articles/38543335188756-OSCP-Body-of-knowledge) defines a broader curriculum. Client-side exercises, memory-corruption/adaptation exercises, specific defense/runtime behavior and full integrated target-lab chains remain incomplete. The archive's presence is not proof of tested coverage.

## Next records to add

1. Fill the target/tool/version and expected-versus-observed fields for one procedure at a time.
2. Add a successful and a denied/invalid condition, including the decision to stop or switch.
3. Reproduce one complete synthetic lab chain with evidence and restoration, then a complete report export.
4. Recheck exam rules and version-specific behavior before the next attempt/release.

Use [the technique template](../templates/technique.md). Add depth or a missing record before adding more tool lists.
