#!/bin/bash

rm -rf tmp
mkdir -p tmp

echo "creating whitelist"
cat data/whitelist.txt | python csirtg_urlsml/url.py --good > tmp/good.csv

echo "creating blacklist"
cat data/blacklist.txt | python csirtg_urlsml/url.py > tmp/bad.csv

echo "merging lists"
cat tmp/good.csv tmp/bad.csv | gshuf > tmp/training.csv

TESTS="http://g00gle.com/about-us
https://www.joyrideme.com/uploads/id/account
http://www.karinarohde.com.br/wp-content/newdocxb/94717fa5cff4c50a4ab9ae855ec894d1
http://english.gov.cn/about-us
https://aws.amazon.com
http://www.bankwest.com.au/security-centre/bankwest-privacy-policy
https://csirtg.io
https://ringcentral.com
https://store.apple.com
https://gallery.mailchimp.com/27aac8a65e64c994c4416d6b8/images/leafshadowvert.png
https://security.duke.edu
"


for T in $TESTS; do
  echo "Testing $T"
  cat tmp/training.csv | python csirtg_urlsml/train.py -i $T
done
