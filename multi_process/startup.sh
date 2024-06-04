#!/bin/bash

mongod --bind_ip_all & 
P1=$!
gunicorn -w 4 -b 0.0.0.0:5500 app:application &
P2=$!
wait $P1 $P2
