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
    * [Fully Qualified Names & Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers)
    * [Declarations](#declarations)
    * [Expressions](#expressions)
    * [Operator Precedence Table](#operator-precedence-table)
    * [Member Access](#member-access)
    * [Map and Array Indexing](#map-and-array-indexing)
    * [Pair Indexing](#pair-indexing)
    * [Function Calls](#function-calls)
    * [Array Literals](#array-literals)
    * [Map Literals](#map-literals)
    * [Pair Literals](#pair-literals)
  * [Document](#document)
  * [Import Statements](#import-statements)
  * [Task Definition](#task-definition)
    * [Sections](#sections)
    * [Command Section](#command-section)
      * [Command Parts](#command-parts)
      * [Command Part Options](#command-part-options)
        * [sep](#sep)
        * [true and false](#true-and-false)
        * [default](#default)
      * [Alternative heredoc syntax](#alternative-heredoc-syntax)
      * [Stripping Leading Whitespace](#stripping-leading-whitespace)
    * [Outputs Section](#outputs-section)
    * [String Interpolation](#string-interpolation)
    * [Runtime Section](#runtime-section)
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
        * [Sub Workflows](#sub-workflows)
    * [Scatter](#scatter)
    * [Loops](#loops)
    * [Conditionals](#conditionals)
    * [Parameter Metadata](#parameter-metadata)
    * [Metadata](#metadata)
    * [Outputs](#outputs)
* [Namespaces](#namespaces)
* [Scope](#scope)
* [Optional Parameters & Type Constraints](#optional-parameters--type-constraints)
  * [Prepending a String to an Optional Parameter](#prepending-a-string-to-an-optional-parameter)
* [Scatter / Gather](#scatter--gather)
* [Variable Resolution](#variable-resolution)
  * [Task-Level Resolution](#task-level-resolution)
  * [Workflow-Level Resolution](#workflow-level-resolution)
* [Computing Inputs](#computing-inputs)
  * [Task Inputs](#task-inputs)
  * [Workflow Inputs](#workflow-inputs)
  * [Specifying Workflow Inputs in JSON](#specifying-workflow-inputs-in-json)
* [Type Coercion](#type-coercion)
* [Standard Library](#standard-library)
  * [File stdout()](#file-stdout)
  * [File stderr()](#file-stderr)
  * [Array\[String\] read_lines(String|File)](#arraystring-read_linesstringfile)
  * [Array\[Array\[String\]\] read_tsv(String|File)](#arrayarraystring-read_tsvstringfile)
  * [Map\[String, String\] read_map(String|File)](#mapstring-string-read_mapstringfile)
  * [Object read_object(String|File)](#object-read_objectstringfile)
  * [Array\[Object\] read_objects(String|File)](#arrayobject-read_objectsstringfile)
  * [mixed read_json(String|File)](#mixed-read_jsonstringfile)
  * [Int read_int(String|File)](#int-read_intstringfile)
  * [String read_string(String|File)](#string-read_stringstringfile)
  * [Float read_float(String|File)](#float-read_floatstringfile)
  * [Boolean read_boolean(String|File)](#boolean-read_booleanstringfile)
  * [File write_lines(Array\[String\])](#file-write_linesarraystring)
  * [File write_tsv(Array\[Array\[String\]\])](#file-write_tsvarrayarraystring)
  * [File write_map(Map\[String, String\])](#file-write_mapmapstring-string)
  * [File write_object(Object)](#file-write_objectobject)
  * [File write_objects(Array\[Object\])](#file-write_objectsarrayobject)
  * [File write_json(mixed)](#file-write_jsonmixed)
  * [Float size(File, \[String\])](#float-sizefile-string)
  * [String sub(String, String, String)](#string-substring-string-string)
  * [Array\[Int\] range(Int)](#arrayint-rangeint)
  * [Array\[Array\[X\]\] transpose(Array\[Array\[X\]\])](#arrayarrayx-transposearrayarrayx)
  * [Array\[Pair(X,Y)\] zip(Array\[X\], Array\[Y\])](#arraypairxy-ziparrayx-arrayy)
  * [Array\[Pair(X,Y)\] cross(Array\[X\], Array\[Y\])](#arraypairxy-crossarrayx-arrayy)
  * [Integer length(Array\[X\])](#integer-lengtharrayx)
  * [Array\[String\] prefix(String, Array\[X\])](#arraystring-prefixstring-arrayx)
  * [X select_first(Array\[X?\])](#x-select_firstarrayx)
  * [Array\[X\] select_all(Array\[X?\])](#arrayx-select_allarrayx)
  * [Boolean defined(X?)](#boolean-definedx)
  * [String basename(String)](#string-basenamestring)
  * [Int floor(Float), Int ceil(Float) and Int round(Float)](#int-floorfloat-int-ceilfloat-and-int-roundfloat)
* [Data Types & Serialization](#data-types--serialization)
  * [Serialization of Task Inputs](#serialization-of-task-inputs)
    * [Primitive Types](#primitive-types)
    * [Compound Types](#compound-types)
      * [Array serialization](#array-serialization)
        * [Array serialization by expansion](#array-serialization-by-expansion)
        * [Array serialization using write_lines()](#array-serialization-using-write_lines)
        * [Array serialization using write_json()](#array-serialization-using-write_json)
      * [Map serialization](#map-serialization)
        * [Map serialization using write_map()](#map-serialization-using-write_map)
        * [Map serialization using write_json()](#map-serialization-using-write_json)
      * [Object serialization](#object-serialization)
        * [Object serialization using write_object()](#object-serialization-using-write_object)
        * [Object serialization using write_json()](#object-serialization-using-write_json)
      * [Array\[Object\] serialization](#arrayobject-serialization)
        * [Array\[Object\] serialization using write_objects()](#arrayobject-serialization-using-write_objects)
        * [Array\[Object\] serialization using write_json()](#arrayobject-serialization-using-write_json)
  * [De-serialization of Task Outputs](#de-serialization-of-task-outputs)
    * [Primitive Types](#primitive-types)
    * [Compound Types](#compound-types)
      * [Array deserialization](#array-deserialization)
        * [Array deserialization using read_lines()](#array-deserialization-using-read_lines)
        * [Array deserialization using read_json()](#array-deserialization-using-read_json)
      * [Map deserialization](#map-deserialization)
        * [Map deserialization using read_map()](#map-deserialization-using-read_map)
        * [Map deserialization using read_json()](#map-deserialization-using-read_json)
      * [Object deserialization](#object-deserialization)
        * [Object deserialization using read_object()](#object-deserialization-using-read_object)
      * [Array\[Object\] deserialization](#arrayobject-deserialization)
        * [Object deserialization using read_objects()](#object-deserialization-using-read_objects)

<!---toc end-->

## Introduction

WDL is meant to be a *human readable and writable* way to express tasks and workflows.  The "Hello World" tool in WDL would look like this:

```wdl
task hello {
  String pattern
  File in

  command {
    egrep '${pattern}' '${in}'
  }

  runtime {
    docker: "broadinstitute/my_image"
  }

  output {
    Array[String] matches = read_lines(stdout())
  }
}

workflow wf {
  call hello
}
```

This describes a task, called 'hello', which has two parameters (`String pattern` and `File in`).  A `task` definition is a way of **encapsulating a UNIX command and environment and presenting them as functions**.  Tasks have both inputs and outputs.  Inputs are declared as declarations at the top of the `task` definition, while outputs are defined in the `output` section.

The user must provide a value for these two parameters in order for this task to be runnable.  Implementations of WDL should accept their [inputs as JSON format](#specifying-workflow-inputs-in-json).  For example, the above task needs values for two parameters: `String pattern` and `File in`:

|Variable           |Value    |
|-------------------|---------|
|wf.hello.pattern   |^[a-z]+$ |
|wf.hello.in        |/file.txt|

Or, in JSON format:

```json
{
  "wf.hello.pattern": "^[a-z]+$",
  "wf.hello.in": "/file.txt"
}
```

Running the `wf` workflow with these parameters would yield a command line from the `call hello`:

```
egrep '^[a-z]+$' '/file.txt'
```

A simple workflow that runs this task in parallel would look like this:

```wdl
workflow example {
  Array[File] files
  scatter(path in files) {
    call hello {input: in=path}
  }
}
```

The inputs to this workflow would be `example.files` and `example.hello.pattern`.

## State of the Specification

**17 August 2015**

* Added concept of fully-qualified-name as well as namespace identifier.
* Changed task definitions to have all inputs as declarations.
* Changed command parameters (`${`...`}`) to accept expressions and fewer "declarative" elements
  * command parameters also are required to evaluate to primitive types
* Added a `output` section to workflows
* Added a lot of functions to the standard library for serializing/deserializing WDL values
* Specified scope, namespace, and variable resolution semantics

# Language Specification

## Global Grammar Rules

### Whitespace, Strings, Identifiers, Constants

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

These are common among many of the following sections

```
$ws = (0x20 | 0x9 | 0xD | 0xA)+
$identifier = [a-zA-Z][a-zA-Z0-9_]+
$string = "([^\\\"\n]|\\[\\"\'nrbtfav\?]|\\[0-7]{1,3}|\\x[0-9a-fA-F]+|\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*"
$string = '([^\\\'\n]|\\[\\"\'nrbtfav\?]|\\[0-7]{1,3}|\\x[0-9a-fA-F]+|\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*'
$boolean = 'true' | 'false'
$integer = [1-9][0-9]*|0[xX][0-9a-fA-F]+|0[0-7]*
$float = (([0-9]+)?\.([0-9]+)|[0-9]+\.|[0-9]+)([eE][-+]?[0-9]+)?
```

`$string` can accept the following between single or double-quotes:

* Any character not in set: `\\`, `"` (or `'` for single-quoted string), `\n`
* An escape sequence starting with `\\`, followed by one of the following characters: `\\`, `"`, `'`, `[nrbtfav]`, `?`
* An escape sequence starting with `\\`, followed by 1 to 3 digits of value 0 through 7 inclusive.  This specifies an octal escape code.
* An escape sequence starting with `\\x`, followed by hexadecimal characters `0-9a-fA-F`.  This specifies a hexidecimal escape code.
* An escape sequence starting with `\\u` or `\\U` followed by either 4 or 8 hexadecimal characters `0-9a-fA-F`.  This specifies a unicode code point

### Types

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

All inputs and outputs must be typed.

```
$type = ($primitive_type | $array_type | $map_type | $object_type) $type_postfix_quantifier?
$primitive_type = ('Boolean' | 'Int' | 'Float' | 'File' | 'String')
$array_type = 'Array' '[' ($primitive_type | $object_type | $array_type) ']'
$object_type = 'Object'
$map_type = 'Map' '[' $primitive_type ',' ($primitive_type | $array_type | $map_type | $object_type) ']'
$type_postfix_quantifier = '?' | '+'
```

Some examples of types:

* `File`
* `Array[File]`
* `Map[String, String]`
* `Object`

Types can also have a `$type_postfix_quantifier` (either `?` or `+`):

* `?` means that the value is optional.  Any expressions that fail to evaluate because this value is missing will evaluate to the empty string.
* `+` can only be applied to `Array` types, and it signifies that the array is required to have one or more values in it

For more details on the `$type_postfix_quantifier`, see the section on [Optional Parameters & Type Constraints](#optional-parameters--type-constraints)

For more information on type and how they are used to construct commands and define outputs of tasks, see the [Data Types & Serialization](#data-types--serialization) section.

### Fully Qualified Names & Namespaced Identifiers

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$fully_qualified_name = $identifier ('.' $identifier)*
$namespaced_identifier = $identifier ('.' $identifier)*
```

A fully qualified name is the unique identifier of any particular `call` or call input or output.  For example:

other.wdl
```wdl
task foobar {
  File in
  command {
    sh setup.sh ${in}
  }
  output {
    File results = stdout()
  }
}
```

main.wdl
```wdl
import "other.wdl" as other

task test {
  String my_var
  command {
    ./script ${my_var}
  }
  output {
    File results = stdout()
  }
}

workflow wf {
  Array[String] arr = ["a", "b", "c"]
  call test
  call test as test2
  call other.foobar
  output {
    test.results
    foobar.results
  }
  scatter(x in arr) {
    call test as scattered_test {
      input: my_var=x
    }
  }
}
```

The following fully-qualified names would exist within `workflow wf` in main.wdl:

* `wf` - References top-level workflow
* `wf.test` - References the first call to task `test`
* `wf.test2` - References the second call to task `test` (aliased as test2)
* `wf.test.my_var` - References the `String` input of first call to task `test`
* `wf.test.results` - References the `File` output of first call to task `test`
* `wf.test2.my_var` - References the `String` input of second call to task `test`
* `wf.test2.results` - References the `File` output of second call to task `test`
* `wf.foobar.results` - References the `File` output of the call to `other.foobar`
* `wf.foobar.input` - References the `File` input of the call to `other.foobar`
* `wf.arr` - References the `Array[String]` declaration on the workflow
* `wf.scattered_test` - References the scattered version of `call test`
* `wf.scattered_test.my_var` - References an `Array[String]` for each element used as `my_var` when running the scattered version of `call test`.
* `wf.scattered_test.results` - References an `Array[File]` which are the accumulated results from scattering `call test`
* `wf.scattered_test.1.results` - References an `File` from the second invocation (0-indexed) of `call test` within the scatter block.  This particular invocation used value "b" for `my_var`

A namespaced identifier has the same syntax as a fully-qualified name.  It is interpreted as the left-hand side being the name of a namespace and then the right-hand side being the name of a workflow, task, or namespace within that namespace.  Consider this workflow:

```wdl
import "other.wdl" as ns
workflow wf {
  call ns.ns2.task
}
```

Here, `ns.ns2.task` is a namespace identifier (see the [Call Statement](#call-statement) section for more details).  Namespace identifiers, like fully-qualified names are left-associative, which means `ns.ns2.task` is interpreted as `((ns.ns2).task)`, which means `ns.ns2` would have to resolve to a namespace so that `.task` could be applied.  If `ns2` was a task definition within `ns`, then this namespaced identifier would be invalid.

### Declarations

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$declaration = $type $identifier ('=' $expression)?
```

Declarations are declared at the top of any [scope](#scope).

In a [task definition](#task-definition), declarations are interpreted as inputs to the task that are not part of the command line itself.

If a declaration does not have an initialization, then the value is expected to be provided by the user before the workflow or task is run.

Some examples of declarations:

* `File x`
* `String y = "abc"`
* `Float pi = 3 + .14`
* `Map[String, String] m`

A declaration may also refer to elements that are outputs of tasks.  For example:

```wdl
task test {
  String var
  command {
    ./script ${var}
  }
  output {
    String value = read_string(stdout())
  }
}

task test2 {
  Array[String] array
  command {
    ./script ${write_lines(array)}
  }
  output {
    Int value = read_int(stdout())
  }
}

workflow wf {
  call test as x {input: var="x"}
  call test as y {input: var="y"}
  Array[String] strs = [x.value, y.value]
  call test2 as z {input: array=strs}
}
```

`strs` in this case would not be defined until both `call test as x` and `call test as y` have successfully completed.  Before that's the case, `strs` is undefined.  If any of the two tasks fail, then evaluation of `strs` should return an error to indicate that the `call test2 as z` operation should be skipped.

### Expressions

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$expression = '(' $expression ')'
$expression = $expression '.' $expression
$expression = $expression '[' $expression ']'
$expression = $expression '(' ($expression (',' $expression)*)? ')'
$expression = '!' $expression
$expression = '+' $expression
$expression = '-' $expression
$expression = if $expression then $expression else $expression
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

#### If then else

This is an operator that takes three arguments, a condition expression, an if-true expression and an if-false expression. The condition is always evaluated. If the condition is true then the if-true value is evaluated and returned. If the condition is false, the if-false expression is evaluated and returned. The return type of the if-then-else should be the same, regardless of which side is evaluated or runtime problems might occur.

Examples:
 - Choose whether to say "good morning" or "good afternoon":
```
Boolean morning = ...
String greeting = "good " + if morning then "morning" else "afternoon"
```
- Choose how much memory to use for a task:
```
Int array_length = length(array)
runtime {
  memory: if array_length > 100 then "16GB" else "8GB"
} 
```


### Operator Precedence Table

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

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

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

The syntax `x.y` refers to member access.  `x` must be an object or task in a workflow.  A Task can be thought of as an object where the attributes are the outputs of the task.

```wdl
workflow wf {
  Object obj
  Object foo

  # This would cause a syntax error,
  # because foo is defined twice in the same namespace.
  call foo {
    input: var=obj.attr # Object attribute
  }

  call foo as foo2 {
    input: var=foo.out # Task output
  }
}
```

### Map and Array Indexing

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

The syntax `x[y]` is for indexing maps and arrays.  If `x` is an array, then `y` must evaluate to an integer.  If `x` is a map, then `y` must evaluate to a key in that map.

### Pair Indexing

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given a Pair `x`, the left and right elements of that type can be accessed using the syntax `x.left` and `x.right`. 

### Function Calls

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Function calls, in the form of `func(p1, p2, p3, ...)`, are either [standard library functions](#standard-library) or engine-defined functions.

In this current iteration of the spec, users cannot define their own functions.

### Array Literals

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Arrays values can be specified using Python-like syntax, as follows:

```
Array[String] a = ["a", "b", "c"]
Array[Int] b = [0,1,2]
```

### Map Literals

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Maps values can be specified using a similar Python-like sytntax:

```
Map[Int, Int] = {1: 10, 2: 11}
Map[String, Int] = {"a": 1, "b": 2}
```

### Pair Literals

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Pair values can be specified inside of a WDL using another Python-like syntax, as follows:

```
Pair[Int, String] twenty_threes = (23, "twenty-three")
```

Pair values can also be specified within the [workflow inputs JSON](https://github.com/broadinstitute/wdl/blob/develop/SPEC.md#specifying-workflow-inputs-in-json) with a `Left` and `Right` value specified using JSON style syntax. For example, given a workflow `wf_hello` and workflow-level variable `twenty_threes`, it could be declared in the workflow inputs JSON as follows:
```
{
  "wf_hello.twenty_threes": { "Left": 23, "Right": "twenty-three" }
}
```

## Document

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$document = ($import | $task | $workflow)+
```

`$document` is the root of the parse tree and it consists of one or more import statement, task, or workflow definition

## Import Statements

:pig2: Coming soon in [Cromwell](https://github.com/broadinstitute/cromwell)

A WDL file may contain import statements to include WDL code from other sources

```
$import = 'import' $ws+ $string ($ws+ 'as' $ws+ $identifier)?
```

The import statement specifies that `$string` which is to be interpted as a URI which points to a WDL file.  The engine is responsible for resolving the URI and downloading the contents.  The contents of the document in each URI must be WDL source code.

Every imported WDL file requires a namespace which can be specified using an identifier (via the `as $identifier` syntax). If you do not explicitly specify a namespace identifier then the default namespace is the filename of the imported WDL, minus the .wdl extension.
For all imported WDL files, the tasks and workflows imported from that file will only be accessible through that assigned [namespace](#namespaces).

```wdl
import "http://example.com/lib/analysis_tasks" as analysis
import "http://example.com/lib/stdlib"


workflow wf {
  File bam_file

  # file_size is from "http://example.com/lib/stdlib"
  call stdlib.file_size {
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

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

A task is a declarative construct with a focus on constructing a command from a template.  The command specification is interpreted in an engine specific way, though a typical case is that a command is a UNIX command line which would be run in a Docker image.

Tasks also define their outputs, which is essential for building dependencies between tasks.  Any other data specified in the task definition (e.g. runtime information and meta-data) is optional.

```
$task = 'task' $ws+ $identifier $ws* '{' $ws* $declaration* $task_sections $ws* '}'
```

For example, `task name { ... }`.  Inside the curly braces defines the sections.

### Sections

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

The task has one or more sections:

```
$task_sections = ($command | $runtime | $task_output | $parameter_meta | $meta)+
```

> *Additional requirement*: Exactly one `$command` section needs to be defined, preferably as the first section.

### Command Section

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$command = 'command' $ws* '{' (0xA | 0xD)* $command_part+ $ws+ '}'
$command = 'command' $ws* '<<<' (0xA | 0xD)* $command_part+ $ws+ '>>>'
```

A command is a *task section* that starts with the keyword 'command', and is enclosed in curly braces or `<<<` `>>>`.  The body of the command specifies the literal command line to run with placeholders (`$command_part_var`) for the parts of the command line that needs to be filled in.

#### Command Parts

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$command_part = $command_part_string | $command_part_var
$command_part_string = ^'${'+
$command_part_var = '${' $var_option* $expression '}'
```

The parser should read characters from the command line until it reaches a `${` character sequence.  This is interpreted as a literal string (`$command_part_string`).

The parser should interpret any variable enclosed in `${`...`}` as a `$command_part_var`.

The `$expression` usually references declarations at the task level.  For example:

```wdl
task test {
  String flags
  command {
    ps ${flags}
  }
}
```

In this case `flags` within the `${`...`}` is an expression.  The `$expression` can also be more complex, like a function call: `write_lines(some_array_value)`

> **NOTE**: the `$expression` in this context can only evaluate to a primitive type (e.g. not `Array`, `Map`, or `Object`).  The only exception to this rule is when `sep` is specified as one of the `$var_option` fields

As another example, consider how the parser would parse the following command:

```
grep '${start}...${end}' ${input}
```

This command would be parsed as:

* `grep '` - command_part_string
* `${start}` - command_part_var
* `...` - command_part_string
* `${end}` - command_part_var
* `' ` - command_part_string
* `${input}` - command_part_var

#### Command Part Options

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$var_option = $var_option_key $ws* '=' $ws* $var_option_value
$var_option_key = 'sep' | 'true' | 'false' | 'quote' | 'default'
$var_option_value = $expression
```

The `$var_option` is a set of key-value pairs for any additional and less-used options that need to be set on a parameter.

##### sep

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

'sep' is interpreted as the separator string used to join multiple parameters together.  `sep` is only valid if the expression evaluates to an `Array`.

For example, if there were a declaration `Array[Int] ints = [1,2,3]`, the command `python script.py ${sep=',' numbers}` would yield the command line:

```
python script.py 1,2,3
```

Alternatively, if the command were `python script.py ${sep=' ' numbers}` it would parse to:

```
python script.py 1 2 3
```

> *Additional Requirements*:
>
> 1.  sep MUST accept only a string as its value

##### true and false

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

'true' and 'false' are only used for type Boolean and they specify what the parameter returns when the Boolean is true or false, respectively.

For example, `${true='--enable-foo', false='--disable-foo' Boolean yes_or_no}` would evaluate to either `--enable-foo` or `--disable-foo` based on the value of yes_or_no.

If either value is left out, then it's equivalent to specifying the empty string.  If the parameter is `${true='--enable-foo' Boolean yes_or_no}`, and a value of false is specified for this parameter, then the parameter will evaluate to the empty string.

> *Additional Requirement*:
>
> 1.  `true` and `false` values MUST be strings.
> 2.  `true` and `false` are only allowed if the type is `Boolean`

##### default

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

This specifies the default value if no other value is specified for this parameter.

```
task default_test {
  String? s
  command {
    ./my_cmd ${default="foobar" s}
  }
}
```

This task takes an optional `String` parameter and if a value is not specified, then the value of `foobar` will be used instead.

> *Additional Requirements*:
>
> 1.  The type of the expression must match the type of the parameter
> 2.  If 'default' is specified, the `$type_postfix_quantifier` for the variable's type MUST be `?`

#### Alternative heredoc syntax

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Sometimes a command is sufficiently long enough or might use `{` characters that using a different set of delimiters would make it more clear.  In this case, enclose the command in `<<<`...`>>>`, as follows:

```wdl
task heredoc {
  File in

  command<<<
  python <<CODE
    with open("${in}") as fp:
      for line in fp:
        if not line.startswith('#'):
          print(line.strip())
  CODE
  >>>
}
```

Parsing of this command should be the same as the prior section describes.

#### Stripping Leading Whitespace

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Any text inside of the `command` section, after instantiated, should have all *common leading whitespace* removed.  In the `task heredoc` example in the previous section, if the user specifies a value of `/path/to/file` as the value for `File in`, then the command should be:

```
python <<CODE
  with open("/path/to/file") as fp:
    for line in fp:
      if not line.startswith('#'):
        print(line.strip())
CODE
```

The 2-spaces that were common to each line were removed.

If the user mixes tabs and spaces, the behavior is undefined.  A warning is suggested, and perhaps a convention of 4 spaces per tab.  Other implementations might return an error in this case.

### Outputs Section

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

The outputs section defines which of the files and values should be exported after a successful run of this tool.

```
$task_output = 'output' $ws* '{' ($ws* $task_output_kv $ws*)* '}'
$task_output_kv = $type $identifier $ws* '=' $ws* $string
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

As with inputs, the outputs can reference previous outputs in the same block. The only requirement is that the output being referenced must be specified *before* the output which uses it.

```
output {
  String a = "a"
  String ab = a + "b"
}
```


Globs can be used to define outputs which contain many files.  The glob function generates an array of File outputs:

```
output {
  Array[File] output_bams = glob("*.bam")
}
```

### String Interpolation

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Within tasks, any string literal can use string interpolation to access the value of any of the task's inputs.  The most obvious example of this is being able to define an output file which is named as function of its input.  For example:

```wdl
task example {
  String prefix
  File bam
  command {
    python analysis.py --prefix=${prefix} ${bam}
  }
  output {
    File analyzed = "${prefix}.out"
    File bam_sibling = "${bam}.suffix"
  }
}
```

Any `${identifier}` inside of a string literal must be replaced with the value of the identifier.  If prefix were specified as `foobar`, then `"${prefix}.out"` would be evaluated to `"foobar.out"`.

### Runtime Section

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$runtime = 'runtime' $ws* '{' ($ws* $runtime_kv $ws*)* '}'
$runtime_kv = $identifier $ws* '=' $ws* $expression
```

The runtime section defines key/value pairs for runtime information needed for this task.  Individual backends will define which keys they will inspect so a key/value pair may or may not actually be honored depending on how the task is run.

Values can be any expression and it is up to the engine to reject keys and/or values that do not make sense in that context.  For example, consider the following WDL:

```wdl
task test {
  command {
    python script.py
  }
  runtime {
    docker: ["ubuntu:latest", "broadinstitute/scala-baseimage"]
  }
}
```

The value for the `docker` runtime attribute in this case is an array of values.  The parser should accept this.  Some engines might interpret it as an "either this image or that image" or could reject it outright.

Since values are expressions, they can also reference variables in the task:

```wdl
task test {
  String ubuntu_version

  command {
    python script.py
  }
  runtime {
    docker: "ubuntu:" + ubuntu_version
  }
}
```

Most key/value pairs are arbitrary.  However, the following keys have recommended conventions:

#### docker

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Location of a Docker image for which this task ought to be run.  This can have a format like `ubuntu:latest` or `broadinstitute/scala-baseimage` in which case it should be interpreted as an image on DockerHub (i.e. it is valid to use in a `docker pull` command).

```wdl
task docker_test {
  String arg

  command {
    python process.py ${arg}
  }
  runtime {
    docker: "ubuntu:latest"
  }
}
```

#### memory

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Memory requirements for this task.  Two kinds of values are supported for this attributes:

* `Int` - Intepreted as bytes
* `String` - This should be a decimal value with suffixes like `B`, `KB`, `MB` or binary suffixes `KiB`, `MiB`.  For example: `6.2 GB`, `5MB`, `2GiB`.

```wdl
task memory_test {
  String arg

  command {
    python process.py ${arg}
  }
  runtime {
    memory: "2GB"
  }
}
```

### Parameter Metadata Section

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$parameter_meta = 'parameter_meta' $ws* '{' ($ws* $parameter_meta_kv $ws*)* '}'
$parameter_meta_kv = $identifier $ws* '=' $ws* $string
```

This purely optional section contains key/value pairs where the keys are names of parameters and the values are string descriptions for those parameters.

> *Additional requirement*: Any key in this section MUST correspond to a parameter in the command line

### Metadata Section

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$meta = 'meta' $ws* '{' ($ws* $meta_kv $ws*)* '}'
$meta_kv = $identifier $ws* '=' $ws* $string
```

This purely optional section contains key/value pairs for any additional meta data that should be stored with the task.  For example, perhaps author or contact email.

### Examples

#### Example 1: Simplest Task

```wdl
task hello_world {
  command {echo hello world}
}
```

#### Example 2: Inputs/Outputs

```wdl
task one_and_one {
  String pattern
  File infile

  command {
    grep ${pattern} ${infile}
  }
  output {
    File filtered = stdout()
  }
}
```

#### Example 3: Runtime/Metadata

```wdl
task runtime_meta {
  String memory_mb
  String sample_id
  String param
  String sample_id

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

```wdl
task bwa_mem_tool {
  Int threads
  Int min_seed_length
  Int min_std_max_min
  File reference
  File reads

  command {
    bwa mem -t ${threads} \
            -k ${min_seed_length} \
            -I ${sep=',' min_std_max_min+} \
            ${reference} \
            ${sep=' ' reads+} > output.sam
  }
  output {
    File sam = "output.sam"
  }
  runtime {
    docker: "broadinstitute/baseimg"
  }
}
```

Notable pieces in this example is `${sep=',' min_std_max_min+}` which specifies that min_std_max_min can be one or more integers (the `+` after the variable name indicates that it can be one or more).  If an `Array[Int]` is passed into this parameter, then it's flattened by combining the elements with the separator character (`sep=','`).

This task also defines that it exports one file, called 'sam', which is the stdout of the execution of bwa mem.

The 'docker' portion of this task definition specifies which that this task must only be run on the Docker image specified.

#### Example 5: Word Count

```wdl
task wc2_tool {
  File file1
  command {
    wc ${file1}
  }
  output {
    Int count = read_int(stdout())
  }
}

workflow count_lines4_wf {
  Array[File] files
  scatter(f in files) {
    call wc2_tool {
      input: file1=f
    }
  }
  output {
    wc2_tool.count
  }
}
```

In this example, it's all pretty boilerplate, declarative code, except for some language-y like features, like `firstline(stdout)` and `append(list_of_count, wc2-tool.count)`.  These both can be implemented fairly easily if we allow for custom function definitions.  Parsing them is no problem.  Implementation would be fairly simple and new functions would not be hard to add.  Alternatively, this could be something like JavaScript or Python snippets that we run.

#### Example 6: tmap

This task should produce a command line like this:

```
tmap mapall \
stage1 map1 --min-seq-length 20 \
       map2 --min-seq-length 20 \
stage2 map1 --max-seq-length 20 --min-seq-length 10 --seed-length 16 \
       map2 --max-seed-hits -1 --max-seq-length 20 --min-seq-length 10
```

Task definition would look like this:

```wdl
task tmap_tool {
  Array[String] stages
  File reads

  command {
    tmap mapall ${sep=' ' stages} < ${reads} > output.sam
  }
  output {
    File sam = "output.sam"
  }
}
```

For this particular case where the command line is *itself* a mini DSL, The best option at that point is to allow the user to type in the rest of the command line, which is what `${sep=' ' stages+}` is for.  This allows the user to specify an array of strings as the value for `stages` and then it concatenates them together with a space character

|Variable|Value|
|--------|-----|
|reads   |/path/to/fastq|
|stages  |["stage1 map1 --min-seq-length 20 map2 --min-seq-length 20", "stage2 map1 --max-seq-length 20 --min-seq-length 10 --seed-length 16  map2 --max-seed-hits -1 --max-seq-length 20 --min-seq-length 10"]|

## Workflow Definition

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$workflow = 'workflow' $ws* '{' $ws* $workflow_element* $ws* '}'
$workflow_element = $call | $loop | $conditional | $declaration | $scatter | $parameter_meta | $meta
```

A workflow is defined as the keyword `workflow` and the body being in curly braces.

An example of a workflow that runs one task (not defined here) would be:

```wdl
workflow wf {
  Array[File] files
  Int threshold
  Map[String, String] my_map

  call analysis_job {
    input: search_paths=files, threshold=threshold, gender_lookup=my_map
  }
}
```

### Call Statement

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$call = 'call' $ws* $namespaced_identifier $ws+ ('as' $identifier)? $ws* $call_body?
$call_body = '{' $ws* $inputs? $ws* '}'
$inputs = 'input' $ws* ':' $ws* $variable_mappings
$variable_mappings = $variable_mapping_kv (',' $variable_mapping_kv)*
$variable_mapping_kv = $identifier $ws* '=' $ws* $expression
```

A workflow may call other tasks/workflows via the `call` keyword.  The `$namespaced_identifier` is the reference to which task to run.  Most commonly, it's simply the name of a task (see examples below), but it can also use `.` as a namespace resolver.

See the section on [Fully Qualified Names & Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers) for details about how the `$namespaced_identifier` ought to be interpreted

All `call` statements must be uniquely identifiable.  By default, the call's unique identifier is the task name (e.g. `call foo` would be referenced by name `foo`).  However, if one were to `call foo` twice in a workflow, each subsequent `call` statement will need to alias itself to a unique name using the `as` clause: `call foo as bar`.

A `call` statement may reference a workflow too (e.g. `call other_workflow`).  In this case, the `$inputs` section specifies a subset of the workflow's inputs and must specify fully qualified names.

```wdl
import "lib.wdl" as lib
workflow wf {
  call my_task
  call my_task as my_task_alias
  call my_task as my_task_alias2 {
    input: threshold=2
  }
  call lib.other_task
}
```

The `$call_body` is optional and is meant to specify how to satisfy a subset of the the task or workflow's input parameters as well as a way to map tasks outputs to variables defined in the [visible scopes](#scope).

A `$variable_mapping` in the `$inputs` section maps parameters in the task to expressions.  These expressions usually reference outputs of other tasks, but they can be arbitrary expressions.

As an example, here is a workflow in which the second task requires an output from the first task:

```wdl
task task1 {
  command {
    python do_stuff.py
  }
  output {
    File results = stdout()
  }
}
task task2 {
  File foobar
  command {
    python do_stuff2.py ${foobar}
  }
  output {
    File results = stdout()
  }
}
workflow wf {
  call task1
  call task2 {
    input: foobar=task1.results
  }
}
```

#### Sub Workflows

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Workflows can also be called inside of workflows.

`main.wdl`
```
import "sub_wdl.wdl" as sub

workflow main_workflow {

    call sub.wf_hello { input: wf_hello_input = "sub world" }
    
    output {
        String main_output = wf_hello.salutation
    }
}
```

`sub_wdl.wdl`
```
task hello {
  String addressee
  command {
    echo "Hello ${addressee}!"
  }
  runtime {
      docker: "ubuntu:latest"
  }
  output {
    String salutation = read_string(stdout())
  }
}

workflow wf_hello {
  String wf_hello_input
  
  call hello {input: addressee = wf_hello_input }
  
  output {
    String salutation = hello.salutation
  }
}
```

Note that because a wdl file can only contain 1 workflow, sub workflows can only be used through imports.
Otherwise, calling a workflow or a task is equivalent syntactically.
Inputs are specified and outputs retrieved the same way as they are for task calls.

### Scatter

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$scatter = 'scatter' $ws* '(' $ws* $scatter_iteration_statment $ws*  ')' $ws* $scatter_body
$scatter_iteration_statment = $identifier $ws* 'in' $ws* $expression
$scatter_body = '{' $ws* $workflow_element* $ws* '}'
```

A "scatter" clause defines that everything in the body (`$scatter_body`) can be run in parallel.  The clause in parentheses (`$scatter_iteration_statement`) declares which collection to scatter over and what to call each element.

The `$scatter_iteration_statement` has two parts: the "item" and the "collection".  For example, `scatter(x in y)` would define `x` as the item, and `y` as the collection.  The item is always an identifier, while the collection is an expression that MUST evaluate to an `Array` type.  The item will represent each item in that expression.  For example, if `y` evaluated to an `Array[String]` then `x` would be a `String`.

The `$scatter_body` defines a set of scopes that will execute in the context of this scatter block.

For example, if `$expression` is an array of integers of size 3, then the body of the scatter clause can be executed 3-times in parallel.  `$identifier` would refer to each integer in the array.

```
scatter(i in integers) {
  call task1{input: num=i}
  call task2{input: num=task1.output}
}
```

In this example, `task2` depends on `task1`.  Variable `i` has an implicit `index` attribute to make sure we can access the right output from `task1`.  Since both task1 and task2 run N times where N is the length of the array `integers`, any scalar outputs of these tasks is now an array.

### Loops

:pig2: Coming soon in [Cromwell](https://github.com/broadinstitute/cromwell)

```
$loop = 'while' '(' $expression ')' '{' $workflow_element* '}'
```

Loops are distinct from scatter clauses because the body of a while loop needs to be executed to completion before another iteration is considered for iteration.  The `$expression` condition is evaluated only when the iteration count is zero or if all `$workflow_element`s in the body have completed successfully for the current iteration.

### Conditionals

:pig2: Available in [Cromwell](https://github.com/broadinstitute/cromwell) version 24 and higher

```
$conditional = 'if' '(' $expression ')' '{' $workflow_element* '}'
```

Conditionals only execute the body if the expression evaluates to true.

* When a call's output is referenced outside the same containing `if` it will need to be handled as an optional type. E.g.
```
workflow foo {
  # Call 'x', producing a Boolean output:
  call x
  Boolean x_out = x.out

  # Call 'y', producing an Int output, in a conditional block:
  if (x_out) {
    call y
    Int y_out = y.out
  }
  
  # Outside the if block, we have to handle this output as optional:
  Int? y_out_maybe = y.out

  # Call 'z' which takes an optional Int input:
  call z { input: optional_int = y_out_maybe }
}
```
* Optional types can be coalesced by using the `select_all` and `select_first` array functions:
```
workflow foo {
  Array[Int] scatter_range = [1, 2, 3, 4, 5]
  scatter (i in scatter_range) {
    call x { input: i = i }
    if (x.validOutput) {
      Int x_out = x.out
    }
  }

  # Because it was declared inside the scatter and the if-block, the type of x_out is different here:
  Array[Int?] x_out_maybes = x_out

  # We can select only the valid elements with select_all:
  Array[Int] x_out_valids = select_all(x_out_maybes)

  # Or we can select the first valid element:
  Int x_out_first = select_first(x_out_maybes)
}
```

### Parameter Metadata

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$wf_parameter_meta = 'parameter_meta' $ws* '{' ($ws* $wf_parameter_meta_kv $ws*)* '}'
$wf_parameter_meta_kv = $identifier $ws* '=' $ws* $string
```

This purely optional section contains key/value pairs where the keys are names of parameters and the values are string descriptions for those parameters.

> *Additional requirement*: Any key in this section MUST correspond to a worflow input

As an example:
```
  parameter_meta {
    memory_mb: "Amount of memory to allocate to the JVM"
    param: "Some arbitrary parameter"
    sample_id: "The ID of the sample in format foo_bar_baz"
  }
```

### Metadata

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```
$wf_meta = 'meta' $ws* '{' ($ws* $wf_meta_kv $ws*)* '}'
$wf_meta_kv = $identifier $ws* '=' $ws* $string
```

This purely optional section contains key/value pairs for any additional meta data that should be stored with the workflow.  For example, perhaps author or contact email.

As an example:
```
  meta {
    author: "Joe Somebody"
    email: "joe@company.org"
  }
```

### Outputs

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Each `workflow` definition can specify an optional `output` section.  This section lists outputs from individual `call`s that you also want to expose as outputs to the `workflow` itself.
If the `output {...}` section is omitted, then the workflow includes all outputs from all calls in its final output.
Workflow outputs follow the same syntax rules as task outputs.
They can reference call outputs, workflow inputs and previous workflow outputs.
e.g:

```
task t {
  command {
    # do something
  }
  output {
    String out = "out"
  }
}

workflow w {
  String w_input = "some input"
  
  call t
  call t as u
  
  output {
    String t_out = t.out
    String u_out = u.out
    String input_as_output = w_input
    String previous_output = u_out
  }
}
```

Note that they can't reference call inputs. However this can be achieved by declaring the desired call input as an output.
Expressions are allowed.

When declaring a workflow output that points to a call inside a scatter, the aggregated call is used.
e.g:

```
task t {
  command {
    # do something
  }
  output {
    String out = "out"
  }
}

workflow w {
  Array[Int] arr = [1, 2]
  
  scatter(i in arr) {
    call t
  }
  
  output {
    Array[String] t_out = t.out
  }
}
```

`t_out` has an `Array[String]` result type, because `call t` is inside a scatter.

*THE FOLLOWING SYNTAX IS DEPRECATED BUT IS STILL SUPPORTED TO MAINTAIN BACKWARD COMPATIBILITY*
```
$workflow_output = 'output' '{' ($workflow_output_fqn ($workflow_output_fqn)* '}'
$workflow_output_fqn = $fully_qualified_name '.*'?
```

Replacing call output names with a `*` acts as a match-all wildcard. 

The output names in this section must be qualified with the call which created them, as in the example below.

```
task task1 {
  command { ./script }
  output { File results = stdout() }
}

task task2 {
  command { ./script2 }
  output {
    File results = stdout()
    String value = read_string("some_file")
  }
}

workflow wf {
  call task1
  call task2 as altname
  output {
    task1.*
    altname.value
  }
}
```

In this example, the fully-qualified names that would be exposed as workflow outputs would be `wf.task1.results`, `wf.altname.value`.

# Namespaces

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Import statements can be used to pull in tasks/workflows from other locations as well as to create namespaces.  In the simplest case, an import statement adds the tasks/workflows that are imported into the specified namespace.  For example:

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
import "tasks.wdl" as pyTasks

workflow wf {
  call pyTasks.x
  call pyTasks.y
}
```

Tasks `x` and `y` are inside the namespace `pyTasks`, which is different from the `wf` namespace belonging to the primary workflow.  However, if no namespace is specified for tasks.wdl:

workflow.wdl
```
import "tasks.wdl"

workflow wf {
  call tasks.x
  call tasks.y
}
```

Now everything inside of `tasks.wdl` must be accessed through the default namespace `tasks`.

Each namespace may contain namespaces, tasks, and at most one workflow.  The names of the contained namespaces, tasks, and workflow need to be unique within that namespace. For example, one cannot import two workflows while they have the same namespace identifier. Additionally, a workflow and a namespace both named `foo` cannot exist inside a common namespace. Similarly there cannot be a task `foo` in a workflow also named `foo`.
However, you can import two workflows with different namespace identifiers that have identically named tasks. For example, you can import namespaces `foo` and `bar`, both of which contain a task `baz`, and you can call `foo.baz` and `bar.baz` from the same primary workflow.

# Scope

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Scopes are defined as:

* `workflow {...}` blocks
* `call` blocks
* `while(expr) {...}` blocks
* `if(expr) {...}` blocks
* `scatter(x in y) {...}` blocks

Inside of any scope, variables may be [declared](#declarations).  The variables declared in that scope are visible to any sub-scope, recursively.  For example:

```
task my_task {
  Int x
  File f
  command {
    my_cmd --integer=${var} ${f}
  }
}

workflow wf {
  Array[File] files
  Int x = 2
  scatter(file in files) {
    Int x = 3
    call my_task {
      Int x = 4
      input: var=x, f=file
    }
  }
}
```

`my_task` will use `x=4` to set the value for `var` in its command line.  However, `my_task` also needs a value for `x` which is defined at the task level.  Since `my_task` has two inputs (`x` and `var`), and only one of those is set in the `call my_task` declaration, the value for `my_task.x` still needs to be provided by the user when the workflow is run.

# Optional Parameters & Type Constraints

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

[Types](#types) can be optionally suffixed with a `?` or `+` in certain cases.

* `?` means that the parameter is optional.  A user does not need to specify a value for the parameter in order to satisfy all the inputs to the workflow.
* `+` applies only to `Array` types and it represents a constraint that the `Array` value must containe one-or-more elements.

```
task test {
  Array[File]  a
  Array[File]+ b
  Array[File]? c
  #File+ d <-- can't do this, + only applies to Arrays

  command {
    /bin/mycmd ${sep=" " a}
    /bin/mycmd ${sep="," b}
    /bin/mycmd ${write_lines(c)}
  }
}

workflow wf {
  call test
}
```

If you provided these values for inputs:

|var      |value|
|---------|-----|
|wf.test.a|["1", "2", "3"]|
|wf.test.b|[]|

The workflow engine should reject this because `wf.test.b` is required to have at least one element.  If we change it to:

|var      |value|
|---------|-----|
|wf.test.a|["1", "2", "3"]|
|wf.test.b|["x"]|

This would be valid input because `wf.test.c` is not required.  Given these values, the command would be instantiated as:

```
/bin/mycmd 1 2 3
/bin/mycmd x
/bin/mycmd
```

If our inputs were:

|var      |value|
|---------|-----|
|wf.test.a|["1", "2", "3"]|
|wf.test.b|["x","y"]|
|wf.test.c|["a","b","c","d"]|

Then the command would be instantiated as:

```
/bin/mycmd 1 2 3
/bin/mycmd x,y
/bin/mycmd /path/to/c.txt
```

## Prepending a String to an Optional Parameter

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Sometimes, optional parameters need a string prefix.  Consider this task:

```wdl
task test {
  String? val
  command {
    python script.py --val=${val}
  }
}
```

Since `val` is optional, this command line can be instantiated in two ways:

```
python script.py --val=foobar
```

Or

```
python script.py --val=
```

The latter case is very likely an error case, and this `--val=` part should be left off if a value for `val` is omitted.  To solve this problem, modify the expression inside the template tag as follows:

```
python script.py ${"--val=" + val}
```

# Scatter / Gather

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

The `scatter` block is meant to parallelize a series of identical tasks but give them slightly different inputs.  The simplest example is:

```wdl
task inc {
  Int i

  command <<<
  python -c "print(${i} + 1)"
  >>>

  output {
    Int incremented = read_int(stdout())
  }
}

workflow wf {
  Array[Int] integers = [1,2,3,4,5]
  scatter(i in integers) {
    call inc{input: i=i}
  }
}
```

Running this workflow (which needs no inputs), would yield a value of `[2,3,4,5,6]` for `wf.inc`.  While `task inc` itself returns an `Int`, when it is called inside a scatter block, that type becomes an `Array[Int]`.

Any task that's downstream from the call to `inc` and outside the scatter block must accept an `Array[Int]`:


```wdl
task inc {
  Int i

  command <<<
  python -c "print(${i} + 1)"
  >>>

  output {
    Int incremented = read_int(stdout())
  }
}

task sum {
  Array[Int] ints

  command <<<
  python -c "print(${sep="+" ints})"
  >>>

  output {
    Int sum = read_int(stdout())
  }
}

workflow wf {
  Array[Int] integers = [1,2,3,4,5]
  scatter (i in integers) {
    call inc {input: i=i}
  }
  call sum {input: ints = inc.increment}
}
```

This workflow will output a value of `20` for `wf.sum.sum`.  This works because `call inc` will output an `Array[Int]` because it is in the scatter block.

However, from inside the scope of the scatter block, the output of `call inc` is still an `Int`.  So the following is valid:

```wdl
workflow wf {
  Array[Int] integers = [1,2,3,4,5]
  scatter(i in integers) {
    call inc {input: i=i}
    call inc as inc2 {input: i=inc.incremented}
  }
  call sum {input: ints = inc2.increment}
}
```

In this example, `inc` and `inc2` are being called in serial where the output of one is fed to another.  inc2 would output the array `[3,4,5,6,7]`

# Variable Resolution

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Inside of [expressions](#expressions), variables are resolved differently depending on if the expression is in a `task` declaration or a `workflow` declaration

## Task-Level Resolution

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Inside a task, resolution is trivial: The variable referenced MUST be a [declaration](#declarations) of the task.  For example:

```wdl
task my_task {
  Array[String] strings
  command {
    python analyze.py --strings-file=${write_lines(strings)}
  }
}
```

Inside of this task, there exists only one expression: `write_lines(strings)`.  In here, when the expression evaluator tries to resolve `strings`, which must be a declaration of the task (in this case it is).

## Workflow-Level Resolution

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

In a workflow, resolution works by traversing the scope heirarchy starting from expression that references the variable.

```wdl
workflow wf {
  String s = "wf_s"
  String t = "t"
  call my_task {
    String s = "my_task_s"
    input: in0 = s+"-suffix", in1 = t+"-suffix"
  }
}
```

In this example, there are two expressions: `s+"-suffix"` and `t+"-suffix"`.  `s` is resolved as `"my_task_s"` and `t` is resolved as `"t"`.

# Computing Inputs

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Both tasks and workflows have a typed inputs that must be satisfied in order to run.  The following sections describe how to compute inputs for `task` and `workflow` declarations

## Task Inputs

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Tasks define all their inputs as declarations at the top of the task definition.

```wdl
task test {
  String s
  Int i
  Float f

  command {
    ./script.sh -i ${i} -f ${f}
  }
}
```

In this example, `s`, `i`, and `f` are inputs to this task.  Even though the command line does not reference `${s}`.  Implementations of WDL engines may display a warning or report an error in this case, since `s` isn't used.

## Workflow Inputs

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Workflows have declarations, like tasks, but a workflow must also account for all calls to sub-tasks when determining inputs.

Workflows also return their inputs as fully qualified names.  Tasks only return the names of the variables as inputs (as they're guaranteed to be unique within a task).  However, since workflows can call the same task twice, names might collide.  The general algorithm for computing inputs going something like this:

* Take all inputs to all `call` statements in the workflow
* Subtract out all inputs that are satisfied through the `input: ` section
* Add in all declarations which don't have a static value defined

Consider the following workflow:

```wdl
task t1 {
  String s
  Int x

  command {
    ./script --action=${s} -x${x}
  }
  output {
    Int count = read_int(stdout())
  }
}

task t2 {
  String s
  Int t
  Int x

  command {
    ./script2 --action=${s} -x${x} --other=${t}
  }
  output {
    Int count = read_int(stdout())
  }
}

task t3 {
  Int y
  File ref_file # Do nothing with this

  command {
    python -c "print(${y} + 1)"
  }
  output {
    Int incr = read_int(stdout())
  }
}

workflow wf {
  Int int_val
  Int int_val2 = 10
  Array[Int] my_ints
  File ref_file

  call t1 {
    input: x=int_val
  }
  call t2 {
    input: x=int_val, t=t1.count
  }
  scatter(i in my_ints) {
    call t3 {
      input: y=i, ref=ref_file
    }
  }
}
```

The inputs to `wf` would be:

* `wf.t1.s` as a `String`
* `wf.t2.s` as a `String`
* `wf.int_val` as an `Int`
* `wf.my_ints` as an `Array[Int]`
* `wf.ref_file` as a `File`

## Specifying Workflow Inputs in JSON

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Once workflow inputs are computed (see previous section), the value for each of the fully-qualified names needs to be specified per invocation of the workflow.  Workflow inputs are specified in JSON or YAML format.  In JSON, the inputs to the workflow in the previous section can be:

```
{
  "wf.t1.s": "some_string",
  "wf.t2.s": "some_string",
  "wf.int_val": 3,
  "wf.my_ints": [5,6,7,8],
  "wf.ref_file": "/path/to/file.txt"
}
```

It's important to note that the type in JSON must be coercable to the WDL type.  For example `wf.int_val` expects an integer, but if we specified it in JSON as `"wf.int_val": "3"`, this coercion from string to integer is not valid and would result in a type error.  See the section on [Type Coercion](#type-coercion) for more details.

# Type Coercion

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

WDL values can be created from either JSON values or from native language values.  The below table references String-like, Integer-like, etc to refer to values in a particular programming language.  For example, "String-like" could mean a `java.io.String` in the Java context or a `str` in Python.  An "Array-like" could refer to a `Seq` in Scala or a `list` in Python.

|WDL Type |Can Accept   |Notes / Constraints|
|---------|-------------|-------------------|
|`String` |JSON String||
|         |String-like||
|         |`String`|Identity coercion|
|         |`File`||
|`File`   |JSON String|Interpreted as a file path|
|         |String-like|Interpreted as file path|
|         |`String`|Interpreted as file path|
|         |`File`|Identity Coercion|
|`Int`    |JSON Number|Use floor of the value for non-integers|
|         |Integer-like||
|         |`Int`|Identity coercion|
|`Float`  |JSON Number||
|         |Float-like||
|         |`Float`|Identity coercion|
|`Boolean`|JSON Boolean||
|         |Boolean-like||
|         |`Boolean`|Identity coercion|
|`Array[T]`|JSON Array|Elements must be coercable to `T`|
|          |Array-like|Elements must be coercable to `T`|
|`Map[K, V]`|JSON Object|keys and values must be coercable to `K` and `V`, respectively|
|           |Map-like|keys and values must be coercable to `K` and `V`, respectively|

# Standard Library

## File stdout()

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Returns a `File` reference to the stdout that this task generated.

## File stderr()

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Returns a `File` reference to the stderr that this task generated.

## Array[String] read_lines(String|File)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given a file-like object (`String`, `File`) as a parameter, this will read each line as a string and return an `Array[String]` representation of the lines in the file.

The order of the lines in the returned `Array[String]` must be the order in which the lines appear in the file-like object.

This task would `grep` through a file and return all strings that matched the pattern:

```wdl
task do_stuff {
  String pattern
  File file
  command {
    grep '${pattern}' ${file}
  }
  output {
    Array[String] matches = read_lines(stdout())
  }
}
```

## Array[Array[String]] read_tsv(String|File)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

the `read_tsv()` function takes one parameter, which is a file-like object (`String`, `File`) and returns an `Array[Array[String]]` representing the table from the TSV file.

If the parameter is a `String`, this is assumed to be a local file path relative to the current working directory of the task.

For example, if I write a task that outputs a file to `./results/file_list.tsv`, and my task is defined as:

```wdl
task do_stuff {
  File file
  command {
    python do_stuff.py ${file}
  }
  output {
    Array[Array[String]] output_table = read_tsv("./results/file_list.tsv")
  }
}
```

Then when the task finishes, to fulfull the `outputs_table` variable, `./results/file_list.tsv` must be a valid TSV file or an error will be reported.

## Map[String, String] read_map(String|File)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given a file-like object (`String`, `File`) as a parameter, this will read each line from a file and expect the line to have the format `col1\tcol2`.  In other words, the file-like object must be a two-column TSV file.

This task would `grep` through a file and return all strings that matched the pattern:

The following task would write a two-column TSV to standard out and that would be interpreted as a `Map[String, String]`:

```wdl
task do_stuff {
  String flags
  File file
  command {
    ./script --flags=${flags} ${file}
  }
  output {
    Map[String, String] mapping = read_map(stdout())
  }
}
```

## Object read_object(String|File)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given a file-like object that contains a 2-row and n-column TSV file, this function will turn that into an Object.

```wdl
task test {
  command <<<
    python <<CODE
    print('\t'.join(["key_{}".format(i) for i in range(3)]))
    print('\t'.join(["value_{}".format(i) for i in range(3)]))
    CODE
  >>>
  output {
    Object my_obj = read_object(stdout())
  }
}
```

The command will output to stdout the following:

```
key_1\tkey_2\tkey_3
value_1\tvalue_2\tvalue_3
```

Which would be turned into an `Object` in WDL that would look like this:

|Attribute|Value|
|---------|-----|
|key_1    |"value_1"|
|key_2    |"value_2"|
|key_3    |"value_3"|

## Array[Object] read_objects(String|File)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given a file-like object that contains a 2-row and n-column TSV file, this function will turn that into an Object.

```wdl
task test {
  command <<<
    python <<CODE
    print('\t'.join(["key_{}".format(i) for i in range(3)]))
    print('\t'.join(["value_{}".format(i) for i in range(3)]))
    print('\t'.join(["value_{}".format(i) for i in range(3)]))
    print('\t'.join(["value_{}".format(i) for i in range(3)]))
    CODE
  >>>
  output {
    Array[Object] my_obj = read_objects(stdout())
  }
}
```

The command will output to stdout the following:

```
key_1\tkey_2\tkey_3
value_1\tvalue_2\tvalue_3
value_1\tvalue_2\tvalue_3
value_1\tvalue_2\tvalue_3
```

Which would be turned into an `Array[Object]` in WDL that would look like this:

|Index|Attribute|Value|
|-----|---------|-----|
|0    |key_1    |"value_1"|
|     |key_2    |"value_2"|
|     |key_3    |"value_3"|
|1    |key_1    |"value_1"|
|     |key_2    |"value_2"|
|     |key_3    |"value_3"|
|2    |key_1    |"value_1"|
|     |key_2    |"value_2"|
|     |key_3    |"value_3"|

## mixed read_json(String|File)

:pig2: Coming soon in [Cromwell](https://github.com/broadinstitute/cromwell)

the `read_json()` function takes one parameter, which is a file-like object (`String`, `File`) and returns a data type which matches the data structure in the JSON file.  The mapping of JSON type to WDL type is:

|JSON Type|WDL Type|
|---------|--------|
|object|`Map[String, ?]`|
|array|`Array[?]`|
|number|`Int` or `Float`|
|string|`String`|
|boolean|`Boolean`|
|null|???|

If the parameter is a `String`, this is assumed to be a local file path relative to the current working directory of the task.

For example, if I write a task that outputs a file to `./results/file_list.json`, and my task is defined as:

```wdl
task do_stuff {
  File file
  command {
    python do_stuff.py ${file}
  }
  output {
    Map[String, String] output_table = read_json("./results/file_list.json")
  }
}
```

Then when the task finishes, to fulfull the `output_table` variable, `./results/file_list.json` must be a valid TSV file or an error will be reported.

## Int read_int(String|File)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

The `read_int()` function takes a file path which is expected to contain 1 line with 1 integer on it.  This function returns that integer.

## String read_string(String|File)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

The `read_string()` function takes a file path which is expected to contain 1 line with 1 string on it.  This function returns that string.

No trailing newline characters should be included

## Float read_float(String|File)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

The `read_float()` function takes a file path which is expected to contain 1 line with 1 floating point number on it.  This function returns that float.

## Boolean read_boolean(String|File)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

The `read_boolean()` function takes a file path which is expected to contain 1 line with 1 Boolean value (either "true" or "false" on it).  This function returns that Boolean value.

## File write_lines(Array[String])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given something that's compatible with `Array[String]`, this writes each element to it's own line on a file.  with newline `\n` characters as line separators.

```wdl
task example {
  Array[String] array = ["first", "second", "third"]
  command {
    ./script --file-list=${write_lines(array)}
  }
}
```

If this task were run, the command might look like:

```
./script --file-list=/local/fs/tmp/array.txt
```

And `/local/fs/tmp/array.txt` would contain:

```
first
second
third
```

## File write_tsv(Array[Array[String]])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given something that's compatible with `Array[Array[String]]`, this writes a TSV file of the data structure.

```wdl
task example {
  Array[String] array = [["one", "two", "three"], ["un", "deux", "trois"]]
  command {
    ./script --tsv=${write_tsv(array)}
  }
}
```

If this task were run, the command might look like:

```
./script --tsv=/local/fs/tmp/array.tsv
```

And `/local/fs/tmp/array.tsv` would contain:

```
one\ttwo\tthree
un\tdeux\ttrois
```

## File write_map(Map[String, String])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given something that's compatible with `Map[String, String]`, this writes a TSV file of the data structure.

```wdl
task example {
  Map[String, String] map = {"key1": "value1", "key2": "value2"}
  command {
    ./script --map=${write_map(map)}
  }
}
```

If this task were run, the command might look like:

```
./script --tsv=/local/fs/tmp/map.tsv
```

And `/local/fs/tmp/map.tsv` would contain:

```
key1\tvalue1
key2\tvalue2
```

## File write_object(Object)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given any `Object`, this will write out a 2-row, n-column TSV file with the object's attributes and values.

```
task test {
  Object input
  command <<<
    /bin/do_work --obj=${write_object(input)}
  >>>
  output {
    File results = stdout()
  }
}
```

if `input` were to have the value:

|Attribute|Value|
|---------|-----|
|key_1    |"value_1"|
|key_2    |"value_2"|
|key_3    |"value_3"|

The command would instantiate to:

```
/bin/do_work --obj=/path/to/input.tsv
```

Where `/path/to/input.tsv` would contain:

```
key_1\tkey_2\tkey_3
value_1\tvalue_2\tvalue_3
```

## File write_objects(Array[Object])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given any `Array[Object]`, this will write out a 2+ row, n-column TSV file with each object's attributes and values.

```wdl
task test {
  Array[Object] in
  command <<<
    /bin/do_work --obj=${write_objects(in)}
  >>>
  output {
    File results = stdout()
  }
}
```

if `in` were to have the value:

|Index|Attribute|Value|
|-----|---------|-----|
|0    |key_1    |"value_1"|
|     |key_2    |"value_2"|
|     |key_3    |"value_3"|
|1    |key_1    |"value_4"|
|     |key_2    |"value_5"|
|     |key_3    |"value_6"|
|2    |key_1    |"value_7"|
|     |key_2    |"value_8"|
|     |key_3    |"value_9"|

The command would instantiate to:

```
/bin/do_work --obj=/path/to/input.tsv
```

Where `/path/to/input.tsv` would contain:

```
key_1\tkey_2\tkey_3
value_1\tvalue_2\tvalue_3
value_4\tvalue_5\tvalue_6
value_7\tvalue_8\tvalue_9
```

## File write_json(mixed)

:pig2: Coming soon in [Cromwell](https://github.com/broadinstitute/cromwell)

Given something with any type, this writes the JSON equivalent to a file.  See the table in the definition of [read_json()](#mixed-read_jsonstringfile)

```wdl
task example {
  Map[String, String] map = {"key1": "value1", "key2": "value2"}
  command {
    ./script --map=${write_json(map)}
  }
}
```

If this task were run, the command might look like:

```
./script --tsv=/local/fs/tmp/map.json
```

And `/local/fs/tmp/map.json` would contain:

```
{
  "key1": "value1"
  "key2": "value2"
}
```

## Float size(File, [String])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given a `File` and a `String` (optional), returns the size of the file in Bytes or in the unit specified by the second argument.

```wdl
task example {
  File input_file
  
  command {
    echo "this file is 22 bytes" > created_file
  }
  
  output {
    Float input_file_size = size(input_file)
    Float created_file_size = size("created_file") # 22.0
    Float created_file_size_in_KB = size("created_file", "K") # 0.022
  }
}
```

Supported units are KiloByte ("K", "KB"), MegaByte ("M", "MB"), GigaByte ("G", "GB"), TeraByte ("T", "TB") as well as their [binary version](https://en.wikipedia.org/wiki/Binary_prefix) "Ki" ("KiB"), "Mi" ("MiB"), "Gi" ("GiB"), "Ti" ("TiB").
Default unit is Bytes ("B").


## String sub(String, String, String)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given 3 String parameters `input`, `pattern`, `replace`, this function will replace any occurrence matching `pattern` in `input` by `replace`.
`pattern` is expected to be a [regular expression](https://en.wikipedia.org/wiki/Regular_expression). Details of regex evaluation will depend on the execution engine running the WDL.

Example 1:

```wdl
  String chocolike = "I like chocolate when it's late"

  String chocolove = sub(chocolike, "like", "love") # I love chocolate when it's late
  String chocoearly = sub(chocolike, "late", "early") # I like chocoearly when it's early
  String chocolate = sub(chocolike, "late$", "early") # I like chocolate when it's early
}
```

The sub function will also accept `input` and `replace` parameters that can be coerced to a String (e.g. File). This can be useful to swap the extension of a filename for example

Example 2:

```wdl
  task example {
  File input_file = "my_input_file.bam"
  String output_file_name = sub(input_file, "\\.bam$", ".index") # my_input_file.index

  command {
    echo "I want an index instead" > ${output_file_name}
  }

  output {
    File outputFile = output_file_name
  }
}
```

## Array[Int] range(Int)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given an integer argument, the `range` function creates an array of integers of length equal to the given argument. For example `range(3)` provides the array: `(0, 1, 2)`.

## Array[Array[X]] transpose(Array[Array[X]])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given a two dimensional array argument, the `transpose` function transposes the two dimensional array according to the standard matrix transpose rules. For example `transpose( ((0, 1, 2), (3, 4, 5)) )` will return the rotated two-dimensional array: `((0, 3), (1, 4), (2, 5))`.

## Array[Pair[X,Y]] zip(Array[X], Array[Y])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given any two Object types, the `zip` function returns the dot product of those Object types in the form of a Pair object.

```
Pair[Int, String] p = (0, "z")
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b", "c" ]
Array[String] zs = [ "d", "e" ]

Array[Pair[Int, String]] zipped = zip(xs, ys)     # i.e.  zipped = [ (1, "a"), (2, "b"), (3, "c") ]
```

## Array[Pair[X,Y]] cross(Array[X], Array[Y])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given any two Object types, the `cross` function returns the cross product of those Object types in the form of a Pair object.

```
Pair[Int, String] p = (0, "z")
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b", "c" ]
Array[String] zs = [ "d", "e" ]

Array[Pair[Int, String]] crossed = cross(xs, zs) # i.e. crossed = [ (1, "d"), (1, "e"), (2, "d"), (2, "e"), (3, "d"), (3, "e") ]
```

## Integer length(Array[X])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given an Array, the `length` function returns the number of elements in the Array as an Integer.

```
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b", "c" ]
Array[String] zs = [ ]

Integer xlen = length(xs) # 3
Integer ylen = length(ys) # 3
Integer zlen = length(zs) # 0
```

## Array[String] prefix(String, Array[X])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given a String and an Array[X] where X is a primitive type, the `prefix` function returns an array of strings comprised
of each element of the input array prefixed by the specified prefix string.  For example:

```
Array[String] env = ["key1=value1", "key2=value2", "key3=value3"]
Array[String] env_param = prefix("-e ", env) # ["-e key1=value1", "-e key2=value2", "-e key3=value3"]

Array[Integer] env2 = [1, 2, 3]
Array[String] env2_param = prefix("-f ", env2) # ["-f 1", "-f 2", "-f 3"]
```

## X select_first(Array[X?])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given an array of optional values, `select_first` will select the first defined value and return it. Note that this is a runtime check and requires that at least one defined value will exist: if no defined value is found when select_first is evaluated, the workflow will fail.

## Array[X] select_all(Array[X?])

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Given an array of optional values, `select_all` will select only those elements which are defined.

## Boolean defined(X?)

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

This function will return `false` if the argument is an unset optional value. It will return `true` in all other cases.

## String basename(String)

:pig2: [Supported in Cromwell 27](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

- This function returns the basename of a file path passed to it: `basename("/path/to/file.txt")` returns `"file.txt"`.
- Also supports an optional parameter, suffix to remove: `basename("/path/to/file.txt", ".txt")` returns `"file"`.

## Int floor(Float), Int ceil(Float) and Int round(Float)

:pig2: [Supported in Cromwell 28](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

- These functions convert a Float value into an Int by:
  - floor: Round **down** to the next lower integer
  - ceil: Round **up** to the next higher integer
  - round: Round to the nearest integer based on standard rounding rules

# Data Types & Serialization

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Tasks and workflows are given values for their input parameters in order to run.  The type of each of those input parameters are declarations on the `task` or `workflow`.  Those input parameters can be any [valid type](#types):

Primitive Types:

* String
* Int
* Float
* File
* Boolean

Compound Types:

* Array
* Map
* Object
* Pair

When a WDL workflow engine instantiates a command specified in the `command` section of a `task`, it must serialize all `${...}` tags in the command into primitive types.

For example, if I'm writing a tool that operates on a list of FASTQ files, there are a variety of ways that this list can be passed to that task:

* A file containing one file path per line (e.g. `Rscript analysis.R --files=fastq_list.txt`)
* A file containing a JSON list (e.g. `Rscript analysis.R --files=fastq_list.json`)
* Enumerated on the command line (e.g. (`Rscript analysis.R 1.fastq 2.fastq 3.fastq`)

Each of these methods has its merits and one method might be better for one tool while another method would be better for another tool.

On the other end, tasks need to be able to communicate data structures back to the workflow engine.  For example, let's say this same tool that takes a list of FASTQs wants to return back a `Map[File, Int]` representing the number of reads in each FASTQ.  A tool might choose to output it as a two-column TSV or as a JSON object and WDL needs to know how to convert that to the proper data type.

WDL provides some [standard library functions](#standard-library) for converting compound types like `Array` into primitive types, like `File`.

When a task finishes, the `output` section defines how to convert the files and stdout/stderr into WDL types.  For example,

```wdl
task test {
  Array[File] files
  command {
    Rscript analysis.R --files=${sep=',' files}
  }
  output {
    Array[String] strs = read_lines(stdout())
  }
}
```

Here, the expression `read_lines(stdout())` says "take the output from stdout, break into lines, and return that result as an Array[String]".  See the definition of [read_lines](#arraystring-read_linesstringfile) and [stdout](#file-stdout) for more details.

## Serialization of Task Inputs

### Primitive Types

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Serializing primitive inputs into strings is intuitively easy because the value is just turned into a string and inserted into the command line.

Consider this example:

```wdl
task output_example {
  String s
  Int i
  Float f

  command {
    python do_work.py ${s} ${i} ${f}
  }
}
```

If I provide values for the declarations in the task as:

|var|value|
|---|-----|
|s  |"str"|
|i  |2    |
|f  |1.3  |

Then, the command would be instantiated as:

```
python do_work.py str 2 1.3
```

### Compound Types

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Compound types, like `Array` and `Map` must be converted to a primitive type before it can be used in the command.  There are many ways to turn a compound types into primitive types, as laid out in following sections

#### Array serialization

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Arrays can be serialized in two ways:

* **Array Expansion**: elements in the list are flattened to a string with a separator character.
* **File Creation**: create a file with the elements of the array in it and passing that file as the parameter on the command line.

##### Array serialization by expansion

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

The array flattening approach can be done if a parameter is specified as `${sep=' ' my_param}`.  `my_param` must be declared as an `Array` of primitive types.  When the value of `my_param` is specified, then the values are joined together with the separator character (a space in this case).  For example:

```wdl
task test {
  Array[File] bams
  command {
    python script.py --bams=${sep=',' bams}
  }
}
```

If passed an array for the value of `bams`:

|Element       |
|--------------|
|/path/to/1.bam|
|/path/to/2.bam|
|/path/to/3.bam|

Would produce the command `python script.py --bams=/path/to/1.bam,/path/to/2.bam,/path/to/1.bam`

##### Array serialization using write_lines()

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

An array may be turned into a file with each element in the array occupying a line in the file.

```wdl
task test {
  Array[File] bams
  command {
    sh script.sh ${write_lines(bams)}
  }
}
```

if `bams` is given this array:

|Element       |
|--------------|
|/path/to/1.bam|
|/path/to/2.bam|
|/path/to/3.bam|

Then, the resulting command line could look like:

```
sh script.sh /jobs/564758/bams
```

Where `/jobs/564758/bams` would contain:

```
/path/to/1.bam
/path/to/2.bam
/path/to/3.bam
```

##### Array serialization using write_json()

:pig2: Coming soon in [Cromwell](https://github.com/broadinstitute/cromwell)

The array may be turned into a JSON document with the file path for the JSON file passed in as the parameter:

```wdl
task test {
  Array[File] bams
  command {
    sh script.sh ${write_json(bams)}
  }
}
```

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

#### Map serialization

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Map types cannot be serialized on the command line directly and must be serialized through a file

##### Map serialization using write_map()

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

The map type can be serialized as a two-column TSV file and the parameter on the command line is given the path to that file, using the `write_map()` function:

```wdl
task test {
  Map[String, Float] sample_quality_scores
  command {
    sh script.sh ${write_map(sample_quality_scores)}
  }
}
```

if `sample_quality_scores` is given this Map[String, Float] as:

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

##### Map serialization using write_json()

:pig2: Coming soon in [Cromwell](https://github.com/broadinstitute/cromwell)

The map type can also be serialized as a JSON file and the parameter on the command line is given the path to that file, using the `write_json()` function:

```wdl
task test {
  Map[String, Float] sample_quality_scores
  command {
    sh script.sh ${write_json(sample_quality_scores)}
  }
}
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

#### Object serialization

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

An object is a more general case of a map where the keys are strings and the values are of arbitrary types and treated as strings.  Objects can be serialized with either `write_object()` or `write_json()` functions:

##### Object serialization using write_object()

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

```wdl
task test {
  Object sample
  command {
    perl script.pl ${write_object(sample)}
  }
}
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

##### Object serialization using write_json()

:pig2: Coming soon in [Cromwell](https://github.com/broadinstitute/cromwell)

```wdl
task test {
  Object sample
  command {
    perl script.pl ${write_json(sample)}
  }
}
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
#### Array[Object] serialization

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

`Array[Object]` must guarantee that all objects in the array have the same set of attributes.  These can be serialized with either `write_objects()` or `write_json()` functions, as described in following sections.

##### Array[Object] serialization using write_objects()

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

an `Array[Object]` can be serialized using `write_objects()` into a TSV file:

```wdl
task test {
  Array[Object] sample
  command {
    perl script.pl ${write_objects(sample)}
  }
}
```

if sample is provided as:

|Index|Attribute|Value  |
|-----|---------|-------|
|0    |attr1    |value1 |
|     |attr2    |value2 |
|     |attr3    |value3 |
|     |attr4    |value4 |
|1    |attr1    |value5 |
|     |attr2    |value6 |
|     |attr3    |value7 |
|     |attr4    |value8 |

Then, the resulting command line could look like:

```
perl script.pl /jobs/564759/sample.tsv
```

Where `/jobs/564759/sample.tsv` would contain:

```
attr1\tattr2\tattr3\tattr4
value1\tvalue2\tvalue3\tvalue4
value5\tvalue6\tvalue7\tvalue8
```

##### Array[Object] serialization using write_json()

:pig2: Coming soon in [Cromwell](https://github.com/broadinstitute/cromwell)

an `Array[Object]` can be serialized using `write_json()` into a JSON file:

```wdl
task test {
  Array[Object] sample
  command {
    perl script.pl ${write_json(sample)}
  }
}
```

if sample is provided as:

|Index|Attribute|Value  |
|-----|---------|-------|
|0    |attr1    |value1 |
|     |attr2    |value2 |
|     |attr3    |value3 |
|     |attr4    |value4 |
|1    |attr1    |value5 |
|     |attr2    |value6 |
|     |attr3    |value7 |
|     |attr4    |value8 |

Then, the resulting command line could look like:

```
perl script.pl /jobs/564759/sample.json
```

Where `/jobs/564759/sample.json` would contain:

```
[
  {
    "attr1": "value1",
    "attr2": "value2",
    "attr3": "value3",
    "attr4": "value4"
  },
  {
    "attr1": "value5",
    "attr2": "value6",
    "attr3": "value7",
    "attr4": "value8"
  }
]
```

## De-serialization of Task Outputs

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

A task's command can only output data as files.  Therefore, every de-serialization function in WDL takes a file input and returns a WDL type

### Primitive Types

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

De-serialization of primitive types is done through a `read_*` function.  For example, `read_int("file/path")` and `read_string("file/path")`.

For example, if I have a task that outputs a `String` and an `Int`:

```wdl
task output_example {
  String param1
  String param2
  command {
    python do_work.py ${param1} ${param2} --out1=int_file --out2=str_file
  }
  output {
    Int my_int = read_int("int_file")
    String my_str = read_string("str_file")
  }
}
```

Both files `file_with_int` and `file_with_uri` should contain one line with the value on that line.  This value is then validated against the type of the variable.  If `file_with_int` contains a line with the text "foobar", the workflow must fail this task with an error.

### Compound Types

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Tasks can also output to a file or stdout/stderr an `Array`, `Map`, or `Object` data structure in a two major formats:

* JSON - because it fits naturally with the types within WDL
* Text based / TSV - These are usually simple table and text-based encodings (e.g. `Array[String]` could be serialized by having each element be a line in a file)

#### Array deserialization

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Maps are deserialized from:

* Files that contain a JSON Array as their top-level element.
* Any file where it is desirable to interpret each line as an element of the `Array`.

##### Array deserialization using read_lines()

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

`read_lines()` will return an `Array[String]` where each element in the array is a line in the file.

This return value can be auto converted to other `Array` types.  For example:

```wdl
task test {
  command <<<
    python <<CODE
    import random
    for i in range(10):
      print(random.randrange(10))
    CODE
  >>>
  output {
    Array[Int] my_ints = read_lines(stdout())
  }
}
```

`my_ints` would contain ten random integers ranging from 0 to 10.

##### Array deserialization using read_json()

:pig2: Coming soon in [Cromwell](https://github.com/broadinstitute/cromwell)

`read_json()` will return whatever data type resides in that JSON file

```wdl
task test {
  command <<<
    echo '["foo", "bar"]'
  >>>
  output {
    Array[String] my_array = read_json(stdout())
  }
}
```

This task would assign the array with elements `"foo"` and `"bar"` to `my_array`.

If the echo statement was instead `echo '{"foo": "bar"}'`, the engine MUST fail the task for a type mismatch.

#### Map deserialization

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Maps are deserialized from:

* Files that contain a JSON Object as their top-level element.
* Files that contain a two-column TSV file.

##### Map deserialization using read_map()

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

`read_map()` will return an `Map[String, String]` where the keys are the first column in the TSV input file and the corresponding values are the second column.

This return value can be auto converted to other `Map` types.  For example:

```wdl
task test {
  command <<<
    python <<CODE
    for i in range(3):
      print("key_{idx}\t{idx}".format(idx=i)
    CODE
  >>>
  output {
    Map[String, Int] my_ints = read_map(stdout())
  }
}
```

This would put a map containing three keys (`key_0`, `key_1`, and `key_2`) and three respective values (`0`, `1`, and `2`) as the value of `my_ints`

##### Map deserialization using read_json()

:pig2: Coming soon in [Cromwell](https://github.com/broadinstitute/cromwell)

`read_json()` will return whatever data type resides in that JSON file.  If that file contains a JSON object with homogeneous key/value pair types (e.g. `string -> int` pairs), then the `read_json()` function would return a `Map`.

```wdl
task test {
  command <<<
    echo '{"foo":"bar"}'
  >>>
  output {
    Map[String, String] my_map = read_json(stdout())
  }
}
```

This task would assign the one key-value pair map in the echo statement to `my_map`.

If the echo statement was instead `echo '["foo", "bar"]'`, the engine MUST fail the task for a type mismatch.

#### Object deserialization

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

Objects are deserialized from files that contain a two-row, n-column TSV file.  The first row are the object attribute names and the corresponding entries on the second row are the values.

##### Object deserialization using read_object()

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

`read_object()` will return an `Object` where the keys are the first row in the TSV input file and the corresponding values are the second row (corresponding column).

```wdl
task test {
  command <<<
    python <<CODE
    print('\t'.join(["key_{}".format(i) for i in range(3)]))
    print('\t'.join(["value_{}".format(i) for i in range(3)]))
    CODE
  >>>
  output {
    Object my_obj = read_object(stdout())
  }
}
```

This would put an object containing three attributes (`key_0`, `key_1`, and `key_2`) and three respective values (`value_0`, `value_1`, and `value_2`) as the value of `my_obj`

#### Array[Object] deserialization

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

`Array[Object]` MUST assume that all objects in the array are homogeneous (they have the same attributes, but the attributes don't have to have the same values)

An `Array[Object]` is deserialized from files that contains at least 2 rows and a uniform n-column TSV file.  The first row are the object attribute names and the corresponding entries on the subsequent rows are the values

##### Object deserialization using read_objects()

:pig2: [Cromwell supported](https://github.com/broadinstitute/cromwell#wdl-support) :white_check_mark:

`read_object()` will return an `Object` where the keys are the first row in the TSV input file and the corresponding values are the second row (corresponding column).

```wdl
task test {
  command <<<
    python <<CODE
    print('\t'.join(["key_{}".format(i) for i in range(3)]))
    print('\t'.join(["value_{}".format(i) for i in range(3)]))
    print('\t'.join(["value_{}".format(i) for i in range(3)]))
    print('\t'.join(["value_{}".format(i) for i in range(3)]))
    CODE
  >>>
  output {
    Array[Object] my_obj = read_objects(stdout())
  }
}
```

This would create an array of **three identical** `Object`s containing three attributes (`key_0`, `key_1`, and `key_2`) and three respective values (`value_0`, `value_1`, and `value_2`) as the value of `my_obj`
