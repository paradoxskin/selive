#!/bin/bash
python ./se.py &
mitmdump -q -p 9010 -s cutoff.py
echo
echo "[-] finishing..."
ps -aux|grep -v grep|grep "selenium --headless"|awk '{print $2}'|xargs kill
echo "[+] done"
