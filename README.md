![Chrome dragon surrounded by orange light with OSCP+ in the lower-right corner](assets/oscp-field-notes-cover.png)

# OSCP Field Manual

Practical notes for moving from an observation to a tested decision, evidence and a reproducible report. Start with your current situation; keep the command archive for variants.

## Choose your situation

| Situation | Open | Finish with |
|---|---|---|
| Starting a target | [Discovery and priorities](docs/methodology.md) | Services saved, one ranked hypothesis and a next test |
| FTP, SSH, DNS, SMTP, LDAP, SNMP or RPC | [Service triage](docs/services.md) · [NFS export inspection](docs/nfs.md) | A protocol result and a bounded next question |
| Website, parameter or API | [Web triage](docs/web.md) · [Manual SQLi](docs/sql-injection.md) | A baseline, contrasting result and bounded conclusion |
| SMB exposed or credentials found | [SMB decisions](docs/smb.md) | Verified account scope, readable resource and next action |
| File-read or shell access | [Targeted file triage](docs/file-triage.md) | A relevant configuration or secret with a recorded origin |
| Need higher privileges | [Privilege triage](docs/privilege-escalation.md) · [Windows services](docs/windows-services.md) · [Linux permissions](docs/linux-permissions.md) | Identity, effective permission and trigger established |
| Domain access | [AD decisions](docs/active-directory.md) | A verified principal/resource/permission transition |
| Internal service or callback unreachable | [Pivoting](docs/pivoting.md) | Forward and return path checked independently |
| An attempt fails | [Troubleshooting](docs/troubleshooting.md) | One failure layer identified and one controlled test |
| Exam preparation and proof | [Exam checklist](docs/exam.md) · [Time management](#exam-mindset--time-management) | Required access, screenshot, panel and report milestones tracked |
| Client engagement | [Pentest workflow](docs/pentest.md) · [Engagement brief](templates/engagement.md) · [Client report](templates/client-report.md) | A scoped test and a justified, reproducible finding |

## Use a procedure

Each primary procedure names its execution host/console, prerequisites, a minimal test, an interpretable result and the next decision. Output labeled **illustrative** is synthetic. A claim of **lab-tested** needs a dated record with versions and actual observations; the [validation page](docs/lab-validation.md) lists exactly what was exercised.

> **Exam Tip:** Understand what a tool sends and verify the important conclusions manually. Use permitted inventory tools where they save time; keep automatic exploitation and other restricted features out of the exam workflow. [Official rules](https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide).

## Start a private notebook

Run from this repository on Kali/Python 3; use a directory outside the repository:

```bash
python3 scripts/new_session.py ~/oscp-private/lab-01
# For a client-style notebook instead:
python3 scripts/new_session.py ~/pentest-private/assessment-01 --mode pentest
```

The initializer copies the relevant templates and creates scans/evidence/files/notes folders. It refuses an existing destination. For each additional target, copy the blank machine template to a distinct file in your private notebook.

## Exam Mindset & Time Management

Write `observation → hypothesis → smallest test → result → next action`. Revisit the inventory when you find a new hostname, credential, privilege or route. These timeboxes are suggestions to rehearse, not OffSec requirements:

| Moment | Action and decision |
|---|---|
| First 15–30 minutes | Read objectives, verify VPN, prepare notes and begin service discovery. |
| First pass per host | Inspect exposed services; prioritize a specific credential, file or permission over a version-only guess. |
| Every 45–60 minutes on one hypothesis | With no new evidence, record the failed condition and switch service or host. |
| Every access/privilege milestone | Check identity, save the path and capture/submit the required proof immediately. |
| Between focused blocks | Take breaks and planned food/rest; repeated identical attempts are a cue to reset the hypothesis. |
| Last 60–90 practical minutes | Audit known evidence and panel submissions while the machines remain accessible. |
| Reporting window | Reproduce the path from notes, inspect the exported PDF, verify packaging/upload and keep a time buffer. |

Before switching targets, record current identity, tested services, verified credentials, rejected hypotheses, running jobs and **one next test**. The [exam checklist](docs/exam.md) covers rules and evidence; the [training page](docs/training.md) covers rehearsal.

## References and validation

- [Command archive](docs/reference/commands.md): technical variants and historical lab material, with attribution.
- [Historical file locations](docs/reference/file-locations.md): use after identifying the relevant OS/product.
- [Retired snippets](docs/reference/retired-snippets.md): original defective demonstrations and their limitations.
- [Lab validation and repeatable checks](docs/lab-validation.md) · [Toolkit](docs/toolkit.md) · [Technique template](templates/technique.md).
- [Coverage](docs/coverage.md) · [Command correction history](docs/command-audit.md) · [CVE references](docs/cve-references.md) · [Contributing](CONTRIBUTING.md).

## Existing bookmarks

Older README section links now land on the related workflow/reference below. The command material and attribution remain available in the archive.

<a id="oscp-ultimate-field-manual"></a>
<a id="contents"></a>
<a id="how-to-use-this-manual"></a>
<a id="find-your-next-step"></a>
<a id="start-a-lab-notebook"></a>
<a id="general"></a>
<a id="oscp-commands"></a>

[Getting started](docs/start-here.md).

<a id="command-reference"></a>
<a id="quick-setup"></a>
<a id="exports"></a>
<a id="environment-variables"></a>
<a id="aliases-suggestion"></a>
<a id="optional-bash-aliases"></a>
<a id="scanning"></a>
<a id="important-locations"></a>
<a id="github-recon"></a>
<a id="connecting-to-rdp"></a>
<a id="adding-ssh-public-key"></a>
<a id="file-transfers"></a>
<a id="windows-to-kali"></a>
<a id="adding-users"></a>
<a id="windows"></a>
<a id="linux"></a>
<a id="password-hash-cracking"></a>
<a id="password-list-mentioned-in-the-offsec-discord-500-worst-passwordstxt"></a>
<a id="hash-identifier"></a>
<a id="fcrackzip"></a>
<a id="john"></a>
<a id="keepass2john"></a>
<a id="hashcat"></a>
<a id="pivoting-through-ssh"></a>
<a id="dealing-with-passwords"></a>
<a id="impacket"></a>
<a id="evil-winrm"></a>
<a id="mimikatz"></a>
<a id="ligolo-ng"></a>

[Setup, access and credential reference](docs/reference/commands.md#setup-and-access).

<a id="recon-and-enumeration"></a>
<a id="port-scanning"></a>
<a id="ftp-enumeration"></a>
<a id="ssh-enumeration"></a>
<a id="smb-enumeration"></a>
<a id="https-enumeration"></a>
<a id="wordpress"></a>
<a id="drupal"></a>
<a id="joomla"></a>
<a id="dns-enumeration"></a>
<a id="smtp-enumeration"></a>
<a id="ldap-enumeration"></a>
<a id="nfs-enumeration"></a>
<a id="snmp-enumeration"></a>
<a id="rpc-enumeration"></a>

[Discovery workflow](docs/methodology.md) · [protocol reference](docs/reference/commands.md#recon-and-enumeration).

<a id="web-attacks"></a>
<a id="directory-traversal"></a>
<a id="local-file-inclusion"></a>
<a id="sql-injection"></a>

[Web workflow](docs/web.md) · [historical web reference](docs/reference/commands.md#web-attacks).

<a id="exploitation"></a>
<a id="finding-exploits"></a>
<a id="searchsploit"></a>
<a id="reverse-shells"></a>
<a id="msfvenom"></a>
<a id="one-liners"></a>
<a id="groovy-reverse-shell"></a>

[Choose and verify an exploit](docs/methodology.md#4-validate-an-exploit-before-adapting-it) · [historical access reference](docs/reference/commands.md#exploitation).

<a id="windows-privilege-escalation"></a>
<a id="manual-enumeration-commands"></a>
<a id="automated-scripts"></a>
<a id="token-impersonation"></a>
<a id="services"></a>
<a id="binary-hijacking"></a>
<a id="unquoted-service-path"></a>
<a id="insecure-service-executables"></a>
<a id="weak-registry-permissions"></a>
<a id="dll-hijacking"></a>
<a id="dll-hijacking-adding-new-user-into-administrators-group"></a>
<a id="autorun"></a>
<a id="alwaysinstallelevated"></a>
<a id="scheduled-tasks"></a>
<a id="startup-apps"></a>
<a id="insecure-gui-apps"></a>
<a id="sam-and-system"></a>
<a id="passwords"></a>
<a id="sensitive-files"></a>
<a id="config-files"></a>
<a id="registry"></a>
<a id="runas---savedcreds"></a>
<a id="pass-the-hash"></a>

[Windows service decisions](docs/windows-services.md) · [Windows archive](docs/reference/commands.md#windows-privilege-escalation).

<a id="linux-privilege-escalation"></a>
<a id="tty-shell"></a>
<a id="basic"></a>
<a id="manual-enumeration"></a>
<a id="automated-scripts-1"></a>
<a id="sensitive-information"></a>
<a id="sudosuidcapabilities"></a>
<a id="sudo"></a>
<a id="suidset-owner-user-id"></a>
<a id="capabilities"></a>
<a id="cron-jobs"></a>
<a id="nc-netcat"></a>
<a id="nfs"></a>
<a id="path"></a>
<a id="writable-etcpasswd-file"></a>
<a id="exploiting-kernel-vulnerabilities"></a>
<a id="cve---linux"></a>

[Linux permission decisions](docs/linux-permissions.md) · [Linux archive](docs/reference/commands.md#linux-privilege-escalation).

<a id="post-exploitation"></a>
<a id="sensitive-information-1"></a>
<a id="powershell-history"></a>
<a id="searching-for-passwords"></a>
<a id="searching-in-registry-for-passwords"></a>
<a id="kdbx-files"></a>
<a id="dumping-hashes"></a>

[Targeted file triage](docs/file-triage.md) · [post-access archive](docs/reference/commands.md#post-exploitation).

<a id="active-directory-pentesting"></a>
<a id="enumeration"></a>
<a id="powerview"></a>
<a id="domain"></a>
<a id="bloodhound"></a>
<a id="ldapdomaindump"></a>
<a id="plumhound"></a>
<a id="pingcastle"></a>
<a id="psloggedon"></a>
<a id="gpp-or-cpassword"></a>
<a id="attacking-active-directory"></a>
<a id="zerologon"></a>
<a id="password-spraying"></a>
<a id="deadpotato-seimpersonateprivilege"></a>
<a id="as-rep-roasting"></a>
<a id="kerberoasting"></a>
<a id="silver-tickets"></a>
<a id="secretsdump"></a>
<a id="dumping-ntdsdit"></a>
<a id="lateral-movement-in-active-directory"></a>
<a id="psexec---smbexec---wmiexec---atexec"></a>
<a id="winrs"></a>
<a id="netexec"></a>
<a id="kpcli---keepass-password-manager"></a>
<a id="pass-the-ticket"></a>
<a id="dcom"></a>
<a id="golden-ticket"></a>
<a id="shadow-copies"></a>
<a id="windows-powershell-payload-encoding"></a>

[AD workflow](docs/active-directory.md) · [AD archive](docs/reference/commands.md#active-directory-pentesting).

<a id="references"></a>

[Original attribution](docs/reference/commands.md#references).
