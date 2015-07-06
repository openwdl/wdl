# Workflow Description Language

## Table Of Contents

<!---toc start-->

* [Workflow Description Language](#workflow-description-language)
  * [Table Of Contents](#table-of-contents)
  * [Introduction](#introduction)
  * [State of the Specification](#state-of-the-specification)
* [Language Specification](#language-specification)
  * [Global Grammar Rules](#global-grammar-rules)
    * [Whitespace, Strings, Identifiers, Constants](#whitespace-strings-identifiers-constants)
    * [Types](#types)
    * [Declarations](#declarations)
    * [Expressions](#expressions)
    * [Operator Precedence Table](#operator-precedence-table)
    * [Member Access](#member-access)
    * [Map and Array Indexing](#map-and-array-indexing)
    * [Function Calls](#function-calls)
    * [Array Literals](#array-literals)
    * [Map Literals](#map-literals)
  * [Document](#document)
  * [Import Statements](#import-statements)
  * [Task Definition](#task-definition)
    * [Sections](#sections)
    * [Command Section](#command-section)
    * [Command Parts](#command-parts)
    * [Command Parts (alternative heredoc syntax)](#command-parts-alternative-heredoc-syntax)
    * [Command Part Options](#command-part-options)
      * [sep](#sep)
      * [true and false](#true-and-false)
      * [serialize](#serialize)
      * [default](#default)
    * [Outputs Section](#outputs-section)
    * [Runtime Section](#runtime-section)
      * [serialize](#serialize)
      * [docker](#docker)
      * [memory](#memory)
    * [Parameter Metadata Section](#parameter-metadata-section)
    * [Metadata Section](#metadata-section)
    * [Examples](#examples)
      * [Example 1: Simplest Task](#example-1-simplest-task)
      * [Example 2: Inputs/Outputs](#example-2-inputsoutputs)
      * [Example 3: Runtime/Metadata](#example-3-runtimemetadata)
      * [Example 4: BWA mem](#example-4-bwa-mem)
      * [Example 5: Word Count](#example-5-word-count)
      * [Example 6: tmap](#example-6-tmap)
  * [Workflow Definition](#workflow-definition)
    * [Call Sub-Tasks](#call-sub-tasks)
    * [Scatter](#scatter)
    * [Loops](#loops)
    * [Conditionals](#conditionals)
    * [Outputs](#outputs)
    * [Examples](#examples)
      * [Example 1: dRanger](#example-1-dranger)
* [Variable Resolution & Scoping](#variable-resolution--scoping)
* [Standard Library Functions](#standard-library-functions)
  * [mixed stdout()](#mixed-stdout)
  * [mixed stderr()](#mixed-stderr)
  * [mixed tsv(String|File|Uri)](#mixed-tsvstringfileuri)
  * [mixed json(String|File|Uri)](#mixed-jsonstringfileuri)
  * [Int read_int(String|File|Uri)](#int-read_intstringfileuri)
  * [String read_string(String|File|Uri)](#string-read_stringstringfileuri)
  * [Float read_float(String|File|Uri)](#float-read_floatstringfileuri)
  * [Boolean read_boolean(String|File|Uri)](#boolean-read_booleanstringfileuri)
* [Data Types & Serialization](#data-types--serialization)
  * [Overview](#overview)
  * [Serialization](#serialization)
    * [Serialization of Primitive Output Types](#serialization-of-primitive-output-types)
    * [Serialization of Compound Output Types](#serialization-of-compound-output-types)
  * [Primitive Types](#primitive-types)
    * [String](#string)
    * [Int and Float](#int-and-float)
    * [File and Uri](#file-and-uri)
    * [Boolean](#boolean)
  * [Compound Types](#compound-types)
    * [array](#array)
      * [array serialization by expansion](#array-serialization-by-expansion)
      * [array serialization as TSV](#array-serialization-as-tsv)
      * [array serialization as JSON](#array-serialization-as-json)
    * [map](#map)
      * [map serialization as TSV](#map-serialization-as-tsv)
      * [map serialization as JSON](#map-serialization-as-json)
    * [object](#object)
      * [object serialization as TSV](#object-serialization-as-tsv)
      * [object serialization as JSON](#object-serialization-as-json)
      * [Array\[object\]](#arrayobject)
* [Workflow Execution Algorithm](#workflow-execution-algorithm)
  * [Symbol Table Construction](#symbol-table-construction)
  * [Symbol Table Initial Population](#symbol-table-initial-population)
  * [Execution Table Construction](#execution-table-construction)
  * [Workflow Evaluation](#workflow-evaluation)
  * [Workflow Termination](#workflow-termination)
  * [Example 1: Two-step parallel workflow](#example-1-two-step-parallel-workflow)
  * [Example 2: Loops](#example-2-loops)
  * [Example 3: Nested Scatter](#example-3-nested-scatter)
  * [Example 4: Nested Workflows and Scope](#example-4-nested-workflows-and-scope)
  * [Example 5: Workflow scattering](#example-5-workflow-scattering)
  * [Example 6: Workflow Outputs](#example-6-workflow-outputs)
  * [Example 7: Output a Map](#example-7-output-a-map)
* [Notes & Things to Clarify](#notes--things-to-clarify)
  * [Workflow output syntax](#workflow-output-syntax)
  * [public/private -or- export statements](#publicprivate--or--export-statements)
  * [Various loop issues](#various-loop-issues)
  * [Explicit vs. Implicit output mappings](#explicit-vs-implicit-output-mappings)
  * [Additional Syntax Checks](#additional-syntax-checks)
* [Implementations](#implementations)

<!---toc end-->

## Introduction

WDL is meant to be a *human readable and writable* way to express tools and workflows.  The "Hello World" tool in WDL would look like this:

```
task hello {
  command {
    egrep '${pattern}' '${File in}'
  }
}
```

This describes a task, called 'hello', which has one parameter (message).  The value of the parameters (called "job parameters") is provided in a language specific way.  The reference implementation accepts the value of the parameters in JSON.  For example:

|Variable|Value    |
|--------|---------|
|pattern |^[a-z]+$ |
|in      |/file.txt|

Running the hello tool with these job parameters would yield a command line:

```
egrep '^[a-z]+$' '/file.txt'
```

A simple workflow that runs this task in parallel would look like this:

```
workflow example {
  Array[File] files
  scatter(path in files) {
    call hello {input: in=path}
  }
}
```

The inputs to this workflow would be `files` and `hello.pattern`.

## State of the Specification

This specification is still in the draft phase.  Most of the basics are fairly set in stone but there are some areas of this spec that will be changing rapidly.

Current things that are being worked out:

1.  [Loop syntax and semantics](https://groups.google.com/forum/#!topic/workflow-description-language/FvzQVOs1KFs)
2.  Expression Semantics
3.  [Workflow Output Syntax](https://groups.google.com/forum/#!topic/workflow-description-language/EE-mDCACToY)
4.  Literal syntax for Object, Array, Map, and File types
5.  Objects vs. Maps.  Should objects even exist?  How will they be specified?

# Language Specification

## Global Grammar Rules

### Whitespace, Strings, Identifiers, Constants

These are common among many of the following sections

```
$ws = (0x20 | 0x9 | 0xD | 0xA)+
$identifier = [a-zA-Z][a-zA-Z0-9_]+
$string = "[^"]" | '[^']'
$boolean = 'true' | 'false'
$integer = [1-9][0-9]*
$float = -?[0-9]*.[0-9]+
```

> **TODO**: Allow escape sequences in strings

### Types

All inputs and outputs must be typed.

```
$type = $primitive_type | $collection_type
$primitive_type = ('Boolean' | 'Int' | 'Float' | 'Uri' | 'File' | 'String' | 'Object')
$collection_type = 'Array' '[' $type ']'
$collection_type = 'Map' '[' ($primitive_type - 'object') ',' ($primitive_type - 'object') ']'
```

Some examples of types:

* `File`
* `Array[File]`
* `Map[String, String]`
* `Object`

For more information on types, see the [Data Types & Serialization](#data-types--serialization) section.

### Declarations

```
$declaration = $type $identifier ('=' $expression)?
```

Declarations are declared at the top of any [scope](#TODO).

In a [task definition](#task-definition), declarations are interpreted as inputs to the task that are not part of the command line itself.

If a declaration does not have an initialization, then the value is expected to be provided by the user before the workflow or task is run.

Some examples of declarations:

* `File x`
* `String y = "abc"`
* `Float pi = 3 + .14`
* `Map[String, String] m`

### Expressions

```
$expression = '(' $expression ')'
$expression = $expression '.' $expression
$expression = $expression '[' $expression ']'
$expression = $expression '(' ($expression (',' $expression)*)? ')'
$expression = '!' $expression
$expression = '+' $expression
$expression = '-' $expression
$expression = $expression '*' $expression
$expression = $expression '%' $expression
$expression = $expression '/' $expression
$expression = $expression '+' $expression
$expression = $expression '-' $expression
$expression = $expression '<' $expression
$expression = $expression '=<' $expression
$expression = $expression '>' $expression
$expression = $expression '>=' $expression
$expression = $expression '==' $expression
$expression = $expression '!=' $expression
$expression = $expression '&&' $expression
$expression = $expression '||' $expression
$expression = '{' ($expression ':' $expression)* '}'
$expression = '[' $expression* ']'
$expression = $string | $integer | $float | $boolean | $identifier
```

Below are the valid results for operators on types.  Any combination not in the list will result in an error.

|LHS Type   |Operators  |RHS Type         |Result   |Semantics|
|-----------|-----------|-----------------|---------|---------|
|`Boolean`|`==`|`Boolean`|`Boolean`||
|`Boolean`|`!=`|`Boolean`|`Boolean`||
|`Boolean`|`>`|`Boolean`|`Boolean`||
|`Boolean`|`>=`|`Boolean`|`Boolean`||
|`Boolean`|`<`|`Boolean`|`Boolean`||
|`Boolean`|`<=`|`Boolean`|`Boolean`||
|`Boolean`|`||`|`Boolean`|`Boolean`||
|`Boolean`|`&&`|`Boolean`|`Boolean`||
|`File`|`+`|`File`|`File`|Append file paths|
|`File`|`==`|`File`|`Boolean`||
|`File`|`!=`|`File`|`Boolean`||
|`File`|`+`|`String`|`File`||
|`File`|`==`|`String`|`Boolean`||
|`File`|`!=`|`String`|`Boolean`||
|`Float`|`+`|`Float`|`Float`||
|`Float`|`-`|`Float`|`Float`||
|`Float`|`*`|`Float`|`Float`||
|`Float`|`/`|`Float`|`Float`||
|`Float`|`%`|`Float`|`Float`||
|`Float`|`==`|`Float`|`Boolean`||
|`Float`|`!=`|`Float`|`Boolean`||
|`Float`|`>`|`Float`|`Boolean`||
|`Float`|`>=`|`Float`|`Boolean`||
|`Float`|`<`|`Float`|`Boolean`||
|`Float`|`<=`|`Float`|`Boolean`||
|`Float`|`+`|`Int`|`Float`||
|`Float`|`-`|`Int`|`Float`||
|`Float`|`*`|`Int`|`Float`||
|`Float`|`/`|`Int`|`Float`||
|`Float`|`%`|`Int`|`Float`||
|`Float`|`==`|`Int`|`Boolean`||
|`Float`|`!=`|`Int`|`Boolean`||
|`Float`|`>`|`Int`|`Boolean`||
|`Float`|`>=`|`Int`|`Boolean`||
|`Float`|`<`|`Int`|`Boolean`||
|`Float`|`<=`|`Int`|`Boolean`||
|`Float`|`+`|`String`|`String`||
|`Int`|`+`|`Float`|`Float`||
|`Int`|`-`|`Float`|`Float`||
|`Int`|`*`|`Float`|`Float`||
|`Int`|`/`|`Float`|`Float`||
|`Int`|`%`|`Float`|`Float`||
|`Int`|`==`|`Float`|`Boolean`||
|`Int`|`!=`|`Float`|`Boolean`||
|`Int`|`>`|`Float`|`Boolean`||
|`Int`|`>=`|`Float`|`Boolean`||
|`Int`|`<`|`Float`|`Boolean`||
|`Int`|`<=`|`Float`|`Boolean`||
|`Int`|`+`|`Int`|`Int`||
|`Int`|`-`|`Int`|`Int`||
|`Int`|`*`|`Int`|`Int`||
|`Int`|`/`|`Int`|`Int`|Integer division|
|`Int`|`%`|`Int`|`Int`|Integer division, return remainder|
|`Int`|`==`|`Int`|`Boolean`||
|`Int`|`!=`|`Int`|`Boolean`||
|`Int`|`>`|`Int`|`Boolean`||
|`Int`|`>=`|`Int`|`Boolean`||
|`Int`|`<`|`Int`|`Boolean`||
|`Int`|`<=`|`Int`|`Boolean`||
|`Int`|`+`|`String`|`String`||
|`String`|`+`|`Float`|`String`||
|`String`|`+`|`Int`|`String`||
|`String`|`+`|`String`|`String`||
|`String`|`==`|`String`|`Boolean`||
|`String`|`!=`|`String`|`Boolean`||
|`String`|`>`|`String`|`Boolean`||
|`String`|`>=`|`String`|`Boolean`||
|`String`|`<`|`String`|`Boolean`||
|`String`|`<=`|`String`|`Boolean`||
||`-`|`Float`|`Float`||
||`+`|`Float`|`Float`||
||`-`|`Int`|`Int`||
||`+`|`Int`|`Int`||
||`!`|`Boolean`|`Boolean`||

### Operator Precedence Table

| Precedence | Operator type         | Associativity | Example              |
|------------|-----------------------|---------------|----------------------|
| 12         | Grouping              | n/a           | (x)                  |
| 11         | Member Access         | left-to-right | x.y                  |
| 10         | Index                 | left-to-right | x[y]                 |
| 9          | Function Call         | left-to-right | x(y,z,...)           |
| 8          | Logical NOT           | right-to-left | !x                   |
|            | Unary Plus            | right-to-left | +x                   |
|            | Unary Negation        | right-to-left | -x                   |
| 7          | Multiplication        | left-to-right | x*y                  |
|            | Division              | left-to-right | x/y                  |
|            | Remainder             | left-to-right | x%y                  |
| 6          | Addition              | left-to-right | x+y                  |
|            | Subtraction           | left-to-right | x-y                  |
| 5          | Less Than             | left-to-right | x<y                  |
|            | Less Than Or Equal    | left-to-right | x<=y                 |
|            | Greater Than          | left-to-right | x>y                  |
|            | Greater Than Or Equal | left-to-right | x>=y                 |
| 4          | Equality              | left-to-right | x==y                 |
|            | Inequality            | left-to-right | x!=y                 |
| 3          | Logical AND           | left-to-right | x&&y                 |
| 2          | Logical OR            | left-to-right | x\|\|y               |
| 1          | Assignment            | right-to-left | x=y                  |

### Member Access

The syntax `x.y` refers to member access.  `x` must be an object or task in a workflow.  A Task can be thought of as an object where the attributes are the outputs of the task.

```
workflow wf {
  object obj

  # This would cause a syntax error, because task1 is defined twice
  object task1

  call task1 {
    input: var=obj.attr # Object attribute
  }
  call task2 {
    input: task1.output # Task output
  }
}
```

### Map and Array Indexing

The syntax `x[y]` is for indexing maps and arrays.  If `x` is an array, then `y` must evaluate to an integer.  If `x` is a map, then `y` must evaluate to a key in that map.

### Function Calls

Function calls, in the form of `func(p1, p2, p3, ...)`, are either [standard library functions](#standard-library-functions) or engine-defined functions.  In this current iteration of the spec, users cannot define their own functions.

### Array Literals

Arrays values can be specified using Python-like syntax, as follows:

```
Array[String] a = ["a", "b", "c"]
Array[Int] b = [0,1,2]
```

### Map Literals

Maps values can be specified using a similar Python-like sytntax:

```
Map[Int, Int] = {1: 10, 2: 11}
Map[String, Int] = {"a": 1, "b": 2}
```

## Document

```
$document = ($import | $task | $workflow)+
```

`$document` is the root of the parse tree and it consists of one or more import statement, task, or workflow definition

## Import Statements

A WDL file may contain import statements to include WDL code from other sources

```
$import = 'import' $string ('as' $identifier)?
```

The import statement specifies that `$string` which is to be interpted as a URI which points to a WDL file.  The engine is responsible for resolving the URI and downloading the contents.  The contents of the document in each URI must be WDL source code.

If a namespace identifier (via the `as $identifer` syntax) is specified, then all the tasks and workflows imported will only be accessible through that [namespace](#namespaces).  If no namespace identifier is specified, then all tasks and workflows from the URI are imported into the current namespace.

```
import "http://example.com/lib/stdlib"
import "http://example.com/lib/analysis_tasks" as analysis

workflow wf {
  File bam_file

  # file_size is from "http://example.com/lib/stdlib"
  call file_size {
    input: file=bam_file
  }
  call analysis.my_analysis_task {
    input: size=file_size.bytes, file=bam_file
  }
}
```

Engines should at the very least support the following protocols for import URIs:

* `http://` and `https://`
* `file://`
* no protocol (which should be interpreted as `file://`

## Task Definition

A task is a declarative construct with a focus on constructing a command from a template.  The command specification is interpreted in an engine specific way, though a typical case is that a command is a UNIX command line which would be run in a Docker image.

Tasks also define their outputs, which is essential for building dependencies between tasks.  Any other data specified in the task definition (e.g. runtime information and meta-data) is optional.

```
$task = 'task' $ws+ $identifier $ws* '{' $declaration* $task_sections '}'
```

For example, `task name { ... }`.  Inside the curly braces defines the sections.

### Sections

The task has one or more sections:

```
$task_sections = ($command | $runtime | $outputs | $parameter_meta | $meta)+
```

> *Additional requirement*: Exactly one `$command` section needs to be defined, preferably as the first section.

### Command Section

```
$command = 'command' $ws* '{' (0xA | 0xD)* $command_part+ $ws+ '}'
$command = 'command' $ws* '<<<' (0xA | 0xD)* $command_part+ $ws+ '>>>'
```

A command is a *task section* that starts with the keyword 'command', and is enclosed in curly braces.  The body of the command specifies the literal command line to run with placeholders (`$command_part_var`) for the parts of the command line that needs to be filled in.

### Command Parts

```
$command_part = $command_part_string | $command_part_var
$command_part_string = ^'${'+
$command_part_var = '${' $var_option* $string? $type? $identifier $postfix_quantifier? '}'
$postfix_quantifier = '?' | '+' | '*'
```

The parser should read characters from the command line until it reaches a `${` character sequence.  This is interpreted as a literal string (`$command_part_string`).

The parser should interpret any variable enclosed in `${`...`}` as a `$command_part_var`.

The `$string?` portion of `$command_part_var` is interpreted as a prefix that should be prepended to the variable if it's specified.  In the case where the parameter is required, it is better practice to keep this *outside* of the variable (e.g. `-t ${my_param}`) however, if the parameter is optional, it's necessary to keep it *inside* the variable definition to avoid a straggling flag if the parameter is not specified (e.g. `${'-t ' my_param?}`)

the `$type?` portion of `$command_part_var` is also optional, and the default is `string`.

The `$postfix_quantifier` are regular expression-like modifiers for a parameter.

* `?` means this parameter is optional
* `+` and `*` mean that this parameter can accept 1 or more, or 0 or more (respectively) values.  If one value is given it is treated as normal.  If an *array* of values is passed in then the values are joined together using the 'sep' field in `$var_option`

> *Additional requirement*: If `$postfix_quantifier` is either `+` or `*`, 'sep' must be set for `$var_option`

```
grep '${start}...${end}' ${File input}
```

This command would be parsed as:

* `grep '` - command_part_string
* `${start}` - command_part_var
* `...` - command_part_string
* `${end}` - command_part_var
* `' ` - command_part_string
* `${File input}` - command_part_var


### Command Parts (alternative heredoc syntax)

Sometimes a command is sufficiently long enough or might use `{` characters that using a different set of delimiters would make it more clear.  In this case, enclose the command in `<<<`...`>>>`, as follows:

```
task heredoc {
  command<<<
  python <<CODE
    with open("${File in}") as fp:
      for line in fp:
        if not line.startswith('#'):
          print(line.strip())
  CODE
  >>>
  }
}
```

Parsing of this command should be the same as the prior section describes.

> **Note**: the parser should strip any whitespace common to each line in the command.  In the example above, 2 characters should be stripped from the beginning of each line.

### Command Part Options

```
$var_option = $var_option_key $ws* '=' $ws* $var_option_value
$var_option_key = 'sep' | 'true' | 'false' | 'serialize' | 'quote' | 'default'
$var_option_value = $expression
```

The `$var_option` is a set of key-value pairs for any additional and less-used options that need to be set on a parameter.

#### sep

'sep' is interpreted as the separator string used to join multiple parameters together.  For example, passing the list `[1,2,3]` as a parameter to the command `python script.py ${sep=',' Int numbers+}` would yield the command line:

```
python script.py 1,2,3
```

Alternatively, if the command were `python script.py ${sep=' ' Int numbers+}` it would parse to:

```
python script.py 1 2 3
```

> *Additional Requirements*:
>
> 1.  sep MUST accept only a string as its value
> 2.  sep MUST be set if the postfix quantifier is `+` or `*`

#### true and false

'true' and 'false' are only used for type Boolean and they specify what the parameter returns when the Boolean is true or false, respectively.

For example, `${true='--enable-foo', false='--disable-foo' Boolean yes_or_no}` would evaluate to either `--enable-foo` or `--disable-foo` based on the value of yes_or_no.

If either value is left out, then it's equivalent to specifying the empty string.  If the parameter is `${true='--enable-foo' Boolean yes_or_no}`, and a value of false is specified for this parameter, then the parameter will evaluate to the empty string.

> *Additional Requirement*:
>
> 1.  `true` and `false` values MUST be strings.
> 2.  `true` and `false` are only allowed if the type is `Boolean`

#### serialize

'serialize' expresses how this parameter expects its input to be serialized.  For compound types, the value for this key is the serialization format (e.g. `json`, `tsv`).  A default may be set at the task level under the runtime section.

> *Additional Requirement*: if serialize is specified, the type MUST be a compound type (e.g. `array`, `map`).  Valid values for this parameter are implementation specific but `json` and `tsv` MUST be allowed.

#### default

This specifies the default value if no other value is specified for this parameter.

> *Additional Requirements*:
>
> 1.  The type of the expression must match the type of the parameter
> 2.  If 'default' is specified, the `$postfix_quantifier` MUST be `?`

### Outputs Section

The outputs section defines which of the files and values should be exported after a successful run of this tool.

```
$outputs = 'outputs' $ws* '{' ($ws* $output_kv $ws*)* '}'
$output_kv = $type $identifier $ws* '=' $ws* $string
```

The outputs section contains typed variable definitions and a binding to the variable that they export.

The left-hand side of the equality defines the type and name of the output.

The right-hand side defines the path to the file that contains that variable definition.

For example, if a task's output section looks like this:

```
output {
  Int threshold = "threshold.txt"
}
```

Then the task is expecting a file called "threshold.txt" in the current working directory where the task was executed.  Inside of that file must be one line that contains only an integer and whitespace.  See the [Data Types & Serialization](#data-types--serialization) section for more details.

The filename strings may also contain variable definitions themselves:

```
output {
  Array[String] quality_scores = "${sample_id}.scores.txt"
}
```

If this is the case, then `sample_id` is considered an input to the task.

> *Additional requirement*: Any variable in the filename string MUST be of type string.

Finally, glob-style `*` may be used in the filename.  The glob may only match more than 1 file if the output is of type `array`

### Runtime Section

```
$runtime = 'runtime' $ws* '{' ($ws* $runtime_kv $ws*)* '}'
$runtime_kv = $identifier $ws* '=' $ws* $string
```

The runtime section defines key/value pairs for runtime information needed for this task.  Values are only interpreted by execution backends and will be stored as raw strings until that point. Individual backends will define which keys they will inspect so a key/value pair may or may not actually be honored depending on how the task is run.

While the key/value pairs are arbitrary, but a few of them have special meaning:

#### serialize

Can contain values `json`, `tsv`, or any implementation specific values.

This value specifies the default serialization method for inputs and outputs of this task.  See the section on [Data Types & Serialization](#data-types--serialization) for more information.


#### docker

Location of a Docker image for which this task ought to be run

> **TODO**: What is the actual format of the docker field?  URI?

#### memory

Memory requirements for this task.  This should be an integer value with suffixes like `B`, `KB`, `MB`, ... or binary suffixes `KiB`, `MiB`, ...


### Parameter Metadata Section

```
$parameter_meta = 'parameter_meta' $ws* '{' ($ws* $parameter_meta_kv $ws*)* '}'
$parameter_meta_kv = $identifier $ws* '=' $ws* $string
```

This purely optional section contains key/value pairs where the keys are names of parameters and the values are string descriptions for those parameters.

> *Additional requirement*: Any key in this section MUST correspond to a parameter in the command line

### Metadata Section

```
$meta = 'meta' $ws* '{' ($ws* $meta_kv $ws*)* '}'
$meta_kv = $identifier $ws* '=' $ws* $string
```

This purely optional section contains key/value pairs for any additional meta data that should be stored with the task.  For example, perhaps author or contact email.

### Examples

#### Example 1: Simplest Task

```
task hello_world {
  command {echo hello world}
}
```

#### Example 2: Inputs/Outputs

```
task one_and_one {
  command {
    grep ${pattern} ${File infile}
  }
  output {
    File filtered = stdout()
  }
}
```

#### Example 3: Runtime/Metadata

```
task runtime_meta {
  command {
    java -Xmx${memory_mb}M -jar task.jar -id ${sample_id} -param ${param} -out ${sample_id}.out
  }
  output {
    File results = "${sample_id}.out"
  }
  runtime {
    docker: "broadinstitute/baseimg"
  }
  parameter_meta {
    memory_mb: "Amount of memory to allocate to the JVM"
    param: "Some arbitrary parameter"
    sample_id: "The ID of the sample in format foo_bar_baz"
  }
  meta {
    author: "Joe Somebody"
    email: "joe@company.org"
  }
}
```

#### Example 4: BWA mem

This is an redesign of [BWA mem in CWL](https://github.com/common-workflow-language/common-workflow-language/blob/master/conformance/draft-2/bwa-mem-tool.cwl)

```
task bwa-mem-tool {
  command {
    bwa mem -t ${Int threads} \
            -k ${Int min_seed_length} \
            -I ${sep=',' Int min_std_max_min+} \
            ${File reference} \
            ${sep=' ' File reads+} > output.sam
  }
  output {
    File sam = "output.sam"
  }
  runtime {
    docker: "images.sbgenomics.com/rabix/bwa:9d3b9b0359cf"
  }
}
```

Notable pieces in this example is `${sep=',' Int min_std_max_min+}` which specifies that min_std_max_min can be one or more integers (the `+` after the variable name indicates that it can be one or more).  If an `Array[Int]` is passed into this parameter, then it's flattened by combining the elements with the separator character (`sep=','`).

This task also defines that it exports one file, called 'sam', which is the stdout of the execution of bwa mem.

The 'docker' portion of this task definition specifies which that this task must only be run on the Docker image specified.

#### Example 5: Word Count

Here's an example of how to rewrite [wc2-tool](https://github.com/common-workflow-language/common-workflow-language/blob/master/conformance/draft-2/wc2-tool.cwl) and [count-lines4-wf](https://github.com/common-workflow-language/common-workflow-language/blob/master/conformance/draft-2/count-lines4-wf.cwl) (also as a [generalized collection](https://gist.github.com/dshiga/3c3c54ee8468e23d0a5b)):

```
task wc2-tool {
  command {
    wc ${File file1}
  }
  output {
    Int count = read_int(stdout())
  }
}

workflow count-lines4-wf {
  Array[File] files
  scatter(f in files) {
    call wc2-tool {
      input: file1=f
    }
  }
  output {
    wc2-tool.count
  }
}
```

In this example, it's all pretty boilerplate, declarative code, except for some language-y like features, like `firstline(stdout)` and `append(list_of_count, wc2-tool.count)`.  These both can be implemented fairly easily if we allow for custom function definitions.  Parsing them is no problem.  Implementation would be fairly simple and new functions would not be hard to add.  Alternatively, this could be something like JavaScript or Python snippets that we run.

#### Example 6: tmap

Next, is an implementation of the [tmap-tool](https://github.com/common-workflow-language/common-workflow-language/blob/master/conformance/draft-2/tmap-tool.cwl) (and corresponding job, [tmap-job](https://github.com/common-workflow-language/common-workflow-language/blob/master/conformance/draft-2/tmap-job.json))

This should produce a command line like this:

```
tmap mapall \
stage1 map1 --min-seq-length 20 \
       map2 --min-seq-length 20 \
stage2 map1 --max-seq-length 20 --min-seq-length 10 --seed-length 16 \
       map2 --max-seed-hits -1 --max-seq-length 20 --min-seq-length 10
```

Task definition would look like this:

```
task tmap-tool {
  command {
    tmap mapall ${sep=' ' stages+} < ${File reads} > output.sam
  }
  output {
    File sam = "output.sam"
  }
}
```

The syntax element `${sep=' ' stages+}` is a compromise.  CWL's JSON implementation chooses to try to hide the flags and parameters to the `tmap` command.  The result is almost 200 lines of code leaving the user having to instead learn a JSON format for mapping to the exact same set of parameters.  Now instead of just having to learn how `tmap` works, the user has to learn how *CWL maps to tmap*.

For this particular case where the command line is *itself* a mini DSL, The best option at that point is to allow the user to type in the rest of the command line, which is what `${sep=' ' stages+}` is for.  This allows the user to specify an array of strings as the value for `stages` and then it concatenates them together with a space character

|Variable|Value|
|--------|-----|
|reads   |/path/to/fastq|
|stages  |["stage1 map1 --min-seq-length 20 map2 --min-seq-length 20", "stage2 map1 --max-seq-length 20 --min-seq-length 10 --seed-length 16  map2 --max-seed-hits -1 --max-seq-length 20 --min-seq-length 10"]|

## Workflow Definition

```
$workflow = 'workflow' $ws* '{' $workflow_element* '}'
$workflow_element = $call | $loop | $conditional | $declaration | $scatter
```

A workflow is defined as the keyword `workflow` and the body being in curly braces.

```
workflow wf {
  Array[File] files
  Int threshold
  Map[String, String] my_map
}
```

### Call Sub-Tasks

```
$call = 'call' $namespaced_task ('as' $identifier)? $call_body?
$namespaced_task = $identifier ('.' $identifier)*
$call_body = '{' $inputs? $outputs? '}'
$inputs = 'input' ':' $variable_mappings
$variable_mappings = $identifier '=' $expression (',' $identifier '=' $expression)*
```

A workflow may call other tasks via the `call` keyword.  The `$namespaced_task` is the reference to which task to run, usually this is an identifier or it may use the dot notation if the task was included via an [import statement](#import-statements).  All `calls` must be uniquely identifiable, which is why one would use the `as alias` syntax.

```
import "lib"
workflow wf {
  call my_task
  call my_task as my_task_alias
  call my_task as my_task_alias2 {
    input: threshold=2
  }
  call lib.other_task
}
```

The `$call_body` is optional and is meant to specify how to satisfy a subset of the the task's input parameters as well as a way to map tasks outputs to variables defined in the [visible scopes](#TODO).

A `$variable_mapping` in the `$inputs` section maps parameters in the task to expressions.  These expressions usually reference outputs of other tasks, but they can be arbitrary expressions.

As an example, here is a workflow in which the second task references an output from the first task:

```
task task1 {
  command {python do_stuff.py}
  output {file results = stdout()}
}
task task2 {
  command {python do_stuff2.py ${File foobar}}
  output {file results = stdout()}
}
workflow wf {
  call task1
  call task2 {input: foobar=task1.results}
}
```

### Scatter

```
$scatter = 'scatter' '(' $identifier 'in' $expression ')' '{' $workflow_element* '}'
```

A "scatter" clause defines that the everything in the body can be run in parallel.  The clause in parenthesis declares which collection to scatter over and what to call each element.

For example, if `$expression` is an array of integers of size 3, then the body of the scatter clause can be executed 3-times in parallel.  `$identifier` would refer to each integer in the array.

> **Question** can the `$expression` be a map?

```
scatter(i in integers) {
  call task1{input: num=i}
  call task2{input: num=task1.output[i.index]}
}
```

In this example, `task2` depends on `task1`.  Variable `i` has an implicit `index` attribute to make sure we can access the right output from `task1`.  Since both task1 and task2 run N times where N is the length of the array `integers`, any scalar outputs of these tasks is now an array.

### Loops

```
$loop = 'while' '(' $expression ')' '{' $workflow_element* '}'
```

Loops are distinct from scatter clauses because the body of a while loop needs to be executed to completion before another iteration is considered for iteration.  The `$expression` condition is evaluated only when the iteration count is zero or if all `$workflow_element`s in the body have completed successfully for the current iteration.

### Conditionals

```
$conditional = 'if' '(' $expression ')' '{' $workflow_element* '}'
```

Conditionals only execute the body if the expression evaluates to true

### Outputs

```
$outputs = 'output' '{' ($expression (',' $expression)*)? '}'
```

Some ideas for workflow output syntax:

```
task1 # All outputs of task1  
task1.* # Same  
task1 <*, !out1, !out2> # Exclusion list  
task1 <!out1, !out2> # Maybe implies *?  
task1 <out3, out4> # Inclusion list  
task1.<out2, !out3> # Dot notation?  
task1.<out5, *> # Error, * and inclusion elements are mutually exclusive?  
```

This section defines what variables the workflow exports.

> **TODO**: Need to define how these are structured

> **Question**: Is there a way to specify exclusion lists?  We can specify `some_task.*` for all of that task's outputs, but what about all of that task's outputs except for a few?

### Examples

#### Example 1: dRanger

```
workflow dRanger {
  call LaneBlackList
  scatter(sample in samples) {
    call dRangerPreprocess {
      input: blacklist=LaneBlackList.blacklist
    }
  }
  call dRangerRun {
    input: dirs = dRangerPreprocess.dir
  }
  scatter(sample in samples) {
    call BreakPointer {
      input: lane.blacklist=LaneBlackList.blacklist,
             dRanger_results.txt=dRangerRun.forBP,
             insertionsize=dRangerPreprocess.all_isz[sample.index]
    }
  }
  call CreateCircosPlot {
    input: dRanger_file=dRangerRun.forBP
  }
  call dRangerFinalize {
    input: BP=BreakPointer.BP, dRmatfile=dRangerRun.mat, circospng=CreateCircosPlot.circos_png
  }
  output {
    dRangerFinalize.dRanger_results
  }
}
```

# Variable Resolution & Scoping

Scopes are defined as:

* `workflow {...}` blocks
* `call` statements
* `while(expr) {...}` blocks
* `if(expr) {...}` blocks
* `scatter(x in y) {...}` blocks

Inside of any scope, variables may be [declared](#declarations).  The variables declared in that scope are visible to any sub-scope, recursively.  For example:

```
task my_task {
  Int x
  command {
    my_cmd --integer=${var}
  }
}

workflow wf {
  Int x = 2
  workflow wf2 {
    Int x = 3
    call my_task {
      Int x = 4
      input: var=x
    }
  }
}
```

`my_task` will use `x=4` to set the value for `var` in its command line.  However, my_task also needs a value for `x` which is defined at the task level.  Since `my_task` has two inputs (`x` and `var`), and only one of those is set in the `call my_task` declaration, the value for `my_task.x` still needs to be provided by the user when the workflow is run.

# Namespaces

Import statements can be used to pull in tasks/workflows from other locations as well as create namespaces.  In the simplest case, an import statement adds the tasks/workflows that are imported into the current namespace.  For example:

tasks.wdl
```
task x {
  command { python script.py }
}
task y {
  command { python script2.py }
}
```

workflow.wdl
```
import "tasks.wdl"

workflow wf {
  call x
  call y
}
```

Tasks `x` and `y` are in the same namespace as workflow `wf` is.  However, if workflow.wdl could put all of those tasks behind a namespace:

workflow.wdl
```
import "tasks.wdl" as ns

workflow wf {
  call ns.x
  call ns.y
}
```

Now everything inside of `tasks.wdl` must be accessed through the namespace `ns`.

## Additional Namespace Requirements

Each namespace contains: namespaces, tasks, and workflows.  The names of these needs to be unique within that namespace.  For example, there cannot be a task named `foo` and also a namespace named `foo`.  Also there can't be a task and a workflow with the same names, or two workflows with the same name.

# Standard Library

## mixed stdout()

Returns either a `File` or `Uri` of the stdout that this task generated.

## mixed stderr()

Returns either a `File` or `Uri` of the stderr that this task generated.

## mixed tsv(String|File|Uri)

the `tsv()` function takes one parameter, which is a file-like object (`String`, `File`, or `URI`) and returns either an `Array`, `Object`, or `Map` depending on the contents of that file.

If the parameter is a `String`, this is assumed to be a local file path relative to the current working directory of the task.

For example, if I write a task that outputs a file to `./results/file_list.tsv`, and my task is defined as:

```
task do_stuff {
  command {
    python do_stuff.py ${File input}
  }
  output {
    Array[File] outputs = tsv("./results/file_list.tsv")
  }
}
```

Then when the task finishes, to fulfull the `outputs` variable, `./results/file_list.tsv` must contain a single-column TSV with file paths that are valid.

## mixed json(String|File|Uri)

This function works exactly like `tsv()` except that the parameter is expected to be a path to a JSON file containing the data structure

## Int read_int(String|File|Uri)

The `read_int()` function takes a file path which is expected to contain 1 line with 1 integer on it.  This function returns that integer.

## String read_string(String|File|Uri)

The `read_string()` function takes a file path which is expected to contain 1 line with 1 string on it.  This function returns that string.

## Float read_float(String|File|Uri)

The `read_float()` function takes a file path which is expected to contain 1 line with 1 floating point number on it.  This function returns that float.

## Boolean read_boolean(String|File|Uri)

The `read_boolean()` function takes a file path which is expected to contain 1 line with 1 Boolean value (either "true" or "false" on it.  This function returns that Boolean value.

# Data Types & Serialization

## Overview

Tasks and workflows are given values for their input parameters in order to run.  The type of each of those parameters is specified in the `${`...`}` syntax in the task definition.  For example, `${float quality_score}` or `${Array[File] bams}`.  If no type is specified, the default type is `string`.  Those input parameters can be any of the following types:

Primitives:
* [String](#string)
* [Int](#int-and-float)
* [Float](#int-and-float)
* [File](#file-and-uri)
* [Uri](#file-and-uri)
* [Boolean](#boolean)

Compound Types:
* [Array\[Type\]](#array) (e.g. `Array[Int]`, `Array[File]`)
* [Map\[Type, Type\]](#map) (e.g. `Map[String, File]`)
* [Object](#object)

> **Question**: Will we be able to support "stream" types?  This could be as simple as named pipes or as complex as a new system like `stream://path/to/stream` which would mean the contract between tasks and workflows would require tasks to support this protocol.

## Serialization

These types are then passed to the task via a serialization method.  This is the main contract between WDL and the tools themselves.  Tools are expected to understand these the serialization formats for the types that they need to deal with, but WDL offers flexibility in how the data types can be serialized.

For example, if I'm writing a tool that operates on a list of FASTQ files, there are a variety of ways that this list can be passed to that task:

* A file containing one file path per line (e.g. `./mytool fastq_list.txt`)
* A file containing a JSON list (e.g. `./mytool fastq_list.json`)
* Enumerated on the command line (e.g. (`./mytool 1.fastq 2.fastq 3.fastq`)

Each of these methods has its merits and one method might be better for one tool while another method would be better for another tool.

On the other end, tasks need to be able to communicate data structures back to the workflow engine.  For example, let's say this same tool that takes a list of FASTQs wants to return back a `Map[File, Int]` representing the number of reads in each FASTQ.  A tool might choose to output it as a two-column TSV or as a JSON object.

This specification lays out the serialization format for three major types:

* TSV - flat-file serialization meant to capture all basic data structures and providing easy reading/writing.  Also great for compatibility with UNIX tools.
* JSON - for higher-order data types (i.e. `Array[String, Map[int, file]]`) or for tools that prefer JSON over TSV
* Single-File JSON - All inputs and all outputs are done through one file each.

The rest of this spec outlines the types and how they serialize in TSV format.

### Serialization of Primitive Output Types

Serializing primitive inputs makes intuitive sense because the value is just turned into a string and inserted into the command line.

However, outputting primitive types requires that the task write files with those values in them.  The contract is that any task that wants to output a primitive must write that primitive to a file.  The file should only contain one-line for clarity.

For example, if I have a task that outputs a URI and an integer:

```
task output_example {
  command {
    python do_work.py ${param1} ${param2}
  }
  output {
    Int my_int = "file_with_int"
    Uri my_uri = "file_with_uri"
  }
}
```

> **TODO**: What about single-file JSON?

Both of `file_with_int` and `file_with_uri` should contain one line with the value on that line.  This value is then validated against the type of the variable.  If `file_with_int` contains a line with the text "foobar", the workflow must fail this task with an error.

### Serialization of Compound Output Types

Compound types must be outputted via a TSV or JSON file with corresponding file extension.

```
task output_example {
  command {
    python do_work.py ${param1} ${param2}
  }
  output {
    Map[String, file] my_map = "file_with_string_to_file.tsv"
    Array[Int] my_ints = "file_with_ints.json"
  }
}
```

In this case, `my_map` comes from a [TSV file](#map-serialization-as-tsv) and `my_ints` comes from a [JSON File](#array-serialization-as-json).

> **TODO**: What about single-file JSON?

## Primitive Types

All primitive types are serialized as a string and provided as-is to the command line.

### String

The String type is the most basic and default type.  The value is serialized directly as a parameter on the command line, quoted.

```
java -jar MyTool.jar ${my_param}
```

If an invocation of this tool is "foo bar" the value for `my_param`, the resulting command line is:

```
java -jar MyTool.jar foo bar
```

### Int and Float

The Int and Float types are similar in a lot of ways to the String type except that the workflow engine must verify that the provided value for these parameters is compatible with either float or int types.

```
sh script.sh ${Int iterations} --pi=${Float pi}
```

if "foobar" is provided for the `iterations` parameter, the workflow engine should return an error.  However, if the String "2" is provided for `iterations` this should be considered int compatible.  Likewise, valid values for pi could be: 3, "3.14", 3.1.  If we were to provide the values iterations=2 and pi=3.14, the resulting command line would be:

```
sh script.sh 2 --pi=3.14
```

> **TODO**: regular expression patterns for Int and Float (steal from a language standard)

### File and Uri

Like Int and Float types, File and Uri types are a special case and the workflow engine must verify the values of these before calling the tool.  The file type may be a URI starting with `file://`, but the schema is striped when it is called.  URIs are any string that conform to [RFC 3986](https://tools.ietf.org/html/rfc3986).

```
python algorithm.py ${File bam} ${Uri gcs_bucket}
```

If we provide `bam=file:///root/input.bam` and `gcs_bucket=gs://bucket/`, then the resulting command line is:

```
python algorithm.py /root/input.bam gs://bucket/
```

### Boolean

Boolean types are serialized as either the string `true` or `false` on the command line.

## Compound Types

Compound types cannot always be serialized directly to the command line, so there are different strategies for serializing them, which is described in the sections below

> **Note**: The location of the TSV/JSON file is implementation specific.  The only requirement is that it's a path on the local file system.

> **Note**: new-line characters must be \n (0xA) characters.

### array

Arrays can be serialized in two ways:

* **Array Expansion**: elements in the list are flattened to a string with a separator character.
* **File Creation**: create a file with the elements of the array in it and passing that file as the parameter on the command line.

#### array serialization by expansion

The array flattening approach can be done if a parameter is specified as `${sep=' ' File my_param+}`.  This format for specifying a parameter means that `my_param` may take a single file or an array of files.  If an array is specified, then the values are joined together with the separator character (a space).  For example:

```
python script.py --bams=${sep=',' File bams*}
```

If passed an array for the value of `bams`:

|Element       |
|--------------|
|/path/to/1.bam|
|/path/to/2.bam|
|/path/to/3.bam|

Would produce the command `python script.py --bams=/path/to/1.bam,/path/to/2.bam,/path/to/1.bam`

> **Question**: What about if sep=' ' and you don't want to quote?

#### array serialization as TSV

An array may be turned into a file with each element in the array occupying a line in the file.

```
sh script.sh ${serialize='tsv' Array[File] bams}
```

> **NOTE**: the `serialize='tsv'` option is only here for completeness.  A default value for serialization may be provided at the task level or the workflow engine.

if `bams` is given this array:

|Element       |
|--------------|
|/path/to/1.bam|
|/path/to/2.bam|
|/path/to/3.bam|

Then, the resulting command line could look like:

```
sh script.sh /jobs/564758/bams.tsv
```

Where `/jobs/564758/bams.tsv` would contain:

```
/path/to/1.bam
/path/to/2.bam
/path/to/3.bam
```

> *Additional requirement*: Because of the limitations of the TSV file format, multi-dimensional arrays may not be expressed using this approach.  Trying to serialize an `Array[Array[Array[String]]]` in TSV is too cumbersome to support.  Because of this, only arrays of primitive types are supported with TSV serialization.  The syntax checker MUST check that if the serialization format is TSV that the type is compatible

#### array serialization as JSON

The array may be turned into a JSON document with the file path for the JSON file passed in as the parameter:

```
sh script.sh ${serialize='json' Array[File] bams}
```

> **NOTE**: the `serialize='json'` option is only here for completeness.  A default value for serialization may be provided at the task level or the workflow engine.

if `bams` is given this array:

|Element       |
|--------------|
|/path/to/1.bam|
|/path/to/2.bam|
|/path/to/3.bam|

Then, the resulting command line could look like:

```
sh script.sh /jobs/564758/bams.json
```

Where `/jobs/564758/bams.json` would contain:

```
[
  "/path/to/1.bam",
  "/path/to/2.bam",
  "/path/to/3.bam"
]
```

### map

Map types cannot be serialized on the command line directly and must be serialized through a file

#### map serialization as TSV

The map type can be serialized as a two-column TSV file and the parameter on the command line is given the path to that file.

```
sh script.sh ${Map[String, Float] sample_quality_scores}
```

if sample_quality_scores is given this map:

|Key    |Value |
|-------|------|
|sample1|98    |
|sample2|95    |
|sample3|75    |

Then, the resulting command line could look like:

```
sh script.sh /jobs/564757/sample_quality_scores.tsv
```

Where `/jobs/564757/sample_quality_scores.tsv` would contain:

```
sample1\t98
sample2\t95
sample3\t75
```

#### map serialization as JSON

The map type can also be serialized as a JSON file and the parameter on the command line is given the path to that file.

```
sh script.sh ${Map[String, Float] sample_quality_scores}
```

if sample_quality_scores is given this map:

|Key    |Value |
|-------|------|
|sample1|98    |
|sample2|95    |
|sample3|75    |

Then, the resulting command line could look like:

```
sh script.sh /jobs/564757/sample_quality_scores.json
```

Where `/jobs/564757/sample_quality_scores.json` would contain:

```
{
  "sample1": 98,
  "sample2": 95,
  "sample3": 75
}
```

### object

An object is a more general case of a map where the keys are strings and the values are of arbitrary types and treated as strings.

#### object serialization as TSV

```
perl script.pl ${object sample}
```

if sample is provided as:

|Attribute|Value |
|---------|------|
|attr1    |value1|
|attr2    |value2|
|attr3    |value3|
|attr4    |value4|

Then, the resulting command line could look like:

```
perl script.pl /jobs/564759/sample.tsv
```

Where `/jobs/564759/sample.tsv` would contain:

```
attr1\tattr2\tattr3\tattr4
value1\tvalue2\tvalue3\tvalue4
```

#### object serialization as JSON

```
perl script.pl ${object sample}
```

if sample is provided as:

|Attribute|Value |
|---------|------|
|attr1    |value1|
|attr2    |value2|
|attr3    |value3|
|attr4    |value4|

Then, the resulting command line could look like:

```
perl script.pl /jobs/564759/sample.json
```

Where `/jobs/564759/sample.json` would contain:

```
{
  "attr1": "value1",
  "attr2": "value2",
  "attr3": "value3",
  "attr4": "value4",
}
```
#### Array[object]

In the case of TSV serialization, the only difference between `Array[object]` and `object` is that an array would contain more rows.

In the case of JSON serialization, it would be a list of objects.

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
    Array[String] words = tsv(stdout())
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

Upon a job finishing and the return code being set, the `outputs` section is processed for that task.  In the case of the above example, when `wf.grep_pythonic_words` finishes the output mapping `Array[String] words = tsv(stdout())` is processed.  The workflow engine looks for the file called `stdout` in the current working directory where the process was launched.  If it is not found, the task's status gets set to `error` and optionally an error message field gets set describing the nature of why the field was set.

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
    Array[String] words = tsv(stdout())
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
    Array[String] intervals = tsv(stdout())
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
