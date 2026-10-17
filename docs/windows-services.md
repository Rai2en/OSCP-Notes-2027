# Windows services: separate file rights, service rights and the trigger

[Home](../README.md) · [Privilege escalation triage](privilege-escalation.md)

**Status:** documentation reviewed on 2026-10-17; not lab-tested. All outputs below are synthetic illustrations, not results from a target. Commands are inspection only.

## Clue and prerequisites

An inventory reports a privileged service with an unquoted path or a writable component. The useful question is whether your current token controls something that this service will actually execute.

Use an existing **PowerShell session on the target Windows host**. Replace the illustrative service `VendorUpdater` and paths with observed values. No external tool, payload or service restart is needed for these checks. A denied query leaves that part of the evidence unknown.

## 1. Establish identity, executable and service account

```powershell
whoami /user
whoami /groups
whoami /priv
Get-CimInstance Win32_Service -Filter "Name='VendorUpdater'" |
    Select-Object Name,StartName,State,PathName
sc.exe qc VendorUpdater
sc.exe queryex VendorUpdater
```

Illustrative extracts:

```text
User: LAB-WIN\alex
Group: LAB-WIN\ServiceMaintainers    Enabled group

SERVICE_NAME: VendorUpdater
        START_TYPE         : 2   AUTO_START
        BINARY_PATH_NAME   : C:\Program Files\Vendor\Updater\updater.exe --service
        SERVICE_START_NAME : LocalSystem
        STATE              : 4   RUNNING
```

`LocalSystem` identifies the configured service account. A service using `LocalService`, a virtual account or a named account needs its own context assessment. `RUNNING` is a state, and `AUTO_START` is a startup setting; neither grants you permission to restart it. The unquoted path containing spaces is a lead. Establish the executable boundary and candidate search locations before considering it exploitable. Use `sc.exe` explicitly because `sc` can be an alias in PowerShell.

## 2. Read the binary and directory ACLs

Use the executable path established above, without its arguments:

```powershell
icacls 'C:\Program Files\Vendor\Updater\updater.exe'
icacls 'C:\Program Files\Vendor\Updater'
Get-FileHash -Algorithm SHA256 'C:\Program Files\Vendor\Updater\updater.exe'
```

Illustrative extracts:

```text
C:\Program Files\Vendor\Updater\updater.exe
    NT AUTHORITY\SYSTEM:(I)(F)
    BUILTIN\Administrators:(I)(F)
    LAB-WIN\ServiceMaintainers:(M)

C:\Program Files\Vendor\Updater
    LAB-WIN\ServiceMaintainers:(I)(RX)
```

| Item | Interpretation for this example |
|---|---|
| `M` on the file | Modify rights are relevant to changing existing file contents; full control `F` is not required |
| `F` | Full control includes permissions beyond ordinary file modification |
| `RX` on the directory | Read/execute is not permission to create a replacement file there |
| `(I)` | Inherited ACE; it still matters to access, but inspect its scope and origin |
| `ServiceMaintainers` | Relevant only because the current token has this group enabled |

This suggests file-content control, subject to the complete DACL, token and runtime restrictions. It does not prove that a file can be replaced with a rename/copy operation, that it is currently open without restrictive sharing, or that the service configuration can be changed. Keep the exact executable's ACL separate from its parent directory's ACL.

**Negative counterexample:** if the same file also has an explicit `LAB-WIN\alex:(DENY)(WD,AD)`, do not infer content-write access from the group's `M` line. Here `WD` and `AD` are **icacls file** rights for write-data/add-file and append-data/add-subdirectory. Evaluate applicable allow/deny ACEs, their order, inheritance and token membership together; inspect deletion and parent-directory rights separately before claiming replacement. A deny-only token group cannot supply allow rights. `icacls` displays a DACL; it is not an effective-access verdict.

## 3. Decode the service object's DACL

```powershell
sc.exe sdshow VendorUpdater
```

Illustrative **complete DACL for this simplified example**:

```text
D:(A;;CCDCLCRPRC;;;AU)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)
```

An ordinary ACE uses `(type;flags;rights;object-guid;inherit-guid;trustee)`. In the first ACE, `A` is allow and the final `AU` is Authenticated Users. `SY` is LocalSystem and `BA` is Built-in Administrators. Check the token and any other ACEs in the actual output; the example has no deny ACE.

These codes are interpreted **for a service object**, not as directory-service properties:

| SDDL right | Mask | Service permission |
|---|---|---|
| `CC` | `0x0001` | Query configuration |
| `DC` | `0x0002` | Change configuration |
| `LC` | `0x0004` | Query status |
| `RP` | `0x0010` | Start |
| `WP` | `0x0020` | Stop |
| `RC` | `0x20000` | Read the security descriptor |
| `WD` | `0x40000` | Change the DACL |
| `WO` | `0x80000` | Change owner |

In this example, `AU` grants configuration change and start, but not stop. This is independent of the binary's file ACL. A deny-only Administrators group would not make its allow ACE usable. Generic rights, hexadecimal masks or conditional ACEs require their full interpretation; do not search the string for two letters and stop.

## 4. Decide whether a trigger is available

The illustrated service is already running. Start permission (`RP`) cannot be treated as permission to cycle it; stop permission (`WP`) is separate. Service dependencies, accepted controls and operational impact also matter. Do not stop or reboot a host just to test a theory.

| Actual observation | Next decision |
|---|---|
| Privileged account + file modification + confirmed permitted trigger | Candidate path has its principal prerequisites; plan a minimal controlled validation and restoration separately |
| Configuration change + stopped service + start permission | Different candidate path: configuration control; it does not depend on writing the original executable |
| File writable, service running, no reachable trigger | Record file weakness and trigger gap; continue another lead |
| `CC`/`LC` only | Enumeration rights; no configuration-change or start/stop claim |
| `Access is denied` from `sdshow` | Descriptor unavailable to this token; the error does not establish the permissions you could not inspect |
| Service query missing or denied | Check the actual service name and session context; do not report the host free of service weaknesses |

**Proof boundary:** these read-only checks establish configuration and permission evidence. They do not demonstrate privileged code execution. Save actual outputs and distinguish that conclusion from a successfully observed higher-privilege process.

## Traces and cleanup

Record host/time, token groups, service name/account/state, executable path/hash, both ACLs, SDDL and the missing or available trigger. Inspection may be visible in PowerShell, process or endpoint telemetry. No target artifact is created by these commands, and no service state is changed. Keep the evidence in your notes; do not erase logs or history. Any later approved modification needs the original file/configuration, permissions and a restoration check.

## Sources and validation limits

- [Service access rights and masks](https://learn.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights)
- [SDDL ACE fields and right encodings](https://learn.microsoft.com/en-us/windows/win32/secauthz/ace-strings)
- [SDDL trustee abbreviations](https://learn.microsoft.com/en-us/windows/win32/secauthz/sid-strings) and [enabled/deny-only token groups](https://learn.microsoft.com/en-us/windows/win32/secauthz/sid-attributes-in-an-access-token)
- [icacls syntax, rights and ACE ordering](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls)
- [How DACL access checks use the token](https://learn.microsoft.com/en-us/windows/win32/secauthz/how-dacls-control-access-to-an-object)
- [Service accounts](https://learn.microsoft.com/en-us/windows/win32/services/service-user-accounts)

Review covers documented semantics. It does not validate a particular Windows build, application's service behavior or effective access on your target.
