.PHONY: clean env/bin/activate

PYENV = . env/bin/activate;
PYTHON = $(PYENV) python

doc.pdf: env gen.py desc.yaml
	$(PYTHON) gen.py desc.yaml $@

env: env/bin/activate
env/bin/activate: requirements.txt
	test -f $@ || virtualenv --no-site-packages env
	ln -fs env/bin .
	$(PYENV) pip install -r requirements.txt
	touch $@
