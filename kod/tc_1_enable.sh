#!/bin/bash

# obciazany bedzie tylko int do pc1 wiec tylko na nim bedzie htb

for i in {1..5}
do 
  tc qdisc add dev r0-eth${i} root handle 1: htb default 30

  # 
  tc class add dev r0-eth${i} parent 1: classid 1:1 htb rate 10mbit ceil 10mbit
  # voice
  tc class add dev r0-eth${i} parent 1:1 classid 1:10 htb rate 0.5mbit ceil 10mbit
  # http
  tc class add dev r0-eth${i} parent 1:1 classid 1:20 htb rate 4.5mbit ceil 10mbit
  # reszta
  tc class add dev r0-eth${i} parent 1:1 classid 1:30 htb rate 5mbit ceil 10mbit


  # voice
  tc qdisc add dev r0-eth${i} parent 1:10 handle 10: pfifo
  # http
  tc qdisc add dev r0-eth${i} parent 1:20 handle 20: pfifo
  # reszta
  tc qdisc add dev r0-eth${i} parent 1:30 handle 30: pfifo

  # filtrowanie ruchu
  tc filter add dev r0-eth${i} parent 1:0 protocol ip prio 1 u32 match ip dport 5060 0xffff flowid 1:10
  tc filter add dev r0-eth${i} parent 1:0 protocol ip prio 1 u32 match ip dport 80 0xffff flowid 1:20
done

# delete
# tc qdisc del dev r0-eth1 root
