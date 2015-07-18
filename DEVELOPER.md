# Workflow Execution Algorithm

This section outlines an example algorithm to execute tasks and workflows.  It's presented here as a suggestion algorithm and as a learning tool.  The algorithm here is the one used by the reference implementation.

In this algorithm, workflows and tasks are executed the same way.  Tasks should be considered one-step workflows.  The rest of this document will refer only to executing workflows.

Execution relies on two data structures: a symbol table and an execution table.

The symbol table holds variables and their values and some meta-data about them (e.g. their type and whether they're an input or output).

The execution table has an entry for each task that needs to be executed and its current status of execution.

The details of these tables and the algorithm is shown in the following sections.

## Symbol Table Construction

Executing a workflow first depends on determining the variables for the workflow and constructing a **Symbol Table** consisting of all of these variables with null values initially.

Determining the **Symbol Table** entries is done by examining all the tasks in the workflow and extracting every input (everything declared in `${`...`}`) and every output variable.  The name of the variable is prepended with the tasks name, and task aliases may be used at the workflow level.  Here is an example:

```
task t1 {
  command {python script.py ${File path} -n ${sample_name}}
  output {Array[String] result = "${sample_name}.data.txt"}
  runtime {docker: "broadinstitute/job-runner:${docker_version}"}
}
task t2 {
  command {wc -l ${infile1} ${infile2}}
  output {int lines = stdout()}
}
workflow t3 {
  call t1
  call t2 as renamed {
    input: infile2=t1.result
  }
}
```

The initial symbol table construction would be:

|Variable                 |Value           |
|-------------------------|----------------|
|t1.path                  |null            |
|t1.sample_name           |null            |
|t1.docker_version        |null            |
|t1.result                |null            |
|renamed.infile1          |null            |
|renamed.infile2          |null            |

## Symbol Table Initial Population

Next is to populate the initial values.  First, populate internal references.  Any value that starts with a '%ref:' is a reference to a different value in the symbol table.  In this case, we populate a reference from `renamed.infile2` to `t1.result`:

|Variable                 |Value           |
|-------------------------|----------------|
|t1.path                  |null            |
|t1.sample_name           |null            |
|t1.docker_version        |null            |
|t1.result                |null            |
|renamed.infile1          |null            |
|renamed.infile2          |%ref:t1.result  |

The client that is running the workflow MUST provide a valid value (matching or compatible type) for every *input* variable, which is anything inside `${`...`}`.

In this case, let's say the client submits these values:

|Variable                 |Value                      |
|-------------------------|---------------------------|
|t1.path                  |/path/to/input.txt         |
|t1.sample_name           |my_sample                  |
|t1.docker_version        |latest                     |
|renamed.infile1          |/path/to/another_input.txt |

The resulting symbol table would look like:

|**Variable**             |**Value**                  |
|-------------------------|---------------------------|
|t1.path                  |/path/to/input.txt         |
|t1.sample_name           |my_sample                  |
|t1.docker_version        |latest                     |
|**t1.result**            |**null**                   |
|renamed.infile1          |/path/to/another_input.txt |
|renamed.infile2          |%ref:t1.result             |

Notice how the only variable in the symbol table left unassigned is `t1.result` (and by reference, `renamed.infile2` is also unassigned).

## Execution Table Construction

The execution table has one entry for each task with its potentially aliased name.  Initially the **Status** column is set to `not_started`.  This table should include any additional columns to link the execution of this task to the client system.  For example, if jobs are run in Sun GridEngine, there might be an additional column linking to a table which has the SGE Job ID and the current state of that job in SGE.  Alternatively there might simply be a foreign key to a another table which contains implementation-specific information about the particular job.

Valid states for the **Status** field are:

* `not_started` - This task was not yet started because not all of its input parameters are defined
* `started` - All inputs to this task are defined and the task was launched in an implementation specific way
* `successful`- Execution of this task has completed with a zero return code.
* `failed` - Execution of this task has completed with a non-zero return code.
* `skipped` - This task cannot be run because an upstream task that was supposed to produce one of its inputs is in either `error` or `failed` states.
* `error` - The task has finished with a zero return code, but one of the outputs for the task doesn't match its declared type.  Either the format of the file was wrong or the file does not exist.

Terminal states are: `skipped`, `successful`, `failed`, or `error`

A workflow execution table would include at least this:

|**Task**                 |**Index**   |**Status**  |...      |
|-------------------------|------------|------------|---------|
|task1                    |            |not_started |         |
|task2                    |            |not_started |         |

The **Index** field is left blank unless this task is part of a series of scatter tasks, in which case this is an integer >= 0.  Having an index value here means that some of the inputs to the task in the symbol table can be arrays and this index is used to index those arrays.

## Workflow Evaluation

After both the symbol table and execution table are constructed, the algorithm must examine all tasks in the execution table with a `not_started` state (i.e. all of them).  It finds all parameters to the task in the symbol table and if all of them have a value specified, the task is started and the status field gets set to `started`.

The workflow engine is responsible for monitoring the progress of the jobs it runs in an implementation specific way.  Once a job completes, The workflow engine must set the job to either `successful` or `failed`.  The workflow engine must then evaluate the tasks's output mappings and write them to the symbol table.  If evaluation of the output mappings fails, set the status to `error`.  Otherwise, set the status to `successful` if the return code is zero and `failed` otherwise.

> **TODO**: Write a section about evaluating output mappings

When evaluating if a `not_started` job should be started, the workflow engine must set the status to `skipped` and leave the return code undefined if any of is inputs references a job that is in either of these states: `error`, `failed`, or `skipped`.

> **Job Avoidance**: When examining a `not_started` task, the engine might have a way of noticing that this particular task was already run in the past and we have results for it already.  If that's the case, the workflow engine may set the state immediately to `finished` and fulfill its output mappings contract.

## Workflow Termination

A workflow is defined as finished if the following conditions are met:

* All entries in the **Execution Table** are in a terminal state.

## Example 1: Two-step parallel workflow

```
task grep_words {
  command {
    grep '^${start}' ${File infile}
  }
  output {
    Array[String] words = read_lines(stdout())
  }
}
workflow wf {
  File dictionary
  call grep_words as grep_pythonic_words {
    input: start="pythonic", infile=dictionary
  }
  call grep_words as grep_workf_words {
    input: start="workf", infile=dictionary
  }
}
```

Given these parameters values:

|Variable                 |Value                      |
|-------------------------|---------------------------|
|wf.dictionary            |/usr/share/dict/words      |

At start of execution, **Symbol Table** looks like this:

|Name                         |Value                                  |Type         |I/O   |
|-----------------------------|---------------------------------------|-------------|------|
|wf.dictionary                |/usr/share/dict/words                  |file         |input |
|wf.grep_pythonic_words.start |pythonic                               |String       |input |
|wf.grep_pythonic_words.infile|%ref:wf.dictionary                     |file         |input |
|wf.grep_pythonic_words.words |['pythonic', 'pythonical']             |Array[String]|output|
|wf.grep_workf_words.start    |workf                                  |String       |input |
|wf.grep_workf_words.infile   |%ref:wf.dictionary                     |file         |input |
|wf.grep_workf_words.words    |['workfellow', 'workfolk', 'workfolks']|Array[String]|output|

And **Execution Table** looks like this:

|Name                  |Status     |Index|PID |rc  |
|----------------------|-----------|-----|----|----|
|wf.grep_pythonic_words|not_started|     |    |    |
|wf.grep_workf_words   |not_started|     |    |    |

Any field beyond **Task**, **Status**, and **Index** are optional and implementation specific.  In this example, **PID** and **rc** capture the fact that these jobs are running as subprocesses.

The engine will then examine all tasks with a the `not_started` status and look up all their input variables in the **symbol table**.  If there is a value for each of the inputs, the task is started and the status is changed to `started`.  The status of `started` means that the workflow engine has started the job in an implementation-specific way.  Or it might mean simply launching a sub-process in which case the *System Status* field might not be necessary (and perhaps there would be a column for PID).

|Name                  |Status     |Index|PID |rc  |
|----------------------|-----------|-----|----|----|
|wf.grep_pythonic_words|started    |     |1643|    |
|wf.grep_workf_words   |started    |     |1644|    |

The workflow engine is responsible for updating all fields besides the first three in an implementation specific way.  Once the workflow engine determines that a job is done executing, it updates the **Status** field to either `successful` or `failed`.

|Name                  |Status     |Index|PID |rc  |
|----------------------|-----------|-----|----|----|
|wf.grep_pythonic_words|successful |     |1643|0   |
|wf.grep_workf_words   |started    |     |1644|    |

Upon a job finishing and the return code being set, the `outputs` section is processed for that task.  In the case of the above example, when `wf.grep_pythonic_words` finishes the output mapping `Array[String] words = read_lines(stdout())` is processed.  The workflow engine looks for the file called `stdout` in the current working directory where the process was launched.  If it is not found, the task's status gets set to `error` and optionally an error message field gets set describing the nature of why the field was set.

A workflow is defined as finished when all the tasks in the workflow are in a terminal state (i.e. `skipped`, `successful`, `failed`, or `error`).  For this example, let's say the first task succeeds and the second task fails.  The terminal state of the workflow is:

|Name                  |Status     |Index|PID |rc  |
|----------------------|-----------|-----|----|----|
|wf.grep_pythonic_words|successful |     |1643|0   |
|wf.grep_workf_words   |failed     |     |1644|1   |

And now since all entries in the execution table are in a terminal state, the workflow is finished.

## Example 2: Loops

This is a less common case, and likely will only be used in the iterative scatter-gather tasks.

```
task scatter_task {
  command <<<
    egrep ^.{${Int count}}$ ${File in} || exit 0
  >>>
  output {
    Array[String] words = read_lines(stdout())
  }
}

task gather_task {
  command {
    python3 <<CODE
    import json
    with open('count', 'w') as fp:
      fp.write(str(int(${Int count}) - 1))
    with open('wc', 'w') as fp:
      fp.write(str(sum([len(x) for x in json.loads(open("${Array[Array[String]] word_lists}").read())])))
    CODE
  }
  output {
    Int count = read_int("count")
  }
}

workflow wf {
  Array[File] files
  Int count

  while(count > 3) {
    scatter(filename in files) {
      call scatter_task {
        input: in=filename, count=count
      }
    }
    call gather_task {
      input: count=count, word_lists=scatter_task.words
      output: count=count
    }
  }
}
```

If we run the task specifying the value for the two required parameters as:

|Parameter|Value                           |
|---------|--------------------------------|
|wf.files |["test/languages", "test/words"]|
|wf.count |6                               |

In this example, the file `test/languages` contains:

```
c
python
java
c++
js
scala
d
c#
objective-c
php
vb
sql
R
shell
lisp
```

and `test/words` contains:

```
ace
act
bad
bag
cage
cake
call
doggy
daily
dairy
```

**Symbol Table Construction**

The symbol table starts out with the following values defined as a combination of initialized values and user-provided values

|Name                         |Value                           |Type                |I/O   |
|-----------------------------|--------------------------------|--------------------|------|
|wf.files                     |['test/languages', 'test/words']|Array[File]         |input |
|wf.count                     |6                               |Int                 |input |
|wf._w5._s6.filename          |%ref:wf.files                   |Array[File]         |input |
|wf._w5._s6.scatter_task.count|%ref:wf.count                   |String              |input |
|wf._w5._s6.scatter_task.in   |%ref:wf._w5._s6.filename        |File                |input |
|wf._w5._s6.scatter_task.words|                                |Array[Array[String]]|output|
|wf._w5.gather_task.count     |%ref:wf.count                   |Int                 |input |
|wf._w5.gather_task.word_lists|%expr:scatter_task.words        |Array[Array[String]]|input |
|wf._w5.gather_task.count     |%ref:wf.count                   |Int                 |output|

The fully qualified names in this symbol table also include the scopes that a `call` lives inside.  `_s6` refers to a scatter block with an arbitrary unique ID of 6.  `_w5` refers to a while loop with arbitrary unique ID of 5.

If `scatter_task` were not being executed inside of a scatter block, the output (`wf._w5._s6.scatter_task.words`) would only be of type `Array[String]`, but any task executed in a scatter block will have all of its outputs in an array (one entry for each scatter).  This is why `wf._w5._s6.scatter_task.words` has type `Array[Array[String]]`.  Since the scatter and gather steps are inside of a loop, the entries that exist initially in the symbol table are only place holders that will be copied for each iteration.

**Execution Table Construction**

With this particular task, all of the calls happen inside of the loop.  Since we don't know initially if the loop will be executed even once (we might not run `scatter_task` or `gather_task` even once) based on what the loop condition evaluates to.  Because of this, only one entry exists in the execution table initially, and that entry is for the loop itself.

|Name  |Status     |Index|Iter|PID |rc  |
|------|-----------|-----|----|----|----|
|wf._w5|not_started|     |0   |    |    |

Every time the execution table is evaluated (for example, by polling or on an event), the loop table is also evaluated.  The loop's condition is evaluated under the following circumstance:

1.  Execution Table status for the loop is `not_started` AND iteration == 0
2.  Execution Table status for the loop is `running` AND iteration > 0 AND all entries in the execution table for the current iteration are `successful`

If either of these conditions is met, the loop is looked up and the condition evaluated.  The following actions take place based on the evaluation of the loop condition:

* Condition evalutes to `undefined`: this means one of the variables referenced in the conditional is undefined.
  * Do nothing in this case.  It should never be the case that a condition evaluates to `true` or `false` on one pass and then `undefined` on subsequent pass.
* Condition evaluates to `true`:
  * Increment the iteration field on the execution table.
  * Set status to `running` on the execution table for this loop, if it's not already set.
  * Add all child nodes of the loop to the execution table and symbol table with a suffix of `._i1` where the number at the end is the current iteration number.  They should be in state `not_started`.  If any child nodes of the loop are themselves loops, add those to the control flow table.
* Condition evaluates to `false`:
  * Mark the loop in the execution table as `successful`

If the loop is `running` in the execution table, but any of the tasks in the current iteration is NOT `successful`, then mark the loop as `failed` which will prevent any further iterations.  Let any tasks that are not in a terminal state finish.

After the tables are constructed, since the loop is `not_started` and the iteration count is 0, the condition is evaluated.  The condition is `count > 3`, which is looked up in the symbol table and has a value of `true`.  Therefore:

* Increment iteration value to 1
* Set status to `running`
* Add nodes to the symbol table and execution table for this iteration

**Symbol Table**

|Name                             |Value                           |Type                |I/O   |
|---------------------------------|--------------------------------|--------------------|------|
|wf.files                         |['test/languages', 'test/words']|Array[File]         |input |
|wf.count                         |6                               |Int                 |input |
|wf._w5._s6.filename              |%ref:wf.files                   |Array[File]         |input |
|wf._w5._s6.scatter_task.count    |%ref:wf.count                   |String              |input |
|wf._w5._s6.scatter_task.in       |%ref:wf._w5._s6.filename        |file                |input |
|wf._w5._s6.scatter_task.words    |                                |Array[Array[String]]|output|
|wf._w5.gather_task.count         |%ref:wf.count                   |Int                 |input |
|wf._w5.gather_task.word_lists    |%expr:scatter_task.words        |Array[Array[String]]|input |
|wf._w5.gather_task.count         |%ref:wf.count                   |Int                 |output|
|wf._w5._s6.scatter_task._i1.count|%ref:wf.count                   |String              |input |
|wf._w5._s6.scatter_task._i1.in   |%ref:wf._w5._s6.filename        |file                |input |
|wf._w5._s6.scatter_task._i1.words|                                |Array[Array[String]]|output|
|wf._w5.gather_task._i1.count     |%ref:wf.count                   |Int                 |input |
|wf._w5.gather_task._i1.word_lists|%expr:scatter_task.words        |Array[Array[String]]|input |
|wf._w5.gather_task._i1.count     |%ref:wf.count                   |Int                 |output|

**Execution Table**

|Name                       |Status     |Index|Iter|PID |rc  |
|---------------------------|-----------|-----|----|----|----|
|wf._w5                     |started    |     |1   |    |    |
|wf._w5._s6.scatter_task._i1|not_started|0    |    |    |    |
|wf._w5._s6.scatter_task._i1|not_started|1    |    |    |    |
|wf._w5.gather_task._i1     |not_started|     |    |    |    |

When the workflow engine then evaluates the execution table again, it sees that both entries for `wf._w5._s6.scatter_task._i1` are ready to run.

The workflow engine then runs the commands for the two `scatter_task` calls in the current iteration:

```
egrep ^.{6}$ test/languages || exit 0
```

```
egrep ^.{6}$ python/test/words || exit 0
```

**Symbol Table**

|Name                             |Value                           |Type                |I/O   |
|---------------------------------|--------------------------------|--------------------|------|
|wf.files                         |['test/languages', 'test/words']|Array[File]         |input |
|wf.count                         |6                               |Int                 |input |
|wf._w5._s6.filename              |%ref:wf.files                   |Array[File]         |input |
|wf._w5._s6.scatter_task.count    |%ref:wf.count                   |String              |input |
|wf._w5._s6.scatter_task.in       |%ref:wf._w5._s6.filename        |file                |input |
|wf._w5._s6.scatter_task.words    |                                |Array[Array[String]]|output|
|wf._w5.gather_task.count         |%ref:wf.count                   |Int                 |input |
|wf._w5.gather_task.word_lists    |%expr:scatter_task.words        |Array[Array[String]]|input |
|wf._w5.gather_task.count         |%ref:wf.count                   |Int                 |output|
|wf._w5._s6.scatter_task._i1.count|%ref:wf.count                   |String              |input |
|wf._w5._s6.scatter_task._i1.in   |%ref:wf._w5._s6.filename        |file                |input |
|wf._w5._s6.scatter_task._i1.words|[['python'], []]                |Array[Array[String]]|output|
|wf._w5.gather_task._i1.count     |%ref:wf.count                   |Int                 |input |
|wf._w5.gather_task._i1.word_lists|%expr:scatter_task.words        |Array[Array[String]]|input |
|wf._w5.gather_task._i1.count     |%ref:wf.count                   |Int                 |output|

The only thing that changed was a new value for `wf._w5._s6.scatter_task._i1.words`

**Execution Table**

|Name                       |Status     |Index|Iter|PID  |rc  |
|---------------------------|-----------|-----|----|-----|----|
|wf._w5                     |started    |     |1   |     |    |
|wf._w5._s6.scatter_task._i1|successful |0    |    |47844|0   |
|wf._w5._s6.scatter_task._i1|successful |1    |    |47846|0   |
|wf._w5.gather_task._i1     |not_started|     |    |     |    |

Then, the `gather_task` step is ready because the value for `wf._w5._s6.scatter_task._i1.words` is now populated, so the engine runs the command:

```
python3 <<CODE
import json
with open('count', 'w') as fp:
  fp.write(str(int(6) - 1))
with open('wc', 'w') as fp:
  fp.write(str(sum([len(x) for x in json.loads(open("word_lists.json").read())])))
CODE
```

Notice here that the `${Array[Array[String]] word_lists}` parameter is serialized in JSON and the value is a path to the JSON file: `open("word_lists.json").read()`.

The resulting symbol table and execution table looks as follows:

**Symbol Table**

|Name                             |Value                           |Type                |I/O   |
|---------------------------------|--------------------------------|--------------------|------|
|wf.files                         |['test/languages', 'test/words']|Array[File]         |input |
|wf.count                         |5                               |Int                 |input |
|wf._w5._s6.filename              |%ref:wf.files                   |Array[File]         |input |
|wf._w5._s6.scatter_task.count    |%ref:wf.count                   |String              |input |
|wf._w5._s6.scatter_task.in       |%ref:wf._w5._s6.filename        |file                |input |
|wf._w5._s6.scatter_task.words    |                                |Array[Array[String]]|output|
|wf._w5.gather_task.count         |%ref:wf.count                   |Int                 |input |
|wf._w5.gather_task.word_lists    |%expr:scatter_task.words        |Array[Array[String]]|input |
|wf._w5.gather_task.count         |%ref:wf.count                   |Int                 |output|
|wf._w5._s6.scatter_task._i1.count|%ref:wf.count                   |String              |input |
|wf._w5._s6.scatter_task._i1.in   |%ref:wf._w5._s6.filename        |file                |input |
|wf._w5._s6.scatter_task._i1.words|[['python'], []]                |Array[Array[String]]|output|
|wf._w5.gather_task._i1.count     |%ref:wf.count                   |Int                 |input |
|wf._w5.gather_task._i1.word_lists|%expr:scatter_task.words        |Array[Array[String]]|input |
|wf._w5.gather_task._i1.count     |%ref:wf.count                   |Int                 |output|

**Execution Table**

|Name                       |Status    |Index|Iter|PID  |rc  |
|---------------------------|----------|-----|----|-----|----|
|wf._w5                     |started   |     |1   |     |    |
|wf._w5._s6.scatter_task._i1|successful|0    |    |47844|0   |
|wf._w5._s6.scatter_task._i1|successful|1    |    |47846|0   |
|wf._w5.gather_task._i1     |successful|     |    |47848|0   |

After two more iterations, when count is 3 and the loop condition evaluates to `false`, the final symbol table and execution table:

**Symbol Table**

|Name                             |Value                                            |Type                |I/O   |
|---------------------------------|-------------------------------------------------|--------------------|------|
|wf.files                         |['test/languages', 'test/words']                 |Array[File]         |input |
|wf.count                         |3                                                |Int                 |input |
|wf._w5._s6.filename              |%ref:wf.files                                    |Array[File]         |input |
|wf._w5._s6.scatter_task.count    |%ref:wf.count                                    |String              |input |
|wf._w5._s6.scatter_task.in       |%ref:wf._w5._s6.filename                         |file                |input |
|wf._w5._s6.scatter_task.words    |                                                 |Array[Array[String]]|output|
|wf._w5.gather_task.count         |%ref:wf.count                                    |Int                 |input |
|wf._w5.gather_task.word_lists    |%expr:scatter_task.words                         |Array[Array[String]]|input |
|wf._w5.gather_task.count         |%ref:wf.count                                    |Int                 |output|
|wf._w5._s6.scatter_task._i1.count|%ref:wf.count                                    |String              |input |
|wf._w5._s6.scatter_task._i1.in   |%ref:wf._w5._s6.filename                         |file                |input |
|wf._w5._s6.scatter_task._i1.words|[['python'], []]                                 |Array[Array[String]]|output|
|wf._w5.gather_task._i1.count     |%ref:wf.count                                    |Int                 |input |
|wf._w5.gather_task._i1.word_lists|%expr:scatter_task.words                         |Array[Array[String]]|input |
|wf._w5.gather_task._i1.count     |%ref:wf.count                                    |Int                 |output|
|wf._w5._s6.scatter_task._i2.count|%ref:wf.count                                    |String              |input |
|wf._w5._s6.scatter_task._i2.in   |%ref:wf._w5._s6.filename                         |file                |input |
|wf._w5._s6.scatter_task._i2.words|[['scala', 'shell'], ['doggy', 'daily', 'dairy']]|Array[Array[String]]|output|
|wf._w5.gather_task._i2.count     |%ref:wf.count                                    |Int                 |input |
|wf._w5.gather_task._i2.word_lists|%expr:scatter_task.words                         |Array[Array[String]]|input |
|wf._w5.gather_task._i2.count     |%ref:wf.count                                    |Int                 |output|
|wf._w5._s6.scatter_task._i3.count|%ref:wf.count                                    |String              |input |
|wf._w5._s6.scatter_task._i3.in   |%ref:wf._w5._s6.filename                         |file                |input |
|wf._w5._s6.scatter_task._i3.words|[['java', 'lisp'], ['cage', 'cake', 'call']]     |Array[Array[String]]|output|
|wf._w5.gather_task._i3.count     |%ref:wf.count                                    |Int                 |input |
|wf._w5.gather_task._i3.word_lists|%expr:scatter_task.words                         |Array[Array[String]]|input |
|wf._w5.gather_task._i3.count     |%ref:wf.count                                    |Int                 |output|

**Execution Table**

|Name                       |Status    |Index|Iter|PID  |rc  |
|---------------------------|----------|-----|----|-----|----|
|wf._w5                     |successful|     |3   |     |    |
|wf._w5._s6.scatter_task._i1|successful|0    |    |47844|0   |
|wf._w5._s6.scatter_task._i1|successful|1    |    |47846|0   |
|wf._w5.gather_task._i1     |successful|     |    |47848|0   |
|wf._w5._s6.scatter_task._i2|successful|0    |    |47850|0   |
|wf._w5._s6.scatter_task._i2|successful|1    |    |47852|0   |
|wf._w5.gather_task._i2     |successful|     |    |47854|0   |
|wf._w5._s6.scatter_task._i3|successful|0    |    |47856|0   |
|wf._w5._s6.scatter_task._i3|successful|1    |    |47858|0   |
|wf._w5.gather_task._i3     |successful|     |    |47860|0   |

## Example 3: Nested Scatter

```
task wc {
  command {
    echo "${str}" | wc -c
  }
  output {
    Int count = read_int(stdout()) - 1
  }
}

workflow wf {
  Array[Array[Array[String]]] triple_array
  scatter(double_array in triple_array) {
    scatter(single_array in double_array) {
      scatter(item in single_array) {
        call wc{input: str=item}
      }
    }
  }
}
```

The only input to this workflow is `triple_array`:

|Variable       |Value                                                               |
|---------------|--------------------------------------------------------------------|
|wf.triple_array|[[["0","1"],["9","10"]],[["a","b"],["c","d"]],[["w","x"],["y","z"]]]|

The initial symbol table and execution table would look as follows:

**Symbol Table**

|Name                   |Value                                                           |Type                       |I/O   |
|-----------------------|----------------------------------------------------------------|---------------------------|------|
|wf.triple_array        |[[['0', '1'], ['9', '10']], [['a', 'b'], ['c', 'd']], [['w', ...|Array[Array[Array[String]]]|input |
|wf._s3.double_array    |%ref:wf.triple_array                                            |Array[Array[Array[String]]]|input |
|wf._s3._s5.single_array|%flatten:1:wf.triple_array                                      |Array[Array[String]]       |input |
|wf._s3._s5._s7.item    |%flatten:2:wf.triple_array                                      |Array[String]              |input |
|wf._s3._s5._s7.wc.str  |%ref:wf._s3._s5._s7.item                                        |String                     |input |
|wf._s3._s5._s7.wc.count|                                                                |Array[Int]                 |output|

**Execution Table**

|Name             |Status     |Index|Iter|PID |rc  |
|-----------------|-----------|-----|----|----|----|
|wf._s3._s5._s7.wc|not_started|0    |    |    |    |
|wf._s3._s5._s7.wc|not_started|1    |    |    |    |
|wf._s3._s5._s7.wc|not_started|2    |    |    |    |
|wf._s3._s5._s7.wc|not_started|3    |    |    |    |
|wf._s3._s5._s7.wc|not_started|4    |    |    |    |
|wf._s3._s5._s7.wc|not_started|5    |    |    |    |
|wf._s3._s5._s7.wc|not_started|6    |    |    |    |
|wf._s3._s5._s7.wc|not_started|7    |    |    |    |
|wf._s3._s5._s7.wc|not_started|8    |    |    |    |
|wf._s3._s5._s7.wc|not_started|9    |    |    |    |
|wf._s3._s5._s7.wc|not_started|10   |    |    |    |
|wf._s3._s5._s7.wc|not_started|11   |    |    |    |

Notice the `%flatten:2:wf.triple_array` directives.  This represents a lazy evaluation of a list flattening operation with the second parameter representing the number of times to flatten the referenced array.  This operation is evaluated when the value for this symbol is requested (see symbol table below)

This workflow then runs these 12 steps in parallel and then the workflow is completed when they all reach terminal states.  The final symbol table and execution table looks as follows:

**Symbol Table**

|Name                   |Value                                                           |Type                       |I/O   |
|-----------------------|----------------------------------------------------------------|---------------------------|------|
|wf.triple_array        |[[['0', '1'], ['9', '10']], [['a', 'b'], ['c', 'd']], [['w', ...|Array[Array[Array[String]]]|input |
|wf._s3.double_array    |%ref:wf.triple_array                                            |Array[Array[Array[String]]]|input |
|wf._s3._s5.single_array|%flatten:1:wf.triple_array                                      |Array[Array[String]]       |input |
|wf._s3._s5._s7.item    |['0', '1', '9', '10', 'a', 'b', 'c', 'd', 'w', 'x', 'y', 'z']   |Array[String]              |input |
|wf._s3._s5._s7.wc.str  |%ref:wf._s3._s5._s7.item                                        |String                     |input |
|wf._s3._s5._s7.wc.count|[1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1]                            |Array[Int]                 |output|

**Execution Table**

|Name             |Status    |Index|Iter|PID  |rc  |
|-----------------|----------|-----|----|-----|----|
|wf._s3._s5._s7.wc|successful|0    |    |48868|0   |
|wf._s3._s5._s7.wc|successful|1    |    |48871|0   |
|wf._s3._s5._s7.wc|successful|2    |    |48874|0   |
|wf._s3._s5._s7.wc|successful|3    |    |48877|0   |
|wf._s3._s5._s7.wc|successful|4    |    |48880|0   |
|wf._s3._s5._s7.wc|successful|5    |    |48883|0   |
|wf._s3._s5._s7.wc|successful|6    |    |48886|0   |
|wf._s3._s5._s7.wc|successful|7    |    |48889|0   |
|wf._s3._s5._s7.wc|successful|8    |    |48892|0   |
|wf._s3._s5._s7.wc|successful|9    |    |48895|0   |
|wf._s3._s5._s7.wc|successful|10   |    |48898|0   |
|wf._s3._s5._s7.wc|successful|11   |    |48901|0   |

## Example 4: Nested Workflows and Scope

```
task task1 {
  command {sh script.sh}
  output{file out = stdout()}
}

task task2 {
  command {sh script.sh ${File x} ${File y}}
}

workflow wf {
  call task1

  workflow nested {
    File a_file
    call task2 as alias1 {input: x=task1.out, y=a_file}

    workflow nested2 {
      File b_file
      call task2 as alias2 {input: x=a_file, y=b_file}
    }

    # Can't do this
    call task2 as alias3 {input: x=b_file, y=a_file}
  }
}
```

**Symbol Table**

|Variable                                   |Value                                     |
|-------------------------------------------|------------------------------------------|
|nested.a_file                              |/path/to/a_file                           |
|nested2.b_file                             |/path/to/b_file                           |

## Example 5: Workflow scattering

```
task prepare_task {
  command {
    sh prepare.sh ${a} ${b} ${c}
  }
  output {
    Array[String] intervals = read_lines(stdout())
  }
}

task scatter_task {
  command {
    sh scatter.sh ${File bam} --interval ${Interval}
  }
  output {
    File vcf = "output.vcf"
  }
}

task gather_task {
  command {
    sh gather.sh ${Array[File] vcfs}
  }
}

workflow wf {
  call prepare_task
  scatter(interval in prepare_task.intervals) {
    call scatter_task{input: interval=interval}
  }
  call gather_task
}
```

## Example 6: Workflow Outputs

```
task cut_sh {
  command {
    sh cut-to-two.sh ${File tsv_file} ${'-n ' lines?}
  }
  output {
    File out1 = "col1.tsv"
    File out2 = "col2.tsv"
  }
}

task grep {
  command {
    grep some_pattern ${File file1} > grep-output.tsv
  }
  output {
    File grepped = "grep-output.tsv"
  }
}

workflow cut_grep {
  call cut_sh
  call grep {input:file1=cut_sh.out2}
  output {
    grep.*, cut_sh.out1
  }
}
```

## Example 7: Output a Map

Task that operates on a file that's a map of string->file (sample_id -> clean_bam_file)

```
task map-test {
  command { sh foobar.sh ${Map[String, file] in} > something.tsv }
  output { Map[String, Int] out = "something.tsv" }
}
```

# Notes & Things to Clarify

## Workflow output syntax

See [corresponding section](#outputs) for details

## public/private -or- export statements

We need a way to declare which parts of a WDL file are exported and which parts are private

Perhaps a NodeJS-like model of explicit exports:

```
export (task1, task2, wf)
```

Perhaps assume that everything that isn't marked public is automatically private?

```
task t1 {...}
task t2 {...}
public wf my_wf {...}
```

## Seven Bridges Considerations

1) Dependencies on ports in addition to dependencies on tasks (e.g. ps.procs instead of just ps)
2) Defining engine behavior around setting current working directory for tasks.  Dir must be empty, task writes outputs to directory, support relative paths.  Absolute paths may work, engine specific.
3) Enumerating success return codes?  Wrapper script?  extra definition on the task?  Special output mapping (Int rc = ...)?
4) Defining objects (class Sample...)
5) Heterogeneous arrays
6) Supplying values from an object onto the command line
    - Sample s; ${s.id} ${s.bam}; ???
    - Array[Sample] a; ${a.join(', ')}; ???
7) What about files that travel together, like .bam and .bai files?
8) "docker" runtime format
9) Expressions in runtime section
10) Specifying environment variables and assembling / localizing a configuration file (e.g. in /etc)

## Various loop issues

* What if another downstream task sets a variable used in the loop expression?  How do we know when we're *really* done executing the loop?
  * Solution: variables in the loop condition may only be set from within the loop otherwise it's a syntax error
* What if variables in the condition is initialized but nothing inside the loop changes the var?
  * Solution: Check that **exactly one** task inside the loop sets at least one variable in the loop condition -or- don't check and let it either infinitely loop or set a max iteration amount
* What if there's a completely stand-alone task inside a loop?
  * Solution: This task would be pointless because it'd always run with the same inputs.  This should be an error
* How are loop conditions evaluated?
  * Should return one of three values: `undefined` when one of the variables is undefined, or `true` or `false` if everything is defined.


## Explicit vs. Implicit output mappings

Problem:  It's not obvious from this output mapping if it should parse it as TSV or JSON:

```
Map[String, String] my_var = stdout()
```

We could just say "all outputs for a task must use the exact same serialization method".

Though, the more I play around with this syntax the more I don't like the implicit nature of it.

* The syntax doesn't guide the user well.  It's a convention, and not an obvious one.
* It *looks* like a type mismatch
* Trying to do something like `Map[String, String] my_var = subdir + "my_output"` looks more like a type mismatch.

Since function calls are *very* easily supported in WDL, I propose going back to two built-in functions: `tsv()` and `json()`

* `Map[String, String] blah = tsv(subdir + "somefile.tsv")`
* `Array[File] out = json(stdout())`

What about reading primitives from files?

* `int c = stdout()`
* `int c = read_int(stdout())`

## Additional Syntax Checks

* One `command` section
* `sep` is specified if postfix quantifier is a `+` or `*`
* Scatter block must contain at least one task that uses the iteration variable
  * If it doesn't, it must depend on something that does.
* A loop expression can not be statically 'true' (e.g. `true`, `1==1`, etc) or else this is an infinite loop by definition.
* A loop must be able to modify the condition.  One of the outputs of one of the tasks must alter one of the identifiers in the loop condition
* No circular dependencies?
* Tasks outside of the loop cannot set a variable defined in the loop.

# Implementations

Current implementations of the workflow description language description:

* [Reference implementation (Python)](python/)
