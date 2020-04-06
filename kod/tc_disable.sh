#!/bin/bash

# delete

for i in {0..5}
do
    tc qdisc del dev r0-eth${i} root
done