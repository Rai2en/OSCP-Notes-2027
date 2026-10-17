# Service triage: choose one next question

[Home](../README.md) · [Discovery](methodology.md) · [Command variants](reference/commands.md#recon-and-enumeration)

After discovery, choose the row matching an observed service. Commands here are Kali Bash except where a tool console is explicitly named. Set `IP` to the target and replace example domains/accounts with observed values. Source-reviewed on 2026-10-17; target-lab validation is pending. None of the outcome descriptions is a claim of a run against an exam target.

| Observation | First bounded check | Interpret the result / next action |
|---|---|---|
| FTP | `ftp "$IP"`; test anonymous only if appropriate | In the **FTP console**, `ls` lists content and `get <FILE>` retrieves a chosen file. An authentication refusal differs from a data-channel failure. Check passive mode/client routing before concluding an empty directory. |
| SSH | `ssh '<USER>@<IP>'` with an already known credential | Verify the host key, account and resulting identity. A rejected key can mean wrong account, key policy or permissions. A key passphrase prompt is local; an account-password fallback is different. |
| SMB | [SMB procedure](smb.md) | Shares listed, files readable, account authenticated and execution authorized are separate conclusions. |
| HTTP/S | [Web procedure](web.md) | Preserve a working request, hostname and negative baseline before changing parameters or filtering discovery output. |
| DNS | `dig @"$IP" lab.example A`; `dig @"$IP" _ldap._tcp.dc._msdcs.lab.example SRV` for an observed AD domain | A relevant A/SRV record names a resource to investigate. `NXDOMAIN`, an empty answer and a timeout are different findings. Revisit hostname-based web and Kerberos access. |
| SMTP | `nc -nv "$IP" 25`; type `EHLO lab.example`, then `QUIT` in the connection | Record the banner and capabilities. A disabled VRFY command is not evidence of no users; a generic accepted recipient is not proof an account exists. Mail delivery is a separate scoped test. |
| LDAP | `ldapsearch -x -H "ldap://$IP:389" -s base -b '' '(objectClass=*)' defaultNamingContext namingContexts` | RootDSE supplies a base DN when permitted. Empty/denied results may mean policy or a wrong search context; use [AD identity/transport](active-directory.md) and trusted TLS for password binds. |
| NFS | [NFS procedure](nfs.md) | Mount permission, file access, UID mapping and root squashing must be distinguished. |
| SNMP | `snmpget -v2c -c '<KNOWN_COMMUNITY>' "$IP" 1.3.6.1.2.1.1.1.0` | A response establishes that community/version for this OID; record `sysDescr`. A timeout is ambiguous. Request relevant subtrees after a small success, not a blind full MIB walk. |
| MS-RPC | `rpcclient -U '' -N "$IP"`; then `srvinfo` / `enumdomusers` in the **RPC console** | An anonymous bind may succeed while queries are denied. Save names/RIDs actually returned; don't infer account-management rights from a read query. |
| MSSQL | `impacket-mssqlclient '<DOMAIN>/<USER>@<IP>' -windows-auth` when Windows auth is appropriate; enter the password at the prompt | In the **SQL console**, `SELECT SYSTEM_USER, USER_NAME();` records login and DB context. A DB login does not establish `xp_cmdshell`, file-write or OS administrative permission. |

## Example: a negative result that changes the plan

Illustrative observation: FTP login succeeds, `ls` times out, while a version check and control connection work. Hypothesis: data-channel reachability or FTP transfer mode, not bad credentials. Compare the client's passive/active behavior and the route/firewall along that path. If listing succeeds, inspect selected filenames; do not restart password guessing.

## Per-service checklist

- [ ] Correct transport/port and observed hostname?
- [ ] Anonymous, authenticated, local or domain identity recorded?
- [ ] A small request distinguished service behavior from transport failure?
- [ ] Read access separated from write, execution and administration?
- [ ] New names, files and credentials added to the inventory with origin?
- [ ] One next action selected, or a reason to park the service recorded?

Online password guessing is not the default branch of every service. Use evidence-based known pairs, account policy and the engagement/exam constraints before expanding attempts. [Credential scope](active-directory.md#4-track-credentials-and-authentication-types).

Sources: [Nmap protocol discovery](https://nmap.org/book/man-version-detection.html), [Samba](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html), [OpenLDAP ldapsearch](https://www.openldap.org/software/man.cgi?query=ldapsearch&sektion=1), [Net-SNMP snmpget](https://www.net-snmp.org/docs/man/snmpget.html), [Impacket mssqlclient](https://github.com/fortra/impacket/blob/master/examples/mssqlclient.py). Historical variants remain in the archive.
