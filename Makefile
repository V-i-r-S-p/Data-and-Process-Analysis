
all: run


run:

get_venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

get_requirements:
	. .venv/bin/activate && pip freeze > requirements.txt

check:

test:

clear:
