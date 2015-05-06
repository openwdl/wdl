WDL Java Parser
===============

`java8/WdlParser.java` is a Java 8 parser for WDL.  The `Main.java` file is a simple client that parses a WDL file and then prints out the abstract syntax tree

`java7/WdlParser.java` is a Java 7 parser for WDL.  This parser, however, has a dependency on [Apache Commons Codec](https://commons.apache.org/proper/commons-codec/).

Usage
-----

```
$ cd java8
$ java -version
java version "1.8.0_45"
Java(TM) SE Runtime Environment (build 1.8.0_45-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.45-b02, mixed mode)
$ javac *.java
$ java Main ../example.wdl
(Document:
  definitions=[
    (Task:
      name=<example.wdl:1:6 identifier "d2M=">,
      declarations=[],
      sections=[
        (RawCommand:
          parts=[
            <example.wdl:2:12 cmd_part "CiAgICBlY2hvICI=">,
            (CommandParameter:
              name=<example.wdl:3:13 identifier "c3Ry">,


              type=None,
              prefix=None,
              attributes=[],
              postfix=None
            ),
            <example.wdl:3:17 cmd_part "IiB8IHdjIC1jCiAg">
          ]
        ),
        (Outputs:
          attributes=[
            (Output:
              type=<example.wdl:6:5 type "SW50">,
              var=<example.wdl:6:9 identifier "Y291bnQ=">,
              expression=(Subtract:
                lhs=(FunctionCall:
                  name=<example.wdl:6:17 identifier "cmVhZF9pbnQ=">,
                  params=[
                    <example.wdl:6:27 string "c3Rkb3V0">
                  ]
                ),
                rhs=<example.wdl:6:38 integer "MQ==">
              )
            )
          ]
        )
      ]
    ),
    (Workflow:
      name=<example.wdl:10:10 identifier "d2Y=">,
      body=[
        (Declaration:
          type=(Type:
            name=<example.wdl:11:3 type "QXJyYXk=">,
            subtype=[
              <example.wdl:11:9 type "U3RyaW5n">
            ]
          ),
          name=<example.wdl:11:17 identifier "c3RyX2FycmF5">,
          expression=None
        ),
        (Scatter:
          item=<example.wdl:12:11 identifier "cw==">,
          collection=<example.wdl:12:16 identifier "c3RyX2FycmF5">,
          body=[
            (Call:
              task=<example.wdl:13:10 identifier "d2M=">,
              alias=None,
              body=(CallBody:
                declarations=[],
                io=[
                  (Inputs:
                    map=[
                      (IOMapping:
                        key=<example.wdl:13:20 identifier "c3Ry">,
                        value=<example.wdl:13:24 identifier "cw==">
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
