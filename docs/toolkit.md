# Toolkit and preparation

[Home](../README.md) · [Exam rules](exam.md)

Prepare on a disposable Kali VM, record versions, and snapshot a known-working setup before a timed practice. Tool availability and flags depend on the installed release. This is a practical selection, not an exhaustive list or a blanket exam authorization.

| Need | Tools | Manual fallback / prerequisite |
|---|---|---|
| Discovery | Nmap | Protocol checks with curl, nc; route must exist |
| HTTP inspection | Burp Community, curl | Browser devtools; retain cookies and Host header |
| Content discovery | ffuf or Gobuster, SecLists | Baseline a nonexistent path before filtering |
| SMB/RPC | smbclient, rpcclient, NetExec | Distinguish anonymous, local and domain identity |
| SQL | Impacket mssqlclient, mysql client | Inspect identity/permissions before OS execution |
| AD mapping | BloodHound CE, compatible SharpHound/BloodHound.py | PowerShell/LDAP enumeration and ACL inspection |
| Remote access | OpenSSH, Evil-WinRM, FreeRDP | Service permissions; valid credentials alone are insufficient |
| Hashes/archives | John, Hashcat, format-specific converters | Identify the hash format before selecting a mode |
| Local enumeration | linPEAS, winPEAS, PrivescCheck | `sudo -l`, `id`, `whoami /all`, service and file permissions |
| Routing | Ligolo-ng, Chisel, SSH | Match architecture, test both traffic directions |
| Exploit research | SearchSploit, upstream advisories | Read and adapt source; record changes |
| Notes and evidence | Markdown editor, terminal logs, screenshot tool | Separate findings from untested ideas |

Upstream starting points: [Kali tools](https://www.kali.org/tools/), [NetExec](https://www.netexec.wiki/), [Impacket](https://github.com/fortra/impacket), [BloodHound collection](https://bloodhound.specterops.io/collect-data/ce-collection/overview), [Ligolo-ng](https://docs.ligolo.ng/), [Chisel](https://github.com/jpillora/chisel).

## Inventory what is actually installed

```bash
command -v nmap curl smbclient rpcclient nxc evil-winrm john hashcat chisel
nmap --version
nxc --version
python3 --version
```

For each additional tool, record the binary path, release/commit, architecture, source URL and date of a successful lab test in [the tool inventory](../templates/tool-inventory.md). Use the installed help for flags. For Python tools, follow upstream isolated-environment instructions rather than overwriting system packages.

## Rehearse before relying on a tool

- Run a small scan against your lab and save all output formats.
- Transfer a harmless file in both directions and compare checksums.
- Establish SSH/WinRM/RDP sessions appropriate to your lab credentials.
- Import a small compatible BloodHound collection and verify known objects exist.
- Route to an internal service and test a connection back through the pivot.
- Export a sample report and check its screenshots offline.

Prefer a few tools you can diagnose over a folder of untested binaries. SQLMap and mass vulnerability scanners belong to permitted training contexts, not the exam workflow. Metasploit/Meterpreter usage must follow [the specific restrictions](exam.md).

## An actual record versus an empty inventory

The [local HTTP/SQLite record](lab-validation.md#executed-record-http-truefalse-controls) records Python 3.12.14, SQLite 3.53.1 and the exact observed controls on 2026-10-17. That validates the bounded teaching fixture only. The [target-lab matrix](lab-validation.md#target-lab-repetitions-still-required) leaves network/privilege procedures pending until they have equivalent tool/target evidence. Fill the tool inventory from those runs, rather than assuming a downloaded binary works.
