# Find relevant files after access

[Home](../README.md) · [Historical path list](reference/file-locations.md) · [Credential inventory](../templates/credentials.md)

Use this when a web file-read, share or shell exposes files. Start with the observed application and current identity. The examples are illustrative, source-reviewed on 2026-10-17 and not target-lab-tested.

## 1. Identify the useful directory

| Observation | Start here | Question |
|---|---|---|
| Web source/config read | Observed application root and referenced config files | Database identity, service URL, include path or environment file? |
| Readable backup share | Its index, script names and dated config backups | Which host/account used the backup, and is the information current? |
| Linux shell | Current home, application/service directory and readable configs | What runs under this identity, and which secret has a verifiable owner? |
| Windows shell | Current profile, relevant application directory, permitted service config | Saved connection, history, unattended configuration or credential store? |

Do not interpret a database password as an OS password. Record the file, principal, secret type and service before one controlled validation. Stop repeated login attempts when scope or lockout behavior is unclear.

## 2. Linux: examine the application you actually found

Target Bash, replace the example path with the observed root:

```bash
id
pwd
ls -la /var/www/labapp
find /var/www/labapp -maxdepth 2 -type f \( -name '.env' -o -name '*config*' -o -name '*.bak' \)
# Read only a selected accessible file; keep its contents in private notes.
sed -n '1,100p' /var/www/labapp/config/database.ini
```

Illustrative, redacted excerpt:

```text
db_host=127.0.0.1
db_user=appreader
db_password=<private reference CRED-03>
db_name=inventory
```

**Interpretation:** this suggests a database on the application's own host. It does not establish a root password, remote DB exposure or file-write rights. Record `CRED-03` as a database credential from this file. Check the local listener and use a matching DB client only if reachable and in scope; a loopback-only service may require forwarding. A permission denial on the config means this identity cannot read it through this path, not that the file is absent.

## 3. Windows: profile and application before a whole-drive search

Target PowerShell:

```powershell
whoami
Get-ChildItem -Force $env:USERPROFILE
# Use the observed application path; do not run these as one blind filesystem sweep.
Get-ChildItem -LiteralPath 'C:\LabApp' -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -in '.config','.ini','.xml' }
# PSReadLine can be absent in a remote/noninteractive session.
Get-PSReadLineOption | Select-Object HistorySavePath
```

Read a chosen file with `Get-Content -LiteralPath '<PATH>'`. Use the returned history path, rather than another user's hardcoded profile. Documents and backups are leads when their names or application context are relevant. An unreadable file is a recorded limitation; it is not a reason to keep changing permissions blindly.

Illustrative decision: an application config references `LAB\svc_inventory` and SQL server `db01.lab.example`. Record a domain identity, resolve the server and investigate its intended SQL service. Do not assume the same secret authorizes SMB, WinRM or local administration.

## 4. Keep the next test small

| Result | Next decision |
|---|---|
| Secret has a clear current account/service | Make one scoped authentication test and record service/host/result. |
| Old backup contradicts current config | Prefer current evidence; retain the backup as an unverified lead. |
| Many files but no application context | Inspect names, timestamps and references before searching contents broadly. |
| File-read access only | Preserve path/encoding and returned contents; do not infer an interactive shell or execution. |
| Credential store such as KDBX | Identify its version/format and use a matching offline conversion workflow; [reference](reference/commands.md#keepass2john). |

Capture only the evidence needed to show the weakness. For client work use private secret references in notes, redact report excerpts, and follow the [engagement data plan](pentest.md). For the exam, follow the [official file-handling and proof rules](exam.md).

> **Exam Tip:** One relevant config plus a verified identity is often more useful than hundreds of guessed paths. Return to the [historical list](reference/file-locations.md) when you have a product-specific reason.

Sources: [GNU find](https://www.gnu.org/software/findutils/manual/html_mono/find.html), [Get-ChildItem](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem), [PSReadLine history path](https://learn.microsoft.com/en-us/powershell/module/psreadline/get-psreadlineoption).
