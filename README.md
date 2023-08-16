# Script to delete your history message from groups

This script will automatically delete your history message in all joined groups.  
It will check the latest `n` messages of each joined group, and delete the message if:

   1. It was sent from you
   2. The group is not whitelisted
   3. The group was sent at least `t` seconds ago

It's recommended to auto-run this script daily to protect your privacy.

这个脚本会自动从所有已加入群组删除你的历史消息.  
它会检查每个已加入群组的最近的n条消息, 并且在满足以下条件时删除它:

1. 消息是你发的
2. 这个群组不在白名单里
3. 这个消息是一定时间段前发的

我们建议你每天自动运行一次此脚本, 来保护你的隐私.

## How to setup / deploy this script

Refer to this guide (for a similar script): <https://git.recolic.net/root/telegram-antispam-watchdog> (**Click README_en.md**)

The configuration options might be different but you should be able to figure it out.

## 如何安装和运行

请查阅这个指南(为一个类似的脚本): <https://git.recolic.net/root/telegram-antispam-watchdog>

具体配置项目可能有所不同, 但你应该足够聪明可以理解.

