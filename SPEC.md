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
      * [Alternative heredoc syntax](#alternative-heredoc-syntax)
      * [Parameters Used Multiple Times](#parameters-used-multiple-times)
    * [Command Part Options](#command-part-options)
      * [sep](#sep)
      * [true and false](#true-and-false)
      * [serialize](#serialize)
      * [default](#default)
    * [Outputs Section](#outputs-section)
    * [String Interpolation](#string-interpolation)
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
    * [Call Statement](#call-statement)
    * [Scatter](#scatter)
    * [Loops](#loops)
    * [Conditionals](#conditionals)
    * [Outputs](#outputs)
    * [Examples](#examples)
      * [Example 1: dRanger](#example-1-dranger)
* [Variable Resolution & Scoping](#variable-resolution--scoping)
* [Namespaces](#namespaces)
  * [Additional Namespace Requirements](#additional-namespace-requirements)
* [Standard Library](#standard-library)
  * [mixed stdout()](#mixed-stdout)
  * [mixed stderr()](#mixed-stderr)
  * [Array\[String\] read_lines(String|File|Uri)](#arraystring-read_linesstringfileuri)
  * [Array\[Array\[String\]\] read_tsv(String|File|Uri)](#arrayarraystring-read_tsvstringfileuri)
  * [Map\[String, String\] read_map(String|File|Uri)](#mapstring-string-read_mapstringfileuri)
  * [mixed read_json(String|File|Uri)](#mixed-read_jsonstringfileuri)
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


#### Alternative heredoc syntax

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

#### Parameters Used Multiple Times

In some cases it is desirable to use the same parameter twice in a command.  A parameter can be declared multiple times if each declaration is the same.

For example,

```
task test {
  command {
    ./script ${x} ${String x} ${x}
  }
}
```

Since the default type if one isn't specified is `String`, this should be allowed.  If a value of `foo` is specified for `x`, then the command would instantiate to:

```
./script foo foo foo
```

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
  Int threshold = read_int("threshold.txt")
}
```

Then the task is expecting a file called "threshold.txt" in the current working directory where the task was executed.  Inside of that file must be one line that contains only an integer and whitespace.  See the [Data Types & Serialization](#data-types--serialization) section for more details.

The filename strings may also contain variable definitions themselves (see the [String Interpolation](#string-interpolation) section below for more details):

```
output {
  Array[String] quality_scores = read_lines("${sample_id}.scores.txt")
}
```

If this is the case, then `sample_id` is considered an input to the task.

> *Additional requirement*: Any variable in the filename string MUST be of type string.

Finally, glob-style `*` may be used in the filename.  The glob may only match more than 1 file if the output is of type `array`

### String Interpolation

Within tasks, any string literal can use string interpolation to access the value of any of the task's inputs.  The most obvious example of this is being able to define an output file which is named as function of its input.  For example:

```
task example {
  python analysis.py --prefix=${prefix} ${File bam}
  output {
    File analyzed = "${prefix}.out"
    File bam_sibling = "${bam}.suffix"
  }
}
```

Any `${identifier}` inside of a string literal must be replaced with the value of the identifier.  If prefix were specified as `foobar`, then `"${prefix}.out"` would be evaluated to `"foobar.out"`.

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

### Call Statement

```
$call = 'call' $namespaced_task_or_wf ('as' $identifier)? $call_body?
$namespaced_task_or_wf = $identifier ('.' $identifier)*
$call_body = '{' $inputs? $outputs? '}'
$inputs = 'input' ':' $variable_mappings
$variable_mappings = $identifier '=' $expression (',' $identifier '=' $expression)*
```

A workflow may call other tasks/workflows via the `call` keyword.  The `$namespaced_task_or_wf` is the reference to which task to run, usually this is an identifier or it may use the dot notation if the task was included via an [import statement](#import-statements).  All `calls` must be uniquely identifiable, which is why one would use the `as alias` syntax.

A `call` statement may reference a workflow too (e.g. `call other_workflow`).

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
  output {File results = stdout()}
}
task task2 {
  command {python do_stuff2.py ${File foobar}}
  output {File results = stdout()}
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

A "scatter" clause defines that everything in the body can be run in parallel.  The clause in parentheses declares which collection to scatter over and what to call each element.

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

## Array[String] read_lines(String|File|Uri)

Given a file-like object (`String, `File`, or `Uri`) as a parameter, this will read each line as a string and return an `Array[String]` representation of the lines in the file.

The order of the lines in the returned `Array[String]` must be the order in which the lines appear in the file-like object.

This task would `grep` through a file and return all strings that matched the pattern:

```
task do_stuff {
  command {
    grep '${pattern}' ${File input}
  }
  output {
    Array[String] matches = read_lines(stdout())
  }
}
```

## Array[Array[String]] read_tsv(String|File|Uri)

the `read_tsv()` function takes one parameter, which is a file-like object (`String`, `File`, or `Uri`) and returns an `Array[Array[String]]` representing the table from the TSV file.

If the parameter is a `String`, this is assumed to be a local file path relative to the current working directory of the task.

For example, if I write a task that outputs a file to `./results/file_list.tsv`, and my task is defined as:

```
task do_stuff {
  command {
    python do_stuff.py ${File input}
  }
  output {
    Array[Array[String]] output_table = read_tsv("./results/file_list.tsv")
  }
}
```

Then when the task finishes, to fulfull the `outputs_table` variable, `./results/file_list.tsv` must be a valid TSV file or an error will be reported.

## Map[String, String] read_map(String|File|Uri)

Given a file-like object (`String, `File`, or `Uri`) as a parameter, this will read each line from a file and expect the line to have the format `col1\tcol2`.  In other words, the file-like object must be a two-column TSV file.

This task would `grep` through a file and return all strings that matched the pattern:

The following task would write a two-column TSV to standard out and that would be interpreted as a `Map[String, String]`:

```
task do_stuff {
  command {
    ./script --flags=${flags} ${File input}
  }
  output {
    Map[String, String] mapping = read_map(stdout())
  }
}
```

## mixed read_json(String|File|Uri)

the `read_json()` function takes one parameter, which is a file-like object (`String`, `File`, or `Uri`) and returns a data type which matches the data structure in the JSON file.  The mapping of JSON type to WDL type is:

|JSON Type|WDL Type|
|---------|--------|
|object|`Map[String, ?]`|
|array|`Array[?]`|
|number|`Int` or fallback `Float`|
|string|`String`|
|boolean|`Boolean`|
|null|???|

If the parameter is a `String`, this is assumed to be a local file path relative to the current working directory of the task.

For example, if I write a task that outputs a file to `./results/file_list.json`, and my task is defined as:

```
task do_stuff {
  command {
    python do_stuff.py ${File input}
  }
  output {
    Map[String, String] output_table = read_json("./results/file_list.json")
  }
}
```

Then when the task finishes, to fulfull the `output_table` variable, `./results/file_list.json` must be a valid TSV file or an error will be reported.

## Int read_int(String|File|Uri)

The `read_int()` function takes a file path which is expected to contain 1 line with 1 integer on it.  This function returns that integer.

## String read_string(String|File|Uri)

The `read_string()` function takes a file path which is expected to contain 1 line with 1 string on it.  This function returns that string.

No trailing newline characters should be included

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
