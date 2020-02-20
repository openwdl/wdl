
all: generate install

generate:
	bash -i ./scripts/build.sh

install:
	python3 setup.py install

test:
	python3 -m pytest tests/WdlParserTests.py
