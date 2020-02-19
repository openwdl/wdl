# WDL Java Parser

This directory provides a parser implemented in java. The parser is built on top of the Base [WDLBaseLexer.java](src/main/java/org/openwdl/wdl/parser/WDLBaseLexer.java)

# Requirements
- Java 7+

# Building

Building the project can be accomplished using the packaged maven wrapper.

```bash
./mvnw -DskipTests clean package
```

# Running tests

There are a number of tests which can be run using surefire.

```bash
./mvnw test
```
