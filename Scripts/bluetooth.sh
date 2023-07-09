#!/usr/bin/zsh

bt_on=$(bluetoothctl show AC:7B:A1:67:81:BB | grep "Powered: yes")

bt_len=$#bt_on

if (($bt_len == 0))
then
bluetoothctl power on
else
bluetoothctl power off
fi
