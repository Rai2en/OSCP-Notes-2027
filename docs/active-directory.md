# Active Directory: from credentials to a verified path

[Home](../README.md) · [AD commands](../README.md#active-directory-pentesting) · [Pivoting](pivoting.md)

**Validation:** source-reviewed on 2026-10-17. Outputs below are synthetic teaching examples, not captured lab results. Record your own collector/PowerView revision and observed results before treating a path as tested.

## 1. Establish identity and transport

Record the domain DNS name, DC IP/FQDN, current user, local versus domain context, reachable hosts and the route used. Resolve the DC before debugging Kerberos. Verify clock alignment; an authentication error may be transport, DNS or time-related.

Kali example with synthetic lab values:

```bash
export DC_IP=192.0.2.20
export DOMAIN=lab.example
export AD_USER=student
read -rsp 'Lab password: ' AD_PASS; echo
dig @"$DC_IP" "_ldap._tcp.dc._msdcs.$DOMAIN" SRV
nxc smb "$DC_IP" -d "$DOMAIN" -u "$AD_USER" -p "$AD_PASS"
nxc smb "$DC_IP" -d "$DOMAIN" -u "$AD_USER" -p "$AD_PASS" --shares
```

The variable avoids putting a literal password in the command history, but command-line arguments can still be visible to local processes. Keep secrets in your private notebook. Test the known pair on one host before expanding to a documented target list. A successful SMB login does not grant administrative or WinRM access. [NetExec authentication reference](https://www.netexec.wiki/smb-protocol/authentication/checking-credentials-domain).

### Read the result before choosing a remote-access tool

Synthetic excerpt from the known-pair test; formatting and success labels vary by NetExec version:

```text
SMB  192.0.2.20  445  DC01  [+] lab.example\student:<redacted>
```

This establishes that this host accepted this pair for SMB. Now test the specific resource, using the discovered NetBIOS domain `LAB` and a share name returned by enumeration. Kali Bash; `smbclient` prompts for the password:

```bash
smbclient "//$DC_IP/Finance" -U 'LAB\student' -c 'ls'
```

Synthetic negative result:

```text
tree connect failed: NT_STATUS_ACCESS_DENIED
```

**Decision:** retain the verified credential and mark Finance access denied. Do not mark it as invalid or infer local administrator rights. Inspect another documented resource or the directory permissions available to this identity.

| Result | What it establishes | Next discriminating check |
|---|---|---|
| Connection timeout, no protocol response | Transport is unproven | Selected route, destination port and pivot; repeating the password does not test these |
| `STATUS_LOGON_FAILURE` | This attempt failed authentication | Exact principal/domain, secret type and quoting; check account status before another attempt |
| SMB login accepted, share denied | Authentication worked; this resource is not accessible in this context | Share name, share/file permissions and another explicitly permitted resource |
| Share listing/read succeeds | That operation on that share is allowed | Record the file and access level; a read does not establish remote execution |

## 2. Collect and verify the graph

Use a collector compatible with your BloodHound deployment. The repository's older Neo4j/PowerShell examples are legacy notes. For CE, follow [SpecterOps collection guidance](https://bloodhound.specterops.io/collect-data/ce-collection/overview); [BloodHound.py](https://github.com/dirkjanm/BloodHound.py) documents its CE and legacy variants.

```bash
# Kali: only if the CE-compatible bloodhound-ce-python entry point is installed.
mkdir -p bloodhound
cd bloodhound
bloodhound-ce-python -d "$DOMAIN" -u "$AD_USER" -p "$AD_PASS" -ns "$DC_IP" -c All --zip
```

Check collection errors, domain identity and missing hosts before trusting an empty graph. Mark only identities you actually control. For each path, write the source principal, target object, edge/permission and supporting evidence. Verify important permissions against the live directory; a collected graph can be incomplete or stale.

## 3. Interpret permissions before changing anything

| Finding | Verify first | Decision |
|---|---|---|
| GenericAll on a group | Effective right, exact group, inheritance | Membership control may create a useful path |
| GenericAll/ForceChangePassword on a user | Object type and effective right | Password change has consequences; record the modification |
| GenericWrite / WriteDACL / WriteOwner | Allowed attributes, ACL and object type | These are different capabilities, not interchangeable labels |
| Group membership or session edge | Current membership/session and target reachability | Check whether it actually enables the next access method |
| Replication rights | Required rights and scope | DCSync requires appropriate directory permissions |
| Delegation or certificate configuration | Exact configuration and prerequisites | Treat as a separate verified technique, not an automatic shortcut |

Consult the upstream [GenericAll](https://bloodhound.specterops.io/resources/edges/generic-all) and [ForceChangePassword](https://bloodhound.specterops.io/resources/edges/force-change-password) explanations for object-specific behavior. Do not assume an edge named AllExtendedRights always means every useful operation on every object type.

### Worked decision: a GenericAll edge to a group

**Observation:** the graph suggests `STUDENT@LAB.EXAMPLE -> GenericAll -> APP-SUPPORT@LAB.EXAMPLE`. Before considering membership changes, establish that the source SID is yours, the target is the intended group and the live ACL supports the edge.

Windows PowerShell in an existing session for the same authorized domain, with a reviewed local PowerView build already loaded. These are read-only directory queries. Confirm the named functions exist; older PowerView generations differ:

```powershell
Get-Command Get-DomainUser, Get-DomainGroup, Get-DomainObjectAcl -ErrorAction Stop
whoami /user
whoami /groups
$PrincipalSid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value
$Principal = Get-DomainUser -Identity $PrincipalSid -Properties samaccountname,objectsid,distinguishedname
$Group = Get-DomainGroup -Identity 'App-Support' -Properties samaccountname,objectsid,distinguishedname,member,memberof
if ($null -eq $Principal -or $null -eq $Group -or @($Principal).Count -ne 1 -or @($Group).Count -ne 1 -or -not $Principal.distinguishedname -or -not $Group.distinguishedname) {
    throw 'Resolve the exact user and group DN before querying ACLs.'
}
$Principal | Format-List samaccountname,objectsid,distinguishedname
$Group | Format-List samaccountname,objectsid,distinguishedname,member,memberof
Get-DomainGroup -MemberIdentity $Principal.distinguishedname | Select-Object samaccountname,objectsid
$Acl = Get-DomainObjectAcl -Identity $Group.distinguishedname -ResolveGUIDs
$Acl | Format-List ObjectDN,SecurityIdentifier,AceQualifier,ActiveDirectoryRights,AceFlags,ObjectAceType,InheritedObjectAceType
```

Compare **all relevant entries**, not just a filtered Allow row. Synthetic excerpts for interpretation:

```text
Current user SID       : S-1-5-21-111111111-222222222-333333333-1105
Target group DN        : CN=App-Support,OU=Groups,DC=lab,DC=example
SecurityIdentifier     : S-1-5-21-111111111-222222222-333333333-1105
AceQualifier           : AccessAllowed
ActiveDirectoryRights  : GenericAll
AceFlags               : None
```

The trustee matches the current user and this illustrative ACE applies to the group itself. Review the full ACL for applicable denies, inheritance/object restrictions and other trustee entries. An `InheritOnly` entry does not apply to the object carrying it. If the trustee is a group, establish the principal's applicable membership, including nested groups; a directory membership query and the enabled groups in an existing logon token can differ. `-MemberIdentity` helps inspect directory token-group membership; `whoami /groups` describes the present Windows session. Neither command alone computes every effective permission. See [PowerView's function definitions](https://github.com/PowerShellMafia/PowerSploit/blob/master/Recon/PowerView.ps1) and [Microsoft's access-check model](https://learn.microsoft.com/en-us/windows/win32/secauthz/how-dacls-control-access-to-an-object).

**Decision:** record a supported membership-control candidate, then inspect what App-Support actually grants. Follow its `memberof` parents and verify any claimed right on the destination resource. A group name containing “Support” does not establish host administration or WinRM access. This example stops at verification; a membership change would require a permitted test, a recorded original state and a cleanup plan.

**Negative control:** if the only matching GenericAll Allow ACE belongs to SID ending `-1147`, while your SID ends `-1105` and none of your applicable groups matches that trustee, this excerpt provides no right for you. Do not “try it anyway.” Recheck the graph's source identity and collection date. No returned ACL is also inconclusive: distinguish an absent entry from a failed directory query.

## 4. Track credentials and authentication types

For every discovery, note origin, principal, domain/local scope, secret type and verified services in [the credential inventory](../templates/credentials.md).

- AS-REP roasting and Kerberoasting have different account prerequisites; use their distinct [reference sections](../README.md#as-rep-roasting).
- An NT hash, Net-NTLMv2 challenge-response and Kerberos ticket are not interchangeable.
- Cached domain credentials are not automatically reusable as NT hashes.
- Local SAM data is not a dump of the domain database. Record where a hash came from before inferring cross-host access.
- For reuse tests, record the actual username/password pair; avoid accidentally testing every combination of two lists. Check lockout policy before any spraying.

## 5. Move, then re-enumerate

Select SMB/WMI/WinRM/RDP according to reachability and permissions. On each new host, confirm identity, groups, hostname, interfaces, local services and scoped secrets. Revisit the graph with newly verified information. Preserve enough evidence to explain each transition without relying on screenshots alone.

Record the final path in [the machine template](../templates/machine.md). Keep temporary credential variables only for the remaining credential-dependent steps and manage logs privately.

## 6. AD CS and current hardening

For Certipy 5, confirm `certipy find -h`; Kali may expose the launcher as `certipy-ad`. Enumerate first, using your private session variables:

```bash
certipy find -u "$AD_USER@$DOMAIN" -p "$AD_PASS" -dc-ip "$DC_IP" -enabled -text
```

Read the complete CA/template results, not only a vulnerability label. Enrollment permissions, client-authentication EKUs, subject control, approval/signature requirements and identity mapping determine whether a path is usable. The [upstream usage guide](https://github.com/ly4k/Certipy/wiki/05-%E2%80%90-Usage) and [command reference](https://github.com/ly4k/Certipy/wiki/08-%E2%80%90-Command-Reference) document version-specific options and ESC paths.

On updated DCs, strong certificate mapping changes invalidate older UPN-only assumptions; compatibility-mode support ended with the September 2025 updates. Validate SID/mapping behavior and DC patch level rather than assuming an issued certificate authenticates as the requested user. See [Microsoft KB5014754](https://support.microsoft.com/en-us/servicing/os/windows-server/2022/05/kb5014754-certificate-based-authentication-changes-on-windows-domain-controllers).

Shadow Credentials requires effective access to the target's `msDS-KeyCredentialLink` and a compatible authentication environment. It is not the same prerequisite as enrolling in a template. For relay, check destination signing and EPA/channel binding. These paths are documented through [upstream Certipy](https://github.com/ly4k/Certipy); no new PoC is included here.

See [chain compatibility](command-audit.md#recheck-every-transition-in-a-chain) for ticket, DCSync and DCOM limitations. Run `unset AD_PASS` after the final credential-dependent command; this does not erase secrets already captured in logs.
