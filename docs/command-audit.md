# Command compatibility review

[Home](../README.md) · [AD workflow](active-directory.md) · [External CVEs](cve-references.md)

Reviewed **2026-09-10**, from baseline `6ba3826`. Sources and argument definitions were checked; offensive commands were not run against targets. An upstream option can differ from an older installed package. Record `--help`/version output before using a workflow.

## Corrections and version boundaries

| Area | Current guidance | Primary reference |
|---|---|---|
| FreeRDP | Check whether your package provides `xfreerdp3` or `xfreerdp`. Clipboard flags are unrelated to login failures. | [Kali package/help](https://www.kali.org/tools/freerdp3/) |
| WPScan | Use `--output` and `--format`; removed obsolete redirect/log switches. API token is needed for vulnerability database detail. | [Kali package/help](https://www.kali.org/tools/wpscan/) |
| Impacket remote execution | `smbexec` opens a semi-interactive shell and has no trailing command argument. `psexec`, `wmiexec` and `atexec` have different prerequisites and arguments. | [smbexec parser](https://github.com/fortra/impacket/blob/master/examples/smbexec.py) |
| NetExec credential lists | `--no-bruteforce` pairs corresponding rows. Without it, lists test combinations. `--continue-on-success` controls stopping, not pairing or lockout protection. | [CLI definitions](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/cli.py) |
| Hash formats | Impacket uses `LM:NT` (empty LM allowed); hashcat modes depend on the exact hash prefix/type. Removed blanket `--force`. | [Impacket](https://github.com/fortra/impacket), [Hashcat formats](https://hashcat.net/wiki/doku.php?id=example_hashes) |
| BloodHound | CE needs compatible collectors; legacy desktop/Neo4j instructions do not install CE. | [Collectors](https://bloodhound.specterops.io/collect-data/ce-collection/overview), [Python variants](https://github.com/dirkjanm/BloodHound.py) |
| Windows enumeration | Prefer CIM to WMIC. Service-control ACL, binary ACL and restart ability are separate checks. | [Service rights](https://learn.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights) |
| Impersonation tools | SeImpersonate is a prerequisite, not proof of compatibility. PrintSpoofer is archived; inspect OS, service and runtime requirements for each implementation. | [PrintSpoofer](https://github.com/itm4n/PrintSpoofer), [JuicyPotatoNG](https://github.com/antonioCoco/JuicyPotatoNG) |
| Linux enumeration | Corrected PTY quoting, process flags and executable-file search. Sudo rules are user/run-as/argument specific. | [GNU find](https://www.gnu.org/software/findutils/manual/html_mono/find.html), [sudo manual](https://www.sudo.ws/docs/man/sudo.man/) |
| NFS | `showmount` does not reveal root-squash options; server configuration and the target's execution mount matter. | [exports](https://man7.org/linux/man-pages/man5/exports.5.html), [showmount](https://man7.org/linux/man-pages/man8/showmount.8.html) |
| SMB transfer | Guest access and signing policies may prevent older anonymous transfer examples. | [Microsoft SMB hardening](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-security-hardening) |

## Recheck every transition in a chain

| Proposed transition | Required evidence / current limitation |
|---|---|
| Web flaw → shell | Confirm execution under the application identity and a reachable callback path; file read/upload alone is insufficient. |
| Service write access → SYSTEM | Identify privileged service identity, correct executed path, effective write/configuration rights and an available trigger. |
| New local administrator → remote session | Account scope, RDP/WinRM authorization, firewall and remote token policy still apply. |
| SMB authentication → relay | Target protocol protections, signing, channel binding/EPA and usable authentication must all be assessed. Signing changes in newer Windows make legacy assumptions unreliable. |
| Certificate → domain authentication | Check template rights, EKU, issuance conditions, identity/SID mapping and KDC support. A returned PFX is not proof of successful impersonation. |
| Service key → silver ticket | SPN, key type and service behavior matter; PAC signature enforcement can invalidate older forged-ticket recipes. |
| krbtgt key → golden ticket | Domain identity, existing principal, key material, supported encryption and current PAC handling matter; patch levels must be recorded. |
| Local admin → DCSync | Local administrative rights on a member server do not grant domain replication rights. DCSync reads via replication, not by copying NTDS.dit. |
| DCOM access → execution | RPC reachability, activation rights, registered application and authentication-level hardening all matter. |

Hardening references: [certificate mapping KB5014754](https://support.microsoft.com/en-us/servicing/os/windows-server/2022/05/kb5014754-certificate-based-authentication-changes-on-windows-domain-controllers), [PAC signatures KB5020805](https://support.microsoft.com/en-US/servicing/os/windows-server/2022/10/kb5020805-how-to-manage-kerberos-protocol-changes-related-to-cve-2022-37967), [DCOM KB5004442](https://support.microsoft.com/en-us/topic/kb5004442-manage-changes-for-windows-dcom-server-security-feature-bypass-cve-2021-26414-f1400b52-c141-43d2-941e-37ed901c769c).

## Limits of this review

This corrects identified syntax and prerequisite errors; it does not certify every historical payload or third-party binary in the README. Machine-specific DeadPotato instructions, a truncated DCOM payload and blanket kernel-exploit success claims were removed. Existing attributed payload examples were not expanded. New CVE material is external links only.

The notebook scripts are offline and unchanged. Local link checks and the helper tests validate repository mechanics, not exploit success. No PoC was created, installed or executed during this review.

## Field manual follow-up review

Reviewed **2026-10-17** against default-branch baseline `d3496cf`. The complete README and existing topic guides were inspected. This follow-up preserves the existing technical subjects, attributed payloads and legacy compatibility notes, adds a stage-based contents table, ten service checklists and three escalation/AD checklists, and consolidates practical time-management advice in the README. It does not imply that older review dates elsewhere were refreshed.

| Area | Correction or clarification | Primary reference |
|---|---|---|
| Nmap | Separate full TCP discovery from selected-port service checks; retain all three output formats and inconclusive UDP results. Replace broad `vuln` category selection with review of a named script. | [Scan semantics](https://nmap.org/book/man-port-scanning-techniques.html), [output formats](https://nmap.org/book/man-output.html), [NSE selection](https://nmap.org/book/man-nse.html) |
| Windows port checks | Replace a TCPClient loop whose output did not reliably distinguish failed connections; inspect `TcpTestSucceeded` on selected ports. | [Test-NetConnection](https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection) |
| SMB | `-L` lists shares; browse files after connecting to a share. Use `mask *` for recursive retrieval rather than an empty mask. | [smbclient manual](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html) |
| LDAP | Explicit RootDSE base/scope and naming-context discovery; password prompt and trusted TLS for the credentialed example. Older layout-specific bases remain labeled. | [OpenLDAP search options](https://github.com/openldap/openldap/blob/master/clients/tools/ldapsearch.c), [shared bind/TLS options](https://github.com/openldap/openldap/blob/master/clients/tools/common.c) |
| KeePass | Separate John’s labeled extraction from Hashcat input; explain mode/version matching and that kpcli opens a database with a known password. | [John converter](https://github.com/openwall/john/blob/bleeding-jumbo/src/keepass2john.c), [Hashcat example formats](https://hashcat.net/wiki/doku.php?id=example_hashes), [kpcli project](https://sourceforge.net/projects/kpcli/) |
| PowerShell/CMD | Use `$env:APPDATA` and PowerShell file search in PowerShell sections; remove invalid `dir` equality separators and fix `findstr` alternatives in CMD examples. | [Environment variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.5), [findstr](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/findstr) |
| Registry / local hives | Correct `CurrentControlSet` in the SNMP path and named `/system:` / `/sam:` Mimikatz arguments; distinguish SAM from LSA operations. | [SNMP registry](https://learn.microsoft.com/en-us/windows/win32/snmp/registry-parameters), [Mimikatz argument handling](https://github.com/gentilkiwi/mimikatz/blob/master/mimikatz/modules/kuhl_m_lsadump.c) |
| Web traversal | Add `--path-as-is` to curl traversal examples so client normalization does not obscure the request path. This does not establish server exploitability. | [curl manual](https://curl.se/docs/manpage.html#--path-as-is) |
| Payloads | Distinguish staged and single Metasploit payloads/handlers; explicitly encode the existing Python generator’s text as UTF-16LE. No new payload was added. | [Payload types](https://docs.rapid7.com/metasploit/working-with-payloads/), [PowerShell encoded command](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_powershell_exe?view=powershell-5.1) |
| Linux | Correct `/etc/group` and `/proc/<PID>/` paths; quote find name patterns; clarify sudo authentication/run-as rules and SUID/capability conditions. Replace implicit legacy DES generation with an explicit SHA-512 hash prompt in the historical passwd example. | [proc](https://man7.org/linux/man-pages/man5/proc.5.html), [find](https://www.gnu.org/software/findutils/manual/html_mono/find.html), [sudo](https://www.sudo.ws/docs/man/sudo.man/), [OpenSSL passwd](https://docs.openssl.org/master/man1/openssl-passwd/) |
| Shadow copies | Restore the volume root syntax and distinguish Windows collection from Kali parsing; the actual returned shadow-copy device must replace the example number. | [VShadow examples](https://learn.microsoft.com/en-us/windows/win32/vss/vshadow-tool-examples) |
| Exam | Refresh the rule-check date, clarify partial AD scoring and accepted proof capture. Timeboxes are study advice, not policy. | [Official guide](https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide), [official FAQ](https://help.offsec.com/hc/en-us/articles/4412170923924-OSCP-Exam-FAQ) |

Validation is limited to source review, local Markdown navigation/structure checks, the existing helper tests and whitespace checks. No scan, password test, exploitation, payload execution or target-lab validation was performed. Mixed historic transcripts are labeled as text where a single shell language would be misleading. Remaining compatibility work, including old payloads, PowerView function generations and third-party binaries, still requires version-pinned lab evidence.

## Operational workflow revision — 2026-10-17

Baseline `09c2c27`. The preceding entries describe their historical revisions; current execution/validation status is maintained in [the validation record](lab-validation.md).

- Replaced the long README with a situation index and preserved older bookmarks through chapter links. Moved technical variants, the old path wordlist and defective original snippets into separate reference appendices with attribution.
- Corrected the curl query/path explanation and SMB console context; qualified `.git` recovery, account changes, startup/UAC, DLL loading, cron, NFS and PATH assertions. Retired the fragile PHP and `DllMain` demonstrations from the normal command path. Silver-ticket validation now distinguishes HTTP clients from other service protocols.
- Added interpreted SMB, SQL, Windows ACL/SDDL, Linux permission and AD examples, including denied/ambiguous results and next decisions. Fixed the null-result guard before an AD ACL query and PowerShell 5.1-compatible file-extension filtering.
- Added a bounded loopback HTTP/SQLite rehearsal and recorded its actual eight-request result. All other constructed examples remain explicitly illustrative/source-reviewed; no target-lab success is claimed.
- Separated exam reports from client findings/engagement briefs and added a notebook mode selector. The local document checker now resolves ordinary heading and explicit-anchor fragments, including moved references; tests cover those helper behaviors, not offensive success.
