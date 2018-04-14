# csirtg-urlsml-py
simple python library for detecting odd urls in python

https://csirtgadgets.com/commits/2018/3/8/hunting-for-suspicious-domains-using-python-and-sklearn
https://csirtgadgets.com/commits/2018/3/30/hunting-for-threats-like-a-quant

```bash
$ pip install -r dev_requirements.txt
$ python setup.py develop
$ bash rebuild.sh  # this will take a few min..
$ bash build_model.sh

$ csirtg-urlsml -i http://paypal-ate-my-lunch.com
Yes
$ csirtg-urlsml -i http://paypal.com
No
```
