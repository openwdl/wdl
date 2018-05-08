#!/bin/bash

hermes generate ../grammar.hgr --name=wdl --directory=java7 --language=java --java-use-apache-commons --java-imports=org.apache.commons.lang3.StringEscapeUtils
hermes generate ../grammar.hgr --name=wdl --directory=java8 --language=java --java-imports=org.apache.commons.lang3.StringEscapeUtils
