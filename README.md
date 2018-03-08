# csirtg-urlsml-py
simple python library for detecting odd urls in python

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