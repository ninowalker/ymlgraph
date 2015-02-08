
env: env/bin/activate
env/bin/activate: setup.py
	test -f $@ || virtualenv --no-site-packages env
	. $@; pip install -e .
	touch $@
