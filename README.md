# ansible-role-asus-merlin
Ansible role to manage Asus Merlin router

## Requirements
 - Enable jffs partition: https://github.com/RMerl/asuswrt-merlin.ng/wiki/Jffs
 - Enable SSH access: https://levelup.gitconnected.com/how-to-get-maximum-from-your-asus-router-part-2-a23e0f0aa884
 - Connect USB pendrive for Entware repository
 - Install Entware repository using amtm tool:  https://github.com/RMerl/asuswrt-merlin.ng/wiki/Entware
 - Install python3 and openssh-sftp-server
 ```
opkg install python3
opkg install openssh-sftp-server
 ```
 