# Privilege escalation: turn a finding into a decision

[Home](../README.md) · [Windows service example](windows-services.md) · [Linux permission examples](linux-permissions.md)

**Status:** documentation reviewed on 2026-10-17; commands and examples have not been tested in a lab. Example outputs in the linked sheets are illustrative. Record the target's actual output before making a claim.

Start from the identity you have, identify a specific permission boundary, and prove the smallest useful result. A writable file, a SUID bit or a tool's highlighted finding is a candidate. A confirmed path also needs the right execution context and a reachable trigger.

## First five minutes after a shell

Run on the compromised host, in its existing shell. Save the host, user, time and command with each useful observation.

Linux shell:

```bash
id
hostname
sudo -l
ss -lntup
```

Windows PowerShell:

```powershell
whoami /all
hostname
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,OSArchitecture
Get-CimInstance Win32_Service | Select-Object Name,StartName,State,PathName
Get-NetTCPConnection -State Listen | Select-Object LocalAddress,LocalPort,OwningProcess
```

If one command is denied or unavailable, record that limitation and use the other observations. Do not interpret an incomplete enumeration as the absence of a path.

## Choose the next check from the evidence

| Observation | Next check | Decision supported |
|---|---|---|
| Linux sudo rule | Run-as user/group, command arguments, tags and Defaults | What action is allowed, whether authentication is needed, and which identity it can use; see [worked sudo example](linux-permissions.md#1-read-the-sudo-rule-before-running-anything) |
| SUID or file capability | Owner, actual executable, mount, process restrictions and program behavior | Whether the permission changes execution at all; see [SUID](linux-permissions.md#2-check-suid-owner-and-the-execution-mount) and [capabilities](linux-permissions.md#3-a-file-capability-is-not-a-root-shell) |
| Writable Linux job/script | Execution user, exact invoked component, schedule and writable dependencies | Whether a higher-privilege process will consume the component |
| Unqualified command in privileged code | Actual command lookup, effective PATH and permitted environment | Whether a controlled directory is searched; changing your shell's PATH alone proves nothing |
| Windows service finding | Service identity, binary/directory ACLs, service DACL and trigger | Which of file modification, configuration change or execution control is available; see [worked service example](windows-services.md) |
| Scheduled task or logon item | Principal, action, elevation context and reachable event | Who would execute the component and when |
| Saved secret | Source, account scope and one relevant authentication check | Access actually gained; an application password need not be an OS password |
| Loopback listener | Owning process, authentication and route to that listener | Whether a local application deserves targeted enumeration |
| Kernel or token exploit candidate | Exact build, protection/configuration and upstream requirements | Whether the technique applies before introducing a PoC |

Use one enumeration script when it can answer a remaining question. Confirm its relevant findings against the target. A second scanner that repeats the same candidates does not add proof.

## Windows traps that need an extra check

**Autorun:** distinguish the current user's `HKCU` from machine-wide `HKLM`, then determine the user who would sign in and the token used. A future administrator logon does not make the current user's Run entry execute as that administrator. Under normal UAC behavior, membership in Administrators also does not make every logon application elevated. If there is no observed or permitted trigger, record an unconfirmed candidate instead of waiting indefinitely. Sources: [Run/RunOnce](https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys), [UAC token behavior](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/how-it-works).

**DLL loading:** a missing-DLL event alone is insufficient. Establish the exact requested name, architecture, actual search location, privileged process and trigger. A similarly named DLL in a writable folder may never be loaded. Process Monitor itself may require permissions or an interactive session you do not have. Do not replace an application's dependency just to discover its requirements. Avoid process creation in `DllMain`: it runs under the loader lock and can destabilize the host process. Sources: [DLL search order](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order), [DllMain restrictions](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-best-practices).

## Close the loop

For each candidate, record: observed identity → exact permission → missing prerequisite or available trigger → minimal result → next decision. A successful `id`, verified token identity or narrowly scoped permitted read can establish a fact without replacing a binary or creating an account. State the limit of that fact: one allowed root command is not proof of an unrestricted root shell.

If a later exercise requires a state change, first capture the original configuration, file hash/permissions and restoration steps. Preserve evidence and audit records. The linked examples perform inspection and identity/read checks; they do not change service configuration, ACLs, accounts or executable files.
