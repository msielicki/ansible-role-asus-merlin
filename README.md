# ansible-role-asus-merlin
Ansible role to manage Asus Merlin router

# requirements
 - Enable jffs partition: https://github.com/RMerl/asuswrt-merlin.ng/wiki/Jffs
 - Enable SSH access
 - Connect USB pendrive for Entware repository
 - Install Entware repository using amtm tool:  https://github.com/RMerl/asuswrt-merlin.ng/wiki/Entware
 - Install python3 and ssh
 ```
 opkg install openssh-sftp-server
 opkg install python3
 ```