Workflow Description Language (WDL)
===================================

Language Spec
-------------

[WDL Language Specification](SPEC.md)

Overview
--------

The Workflow Description Language is a domain specific language for describing tasks and workflows.

An example WDL file that describes three tasks to run UNIX commands (in this case, `ps`, `grep`, and `wc`) and then link them together in a workflow would look like this:

```
task ps {
  command {
    ps
  }
  output {
    file procs = "stdout"
  }
}

task cgrep {
  command {
    grep '${pattern}' ${file in_file} | wc -l
  }
  output {
    int count = read_int("stdout")
  }
}

task wc {
  command {
    wc -l ${file in_file}
  }
  output {
    int count = read_int("stdout")
  }
}

workflow three_step {
  call ps
  call cgrep {
    input: in_file=ps.procs
  }
  call wc {
    input: in_file=ps.procs
  }
}
```

WDL aims to be able to describe tasks with abstract commands which have inputs.  Abstract commands are a template with parts of the command left for the user to provide a value for.  In the example above, the `task wc` declaration defines a task with one input (`in_file` of type file) and one output (`count` of type int).

Once tasks are defined, WDL allows you to construct a workflow of these tasks.  Since each task defines its inputs and outputs explicitly, you can wire together one task's output to be another task's input and create a dependency graph.  An execution engine can then collect the set of inputs it needs from the user to run each task in the workflow up front and then run the tasks in the right order.

WDL also lets you define more advanced structures, like the ability to call a task in parallel (referred to as 'scattering').  In the example below, the `wc` task is being called n-times where n is the length of the `array[string] str_array` variable.  Each element of the `str_array` is used as the value of the `str` parameter in the call to the `wc` task.

```
task wc {
  command {
    echo "${str}" | wc -c
  }
  output {
    int count = read_int("stdout") - 1
  }
}

workflow wf {
  array[string] str_array
  scatter(s in str_array) {
    call wc{input: str=s}
  }
}
```

Project Goals
-------------

The Workflow Description Language project aims to provide the following:

* The full language specification
* Parsers in a few languages
* Language bindings to make working with WDL easier in the client language

### Tool Authors

WDL aims to make it as easy as possible to create `task` and `workflow` definitions in a WDL file and then validate that your syntax is correct and the wiring is done properly.

### Execution Engine Implementers

The WDL project wants to make it easy for an execution engine to quickly be able to understand WDL files and translate them into a native objects in their language of choice.

For example, using [Cromwell](http://github.com/broadinstitute/cromwell) (Java/Scala implemenation) as the WDL language bindings layer, it should be as easy as the following code to use a WDL file:

```scala
val binding = WdlBinding.process(new File("/path/to/workflow.wdl"))
binding.tasks foreach { task =>
    println(task)
    println(task.command)
}
```

Architecture
------------

![WDL Arch](http://i.imgur.com/OYtIYjf.png)

The WDL Project aims to provide at the very least a language specification and parsers in a few languages.

Scala parser and language bindings will be implemented in the [Cromwell](http://github.com/broadinstitute/cromwell) project.  This implementation will also contain an optional execution engine.

Python parser and language bindings will be provided by the [reference implementation](https://github.com/broadinstitute/wdl/tree/wdl2/python).  This implementation can also be used as an execution engine to run workflows locally.

A Java parser is provided [here](https://github.com/broadinstitute/wdl/tree/wdl2/java)
