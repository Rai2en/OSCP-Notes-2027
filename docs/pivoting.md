# Pivoting and network troubleshooting

[Home](../README.md) · [Troubleshooting](troubleshooting.md)

Record the topology before adding routes. Example: Kali reaches PIVOT; PIVOT reaches an internal server. A route from Kali to the server does not automatically give the server a route back to Kali. Use addresses discovered in your authorized lab, not the example ranges verbatim.

Illustrative topology (documentation-only addresses; no target-lab run is claimed):

```text
Kali 192.0.2.5 <--agent/proxy TCP--> PIVOT 192.0.2.10
                                     PIVOT internal: 198.51.100.10
                                               |
                                     SERVER 198.51.100.20:445
```

## Ligolo-ng: route to the internal network

Commands below follow the upstream documentation checked on 2026-09-10. Confirm your installed console help; older notes use `start` rather than `tunnel_start`.

Kali Bash:

```bash
sudo ip tuntap add user "$(whoami)" mode tun ligolo
sudo ip link set ligolo up
./proxy -selfcert
```

Proxy console: run `certificate_fingerprint`. On the pivot, use the correct agent build and substitute that fingerprint:

```powershell
.\agent.exe -connect <KALI_REACHABLE_IP>:11601 -accept-fingerprint <FINGERPRINT>
```

Proxy console:

```text
session
ifconfig
tunnel_start --tun ligolo
```

Kali Bash, after determining the actual internal subnet:

```bash
sudo ip route add <INTERNAL_CIDR> dev ligolo
ip route get <INTERNAL_HOST_IP>
nmap -sT -Pn -n -p 445,1433,5985 <INTERNAL_HOST_IP>
```

Verify the selected agent, interface and route. Do not overwrite a working VPN route blindly. [Upstream setup](https://docs.ligolo.ng/Quickstart/).

### Interpret the first connectivity test

Illustrative results, normalized to show the fields to inspect:

```text
ip route get 198.51.100.20 -> selected device ligolo
TCP-connect scan of 198.51.100.20:445 -> open, service candidate SMB
```

This supports forward TCP reachability through the chosen agent. It does not establish SMB credentials, execution permission or a return connection. If the route chooses the VPN or default device instead, fix the route/session before retrying authentication. A closed port indicates a reachable endpoint rejecting that connection; `filtered` or a timeout leaves filtering/route/target availability unresolved.

Keep a known listener on Kali and test a harmless download through the return mapping separately. In the illustrative topology, the server uses `198.51.100.10:18080`; using Kali's address would assume a different route that has not been established.

## Return connections and file transfer

In the selected agent's proxy console:

```text
listener_add --addr 0.0.0.0:18080 --to 127.0.0.1:8000 --tcp
listener_add --addr 0.0.0.0:14443 --to 127.0.0.1:4444 --tcp
listener_list
```

The first listener exposes Kali's local port 8000 through PIVOT:18080; the second exposes Kali:4444 through PIVOT:14443. Run your local service before testing. The internal target connects to the **pivot's internal address**, not Kali's unreachable address. Test a harmless file transfer first. [Listener semantics](https://docs.ligolo.ng/Listeners/).

To reach a service bound only to the selected pivot's loopback, Ligolo provides a special mapping:

```bash
sudo ip route add 240.0.0.1/32 dev ligolo
nmap -sT -Pn -n -p 1433 240.0.0.1
```

This reaches loopback on that agent, not loopback on every internal host. [Local-port mapping](https://docs.ligolo.ng/Localhost/).

## Alternatives

SSH local forwarding from Kali, when SSH access to PIVOT is already available:

```bash
ssh -N -L 127.0.0.1:11433:<INTERNAL_SQL_IP>:1433 <USER>@<PIVOT_IP>
```

The destination is reached from the SSH server. Connect your SQL client to Kali's 127.0.0.1:11433. With `-D 127.0.0.1:1080`, SSH provides a local SOCKS proxy instead. See [OpenSSH options](https://man.openbsd.org/ssh).

Chisel reverse forwarding when the pivot can initiate the connection to Kali:

```bash
# Kali; choose a private lab credential and note the displayed fingerprint.
chisel server --port 8000 --reverse --auth <USER>:<PASSWORD>
```

```powershell
# Pivot: maps Kali:11433 to the pivot's own loopback SQL service.
.\chisel.exe client --fingerprint <FINGERPRINT> --auth <USER>:<PASSWORD> <KALI_IP>:8000 R:127.0.0.1:11433:127.0.0.1:1433
```

Choose distinct local ports when running multiple forwards. Consult [Chisel usage](https://github.com/jpillora/chisel) for SOCKS and other forms. Through a TCP SOCKS proxy, use compatible TCP-connect tools; do not expect raw SYN scans or UDP tools to work through an ordinary TCP-only proxy setup.

## When it fails

Check in order: agent connection → selected session → route → destination port → authentication → application response. For callbacks, check the reverse direction separately. Record listener IDs and exact routes for cleanup; remove only those you created. Add a second pivot only after the first route has passed a simple connectivity test.
