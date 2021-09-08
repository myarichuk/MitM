#!/bin/sh

iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 5556 -j REDIRECT --to-port 8080