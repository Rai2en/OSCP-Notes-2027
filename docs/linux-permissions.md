# Linux permissions: test the exact privilege boundary

[Home](../README.md) · [Privilege escalation triage](privilege-escalation.md)

**Status:** documentation reviewed on 2026-10-17; not lab-tested. All outputs below are synthetic illustrations. These checks inspect permissions or perform an already permitted identity/read operation; they do not modify accounts, executable files, sudo rules or file capabilities.

## Clue, prerequisites and console

You have a Linux shell and a sudo, SUID or capability finding. Run these commands **on the target in that existing shell**. Use observed paths and the current identity. `findmnt` comes from util-linux and `getcap` from libcap; an unavailable utility is a coverage gap. Start with one candidate rather than searching every mounted filesystem repeatedly.

```bash
id
hostname
uname -r
```

## 1. Read the sudo rule before running anything

```bash
sudo -l
```

Illustrative output:

```text
Matching Defaults entries for alex on lab-linux:
    env_reset, secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

User alex may run the following commands on lab-linux:
    (backup) NOPASSWD: /usr/bin/head -n 5 /srv/backup/job.log
    (root) PASSWD: /usr/bin/id
```

The first rule permits the listed read operation as **backup**, not root. `NOPASSWD` waives authentication for that rule. The second permits `id` as root and requires authentication unless an applicable cached credential/policy satisfies it. `PASSWD` does not imply root's password; inspect Defaults if the prompt differs from the usual invoking-user authentication.

Honor the command path, run-as user/group, arguments and tags. A literal argument list constrains that command; wildcards or regular expressions require separate review. A command with no arguments specified in sudoers can allow arbitrary arguments, whereas an explicit `""` permits none. Do not assume changing your shell's PATH survives `secure_path` or other environment rules.

For the illustrated rules only, minimal permitted checks are:

```bash
sudo -n -u backup /usr/bin/head -n 5 /srv/backup/job.log
sudo -u root /usr/bin/id
```

Illustrative results:

```text
# First command: five existing log lines, for example:
backup job: completed

# Second command, after accepted authentication if required:
uid=0(root) gid=0(root) groups=0(root)
```

The read proves that exact operation under the selected rule. The `id` result proves one command executed with UID 0; it does not establish an unrestricted shell. Do not run these commands merely because they appear in this sheet: they must match the actual target's rule.

| Negative result | Interpretation and next decision |
|---|---|
| `a password is required` with `-n` | Noninteractive authentication was unavailable; not proof that the rule is absent |
| Command/user not permitted | Recheck path, argument matching and run-as context; stop guessing broader commands |
| Log missing or permission denied | Verify the actual resource and policy; a rule alone does not guarantee useful contents |
| Only a limited backup-user rule | Record the limited boundary and inspect resources relevant to that identity |

## 2. Check SUID owner and the execution mount

Suppose enumeration identifies `/opt/backup/bin/report`. Inspect the resolved executable and the mount from the **target's namespace**:

```bash
readlink -f /opt/backup/bin/report
stat -Lc '%A %a %U:%G %n' /opt/backup/bin/report
file -L /opt/backup/bin/report
findmnt -T /opt/backup/bin/report -o TARGET,FSTYPE,OPTIONS
grep '^NoNewPrivs:' /proc/$$/status
```

Illustrative output:

```text
/opt/backup/bin/report
-rwsr-xr-x 4755 backup:backup /opt/backup/bin/report
/opt/backup/bin/report: ELF 64-bit LSB pie executable, x86-64, ...
TARGET      FSTYPE OPTIONS
/opt/backup ext4   rw,nosuid,nodev,relatime
NoNewPrivs: 0
```

The set-user-ID owner here is **backup**. It would not by itself select root. This mount's `nosuid` prevents the usual SUID privilege transition, so stop this SUID hypothesis; keep any separate file-permission issue as a different finding. Even without `nosuid`, owner and mode only establish prerequisites. The program may drop privilege or expose no useful privileged operation. Linux does not honor the SUID bit on interpreter scripts.

`NoNewPrivs: 1` on the calling process is another reason not to expect privilege gain through subsequent execution. A namespace or container may change the meaning of UID 0; record where the process runs. Do not attach a tracer to a SUID process and then treat its behavior as the normal privilege transition, because tracing can suppress that transition.

**Next decision:** if owner, mount and process conditions permit a transition, inspect the program's documented behavior and a matching [GTFOBins context](https://gtfobins.org/). Use an available identity-reporting option or a narrowly scoped permitted read to demonstrate only the boundary you need. Do not assume a binary listed on GTFOBins is inherently vulnerable, or add SUID to a file to create a finding.

## 3. A file capability is not a root shell

For a discovered capability-bearing executable:

```bash
getcap /usr/bin/ping
findmnt -T /usr/bin/ping -o TARGET,FSTYPE,OPTIONS
grep -E '^(Cap(Inh|Prm|Eff|Bnd|Amb)|NoNewPrivs):' /proc/$$/status
```

Illustrative extract:

```text
/usr/bin/ping cap_net_raw=ep
CapEff: 0000000000000000
NoNewPrivs: 0
```

`cap_net_raw` relates to raw/packet sockets. It does not grant arbitrary file reads, UID changes or a root shell. This can be a normal deployment choice for ping. `e`/`p` describe file capability settings; actual process capabilities follow execution rules. The `/proc/$$/status` output describes **your shell**, not the child that would execute ping. Do not use the shell's zero effective mask to conclude the executable cannot receive its file capability.

If a different binary has a capability relevant to your objective, verify that it exposes the corresponding operation. For example, a read-related capability requires a usable read function; its name alone is not proof of arbitrary command execution. Check mount restrictions, `no_new_privs`, process capability limits and user namespaces before interpreting a failure. A `getcap` error or empty output is not a complete scan of inaccessible files.

**Decision:** close the illustrated ping finding as unrelated to the required privilege boundary. For another candidate, record the exact binary/capability, supported operation and minimal observed result, or the missing prerequisite. Do not set or remove capabilities during triage.

## Traces and cleanup

Record actual command/output, host/user, sudo rule and Defaults, resolved file/owner/mode, mount options, capability and result. Sudo attempts can be logged and may refresh authentication state; file reads may be visible in audit telemetry and affect access times. These examples create no payload or target evidence file. Preserve logs and history. If you later change state in an exercise, record its original value and verify restoration separately.

## Sources and validation limits

- [sudoers manual: run-as, argument matching, tags, environment and authentication](https://manpages.debian.org/bookworm/sudo/sudoers.5.en.html)
- [sudo manual: list, noninteractive and selected-user options](https://manpages.debian.org/bookworm/sudo/sudo.8.en.html)
- [execve: SUID/SGID, nosuid, tracing and no_new_privs](https://man7.org/linux/man-pages/man2/execve.2.html)
- [Linux capabilities and execution rules](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [getcap](https://man7.org/linux/man-pages/man8/getcap.8.html) and [findmnt](https://man7.org/linux/man-pages/man8/findmnt.8.html)
- [GTFOBins scope](https://gtfobins.org/)

Manual behavior depends on the installed versions, target policy and execution environment. No target behavior or exploitability was verified when writing these examples.
