# Workflow Description Language (WDL)

WDL is a workflow language meant to be read and written by humans. Broader documentation is provided
by the [WDL website](https://software.broadinstitute.org/wdl/). Any questions or issues can be discussed at
our [support forum](http://gatkforums.broadinstitute.org/wdl).

* [Draft 1 Language Specification](https://github.com/broadinstitute/wdl/blob/master/SPEC.md) (closed)
* [Draft 2 Language Specification](https://github.com/broadinstitute/wdl/blob/develop/SPEC.md) (open)

Library and engine support is provided by

* [Java parser](java) which provides only a parser to convert a WDL string into an AST
* [wdl4s](http://github.com/broadinstitute/wdl4s) provides Scala bindings for WDL and uses the above Java parser
* [PyWDL](https://github.com/broadinstitute/pywdl) provides Python bindings for WDL
* [Cromwell](http://github.com/broadinstitute/cromwell) is an engine for running WDL workflows.  This uses [wdl4s](http://github.com/broadinstitute/wdl4s)

# Table of Contents

<!---toc start-->

* [Workflow Description Language (WDL)](#workflow-description-language-wdl)
* [Overview](#overview)
* [Getting Started with WDL](#getting-started-with-wdl)

<!---toc end-->

# Overview

The Workflow Description Language is a domain specific language for describing tasks and workflows.

An example WDL file that describes three tasks to run UNIX commands (in this case, `ps`, `grep`, and `wc`) and then link them together in a workflow would look like this:

```wdl
task ps {
  command {
    ps
  }
  output {
    File procs = stdout()
  }
}

task cgrep {
  String pattern
  File in_file
  command {
    grep '${pattern}' ${in_file} | wc -l
  }
  output {
    Int count = read_int(stdout())
  }
}

task wc {
  File in_file
  command {
    cat ${in_file} | wc -l
  }
  output {
    Int count = read_int(stdout())
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

WDL also lets you define more advanced structures, like the ability to call a task in parallel (referred to as 'scattering').  In the example below, the `wc` task is being called n-times where n is the length of the `Array[String] str_array` variable.  Each element of the `str_array` is used as the value of the `str` parameter in the call to the `wc` task.

```
task wc {
  String str
  command {
    echo "${str}" | wc -c
  }
  output {
    Int count = read_int(stdout()) - 1
  }
}

workflow wf {
  Array[String] str_array
  scatter(s in str_array) {
    call wc {
      input: str=s
    }
  }
}
```

# Getting Started with WDL

The [WDL website](https://software.broadinstitute.org/wdl/) has a full [Getting Started](https://software.broadinstitute.org/wdl/userguide/) guide as well as multiple [tutorials](https://software.broadinstitute.org/wdl/userguide/topic?name=wdl-tutorials) and a [support forum](http://gatkforums.broadinstitute.org/wdl). Please check those out to quickly get yourself up and running.
