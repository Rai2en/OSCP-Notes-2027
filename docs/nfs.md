# NFS: export to a readable resource

[Home](../README.md) · [Other services](services.md) · [File triage](file-triage.md)

Use after a scan identifies NFS/mountd or a target config names an export. Source-reviewed on 2026-10-17. Output below is illustrative; this workflow has not been executed against a target lab in this revision.

## Discover, then inspect

Kali Bash, `IP` is an in-scope target. The mount operations require local privileges and an NFS client.

```bash
showmount -e "$IP"
```

Illustrative output:

```text
Export list for 192.0.2.10:
/srv/backup 192.0.2.0/24
```

This names an export and an allowed client range, not read/write rights or root-squash options. Check that your actual routed source fits the server policy. `showmount` can return nothing on an NFSv4-only setup; absence is inconclusive.

Create a dedicated mountpoint inside the private working directory, mount read-only and inspect without executing content:

```bash
mkdir -p mnt/backup
sudo mount -t nfs -o ro,nosuid,nodev,noexec "$IP:/srv/backup" mnt/backup
findmnt -T mnt/backup -o SOURCE,TARGET,FSTYPE,OPTIONS
ls -lan mnt/backup
```

Illustrative listing:

```text
-rw-r----- 1 1002 1002 384 Oct 16 08:00 app-backup.ini
```

**Interpretation:** the file's numeric owner/group is 1002. Determine whether the identity used for NFS has read access; a successful mount does not guarantee a readable file. The local `ro,nosuid,nodev,noexec` flags limit the inspection mount and do not reveal the server's export options or the target's execution mount.

If readable, inspect the selected backup and record its origin with the [file triage procedure](file-triage.md). A discovered service credential creates a new authentication hypothesis; it does not itself grant OS administration.

## Negative or ambiguous results

| Observed result | Meaning / next test |
|---|---|
| `access denied by server while mounting` | Check export path, source network and server authentication/export policy; a discovered export can still deny this client. |
| Mount works, file read is denied | Inspect UID/GID, mode and server mapping. Client root can be squashed to an anonymous identity. |
| `showmount` empty/unreachable but NFS responds | Investigate the observed NFS version and namespace; don't declare NFS absent from mountd alone. |
| Read works, write untested | You have demonstrated read access only. A read-only mount cannot test server write permission. |
| Writable export reported elsewhere | Verify actual identity, server behavior and scope before an agreed write test. No root escalation has been established. |

For an escalation hypothesis, server `no_root_squash`, effective write access, ownership and the target execution mount's treatment of SUID are separate prerequisites. `mount -o rw` cannot grant rights denied by the server. See the [Linux permission procedure](linux-permissions.md) and [historical NFS notes](reference/commands.md#nfs).

## Evidence and cleanup

Save export, source/route, mount options, numeric listing, selected file and a bounded conclusion. Unmount only the mountpoint you created:

```bash
sudo umount mnt/backup
rmdir mnt/backup
```

If busy, leave the mounted directory in other shells and identify the open use; do not force-unmount unrelated mounts. These inspection steps do not modify the remote file.

Sources: [showmount](https://man7.org/linux/man-pages/man8/showmount.8.html), [exports/root squashing](https://man7.org/linux/man-pages/man5/exports.5.html), [NFS client mounts](https://man7.org/linux/man-pages/man5/nfs.5.html).
