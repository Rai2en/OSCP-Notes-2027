# Historical file locations

[Home](../../README.md) · [Targeted file triage](../file-triage.md) · [Command archive](commands.md)

This preserves the former path wordlist. Select paths after identifying OS, product and account; it is not a checklist to walk blindly. Entries include legacy software and may not exist or be readable.

Paths below include legacy installations. On current systems, also inspect `/etc/php/<VERSION>/`, `/etc/systemd/system/`, `/etc/nginx/` and `~/.ssh/id_ed25519` where applicable. Presence and read permissions must be checked; `~` is shell expansion, not a portable web-file path.

> **Exam Tip:** Start with the relevant user or application directory; `tree /F` from `C:\Users` can produce a large amount of output. A directory listing is not proof of privileged access.

<details>
	<summary>Windows</summary>

	C:/Users/Administrator/NTUser.dat # Registry settings
	C:/Documents and Settings/Administrator/NTUser.dat # Registry settings
	C:/apache/logs/access.log # Apache access logs
	C:/apache/logs/error.log # Apache error logs
	C:/apache/php/php.ini # PHP configuration
	C:/boot.ini # Boot configuration
	C:/inetpub/wwwroot/global.asa # IIS global script
	C:/MySQL/data/hostname.err # MySQL error log
	C:/MySQL/data/mysql.err # MySQL error log
	C:/MySQL/data/mysql.log # MySQL general log
	C:/MySQL/my.cnf # MySQL configuration
	C:/MySQL/my.ini # MySQL configuration
	C:/php4/php.ini # PHP configuration
	C:/php5/php.ini # PHP configuration
	C:/php/php.ini # PHP configuration
	C:/Program Files/Apache Group/Apache2/conf/httpd.conf # Apache configuration
	C:/Program Files/Apache Group/Apache/conf/httpd.conf # Apache configuration
	C:/Program Files/Apache Group/Apache/logs/access.log # Apache access logs
	C:/Program Files/Apache Group/Apache/logs/error.log # Apache error logs
	C:/Program Files/FileZilla Server/FileZilla Server.xml # FTP server config
	C:/Program Files/MySQL/data/hostname.err # MySQL error log
	C:/Program Files/MySQL/data/mysql-bin.log # MySQL binary log
	C:/Program Files/MySQL/data/mysql.err # MySQL error log
	C:/Program Files/MySQL/data/mysql.log # MySQL general log
	C:/Program Files/MySQL/my.ini # MySQL configuration
	C:/Program Files/MySQL/my.cnf # MySQL configuration
	C:/Program Files/MySQL/MySQL Server 5.0/data/hostname.err # MySQL error log
	C:/Program Files/MySQL/MySQL Server 5.0/data/mysql-bin.log # MySQL binary log
	C:/Program Files/MySQL/MySQL Server 5.0/data/mysql.err # MySQL error log
	C:/Program Files/MySQL/MySQL Server 5.0/data/mysql.log # MySQL general log
	C:/Program Files/MySQL/MySQL Server 5.0/my.cnf # MySQL configuration
	C:/Program Files/MySQL/MySQL Server 5.0/my.ini # MySQL configuration
	C:/Program Files (x86)/Apache Group/Apache2/conf/httpd.conf # Apache configuration
	C:/Program Files (x86)/Apache Group/Apache/conf/httpd.conf # Apache configuration
	C:/Program Files (x86)/Apache Group/Apache/conf/access.log # Apache access logs
	C:/Program Files (x86)/Apache Group/Apache/conf/error.log # Apache error logs
	C:/Program Files (x86)/FileZilla Server/FileZilla Server.xml # FTP server config
	C:/Program Files (x86)/xampp/apache/conf/httpd.conf # Apache configuration
	C:/WINDOWS/php.ini # PHP configuration
	C:/WINDOWS/Repair/SAM # Backup SAM database
	C:/Windows/repair/system # Backup system hive
	C:/Windows/repair/software # Backup software hive
	C:/Windows/repair/security # Backup security hive
	C:/WINDOWS/System32/drivers/etc/hosts # Hosts file
	C:/Windows/win.ini # Windows initialization
	C:/WINNT/php.ini # PHP configuration
	C:/WINNT/win.ini # Windows initialization
	C:/xampp/apache/bin/php.ini # PHP configuration
	C:/xampp/apache/logs/access.log # Apache access logs
	C:/xampp/apache/logs/error.log # Apache error logs
	C:/Windows/Panther/Unattend/Unattended.xml # Windows setup file
	C:/Windows/Panther/Unattended.xml # Windows setup file
	C:/Windows/debug/NetSetup.log # Network setup log
	C:/Windows/system32/config/AppEvent.Evt # Application event log
	C:/Windows/system32/config/SecEvent.Evt # Security event log
	C:/Windows/system32/config/default.sav # Registry backup
	C:/Windows/system32/config/security.sav # Registry backup
	C:/Windows/system32/config/software.sav # Registry backup
	C:/Windows/system32/config/system.sav # Registry backup
	C:/Windows/system32/config/regback/default # Registry backup
	C:/Windows/system32/config/regback/sam # Registry backup
	C:/Windows/system32/config/regback/security # Registry backup
	C:/Windows/system32/config/regback/system # Registry backup
	C:/Windows/system32/config/regback/software # Registry backup
	C:/Program Files/MySQL/MySQL Server 5.1/my.ini # MySQL configuration
	C:/Windows/System32/inetsrv/config/schema/ASPNET_schema.xml # ASP.NET schema
	C:/Windows/System32/inetsrv/config/applicationHost.config # IIS configuration
	C:/inetpub/logs/LogFiles/W3SVC1/u_ex[YYMMDD].log # IIS log files
</details>

<details>
	<summary>Linux</summary>

	/etc/passwd # User accounts
	/etc/shadow # Password hashes
	/etc/aliases # Email aliases
	/etc/anacrontab # Cron jobs
	/etc/apache2/apache2.conf # Apache configuration
	/etc/apache2/httpd.conf # Apache configuration
	/etc/apache2/sites-enabled/000-default.conf # Apache virtual host
	/etc/at.allow # Allowed at users
	/etc/at.deny # Denied at users
	/etc/bashrc # Bash shell initialization
	/etc/bootptab # BOOTP server configuration
	/etc/chrootUsers # Chroot users
	/etc/chttp.conf # CHTTP server configuration
	/etc/cron.allow # Allowed cron users
	/etc/cron.deny # Denied cron users
	/etc/crontab # Cron jobs
	/etc/cups/cupsd.conf # CUPS configuration
	/etc/exports # NFS shares
	/etc/fstab # Filesystems mount
	/etc/ftpaccess # FTP server access
	/etc/ftpchroot # FTP chroot users
	/etc/ftphosts # FTP host access
	/etc/group # Group accounts
	/etc/grub.conf # Bootloader configuration
	/etc/hosts # Hostname to IP
	/etc/hosts.allow # Allowed hosts
	/etc/hosts.deny # Denied hosts
	/etc/httpd/access.conf # Apache access config
	/etc/httpd/conf/httpd.conf # Apache configuration
	/etc/httpd/httpd.conf # Apache configuration
	/etc/httpd/logs/access_log # Apache access logs
	/etc/httpd/logs/access.log # Apache access logs
	/etc/httpd/logs/error_log # Apache error logs
	/etc/httpd/logs/error.log # Apache error logs
	/etc/httpd/php.ini # PHP configuration
	/etc/httpd/srm.conf # Apache srm config
	/etc/inetd.conf # Inetd service configuration
	/etc/inittab # System initialization
	/etc/issue # Pre-login message
	/etc/knockd.conf # Knockd configuration
	/etc/lighttpd.conf # Lighttpd configuration
	/etc/lilo.conf # LILO bootloader config
	/etc/logrotate.d/ftp # Logrotate FTP logs
	/etc/logrotate.d/proftpd # Logrotate ProFTPD logs
	/etc/logrotate.d/vsftpd.log # Logrotate vsftpd logs
	/etc/lsb-release # Distro info
	/etc/motd # Message of the day
	/etc/modules.conf # Kernel modules
	/etc/motd # Message of the day
	/etc/mtab # Mounted filesystems
	/etc/my.cnf # MySQL configuration
	/etc/my.conf # MySQL configuration
	/etc/mysql/my.cnf # MySQL configuration
	/etc/network/interfaces # Network configuration
	/etc/networks # Network names
	/etc/npasswd # Password file
	/etc/php4.4/fcgi/php.ini # PHP configuration
	/etc/php4/apache2/php.ini # PHP configuration
	/etc/php4/apache/php.ini # PHP configuration
	/etc/php4/cgi/php.ini # PHP configuration
	/etc/php5/apache2/php.ini # PHP configuration
	/etc/php5/apache/php.ini # PHP configuration
	/etc/php/apache2/php.ini # PHP configuration
	/etc/php/apache/php.ini # PHP configuration
	/etc/php/cgi/php.ini # PHP configuration
	/etc/php.ini # PHP configuration
	/etc/php/php4/php.ini # PHP configuration
	/etc/php/php.ini # PHP configuration
	/etc/printcap # Printer capabilities
	/etc/profile # System-wide shell profile
	/etc/proftp.conf # ProFTPd configuration
	/etc/proftpd/proftpd.conf # ProFTPd configuration
	/etc/pure-ftpd.conf # Pure-FTPD configuration
	/etc/pureftpd.passwd # Pure-FTPD password file
	/etc/pureftpd.pdb # Pure-FTPD user database
	/etc/pure-ftpd/pure-ftpd.conf # Pure-FTPD configuration
	/etc/pure-ftpd/pure-ftpd.pdb # Pure-FTPD database
	/etc/pure-ftpd/pureftpd.pdb # Pure-FTPD database
	/etc/redhat-release # RedHat version info
	/etc/resolv.conf # DNS servers
	/etc/samba/smb.conf # Samba configuration
	/etc/snmpd.conf # SNMP daemon config
	/etc/ssh/ssh_config # SSH client config
	/etc/ssh/sshd_config # SSH server config
	/etc/ssh/ssh_host_dsa_key # SSH host key
	/etc/ssh/ssh_host_dsa_key.pub # SSH host key
	/etc/ssh/ssh_host_key # SSH host key
	/etc/ssh/ssh_host_key.pub # SSH host key
	/etc/sysconfig/network # Network settings
	/etc/syslog.conf # Syslog configuration
	/etc/termcap # Terminal capabilities
	/etc/vhcs2/proftpd/proftpd.conf # VHCS2 ProFTPd config
	/etc/vsftpd.chroot_list # VsFTPd chroot list
	/etc/vsftpd.conf # VsFTPd configuration
	/etc/vsftpd/vsftpd.conf # VsFTPd configuration
	/etc/wu-ftpd/ftpaccess # WuFTP access control
	/etc/wu-ftpd/ftphosts # WuFTP hosts
	/etc/wu-ftpd/ftpusers # WuFTP users
	/logs/pure-ftpd.log # Pure-FTPD logs
	/logs/security_debug_log # Security logs
	/logs/security_log # Security logs
	/opt/lampp/etc/httpd.conf # XAMPP Apache config
	/opt/xampp/etc/php.ini # XAMPP PHP config
	/proc/cmdline # Boot command line
	/proc/cpuinfo # CPU information
	/proc/filesystems # Filesystems supported
	/proc/interrupts # Interrupts info
	/proc/ioports # I/O port info
	/proc/meminfo # Memory info
	/proc/modules # Loaded kernel modules
	/proc/mounts # Mounted filesystems
	/proc/net/arp # ARP table
	/proc/net/tcp # TCP connections
	/proc/net/udp # UDP connections
	/proc/<PID>/cmdline # Process command line
	/proc/<PID>/maps # Process memory maps
	/proc/sched_debug # Scheduler debug info
	/proc/self/cwd/app.py # Current working directory app
	/proc/self/environ # Process environment
	/proc/self/net/arp # ARP table
	/proc/stat # System statistics
	/proc/swaps # Swap information
	/proc/version # Kernel version
	/root/anaconda-ks.cfg # Kickstart configuration
	/usr/etc/pure-ftpd.conf # Pure-FTPD configuration
	/usr/lib/php.ini # PHP configuration
	/usr/lib/php/php.ini # PHP configuration
	/usr/local/apache/conf/modsec.conf # ModSecurity config
	/usr/local/apache/conf/php.ini # PHP configuration
	/usr/local/apache/log # Apache logs
	/usr/local/apache/logs # Apache logs
	/usr/local/apache/logs/access_log # Apache access logs
	/usr/local/apache/logs/access.log # Apache access logs
	/usr/local/apache/audit_log # Apache audit logs
	/usr/local/apache/error_log # Apache error logs
	/usr/local/apache/error.log # Apache error logs
	/usr/local/cpanel/logs # cPanel logs
	/usr/local/cpanel/logs/access_log # cPanel access logs
	/usr/local/cpanel/logs/error_log # cPanel error logs
	/usr/local/cpanel/logs/license_log # cPanel license logs
	/usr/local/cpanel/logs/login_log # cPanel login logs
	/usr/local/cpanel/logs/stats_log # cPanel stats logs
	/usr/local/etc/httpd/logs/access_log # HTTPD access logs
	/usr/local/etc/httpd/logs/error_log # HTTPD error logs
	/usr/local/etc/php.ini # PHP configuration
	/usr/local/etc/pure-ftpd.conf # Pure-FTPD configuration
	/usr/local/etc/pureftpd.pdb # Pure-FTPD database
	/usr/local/lib/php.ini # PHP configuration
	/usr/local/php4/httpd.conf # PHP4 HTTPD config
	/usr/local/php4/httpd.conf.php # PHP4 HTTPD PHP config
	/usr/local/php4/lib/php.ini # PHP4 configuration
	/usr/local/php5/httpd.conf # PHP5 HTTPD config
	/usr/local/php5/httpd.conf.php # PHP5 HTTPD PHP config
	/usr/local/php5/lib/php.ini # PHP5 configuration
	/usr/local/php/httpd.conf # PHP HTTPD config
	/usr/local/php/httpd.conf.ini # PHP HTTPD ini config
	/usr/local/php/lib/php.ini # PHP configuration
	/usr/local/pureftpd/etc/pure-ftpd.conf # Pure-FTPD configuration
	/usr/local/pureftpd/etc/pureftpd.pdn # Pure-FTPD database
	/usr/local/pureftpd/sbin/pure-config.pl # Pure-FTPD script
	/usr/local/www/logs/httpd_log # HTTPD logs
	/usr/local/Zend/etc/php.ini # Zend PHP configuration
	/usr/sbin/pure-config.pl # Pure-FTPD script
	/var/adm/log/xferlog # Transfer logs
	/var/apache2/config.inc # Apache2 configuration
	/var/apache/logs/access_log # Apache access logs
	/var/apache/logs/error_log # Apache error logs
	/var/cpanel/cpanel.config # cPanel configuration
	/var/lib/mysql/my.cnf # MySQL configuration
	/var/lib/mysql/mysql/user.MYD # MySQL user data
	/var/local/www/conf/php.ini # PHP configuration
	/var/log/apache2/access_log # Apache access logs
	/var/log/apache2/access.log # Apache access logs
	/var/log/apache2/error_log # Apache error logs
	/var/log/apache2/error.log # Apache error logs
	/var/log/apache/access_log # Apache access logs
	/var/log/apache/access.log # Apache access logs
	/var/log/apache/error_log # Apache error logs
	/var/log/apache/error.log # Apache error logs
	/var/log/apache-ssl/access.log # SSL access logs
	/var/log/apache-ssl/error.log # SSL error logs
	/var/log/auth.log # Authentication logs
	/var/log/boot # Boot logs
	/var/htmp # Temporary files
	/var/log/chttp.log # CHTTP logs
	/var/log/cups/error.log # CUPS error logs
	/var/log/daemon.log # Daemon logs
	/var/log/debug # Debug logs
	/var/log/dmesg # Boot messages
	/var/log/dpkg.log # Package manager logs
	/var/log/exim_mainlog # Exim main logs
	/var/log/exim/mainlog # Exim main logs
	/var/log/exim_paniclog # Exim panic logs
	/var/log/exim.paniclog # Exim panic logs
	/var/log/exim_rejectlog # Exim reject logs
	/var/log/exim/rejectlog # Exim reject logs
	/var/log/faillog # Failed login attempts
	/var/log/ftplog # FTP logs
	/var/log/ftp-proxy # FTP proxy logs
	/var/log/ftp-proxy/ftp-proxy.log # FTP proxy logs
	/var/log/httpd-access.log # HTTPD access logs
	/var/log/httpd/access_log # HTTPD access logs
	/var/log/httpd/access.log # HTTPD access logs
	/var/log/httpd/error_log # HTTPD error logs
	/var/log/httpd/error.log # HTTPD error logs
	/var/log/httpsd/ssl.access_log # SSL access logs
	/var/log/httpsd/ssl_log # SSL logs
	/var/log/kern.log # Kernel logs
	/var/log/lastlog # Last login logs
	/var/log/lighttpd/access.log # Lighttpd access logs
	/var/log/lighttpd/error.log # Lighttpd error logs
	/var/log/lighttpd/lighttpd.access.log # Lighttpd access logs
	/var/log/lighttpd/lighttpd.error.log # Lighttpd error logs
	/var/log/mail.info # Mail information
	/var/log/mail.log # Mail logs
	/var/log/maillog # Mail logs
	/var/log/mail.warn # Mail warnings
	/var/log/message # System messages
	/var/log/messages # System messages
	/var/log/mysqlderror.log # MySQL error log
	/var/log/mysql.log # MySQL logs
	/var/log/mysql/mysql-bin.log # MySQL binary log
	/var/log/mysql/mysql.log # MySQL logs
	/var/log/mysql/mysql-slow.log # MySQL slow query log
	/var/log/proftpd # ProFTPd logs
	/var/log/pureftpd.log # Pure-FTPD logs
	/var/log/pure-ftpd/pure-ftpd.log # Pure-FTPD logs
	/var/log/secure # Security logs
	/var/log/vsftpd.log # VsFTPd logs
	/var/log/wtmp # Login records
	/var/log/xferlog # Transfer logs
	/var/log/yum.log # Yum package manager logs
	/var/mysql.log # MySQL logs
	/var/run/utmp # Current logins
	/var/spool/cron/crontabs/root # Root crontab
	/var/webmin/miniserv.log # Webmin logs
	/var/www/html/__init__.py # Python init file
	/var/www/html/db_connect.php # PHP database connection
	/var/www/html/utils.php # PHP utility file
	/var/www/log/access_log # Web access logs
	/var/www/log/error_log # Web error logs
	/var/www/logs/access_log # Web access logs
	/var/www/logs/error_log # Web error logs
	/var/www/logs/access.log # Web access logs
	/var/www/logs/error.log # Web error logs
	~/.atfp_history # ATFP history
	~/.bash_history # Bash shell history
	~/.bash_logout # Bash logout file
	~/.bash_profile # Bash profile
	~/.bashrc # Bash shell initialization
	~/.gtkrc # GTK settings
	~/.login # Shell login script
	~/.logout # Shell logout script
	~/.mysql_history # MySQL history
	~/.nano_history # Nano editor history
	~/.php_history # PHP shell history
	~/.profile # User profile script
	~/.ssh/authorized_keys # SSH authorized keys
	~/.ssh/id_dsa # DSA SSH key
	~/.ssh/id_dsa.pub # DSA SSH public key
	~/.ssh/id_rsa # RSA SSH key
	~/.ssh/id_ecdsa # ECDSA SSH key
	~/.ssh/id_rsa.pub # RSA SSH public key
	~/.ssh/identity # SSH identity key
	~/.ssh/identity.pub # SSH public key
	~/.viminfo # Vim editor history
	~/.wm_style # Window manager style
	~/.Xdefaults # X Window settings
	~/.xinitrc # X Window init script
	~/.Xresources # X Window resources
	~/.xsession # X Window session script
</details>
