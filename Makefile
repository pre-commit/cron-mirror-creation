all: venv

venv: requirements.txt
	rm -rf venv
	virtualenv venv -ppython3.6
	venv/bin/pip install -r requirements.txt

.PHONY: push
push: venv
	venv/bin/python push.py

.PHONY: push-dry-run
push-dry-run: venv
	venv/bin/python push.py --dry-run
