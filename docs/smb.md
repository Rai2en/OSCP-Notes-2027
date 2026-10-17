# SMB: from a share listing to a verified finding

[Home](../README.md) · [Target workflow](methodology.md) · [AD workflow](active-directory.md) · [Historical commands](../README.md#smb-enumeration)

**Use when:** TCP 445/139 is reachable, a share name was discovered, or a relevant credential becomes available. The immediate question is which identity can list or read which files. Successful authentication, share access, file access and administrative execution are separate findings.

**Status:** documentation-reviewed against the primary sources below; no target or lab execution during this revision. Every output block below is a **synthetic illustration**, shortened for explanation. The address, domain, account and files are invented lab data; substitute verified target values.

## 1. Choose an identity before connecting

**Host/console:** Kali Bash, from a private session directory. Prerequisites: Samba `smbclient` installed, a reachable SMB port, and permission to test the selected identity. Check the installed version/help if an option differs.

```bash
export SMB_IP=192.0.2.20
mkdir -p evidence/smb
smbclient --version
```

Choose one applicable attempt; these are not a password spray:

```bash
# Empty username and password, with no prompt; the server may map this to guest.
smbclient -L "$SMB_IP" -U '%' -N

# A discovered LAB domain account; enter its password at the prompt.
smbclient -L "$SMB_IP" -W LAB -U student

# A discovered FILESRV local account; FILESRV is the target NetBIOS name.
smbclient -L "$SMB_IP" -W FILESRV -U student
```

`-N` only suppresses the password prompt; it does not by itself select an empty username. For a local-account attempt, `-W` must match the server's NetBIOS name. For a domain account, use its actual domain. Record `LAB/student` and `FILESRV/student` separately even if their short names match. These examples use password authentication to an IP; Kerberos needs the proper service name, DNS, ticket and time configuration.

**Synthetic output A — denied before a share list:**

```text
session setup failed: NT_STATUS_LOGON_FAILURE
```

**Interpretation/next decision:** the attempt failed to authenticate; this is not proof that the account is nonexistent or that all SMB access is closed. Verify identity scope and the known credential once. If a domain's authentication policy rejects the method, inspect that constraint rather than repeating guesses. Stop attempts that have no new evidence; consult the [credential inventory](../templates/credentials.md) and lockout policy before additional online tests.

**Synthetic output B — a listing returned:**

```text
Sharename       Type      Comment
---------       ----      -------
LabDocs         Disk      Training handouts
ADMIN$          Disk      Remote Admin
IPC$            IPC       Remote IPC
```

**Interpretation/next decision:** names are visible. This does not prove that `LabDocs` is readable, that `ADMIN$` is accessible, or that empty credentials remained anonymous instead of being mapped to guest. Connect to the relevant known share with the same credentials. A denied listing also does not rule out access to an already known share.

## 2. Connect, list one directory, retrieve one relevant lab file

**Kali Bash:** continue with the identity that returned useful results. For the empty-credential branch use `smbclient "//$SMB_IP/LabDocs" -U '%' -N` instead.

```bash
smbclient "//$SMB_IP/LabDocs" -W LAB -U student
```

**Inside the `smb: \>` console**, enter these commands one at a time. `lcd` selects the Kali destination; `cd` selects a remote directory. The example assumes a `handover` directory and a small `lab-notes.txt` file were observed, rather than guessed.

```text
ls
cd handover
ls
lcd evidence/smb
get lab-notes.txt
quit
```

**Synthetic console transcript — prompts and output shown for interpretation:**

```text
smb: \> ls
  handover                    D        0  ...
smb: \> cd handover
smb: \handover\> ls
  lab-notes.txt               A      148  ...
smb: \handover\> get lab-notes.txt
getting file \handover\lab-notes.txt of size 148 as lab-notes.txt (...)
```

**Back in Kali Bash:** verify the local artifact before reading it or using it as evidence.

```bash
ls -l evidence/smb/lab-notes.txt
sha256sum evidence/smb/lab-notes.txt
sed -n '1,40p' evidence/smb/lab-notes.txt
```

The local hash records the downloaded artifact; it is not a comparison with a server-side hash unless one is separately available. A useful next lead could be an application hostname or configuration path. Record where it came from, then follow that specific lead through the [web workflow](web.md) or [AD workflow](active-directory.md). A username/password-like string is a candidate until verified in its intended scope.

## 3. Interpret a failed operation at the right layer

| Observed result (synthetic wording) | What it establishes | Next smallest check |
|---|---|---|
| `session setup failed: NT_STATUS_LOGON_FAILURE` | The supplied authentication attempt failed | Check domain/local identity, credential and required authentication method |
| `tree connect failed: NT_STATUS_ACCESS_DENIED` | That share connection was refused | Preserve the attempted identity/share; try a different already discovered share if relevant |
| `NT_STATUS_ACCESS_DENIED listing ...` after connection | Connection succeeded; directory enumeration was refused | Record the exact directory; a known file may have different rights |
| `NT_STATUS_ACCESS_DENIED opening remote file ...` | This file open was denied | Distinguish it from a readable sibling; stop claiming the share is wholly readable |
| `NT_STATUS_BAD_NETWORK_NAME` | The requested share name was not accepted | Check exact spelling and the latest listing; do not reinterpret it as a bad password |
| Name-resolution, timeout, signing or protocol error | A transport/negotiation problem needs diagnosis | Recheck route, target name/port and client/server policy; do not weaken policy to force a login |

Different server versions can return different statuses for similar failures. Preserve the full command and error instead of assigning a cause from one string alone. On current Windows versions, signing and guest restrictions can explain failures that old examples omit; see [Microsoft SMB hardening](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-security-hardening).

## 4. Decide whether a write test answers a real question

Only test a write if a discovered path and purpose justify it. In a disposable lab directory, use a uniquely named text marker, verify its content, then remove that same file. Record the action and cleanup. Do not overwrite an existing configuration or executable to establish generic write access.

Read/write access to `LabDocs` does not establish local administrator membership, service-control rights, or remote execution. Before choosing an execution or secret-collection tool, verify its separate privileges and operational requirements in the [AD workflow](active-directory.md). `secretsdump` is not the default follow-up to a successful SMB login.

> **Exam Tip:** A useful SMB note is `identity → share → directory/file → operation → result → next lead`. A list of share names alone does not answer which files you can read.

## Evidence to keep

- [ ] Target address/port and verified server/domain names.
- [ ] Attempted identity and authentication method; distinguish empty-credential and authenticated sessions.
- [ ] Exact share/path and outcomes of listing, file read, and any justified write test.
- [ ] Small relevant artifacts stored privately with source path and local hash.
- [ ] Next lead, failed assumptions, and any changes/cleanup recorded in [machine notes](../templates/machine.md).

## Primary references

- [Samba `smbclient` manual](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html): `-U`, `-N`, `-W`, `-L`, `lcd`, `get`, and the interactive command context.
- [Microsoft SMB security hardening](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-security-hardening): signing, guest access and version-dependent behavior.

These references support command and protocol interpretation; the fictional transcripts above are not evidence of tested target behavior.
