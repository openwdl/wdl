#!/bin/bash

hermes generate ../grammar.hgr --name=wdl --directory=java7 --language=java --java-use-apache-commons
hermes generate ../grammar.hgr --name=wdl --directory=java8 --language=java
