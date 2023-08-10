#!/usr/bin/zsh

bt_on=$(bluetoothctl show 48:89:E7:34:95:2B | grep "Powered: yes")

bt_len=$#bt_on

if (($bt_len == 0))
then
bluetoothctl power on
else
bluetoothctl power off
fi
