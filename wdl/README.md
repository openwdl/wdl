Usage
=====

There are two example .wdl files in this directory that parse:

* MutSig.wdl
* CopyNumberQC.wdl

From Java code, the main interface is the CompositeTask, which can be used in this example to acquire the name of each task:

```java
CompositeTask wdl = new CompositeTask(new File(args[0]));
Map<String, Ast> steps = wdl.getSteps();
for ( Map.Entry<String, Ast> entry : steps.entrySet() ) {
  System.out.println("Step: " + entry.getKey());
}
```

To extract parse tree, and abstract syntax tree information from the command line:

```
$ javac *.java
$ cat simple.wdl
composite_task x {step y[version=0] {}}
$ java WdlMain simple.wdl parsetree
(wdl:
  (_gen0:
    (wdl_entity:
      (composite_task:
        composite_task,
        identifier,
        lbrace,
        (_gen1:
          (composite_task_entity:
            (step:
              step,
              (task_identifier:
                identifier,
                (_gen5:
                  (task_attrs:
                    lsquare,
                    (_gen6:
                      (task_attr:
                        identifier,
                        assign,
                        (task_attr_value:
                          number
                        )
                      ),
                      (_gen6: )
                    ),
                    rsquare
                  )
                )
              ),
              (_gen3: ),
              lbrace,
              (_gen4: ),
              rbrace
            )
          ),
          (_gen1: )
        ),
        rbrace
      )
    ),
    (_gen0: )
  )
)
$ java WdlMain simple.wdl ast
(CompositeTask:
  body=[
    (Step:
      body=[],
      task=(Task:
        attributes=[
          (TaskAttribute:
            value=number,
            key=identifier
          )
        ],
        name=identifier
      ),
      name=None
    )
  ],
  name=identifier
)
$ java WdlMain simple.wdl nodes
Step: y
```
