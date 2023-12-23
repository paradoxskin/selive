#!/bin/bash
#mitmproxy -q -s cutoff.py& disown
mitmdump -q -p 9010 -s cutoff.py
