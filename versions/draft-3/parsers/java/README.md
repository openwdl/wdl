WDL Java Parser
===============

Java 8
------

`java8/WdlParser.java` is a Java 8 parser for WDL.

The `java8/Main.java` file is a simple client that parses a WDL file and then prints out the abstract syntax tree.

This parser has a dependency on [Apache Commons Lang](http://commons.apache.org/proper/commons-lang/).

Java 7
------

`java7/WdlParser.java` is a Java 7 parser for WDL.

This parser, has a dependency on [Apache Commons Lang](http://commons.apache.org/proper/commons-lang/) and [Apache Commons Codec](https://commons.apache.org/proper/commons-codec/).

Usage
-----

Use the `Makefile` within the `java7` and `java8` directories:

```
$ cd java8
$ java -version
java version "1.8.0_45"
Java(TM) SE Runtime Environment (build 1.8.0_45-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.45-b02, mixed mode)
$ make deps compile run clean
... lots of output ...
(Document:
  imports=[],
  definitions=[
    (Task:
      name=<example.wdl:1:6 identifier "d2M=">,
      declarations=[
        (Declaration:
          type=<example.wdl:2:3 type "U3RyaW5n">,
          postfix=None,
          name=<example.wdl:2:10 identifier "c3Ry">,
          expression=None
        )
      ],
      sections=[
        (RawCommand:
          parts=[
            <example.wdl:3:12 cmd_part "CiAgICBlY2hvICI=">,
            (CommandParameter:
              attributes=[],
              expr=<example.wdl:4:13 identifier "c3Ry">
            ),
            <example.wdl:4:17 cmd_part "IiB8IHdjIC1jCiAg">
          ]
        ),
        (Outputs:
          attributes=[
            (Output:
              type=<example.wdl:7:5 type "SW50">,
              var=<example.wdl:7:9 identifier "Y291bnQ=">,
              expression=(Subtract:
                lhs=(FunctionCall:
                  name=<example.wdl:7:17 identifier "cmVhZF9pbnQ=">,
                  params=[
                    <example.wdl:7:26 string "c3Rkb3V0">
                  ]
                ),
                rhs=<example.wdl:7:38 integer "MQ==">
              )
            )
          ]
        )
      ]
    ),
    (Workflow:
      name=<example.wdl:11:10 identifier "d2Y=">,
      body=[
        (Declaration:
          type=<example.wdl:12:3 type "U3RyaW5n">,
          postfix=None,
          name=<example.wdl:12:10 identifier "ZXNj">,
          expression=<example.wdl:12:16 string "YQoiYgki">
        ),
        (Declaration:
          type=(Type:
            name=<example.wdl:13:3 type "QXJyYXk=">,
            subtype=[
              <example.wdl:13:9 type "U3RyaW5n">
            ]
          ),
          postfix=None,
          name=<example.wdl:13:17 identifier "c3RyX2FycmF5">,
          expression=None
        ),
        (Scatter:
          item=<example.wdl:14:11 identifier "cw==">,
          collection=<example.wdl:14:16 identifier "c3RyX2FycmF5">,
          body=[
            (Call:
              task=<example.wdl:15:10 fqn "d2M=">,
              alias=None,
              body=(CallBody:
                declarations=[],
                io=[
                  (Inputs:
                    map=[
                      (IOMapping:
                        key=<example.wdl:15:20 identifier "c3Ry">,
                        value=<example.wdl:15:24 identifier "cw==">
                      )
                    ]
                  )
                ]
              )
            )
          ]
        )
      ]
    )
  ]
)
```
