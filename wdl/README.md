Usage
=====

There are two example .wdl files in the examples/ directory:

* MutSig.wdl
* CopyNumberQC.wdl

From Java code, the main interface is the CompositeTask, which can be used in this example to acquire the name of each task:

```java
CompositeTask ct = new CompositeTask(new File(args[0]));
for ( CompositeTaskNode entry : ct.getNodes() ) {
  System.out.println("Node: " + entry);
}
```

To extract parse tree, and abstract syntax tree information from the command line:

First compile the sources:
```
$ javac *.java
$ cat examples/0.zgr
composite_task foo {
  
  step atask[version=0] {
    output: File("foo.txt") as x;
  }

  for ( item in foo ) {
    step btask[version=0] {
      input: p0=x, p1=s;
      output: File("bar.txt") as y;
    }

    step ctask[version=0] {
      input: p0=x, p1=y;
      output: File("quux.txt") as z;
    }
  }

  step dtask[version=0] {
    input: p0=x, p1=y, p2=z;
    output: File("report.txt") as r;
  }

}
```

Get the abstract syntax tree:

```
$ java WdlMain examples/0.wdl ast
(CompositeTask:
  body=[
    (Step:
      body=[
        (StepOutputList:
          outputs=[
            (StepFileOutput:
              as=(Variable:
                member=None,
                name=identifier
              ),
              file=string
            )
          ]
        )
      ],
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
    ),
    (ForLoop:
      body=[
        (Step:
          body=[
            (StepInputList:
              inputs=[
                (StepInput:
                  parameter=identifier,
                  value=(Variable:
                    member=None,
                    name=identifier
                  )
                ),
                (StepInput:
                  parameter=identifier,
                  value=(Variable:
                    member=None,
                    name=identifier
                  )
                )
              ]
            ),
            (StepOutputList:
              outputs=[
                (StepFileOutput:
                  as=(Variable:
                    member=None,
                    name=identifier
                  ),
                  file=string
                )
              ]
            )
          ],
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
        ),
        (Step:
          body=[
            (StepInputList:
              inputs=[
                (StepInput:
                  parameter=identifier,
                  value=(Variable:
                    member=None,
                    name=identifier
                  )
                ),
                (StepInput:
                  parameter=identifier,
                  value=(Variable:
                    member=None,
                    name=identifier
                  )
                )
              ]
            ),
            (StepOutputList:
              outputs=[
                (StepFileOutput:
                  as=(Variable:
                    member=None,
                    name=identifier
                  ),
                  file=string
                )
              ]
            )
          ],
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
      item=identifier,
      collection=identifier
    ),
    (Step:
      body=[
        (StepInputList:
          inputs=[
            (StepInput:
              parameter=identifier,
              value=(Variable:
                member=None,
                name=identifier
              )
            ),
            (StepInput:
              parameter=identifier,
              value=(Variable:
                member=None,
                name=identifier
              )
            ),
            (StepInput:
              parameter=identifier,
              value=(Variable:
                member=None,
                name=identifier
              )
            )
          ]
        ),
        (StepOutputList:
          outputs=[
            (StepFileOutput:
              as=(Variable:
                member=None,
                name=identifier
              ),
              file=string
            )
          ]
        )
      ],
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
```

Get a view of the graph

```
$ java WdlMain examples/0.wdl graph
[Step: name=dtask]
[Step: name=atask]
[CompositeTaskForScope: collection=foo, var=item, # nodes=2]
[Edge
  from=[Output node=[Step: name=atask], path="foo.txt"],
  to=[Input node=[Step: name=dtask], param=p0],
  var=x
]
[Edge
  from=[Output node=[Step: name=atask], path="foo.txt"],
  to=[Input node=[CompositeTaskForScope: collection=foo, var=item, # nodes=2], param=null],
  var=x
]
[Edge
  from=[Output node=[Step: name=atask], path="foo.txt"],
  to=[Input node=[Step: name=btask], param=p0],
  var=x
]
[Edge
  from=[Output node=[Step: name=atask], path="foo.txt"],
  to=[Input node=[CompositeTaskForScope: collection=foo, var=item, # nodes=2], param=null],
  var=x
]
[Edge
  from=[Output node=[Step: name=atask], path="foo.txt"],
  to=[Input node=[Step: name=ctask], param=p0],
  var=x
]
[Edge
  from=[Output node=[CompositeTaskForScope: collection=foo, var=item, # nodes=2], path="bar.txt"],
  to=[Input node=[Step: name=dtask], param=p1],
  var=y
]
[Edge
  from=[Output node=[Step: name=btask], path="bar.txt"],
  to=[Input node=[Step: name=dtask], param=p1],
  var=y
]
[Edge
  from=[Output node=[Step: name=btask], path="bar.txt"],
  to=[Input node=[Step: name=ctask], param=p1],
  var=y
]
[Edge
  from=[Output node=[CompositeTaskForScope: collection=foo, var=item, # nodes=2], path="quux.txt"],
  to=[Input node=[Step: name=dtask], param=p2],
  var=z
]
[Edge
  from=[Output node=[Step: name=ctask], path="quux.txt"],
  to=[Input node=[Step: name=dtask], param=p2],
  var=z
]
```
