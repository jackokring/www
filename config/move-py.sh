#!/usr/bin/bash

mkdir html/py
mkdir node/py

cd py
for f in client/*.py
do
    cp "$f" ../html/py
done

for f in server/*.py
do
    cp "$f" ../node/py
done