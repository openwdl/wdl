# Workflow Description Language (WDL)

WDL is a workflow language meant to be read and written by humans.

The Workflow Description Language project provides a

* [Draft 1 Language Specification](https://github.com/broadinstitute/wdl/blob/master/SPEC.md) (closed)
* [Draft 2 Language Specification](https://github.com/broadinstitute/wdl/blob/develop/SPEC.md) (open)

for WDL as well as Parsers in [Java](java) and Python using [PyWDL](https://github.com/broadinstitute/pywdl).

For an implementation of an engine that can run WDL, try [Cromwell](http://github.com/broadinstitute/cromwell)

<!---toc start-->

* [Workflow Description Language (WDL)](#workflow-description-language-wdl)
* [Overview](#overview)
* [Getting Started with WDL](#getting-started-with-wdl)
  * [Hello World WDL](#hello-world-wdl)
  * [Modifying Task Outputs](#modifying-task-outputs)
  * [Referencing Files on Disk](#referencing-files-on-disk)
  * [Using Globs to Specify Output](#using-globs-to-specify-output)
  * [Using String Interpolation](#using-string-interpolation)
  * [Aliasing Calls](#aliasing-calls)
  * [Specifying Inputs and Using Declarations](#specifying-inputs-and-using-declarations)
  * [Using Files as Inputs](#using-files-as-inputs)
  * [Scatter/Gather](#scattergather)

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

We'll use Cromwell to run these examples but you can use any WDL engine of your choice. If you don't already have a reference to the Cromwell JAR file, one can be [downloaded](https://github.com/broadinstitute/cromwell/releases)

## Hello World WDL

Create a WDL simple file and save it as `hello.wdl`, for example:

```wdl
task hello {
  String name

  command {
    echo 'hello ${name}!'
  }
  output {
    File response = stdout()
  }
}

workflow test {
  call hello
}
```

Generate a template `hello.json` file with the `inputs` subcommand:

```
$ java -jar cromwell.jar inputs hello.wdl
{
  "test.hello.name": "String"
}
```

WDL has a concept of fully-qualified names.  In the above output, `test.hello.name` is a fully-qualified name which should be read as: the `name` input on the `hello` call within workflow `test`.  Fully-qualified names are used to unambiguously refer to specific elements of a workflow.  All inputs are specified by fully-qualified names and all outputs are returned as fully-qualified names.

Modify this and save it to `hello.json`:

```
{
  "test.hello.name": "world"
}
```

Then, use the `run` subcommand to run the workflow:

```
$ java -jar cromwell.jar run hello.wdl hello.json
... truncated ...
{
  "test.hello.response": "/home/user/test/c1d15098-bb57-4a0e-bc52-3a8887f7b439/call-hello/stdout8818073565713629828.tmp"
}
```

Since the `hello` task returns a `File`, the result is a file that contains the string "hello world!" in it.

## Modifying Task Outputs

Currently the `hello` task returns a `File` with the greeting in it, but what if we wanted to return a `String` instead?
 This can be done by utilizing the `read_string()` function:

```wdl
task hello {
  String str
  command {
    echo 'hello ${name}!'
  }
  output {
    String response = read_string(stdout())
  }
}

workflow test {
  call hello
}
```

Now when this is run, we get the string output for `test.hello.response`:

```
$ java -jar cromwell.jar run hello.wdl hello.json
... truncated ...
{
  "test.hello.response": "Hello world!"
}
```

`read_string` is a function in the [standard library](https://github.com/broadinstitute/wdl/blob/wdl2/SPEC.md#standard-library), which provides other useful functions for converting outputs to WDL data types.

## Referencing Files on Disk

So far we've only been dealing with the standard output of a command, but what if it writes a file to disk?  Consider this example:

```wdl
task hello {
  command {
    echo 'hello ${name}!' > test.out
  }
  output {
    String response = read_string("test.out")
  }
}

workflow test {
  call hello
}
```

Now when this is run, we get the string output for `test.hello.response`:

```
$ java -jar cromwell.jar run hello.wdl hello.json
... truncated ...
{
  "test.hello.response": "Hello world!"
}
```

`read_string` is a function in the [standard library](https://github.com/broadinstitute/wdl/blob/wdl2/SPEC.md#standard-library), which provides other useful functions for converting outputs to WDL data types.

## Using Globs to Specify Output

We can use the glob() function to read multiple files at once:

```wdl
task globber {
  command <<<
    for i in `seq 1 5`
    do
      mkdir out-$i
      echo "globbing is my number $i best hobby" > out-$i/$i.txt
    done
  >>>
  output {
    Array[File] outFiles = glob("out-*/*.txt")
  }
}

workflow test {
  call globber
}
```

The `outFiles` output array will contain all files found by evaluating the specified glob.

## Using String Interpolation

Sometimes, an output file is named as a function of one of its inputs.

```wdl
task hello {
  String name
  command {
    echo 'hello ${name}!' > ${name}.txt
  }
  output {
    String response = read_string("${name}.txt")
  }
}

workflow test {
  call hello
}
```

Here the inputs and outputs are exactly the same as previous examples, however the intermediate output file name of this task is named differently for every invocation.

## Aliasing Calls

Say we wanted to call the `hello` task twice.  Simply adding two `call hello` statements to the body of `workflow test` would result in non-unique fully-qualified names.  To resolve this issue, `call` statements can be aliased using an `as` clause:

```wdl
task hello {
  String name
  command {
    echo 'hello ${name}!'
  }
  output {
    String response = read_string(stdout())
  }
}

workflow test {
  call hello
  call hello as hello2
}
```

Now, we need to specify a value for `test.hello2.name` in the hello.json file"

```
{
  "test.hello.name": "world",
  "test.hello2.name": "boston"
}
```

Running this workflow now produces two outputs:

```
$ java -jar cromwell.jar run hello.wdl hello.json
... truncated ...
{
  "test.hello.response": "Hello world!",
  "test.hello2.response": "Hello boston!"
}
```

## Specifying Inputs and Using Declarations

A `call` can have an optional section to define inputs.  As seen below, the key/value pairs represent the name of the input on the left-hand side and the expression for the input's value on the right-hand side:

```wdl
task hello {
  String name
  String salutation

  command {
    echo '${salutation} ${name}!'
  }
  output {
    String response = read_string(stdout())
  }
}

workflow test {
  call hello {
    input: salutation="greetings"
  }
  call hello as hello2
}
```

Now, the `hello.json` would require three inputs:

```
{
  "test.hello.name": "world",
  "test.hello2.name": "boston",
  "test.hello2.salutation": "hello"
}
```

Running this workflow still gives us the two greetings we expect:

```
$ java -jar cromwell.jar run hello.wdl hello.json
... truncated ...
{
  "test.hello.response": "greetings world!",
  "test.hello2.response": "hello boston!"
}
```

What if we wanted to parameterize the greeting and make it used for all invocations of task `hello`?  In this situation, a declaration can be used:

```wdl
task hello {
  String salutation
  String name
  command {
    echo '${salutation}, ${name}!'
  }
  output {
    String response = read_string(stdout())
  }
}

workflow test {
  String greeting
  call hello {
    input: salutation=greeting
  }
  call hello as hello2 {
    input: salutation=greeting + " and nice to meet you"
  }
}
```

`String greeting` is referenced to satisfy the "salutation" parameter to both invocations of the `hello` task.

The inputs required to run this would be:

```
{
  "test.hello.name": "world",
  "test.hello2.name": "boston",
  "test.greeting": "hello"
}
```

And this would produce the following outputs when run

```
$ java -jar cromwell.jar run hello.wdl hello.json
... truncated ...
{
  "test.hello.response": "hello, world!",
  "test.hello2.response": "hello and nice to meet you, boston!"
}
```

## Using Files as Inputs

So far every example has used the default type of `String` for every input.  Passing files along to tasks is simply a matter of defining the input type as `File`:

```wdl
task grep {
  File file

  command {
    grep -c '^...$' ${file}
  }
  output {
    Int count = read_int(stdout())
  }
}

workflow test {
  call grep
}
```

The `read_int()` function here would read the contents of its parameter, and interpret the first line as an integer and return that value as a WDL `Int` type.

If I specified a file called `test_file` with the contents of:

```
foo
bar
baz
quux
```

And then the inputs JSON file would be:

```
{
  "test.grep.file": "test_file"
}
```

The result of running this would be:

```
$ java -jar cromwell.jar run grep.wdl grep.json
... truncated ...
{
  "test.grep.count": 3
}
```

## Scatter/Gather

Scatter blocks can be used to run the same call multiple times but only varying a specific parameter on each invocation.  Consider the following example:

```wdl
task prepare {
  command <<<
    python -c "print('one\ntwo\nthree\nfour')"
  >>>
  output {
    Array[String] array = read_lines(stdout())
  }
}

task analysis {
  String str
  command <<<
    python -c "print('_${str}_')"
  >>>
  output {
    String out = read_string(stdout())
  }
}

task gather {
  Array[String] array
  command <<<
    echo ${sep=' ' array}
  >>>
  output {
    String str = read_string(stdout())
  }
}

workflow example {
  call prepare
  scatter (x in prepare.array) {
    call analysis {input: str=x}
  }
  call gather {input: array=analysis.out}
}
```

This example calls the `analysis` task once for each element in the array that the `prepare` task outputs.  The resulting outputs of this workflow would be:

```
{
  "example.analysis.out": ["_one_", "_two_", "_three_", "_four_"],
  "example.gather.str": "_one_ _two_ _three_ _four_",
  "example.prepare.array": ["one", "two", "three", "four"]
}
```
