
all: generate install

generate:
	bash -i ./scripts/build.sh

install:
	python2.7 setup.py install


test:
	python2.7 -m WdlParser.tests.WdlParserTests