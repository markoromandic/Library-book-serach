#!/bin/bash

k=1
p=1
P=1
# PROVERA SADRZAJA FOLDERA
if [ ! -f ./fajlovi/knjige.txt ]; then
    echo "knjige.txt not found!"
    k=0
fi
if [ ! -f ./fajlovi/prefiksi.txt ]; then
    echo "prefiksi.txt not found!"
    p=0
fi
if [ ! -f ./fajlovi/PrefixNames_sr.properties ]; then
    echo "PrefixNames_sr.properties not found!"
    P=0
fi
# ISPIS NAZIVA FAJLOVA I BROJ NJEGOVIH LINIJA
for entry in ./fajlovi/*
do
  lines="wc -l $entry"
  echo "$($lines)"
done
# PROVERA knjige.txt AKO POSTOJI
if [ $k == 1 ]; then
    brojlinija="$(grep "200..." ./fajlovi/knjige.txt -cv)"
    zapravolinije="$(grep "200..." ./fajlovi/knjige.txt -v)"
    echo "Number of lines that doesn't contain needed info in knjige.txt: $brojlinija"
    echo "$zapravolinije"
fi
# PROVERA prefiksi.txt AKO IMA
if [ $p == 1 ]; then
    ukupanbrojneispravnihlinija="$(egrep "^[A-Z]{2}-[0-9]{3}[a-z]" -cv ./fajlovi/prefiksi.txt)"
    neispravnelinije="$(egrep "^[A-Z]{2}-[0-9]{3}[a-z]" ./fajlovi/prefiksi.txt -vn)"
    echo "Number of lines that doesn't fit the criteria in prefiksi.txt: $ukupanbrojneispravnihlinija"
    echo "$neispravnelinije"
fi
# PROVERA PrefixNames_sr.properties AKO IMA
if [ $P == 1 ]; then
  ukupanbrojneispravnihlinija="$(egrep "^[A-Z]{2}=" -cv ./fajlovi/PrefixNames_sr.properties)"
  neispravnelinije="$(egrep "^[A-Z]{2}=" -vn ./fajlovi/PrefixNames_sr.properties)"
  echo "Number of lines that doesn't fit the criteria in PrefixNames_sr.properties: $ukupanbrojneispravnihlinija"
  echo "$neispravnelinije"
fi
