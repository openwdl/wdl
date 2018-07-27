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
    * [Object Literals](#object-literals)
    * [Pair Literals](#pair-literals)
  * [Document](#document)
  * [Versioning](#versioning)
  * [Import Statements](#import-statements)
  * [Task Definition](#task-definition)
    * [Task Sections](#task-sections)
    * [Task Inputs](#task-inputs)
      * [Task Input Declaration](#task-input-declaration)
      * [Task Input Localization](#task-input-localization)
    * [Command Section](#command-section)
      * [Expression Placeholders](#command-parts)
      * [Expression Placeholder Options](#command-part-options)
        * [sep](#sep)
        * [true and false](#true-and-false)
        * [default](#default)
      * [Alternative heredoc syntax](#alternative-heredoc-syntax)
      * [Stripping Leading Whitespace](#stripping-leading-whitespace)
    * [Outputs Section](#outputs-section)
      * [Globs](#globs)
        * [Task portability and non-standard BaSH](#task-portability-and-non-standard-bash)
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
    * [Workflow Elements](#workflow-elements)
    * [Workflow Inputs](#workflow-inputs)
      * [Optional Inputs](#optional-inputs)
      * [Declared Inputs: Defaults and Overrides](#declared-inputs-defaults-and-overrides)
        * [Optional inputs with defaults](#optional-inputs-with-defaults)
    * [Call Statement](#call-statement)
      * [Call Input Blocks](#call-input-blocks)
      * [Sub Workflows](#sub-workflows)
    * [Scatter](#scatter)
    * [Conditionals](#conditionals)
    * [Parameter Metadata](#parameter-metadata)
    * [Metadata](#metadata)
    * [Outputs](#outputs)
  * [Struct Definition](#struct-definition)
    * [Declarations](#struct-declarations)
      * [Optional and non Empty Struct Values](#optional-and-non-empty-struct-values)
    * [Using a Struct](#using-a-struct)
      * [Struct Assignment From Object Literal](#struct-assignment-from-object-literal)
      * [Struct Member Access](#struct-member-access)
      * [Importing Structs](#importing-structs)
* [Namespaces](#namespaces)
* [Scope](#scope)
* [Optional Parameters & Type Constraints](#optional-parameters--type-constraints)
  * [Prepending a String to an Optional Parameter](#prepending-a-string-to-an-optional-parameter)
* [Scatter / Gather](#scatter--gather)
* [Variable Resolution](#variable-resolution)
  * [Task-Level Resolution](#task-level-resolution)
  * [Workflow-Level Resolution](#workflow-level-resolution)
* [Computing Inputs](#computing-inputs)
  * [Computing Task Inputs](#task-inputs)
  * [Computing Workflow Inputs](#workflow-inputs)
  * [Specifying Workflow Inputs in JSON](#specifying-workflow-inputs-in-json)
  * [Optional Inputs](#optional-inputs)
  * [Declared Inputs: Defaults and Overrides](#declared-inputs-defaults-and-overrides)
    * [Optional Inputs with Defaults](#optional-inputs-with-defaults)
  * [Call Input Blocks](#call-input-blocks)
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
  * [Array\[Pair(X,Y)\] as_pairs(Map\[X,Y\])](#arraypairxy-as_pairsmapxy)
  * [Map\[X,Y\] as_map(Array\[Pair(X,Y)\])](#mapxy-as_maparraypairxy)
  * [Map\[X,Array\[Y\]\] collect_by_key(Array\[Pair(X,Y)\])](#mapxarrayy-collect_by_keyarraypairxy)
  * [Integer length(Array\[X\])](#integer-lengtharrayx)
  * [Array\[X\] flatten(Array\[Array\[X\]\])](#arrayx-flattenarrayarrayx)
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
  input {
    String pattern
    File in
  }

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
  input {
    Array[File] files
  }
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
* An escape sequence starting with `\\x`, followed by hexadecimal characters `0-9a-fA-F`.  This specifies a hexadecimal escape code.
* An escape sequence starting with `\\u` or `\\U` followed by either 4 or 8 hexadecimal characters `0-9a-fA-F`.  This specifies a unicode code point

### Types

All inputs and outputs must be typed. The following primitive types exist in WDL:

```wdl
Int i = 0                  # An integer value
Float f = 27.3             # A floating point number
Boolean b = true           # A boolean true/false
String s = "hello, world"  # A string value
File f = "path/to/file"    # A file
```

In addition, the following compound types can be constructed, parameterized by other types. In the examples below `P` represents any of the primitive types above, and `X` and `Y` represent any valid type (even nested compound types):
```wdl
Array[X] xs = [x1, x2, x3]                    # An array of Xs
Map[P,Y] p_to_y = { p1: y1, p2: y2, p3: y3 }  # An ordered map from Ps to Ys
Pair[X,Y] x_and_y = (x, y)                    # A pair of one X and one Y
Object o = { "field1": f1, "field2": f2 }     # Object keys are always `String`s
```

Some examples of types:

* `File`
* `Array[File]`
* `Pair[Int, Array[String]]`
* `Map[String, String]`

Types can also have a postfix quantifier (either `?` or `+`):

* `?` means that the value is optional. It can only be used in calls or functions that accept optional values.
* `+` can only be applied to `Array` types, and it signifies that the array is required to be non-empty.

For more details on the postfix quantifiers, see the section on [Optional Parameters & Type Constraints](#optional-parameters--type-constraints)

For more information on type and how they are used to construct commands and define outputs of tasks, see the [Data Types & Serialization](#data-types--serialization) section.

#### Custom  Types

WDL provides the ability to define custom compound types called `Structs`. `Structs` are defined directly in the WDL and are usable like any other type.
For more information on their usage, see the section on [Structs](#struct-definition)

### Fully Qualified Names & Namespaced Identifiers

```
$fully_qualified_name = $identifier ('.' $identifier)*
$namespaced_identifier = $identifier ('.' $identifier)*
```

A fully qualified name is the unique identifier of any particular `call` or call input or output.  For example:

other.wdl
```wdl
task foobar {
  input {
    File in
  }
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
  input {
    String var
  }
  command {
    ./script ${var}
  }
  output {
    String value = read_string(stdout())
  }
}

task test2 {
  input {
    Array[String] array
  }
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

```wdl
workflow wf {
  input {
    Object obj
    Object foo
  }
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

The syntax `x[y]` is for indexing maps and arrays.  If `x` is an array, then `y` must evaluate to an integer.  If `x` is a map, then `y` must evaluate to a key in that map.

### Pair Indexing

Given a Pair `x`, the left and right elements of that type can be accessed using the syntax `x.left` and `x.right`.

### Function Calls

Function calls, in the form of `func(p1, p2, p3, ...)`, are either [standard library functions](#standard-library) or engine-defined functions.

In this current iteration of the spec, users cannot define their own functions.

### Array Literals

Arrays values can be specified using Python-like syntax, as follows:

```
Array[String] a = ["a", "b", "c"]
Array[Int] b = [0,1,2]
```

### Map Literals

Maps values can be specified using a similar Python-like syntax:

```
Map[Int, Int] = {1: 10, 2: 11}
Map[String, Int] = {"a": 1, "b": 2}
```

### Object Literals

Object literals are specified similarly to maps, but require an `object` keyword immediately before the `{`:

```wdl
Object f = object {
  a: 10,
  b: 11
}
```

The `object` keyword allows the field keys to be specified as identifiers, rather than `String` literals (eg `a:` rather than `"a":`).

#### Object Coercion from Map

Objects can be coerced from map literals, but beware the following behavioral difference:
```wdl
String a = "beware"
String b = "key"
String c = "lookup"

# What are the keys to this object?
Object object_syntax = object {
  a: 10,
  b: 11,
  c: 12
}

# What are the keys to this object?
Object map_coercion = {
  a: 10,
  b: 11,
  c: 12
}
```
- If an `Object` is specified using the object-style `Object map_syntax = object { a: ...` syntax then the keys will be `"a"`, `"b"` and `"c"`.
- If an `Object` is specified using the map-style `Object map_coercion = { a: ...` then the keys are expressions, and thus `a` will be a variable reference to the previously defined `String a = "beware"`.

### Pair Literals

Pair values can be specified inside of a WDL using another Python-like syntax, as follows:

```
Pair[Int, String] twenty_threes = (23, "twenty-three")
```

Pair values can also be specified within the [workflow inputs JSON](https://github.com/openwdl/wdl/blob/develop/SPEC.md#specifying-workflow-inputs-in-json) with a `Left` and `Right` value specified using JSON style syntax. For example, given a workflow `wf_hello` and workflow-level variable `twenty_threes`, it could be declared in the workflow inputs JSON as follows:
```
{
  "wf_hello.twenty_threes": { "Left": 23, "Right": "twenty-three" }
}
```

## Document

```
$document = ($import | $task | $workflow)+
```

`$document` is the root of the parse tree and it consists of one or more import statement, task, or workflow definition

## Versioning

For portability purposes it is critical that WDL documents be versioned so an engine knows how to process it. From `draft-3` forward, the first line of all WDL files must be a `version` statement, for example

```wdl
version draft-3
```

Any WDL files which do not have a `version` field must be treated as `draft-2`.  All WDL files used by a workflow must have the same version.

## Import Statements

A WDL file may contain import statements to include WDL code from other sources

```
$import = 'import' $ws+ $string ($ws+ 'as' $ws+ $identifier)?
```

The import statement specifies that `$string` which is to be interpreted as a URI which points to a WDL file.  The engine is responsible for resolving the URI and downloading the contents.  The contents of the document in each URI must be WDL source code.

Every imported WDL file requires a namespace which can be specified using an identifier (via the `as $identifier` syntax). If you do not explicitly specify a namespace identifier then the default namespace is the filename of the imported WDL, minus the .wdl extension.
For all imported WDL files, the tasks and workflows imported from that file will only be accessible through that assigned [namespace](#namespaces).

```wdl
import "http://example.com/lib/analysis_tasks" as analysis
import "http://example.com/lib/stdlib"


workflow wf {
  input {
    File bam_file
  }
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

A task is a declarative construct with a focus on constructing a command from a template.  The command specification is interpreted in an engine and backend agnostic way. The command is a UNIX bash command line which will be run (ideally in a Docker image).

Tasks explicitly define their inputs and outputs which is essential for building dependencies between tasks.

To declare a task, use `task name { ... }`.  Inside the curly braces are the following sections:

### Task Sections

The task may have the following component sections:

- An `input` section (required if the task will have inputs)
- Non-input declarations (as many as needed, optional)
- A `command` section (required)
- A `runtime` section (optional)
- An `output` section (required if the task will have outputs)
- A `meta` section (optional)
- A `parameter_meta` section (optional)

### Task Inputs

#### Task Input Declaration

Tasks declare inputs within the task block. For example:
```wdl
task t {
  input {
    Int i
    File f
  }

  # [... other task sections]
}
```

#### Task Input Localization
`File` inputs must be treated specially since they require localization to within the execution directory:
- Files are localized into the execution directory prior to the task execution commencing.
- When localizing a `File`, the engine may choose to place the file wherever it likes so long as it accords to these rules:
  - The original file name must be preserved even if the path to it has changed.
  - Two input files with the same name must be located separately, to avoid name collision.
  - Two input files which originated in the same storage directory must also be localized into the same directory for task execution (see the special case handling for Versioning Filesystems below).
- When a WDL author uses a `File` input in their [Command Section](#command-section), the fully qualified, localized path to the file is substituted into the command string.

##### Special Case: Versioning Filesystems
Two or more versions of a file in a versioning filesystem might have the same name and come from the same directory. In that case the following special procedure must be used to avoid collision:
  - The first file is always placed as normal according to the usual rules.
  - Subsequent files that would otherwise overwrite this file are instead placed in a subdirectory named for the version.

For example imagine two versions of file `fs://path/to/A.txt` are being localized (labeled version `1.0` and `1.1`). The first might be localized as `/execution_dir/path/to/A.txt`. The second must then be placed in `/execution_dir/path/to/1.1/A.txt`

### Non-Input Declarations

A task can have declarations which are intended as intermediate values rather than inputs. These declarations can be based on input values and can be used within the command section.

For example, this task takes a single `inputs` `Object` but writes it to a JSON file which can then be used by the command:

```wdl
task t {
  input {
    Object inputs
  }
  File objects_json = write_json(inputs)

  # [... other task sections]
}
```

### Command Section

The `command` section is the *task section* that starts with the keyword 'command', and is enclosed in either curly braces `{ ... }` or triple angle braces `<<< ... >>>`.
It defines a shell command which will be run in the execution environment after all of the inputs are staged and before the outputs are evaluated.
The body of the command also allows placeholders for the parts of the command line that need to be filled in.

Expression placeholders are denoted by `${...}` or `~{...}` depending on whether they appear in a `command { }` or `command <<< >>>` body styles.

#### Expression Placeholders

Expression placeholders differ depending on the command section style:

|Command Body Style|Placeholder Style|
|---|---|
|`command { ... }`|`~{}` (preferred) or `${}`|
|`command <<< >>>`|`~{}` only|

These placeholders contain a single expression which will be evaluated using inputs or declarations available in the task.
The placeholders are then replaced in the command script with the result of the evaluation.

For example a command might reference an input to the task, like this:

```wdl
task test {
  input {
    String flags
  }
  command {
    ps ~{flags}
  }
}
```

In this case `flags` within the `${...}` is a variable lookup expression referencing the `flags` input string.
The expression can also be more complex, like a function call: `write_lines(some_array_value)`

Here is the same example using the `command <<<` style:
```wdl
task test {
  String flags
  command <<<
    ps ~{flags}
  >>>
}
```

> **NOTE**: the expression result must ultimately be converted to a string in order to take the place of the placeholder in the command script.
This is immediately possible for WDL primitive types (e.g. not `Array`, `Map`, or `Object`).
To place an array into the command block a separator character must be specified using `sep` (eg `${sep=", " int_array}`).


As another example, consider how the parser would parse the following command:

```
grep '${start}...${end}' ${input}
```

This command would be parsed as:

* `grep '` - literal string
* `${start}` - lookup expression to the variable `start`
* `...` - literal string
* `${end}` - lookup expression to the variable `end`
* `' ` - literal string
* `${input}` - lookup expression to the variable `input`

#### Expression Placeholder Options

Expression placeholder options are `option="value"` pairs that precede the expression in an expression command part and customize the interpolation of the WDL value into the command string being built. The following options are available:

* `sep` - eg `${sep=", " array_value}`
* `true` and `false` - eg `${true="--yes" false="--no" boolean_value}`
* `default` - eg `${default="foo" optional_value}`

Additional explanation for these command part options follows:

##### sep

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

'true' and 'false' are available for expressions which evaluate to `Boolean`s. They specify a string literal to insert into the command block when the result is true or false respectively.

For example, `${true='--enable-foo' false='--disable-foo' allow_foo}` would evaluate the expression `allow_foo` as a variable lookup and depending on its value would either insert the string `--enable-foo` or `--disable-foo` into the command.

Both `true` and `false` cases are required. If one case should insert no value then an empty string literal should be used, eg `${true='--enable-foo' false='' allow_foo}`

> 1.  `true` and `false` values MUST be string literals.
> 2.  `true` and `false` are only allowed if the type is `Boolean`
> 3.  Both `true` and `false` cases are required.
> 4.  Consider using the expression `${if allow_foo then "--enable-foo" else "--disable-foo"}` as a more readable alternative which allows full expressions (rather than string literals) for the true and false cases.

##### default

This specifies the default value if no other value is specified for this parameter.

```
task default_test {
  input {
    String? s
  }
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

Sometimes a command is sufficiently long enough or might use `{` characters that using a different set of delimiters would make it more clear.  In this case, enclose the command in `<<<`...`>>>`, as follows:

```wdl
task heredoc {
  input {
    File in
  }

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

The outputs section defines which values should be exposed as outputs after a successful run of the task. Outputs are declared just like task inputs or declarations in the workflow. The difference being that they are evaluated only after the command line executes and files generated by the command can be used to determine values. Note that outputs require a value expression (unlike inputs, for which an expression is optional)

For example a task's output section might looks like this:

```
output {
  Int threshold = read_int("threshold.txt")
}
```

The task is expecting that a file called "threshold.txt" will exist in the current working directory after the command is executed. Inside that file must be one line that contains only an integer and whitespace.  See the [Data Types & Serialization](#data-types--serialization) section for more details.

As with other string literals in a task definition, Strings in the output section may contain interpolations (see the [String Interpolation](#string-interpolation) section below for more details). Here's an example:

```
output {
  Array[String] quality_scores = read_lines("${sample_id}.scores.txt")
}
```

Note that for this to work, `sample_id` must be declared as an input to the task.

As with inputs, the outputs can reference previous outputs in the same block. The only requirement is that the output being referenced must be specified *before* the output which uses it.

```
output {
  String a = "a"
  String ab = a + "b"
}
```

#### Globs

Globs can be used to define outputs which might contain zero, one, or many files. The glob function therefore returns an array of File outputs:

```
output {
  Array[File] output_bams = glob("*.bam")
}
```

The array of `File`s returned is the set of files found by the bash expansion of the glob string relative to the task's execution directory and in the same order. It's evaluated in the context of the bash shell installed in the docker image running the task.

In other words, you might think of `glob()` as finding all of the files (but not the directories) in the same order as would be matched by running `echo <glob>` in bash from the task's execution directory.

Note that this usually will not include files in nested directories. For example say you have an output `Array[File] a_files = glob("a*")` and the end result of running your command has produced a directory structure like this:
```
execution_directory
├── a1.txt
├── ab.txt
├── a_dir
│   ├── a_inner.txt
├── az.txt
```
Then running `echo a*` in the execution directory would expand to `a1.txt`, `ab.txt`, `a_dir` and `az.txt` in that order. Since `glob()` does not include directories we discard `a_dir` and the result of the WDL glob would be `["a1.txt", "ab.txt", "az.txt"]`.

##### Task portability and non-standard BaSH

Note that some specialized docker images may include a non-standard bash shell which supports more complex glob strings. These complex glob strings might allow expansions which include `a_inner.txt` in the example above.

Therefore to ensure that a WDL is portable when using `glob()`, a docker image should be provided and the WDL author should remember that `glob()` results depend on coordination with the bash implementation installed on that docker image.

### String Interpolation

Within tasks, any string literal can use string interpolation to access the value of any of the task's inputs.  The most obvious example of this is being able to define an output file which is named as function of its input.  For example:

```wdl
task example {
  input {
    String prefix
    File bam
  }
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
  input {
    String ubuntu_version
  }
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

Location of a Docker image for which this task ought to be run.  This can have a format like `ubuntu:latest` or `broadinstitute/scala-baseimage` in which case it should be interpreted as an image on DockerHub (i.e. it is valid to use in a `docker pull` command).

```wdl
task docker_test {
  input {
    String arg
  }
  command {
    python process.py ${arg}
  }
  runtime {
    docker: "ubuntu:latest"
  }
}
```

#### singularity

Location of a Singularity image for which this task ought to be run. This can have a format like `patrickvdb/fastqc-singularity`,
`shub://patrickvdb/fastqc-singularity:latest` or `docker://biocontainers/fastqc:latest`.

```wdl
task docker_test {
  input {
    String arg
  }
  command {
    python process.py ${arg}
  }
  runtime {
    singularity: "docker://ubuntu:latest"
  }
}
```

#### memory

Memory requirements for this task.  Two kinds of values are supported for this attributes:

* `Int` - Interpreted as bytes
* `String` - This should be a decimal value with suffixes like `B`, `KB`, `MB` or binary suffixes `KiB`, `MiB`.  For example: `6.2 GB`, `5MB`, `2GiB`.

```wdl
task memory_test {
  input {
    String arg
  }

  command {
    python process.py ${arg}
  }
  runtime {
    memory: "2GB"
  }
}
```

### Parameter Metadata Section

```
$parameter_meta = 'parameter_meta' $ws* '{' ($ws* $parameter_meta_kv $ws*)* '}'
$parameter_meta_kv = $identifier $ws* ':' $ws* $meta_value
$meta_value = $string | $number | $boolean | 'null' | $meta_object | $meta_array
$meta_object = '{}' | '{' $parameter_meta_kv (, $parameter_meta_kv)* '}'
$meta_array = '[]' |  '[' $meta_value (, $meta_value)* ']'
```

This purely optional section contains key/value pairs where the keys are names of parameters and the values are JSON like expressions that describe those parameters. The engine can ignore this section, with no loss of correctness. The extra information can be used, for example, to generate a user interface.

> *Additional requirement*: Any key in this section MUST correspond to a task input or output.

For example:
```wdl
task wc {
  File f
  Boolean l = false
  String? region
  parameter_meta {
    f : { help: "Count the number of lines in this file" },
    l : { help: "Count only lines" }
    region: {help: "Cloud region",
             suggestions: ["us-west", "us-east", "asia-pacific", "europe-central"]}
  }
  command {
    wc ${true="-l", false=' ' l} ${f}
  }
  output {
     String retval = stdout()
  }
}
```

### Metadata Section

```
$meta = 'meta' $ws* '{' ($ws* $meta_kv $ws*)* '}'
$meta_kv = $identifier $ws* '=' $ws* $meta_value
```

This purely optional section contains key/value pairs for any additional meta data that should be stored with the task.  For example, author, contact email, or engine authorization policies.

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
  input {
    String pattern
    File infile
  }
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
  input {
    String memory_mb
    String sample_id
    String param
    String sample_id
  }
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
  input {
    Int threads
    Int min_seed_length
    Int min_std_max_min
    File reference
    File reads
  }
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
  input {
    File file1
  }
  command {
    wc ${file1}
  }
  output {
    Int count = read_int(stdout())
  }
}

workflow count_lines4_wf {
  input {
    Array[File] files
  }
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
  input {
    Array[String] stages
    File reads
  }
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

A workflow is declared using the keyword `workflow` followed by the workflow name and the workflow body in curly braces.

An example of a workflow that runs one task (not defined here) would be:

```wdl
workflow wf {
  input {
    Array[File] files
    Int threshold
    Map[String, String] my_map
  }
  call analysis_job {
    input: search_paths = files, threshold = threshold, gender_lookup = my_map
  }
}
```

### Workflow Elements

A workflow may have the following elements:

* An `input` section (required if the workflow is to have inputs)
* Intermediate declarations (as many as needed, optional)
* Calls to tasks or subworkflows (as many as needed, optional)
* Scatter blocks (as many as needed, optional)
* If blocks (as many as needed, optional)
* An `output` section (required if the workflow is to have outputs)
* A `meta` section (optional)
* A `parameter_meta` section (optional)

### Workflow Inputs

As with tasks, a workflow must declare its inputs in an `input` section, like this:
```wdl
workflow w {
  input {
    Int i
    String s
  }
}
```



#### Optional Inputs

An optional input is specified like this:

```wdl
workflow foo {
  input {
    Int? x
    File? y
  }
  # ... remaining workflow content
}
```

In these situations, a value may or may not be provided for this input. The following would all be valid input files for the above workflow:
- No inputs:

```json
{ }
```
- Only x:
```json
{
  "x": 100
}
```
- Only y:
```json
{
  "x": null,
  "y": "/path/to/file"
}
```
- x and y:
```json
{
  "x": 1000,
  "y": "/path/to/file"
}
```

#### Declared Inputs: Defaults and Overrides

Tasks and workflows can have default values built-in via expressions, like this:
```wdl
workflow foo {
  input {
    Int x = 5
  }
  ...
}
```

```wdl
task foo {
  input {
    Int x = 5
  }
  ...
}
```

In this case, `x` should be considered an optional input to the task or workflow, but unlike optional inputs without defaults, the type can be `Int` rather than `Int?`. If an input is provided, that value should be used. If no input value for x is provided then the default expression is evaluated and used.

Note that to be considered an optional input, the default value must be provided within the `input` section. If the declaration is in the main body of the workflow it is considered an intermediate value and is not overridable. For example below, the `Int x` is an input whereas `Int y` is not.
```wdl
workflow foo {
  input {
    Int x = 10
  }
  call my_task as t1 { input: int_in = x }
  Int y = my_task.out
  call my_task as t2 { input: int_in = y }
}
```

Note that it is still possible to override intermediate expressions via optional inputs if that's important to the workflow author. A modified version of the above workflow demonstrates this:
```wdl
workflow foo {
  input {
    Int x = 10
    Int y = my_task.out
  }

  call my_task as t1 { input: int_in = x }
  call my_task as t2 { input: int_in = y }
}
```
Note that the control flow of the workflow changes depending on whether the value `Int y` is provided:

* If an input value is provided for `y` then it receives that value immediately and `t2` may start running as soon as the workflow starts.
* In no input value is provided for `y` then it will need to wait for `t1` to complete before it is assigned.


##### Optional inputs with defaults
It *is* possible to provide a default to an optional input type:
```wdl
input {
  String? s = "hello"
}
```
Since the expression is static, this is interpreted as a `String?` value that is set by default, but can be overridden in the inputs file, just like above. Note that if you give a value an optional type like this then you can only use this value in calls or expressions that can handle optional inputs. Here's an example:
```wdl
workflow foo {
  input {
    String? s = "hello"
  }

  call valid { input: s_maybe = s }

  # This would cause a validation error. Cannot use String? for a String input:
  call invalid { input: s_definitely = s }
}

task valid {
  input {
    String? s_maybe
  }
  ...
}

task invalid {
  input {
    String s_definitely
  }
}
```

The rational for this is that a user may want to provide the following input file to alter how `valid` is called, and such an input would invalidate the call to `invalid` since it is unable to accept optional values:
```json
{
  "foo.s": null
}
```

### Call Statement

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
  input {
    File foobar
  }
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

#### Call Input Blocks

As mentioned above, call inputs should be provided via call inputs (`call my_task { input: x = 5 }`), or else they will become workflow inputs (`"my_workflow.my_task.x": 5`) and prevent the workflow from being composed as a subworkflow.
In situations where both are supplied (ie the workflow specifies a call input, and the user tries to supply the same input via an input file), the workflow submission should be rejected because the user has supplied an unexpected input.

The reasoning for this is that the input value is an intrinsic part of the workflow's control flow and that changing it via an input is inherently dangerous to the correct working of the workflow.

As always, if the author chooses to allow it, values provided as inputs can be overridden if they're declared in the `input` block:
```wdl
workflow foo {
  input {
    # This input `my_task_int_in` is usually based on a task output, unless it's overridden in the input set:
    Int my_task_int_in = some_preliminary_task.int_out
  }

  call some_preliminary_task
  call my_task { input: my_task_int_in = x) }
}
```

#### Sub Workflows

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
  input {
    String addressee
  }
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
  input {
    String wf_hello_input
  }

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

```
$scatter = 'scatter' $ws* '(' $ws* $scatter_iteration_statement $ws*  ')' $ws* $scatter_body
$scatter_iteration_statement = $identifier $ws* 'in' $ws* $expression
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

### Conditionals

```
$conditional = 'if' '(' $expression ')' '{' $workflow_element* '}'
```

Conditionals only execute the body if the expression evaluates to true.

* When a call's output is referenced outside the same containing `if` it will need to be handled as an optional type. E.g.

```wdl
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

```wdl
workflow foo {
  input {
    Array[Int] scatter_range = [1, 2, 3, 4, 5]
  }
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
* When conditional blocks are nested, referenced outputs are only ever single-level conditionals (i.e. we never produce `Int??` or deeper):
```wdl
workflow foo {
  input {
    Boolean b
    Boolean c
  }
  if(b) {
    if(c) {
      call x
      Int x_out = x.out
    }
  }
  Int? x_out_maybe = x_out # Even though it's within two 'if's, we don't need Int??

  # Call 'y' which takes an Int input:
  call y { input: int_input = select_first([x_out_maybe, 5]) } # The select_first produces an Int, not an Int?
}
```

### Parameter Metadata

```
$wf_parameter_meta = 'parameter_meta' $ws* '{' ($ws* $wf_parameter_meta_kv $ws*)* '}'
$wf_parameter_meta_kv = $identifier $ws* '=' $ws* $meta_value
```

This purely optional section contains key/value pairs where the keys are names of parameters and the values are JSON like expressions that describe those parameters.

> *Additional requirement*: Any key in this section MUST correspond to a workflow input or output.

As an example:
```
  parameter_meta {
    memory_mb: "Amount of memory to allocate to the JVM"
    param: "Some arbitrary parameter"
    sample_id: "The ID of the sample in format foo_bar_baz"
  }
```

### Metadata

```
$wf_meta = 'meta' $ws* '{' ($ws* $wf_meta_kv $ws*)* '}'
$wf_meta_kv = $identifier $ws* '=' $ws* $meta_value
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

Each `workflow` definition can specify an `output` section.  This section lists outputs as `Type name = expression`, just like task outputs.

Workflow outputs also follow the same syntax rules as task outputs. They are expressions which can reference all call outputs, workflow inputs, intermediate values and previous workflow outputs.
e.g:

```
task t {
  input {
    Int i
  }
  command {
    # do something
  }
  output {
    String out = "out"
  }
}

workflow w {
  input {
    String w_input = "some input"
  }

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

Note that they can't reference call inputs (eg we cannot use `Int i = t.i` as a workflow output). However this can be achieved by also declaring the desired call input as an output of the call.

When declaring a workflow output that points to a call inside a scatter, the aggregated call is used, just like any expression that references it from outside the scatter.
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
  input {
    Array[Int] arr = [1, 2]
  }

  scatter(i in arr) {
    call t
  }

  output {
    Array[String] t_out = t.out
  }
}
```

In this example `t_out` has an `Array[String]` result type, because `call t` is inside a scatter.

#### Omitting Workflow Outputs

If the `output {...}` section is omitted from a top-level workflow then the workflow engine should include all outputs from all calls in its final output.

However, if a workflow is intended to be called as a subworkflow, it is required that outputs are named and specified using expressions in the outputs block, just like task outputs. The rationale here is:
- To present the same interface when calling subworkflows as when calling tasks.
- To make it easy for callers of subworkflows to find out exactly what outputs the call is creating.
- In case of nested subworkflows, to give the outputs at the top level a simple fixed name rather than a long qualified name like `a.b.c.d.out` (which is liable to change if the underlying implementation of `c` changes, for example).

## Struct Definition
A struct is a C-like construct which enables the user to create new compound types that consisting of previously existing types. Structs
can then be used within a `Task` or `Workflow` definition as a declaration in place of any other normal types. The struct takes the place of the
`Object` type in many circumstances and enables proper typing of its members.

Structs are declared separately from any other constructs, and cannot be declared within any `workflow` or `task` definition. They belong to the namespace of the WDL
file which they are written in and are therefore accessible globally within that WDL. Additionally, all structs must be evaluated prior to their use within a `task`,
`workflow` or another `struct`.

Structs may be defined using the `struct` keyword and have a single section consisting of typed declarations.

```wdl
struct name { ... }
```

### Struct Declarations
The only contents of struct are a set of declarations. Declarations can be any primitive or compound type, as well as other structs, and are defined
the same way as they are in any other section. The one caveat to this is that declarations within a struct do not allow an expression statement after
the initial member declaration. Once defined all structs are added to a global namespace accessible from any other construct within the WDL.

for example the following is a valid struct definition
```wdl
struct Name {
    String myString
    Int myInt
}
```
Whereas the following is invalid

```wdl
struct Invalid {
    String myString = "Cannot do this"
    Int myInt
}
```

Compound types can also be used within a struct to easily encapsulate them within a single object. For example
```wdl
struct Name {
    Array[Array[File]] myFiles
    Map[String,Pair[String,File]] myComplexType
    String cohortName
}
```
#### Optional and non Empty Struct Values
Struct declarations can be optional or non-empty (if they are an array type).

```wdl
struct Name {
    Array[File]+ myFiles
    Boolean? myBoolean
}
```

### Using a Struct
When using a struct in the declaration section of either a `workflow` or a `task` or `output` section you define them in the same way you would define any other type.

For example, if I have a struct like the following:
```wdl
struct Person {
    String name
    Int age
}
```

then usage of the struct in a workflow would look like the following:

```wdl

task task_a {
    Person a
    command {
        echo "hello my name is ${a.name} and I am ${a.age} years old"
    }
}

workflow myWorkflow {
    Person a
    call task_a {
        input:
            a = a
    }
}
```

#### Struct Assignment from Object Literal
Structs can be assigned using an object literal. When Writing the object, all entries must conform or be coercible into the underlying type they are being assigned to

```wdl

Person a = {"name": "John","age": 30}

```


### Struct Member Access
In order to access members within a struct, use object notation; ie `myStruct.myName`. If the underlying member is a complex type which supports member access,
you can access its elements in the way defined by that specific type.

For example, if we have defined a struct like the following:
```wdl
struct Experiment {
    Array[File] experimentFiles
    Map[String,String] experimentData
}

```
**Example 1:**
Accessing the nth element of experimentFiles and any element in experimentData would look like:
```wdl
workflow workflow_a {
    Experiment myExperiment
    File firstFile = myExperiment.experimentFiles[0]
    String experimentName = myExperiment.experimentData["name"]


}
```

**Example 2:**
If the struct itself is a member of an Array or another type, yo

```wdl
workflow workflow_a {
    Array[Experiment] myExperiments

    File firstFileFromFirstExperiment = myExperiments[0].experimentFiles[0]
    File eperimentNameFromFirstExperiment = bams[0].experimentData["name"]
    ....
}

```

### Importing Structs
Any `struct` defined within an imported WDL will be added to a global namespace and will not be a part of the imported wdl's namespace. If two structs
are named the same it will be necessary to resolve the conflicting names. To do this, one or more structs may be imported under an
alias defined within the import statement.

For example, if your current WDL defines a struct named `Experiment` and the imported WDL also defines another struct named `Experiment` you can
alias them as follows:

```wdl
import http://example.com/example.wdl as ex alias Experiment as OtherExperiment
```

In order to resolve multiple structs, simply add additional alias statements.
```wdl
import http://example.com/another_exampl.wdl as ex2
    alias Parent as Parent2
    alias Child as Child2
    alias GrandChild as GrandChild2
```

Its important to note, that when importing from file 2, all structs from file 2's global namespace will be imported. This Includes structs from
another imported WDL within file 2, even if they are aliased. If a struct is aliased in file 2, it will be imported into file 1 under its
aliased name.


* Note: Alias can be used even when no conflicts are encountered to uniquely identify any struct


# Namespaces

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

Scopes are defined as:

* `workflow {...}` blocks
* `call` blocks
* `if(expr) {...}` blocks
* `scatter(x in y) {...}` blocks

Inside of any scope, variables may be [declared](#declarations).  The variables declared in that scope are visible to any sub-scope, recursively.  For example:

```wdl
task my_task {
  input {
    Int x
    File f
  }
  command {
    my_cmd --integer=${var} ${f}
  }
}

workflow wf {
  input {
    Array[File] files
    Int x = 2
  }
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

[Types](#types) can be optionally suffixed with a `?` or `+` in certain cases.

* `?` means that the parameter is optional.  A user does not need to specify a value for the parameter in order to satisfy all the inputs to the workflow.
* `+` applies only to `Array` types and it represents a constraint that the `Array` value must contain one-or-more elements.

```wdl
task test {
  input {
    Array[File]  a
    Array[File]+ b
    Array[File]? c
    #File+ d <-- can't do this, + only applies to Arrays
  }
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

Sometimes, optional parameters need a string prefix.  Consider this task:

```wdl
task test {
  input {
    String? val
  }
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

The `scatter` block is meant to parallelize a series of identical tasks but give them slightly different inputs.  The simplest example is:

```wdl
task inc {
  input {
    Int i
  }

  command <<<
  python -c "print(~{i} + 1)"
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
  input {
    Int i
  }

  command <<<
  python -c "print(~{i} + 1)"
  >>>

  output {
    Int incremented = read_int(stdout())
  }
}

task sum {
  input {
    Array[Int] ints
  }
  command <<<
  python -c "print(~{sep="+" ints})"
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
  input {
    Array[Int] integers = [1,2,3,4,5]
  }
  scatter(i in integers) {
    call inc {input: i=i}
    call inc as inc2 {input: i=inc.incremented}
  }
  call sum {input: ints = inc2.increment}
}
```

In this example, `inc` and `inc2` are being called in serial where the output of one is fed to another. inc2 would output the array `[3,4,5,6,7]`

# Variable Resolution

Inside of [expressions](#expressions), variables are resolved differently depending on if the expression is in a `task` declaration or a `workflow` declaration

## Task-Level Resolution

Inside a task, resolution is trivial: The variable referenced MUST be a [declaration](#declarations) of the task.  For example:

```wdl
task my_task {
  input {
    Array[String] strings
  }
  command {
    python analyze.py --strings-file=${write_lines(strings)}
  }
}
```

Inside of this task, there exists only one expression: `write_lines(strings)`.  In here, when the expression evaluator tries to resolve `strings`, which must be a declaration of the task (in this case it is).

## Workflow-Level Resolution

In a workflow, resolution works by traversing the scope hierarchy starting from expression that references the variable.

```wdl
workflow wf {
  input {
    String s = "wf_s"
    String t = "t"
  }
  call my_task {
    String s = "my_task_s"
    input: in0 = s+"-suffix", in1 = t+"-suffix"
  }
}
```

In this example, there are two expressions: `s+"-suffix"` and `t+"-suffix"`.  `s` is resolved as `"my_task_s"` and `t` is resolved as `"t"`.

# Computing Inputs

Both tasks and workflows have a typed inputs that must be satisfied in order to run.  The following sections describe how to compute inputs for `task` and `workflow` declarations.

## Computing Task Inputs

Tasks define all their inputs as declarations within the `input` section. Any non-input declarations are not inputs to the task and therefore cannot be overridden.

```wdl
task test {
  input {
    Int i
    Float f
  }
  String s = "${i}"

  command {
    ./script.sh -i ${s} -f ${f}
  }
}
```

In this example, `i`, and `f` are inputs to this task even though `i` is not directly used in the command section. In comparison, `s` is an input even though the command line references it.

## Computing Workflow Inputs

Workflows have inputs that must be satisfied to run them, just like tasks. Inputs to the workflow are provided as a key/value map where the key is of the form `workflow_name.input_name`.

* If a workflow is to be used as a sub-workflow it must ensure that all of the inputs to its calls are satisfied.
* If a workflow will only ever be submitted as a top-level workflow, it may optionally leave its tasks' inputs unsatisfied. This then forces the engine to additionally supply those inputs at run time. In this case, the inputs' names must be qualified in the inputs as `workflow_name.task_name.input_name`.

Any declaration that appears outside the `input` section is considered an intermediate value and **not** a workflow input. Any declaration can always be moved inside the `input` block to make it overridable.

Consider the following workflow:

```wdl
task t1 {
  input {
    String s
    Int x
  }

  command {
    ./script --action=${s} -x${x}
  }
  output {
    Int count = read_int(stdout())
  }
}

task t2 {
  input {
    String s
    Int t
    Int x
  }

  command {
    ./script2 --action=${s} -x${x} --other=${t}
  }
  output {
    Int count = read_int(stdout())
  }
}

task t3 {
  input {
    Int y
    File ref_file # Do nothing with this
  }

  command {
    python -c "print(${y} + 1)"
  }
  output {
    Int incr = read_int(stdout())
  }
}

workflow wf {
  input {
    Int int_val
    Int int_val2 = 10
    Array[Int] my_ints
    File ref_file
  }

  String not_an_input = "hello"

  call t1 {
    input: x = int_val
  }
  call t2 {
    input: x = int_val, t=t1.count
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

Note that because some call inputs are left unsatisfied, this workflow could not be used as a sub-workflow. To fix that, additional workflow inputs could be added to pass-through `t1.s` and `t2.s`.

## Specifying Workflow Inputs in JSON

Once workflow inputs are computed (see previous section), the value for each of the fully-qualified names needs to be specified per invocation of the workflow.  Workflow inputs are specified as key/value pairs. The mapping from JSON or YAML values to WDL values is codified in the [serialization of task inputs](#serialization-of-task-inputs) section.

In JSON, the inputs to the workflow in the previous section might be:

```
{
  "wf.t1.s": "some_string",
  "wf.t2.s": "some_string",
  "wf.int_val": 3,
  "wf.my_ints": [5,6,7,8],
  "wf.ref_file": "/path/to/file.txt"
}
```

It's important to note that the type in JSON must be coercible to the WDL type.  For example `wf.int_val` expects an integer, but if we specified it in JSON as `"wf.int_val": "three"`, this coercion from string to integer is not valid and would result in a coercion error.  See the section on [Type Coercion](#type-coercion) for more details.

# Type Coercion

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
|`Array[T]`|JSON Array|Elements must be coercible to `T`|
|          |Array-like|Elements must be coercible to `T`|
|`Map[K, V]`|JSON Object|keys and values must be coercible to `K` and `V`, respectively|
|           |Map-like|keys and values must be coercible to `K` and `V`, respectively|

# Standard Library

## File stdout()

Returns a `File` reference to the stdout that this task generated.

## File stderr()

Returns a `File` reference to the stderr that this task generated.

## Array[String] read_lines(String|File)

Given a file-like object (`String`, `File`) as a parameter, this will read each line as a string and return an `Array[String]` representation of the lines in the file.

The order of the lines in the returned `Array[String]` must be the order in which the lines appear in the file-like object.

This task would `grep` through a file and return all strings that matched the pattern:

```wdl
task do_stuff {
  input {
    String pattern
    File file
  }
  command {
    grep '${pattern}' ${file}
  }
  output {
    Array[String] matches = read_lines(stdout())
  }
}
```

If the entire contents of the file can not be read for any reason, the calling task or workflow will be considered to have failed. Examples of failure include but are not limited to not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation imposed file size limits.

## Array[Array[String]] read_tsv(String|File)

the `read_tsv()` function takes one parameter, which is a file-like object (`String`, `File`) and returns an `Array[Array[String]]` representing the table from the TSV file.

If the parameter is a `String`, this is assumed to be a local file path relative to the current working directory of the task.

For example, if I write a task that outputs a file to `./results/file_list.tsv`, and my task is defined as:

```wdl
task do_stuff {
  input {
    File file
  }
  command {
    python do_stuff.py ${file}
  }
  output {
    Array[Array[String]] output_table = read_tsv("./results/file_list.tsv")
  }
}
```

Then when the task finishes, to fulfill the `outputs_table` variable, `./results/file_list.tsv` must be a valid TSV file or an error will be reported.

If the entire contents of the file can not be read for any reason, the calling task or workflow will be considered to have failed. Examples of failure include but are not limited to not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation imposed file size limits.

## Map[String, String] read_map(String|File)

Given a file-like object (`String`, `File`) as a parameter, this will read each line from a file and expect the line to have the format `col1\tcol2`.  In other words, the file-like object must be a two-column TSV file.

This task would `grep` through a file and return all strings that matched the pattern:

The following task would write a two-column TSV to standard out and that would be interpreted as a `Map[String, String]`:

```wdl
task do_stuff {
  input {
    String flags
    File file
  }
  command {
    ./script --flags=${flags} ${file}
  }
  output {
    Map[String, String] mapping = read_map(stdout())
  }
}
```

If the entire contents of the file can not be read for any reason, the calling task or workflow will be considered to have failed. Examples of failure include but are not limited to not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation imposed file size limits.

## Object read_object(String|File)

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

If the entire contents of the file can not be read for any reason, the calling task or workflow will be considered to have failed. Examples of failure include but are not limited to not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation imposed file size limits.

## Array[Object] read_objects(String|File)

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

If the entire contents of the file can not be read for any reason, the calling task or workflow will be considered to have failed. Examples of failure include but are not limited to not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation imposed file size limits.

## mixed read_json(String|File)

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
  input {
    File file
  }
  command {
    python do_stuff.py ${file}
  }
  output {
    Map[String, String] output_table = read_json("./results/file_list.json")
  }
}
```

Then when the task finishes, to fulfill the `output_table` variable, `./results/file_list.json` must be a valid TSV file or an error will be reported.

If the entire contents of the file can not be read for any reason, the calling task or workflow will be considered to have failed. Examples of failure include but are not limited to not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation imposed file size limits.

## Int read_int(String|File)

The `read_int()` function takes a file path which is expected to contain 1 line with 1 integer on it.  This function returns that integer.

If the entire contents of the file can not be read for any reason, the calling task or workflow will be considered to have failed.

## String read_string(String|File)

The `read_string()` function takes a file path which is expected to contain 1 line with 1 string on it.  This function returns that string.

No trailing newline characters should be included

If the entire contents of the file can not be read for any reason, the calling task or workflow will be considered to have failed. Examples of failure include but are not limited to not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation imposed file size limits.

## Float read_float(String|File)

The `read_float()` function takes a file path which is expected to contain 1 line with 1 floating point number on it.  This function returns that float.

If the entire contents of the file can not be read for any reason, the calling task or workflow will be considered to have failed. Examples of failure include but are not limited to not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation imposed file size limits.

## Boolean read_boolean(String|File)

The `read_boolean()` function takes a file path which is expected to contain 1 line with 1 Boolean value (either "true" or "false" on it).  This function returns that Boolean value.

If the entire contents of the file can not be read for any reason, the calling task or workflow will be considered to have failed. Examples of failure include but are not limited to not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation imposed file size limits.

## File write_lines(Array[String])

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

Given any `Object`, this will write out a 2-row, n-column TSV file with the object's attributes and values.

```
task test {
  Object input
  command <<<
    /bin/do_work --obj=~{write_object(input)}
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

Given any `Array[Object]`, this will write out a 2+ row, n-column TSV file with each object's attributes and values.

```wdl
task test {
  input {
    Array[Object] in
  }
  command <<<
    /bin/do_work --obj=~{write_objects(in)}
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

Given something with any type, this writes the JSON equivalent to a file.  See the table in the definition of [read_json()](#mixed-read_jsonstringfile)

```wdl
task example {
  input {
    Map[String, String] map = {"key1": "value1", "key2": "value2"}
  }
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

```json
{
  "key1": "value1"
  "key2": "value2"
}
```

## Float size(File, [String])

Given a `File` and a `String` (optional), returns the size of the file in Bytes or in the unit specified by the second argument.

```wdl
task example {
  input {
    File input_file
  }

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

### Acceptable compound input types
Varieties of the `size` function also exist for the following compound types. The `String` unit is always treated the same as above. Note that to avoid numerical overflow, very long arrays of files should probably favor larger units.
- `Float size(File?, [String])`: Returns the size of the file, if specified, or 0.0 otherwise.
- `Float size(Array[File], [String])`: Returns the sum of sizes of the files in the array.
- `Float size(Array[File?], [String])`: Returns the sum of sizes of all specified files in the array.


## String sub(String, String, String)

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
  input {
    File input_file = "my_input_file.bam"
    String output_file_name = sub(input_file, "\\.bam$", ".index") # my_input_file.index
  }
  command {
    echo "I want an index instead" > ${output_file_name}
  }

  output {
    File outputFile = output_file_name
  }
}
```

## Array[Int] range(Int)

Given an integer argument, the `range` function creates an array of integers of length equal to the given argument. For example `range(3)` provides the array: `(0, 1, 2)`.

## Array[Array[X]] transpose(Array[Array[X]])

Given a two dimensional array argument, the `transpose` function transposes the two dimensional array according to the standard matrix transpose rules. For example `transpose( ((0, 1, 2), (3, 4, 5)) )` will return the rotated two-dimensional array: `((0, 3), (1, 4), (2, 5))`.

## Array[Pair[X,Y]] zip(Array[X], Array[Y])

Given any two Object types, the `zip` function returns the dot product of those Object types in the form of a Pair object.

```
Pair[Int, String] p = (0, "z")
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b", "c" ]
Array[String] zs = [ "d", "e" ]

Array[Pair[Int, String]] zipped = zip(xs, ys)     # i.e.  zipped = [ (1, "a"), (2, "b"), (3, "c") ]
```

## Array[Pair[X,Y]] cross(Array[X], Array[Y])

Given any two Object types, the `cross` function returns the cross product of those Object types in the form of a Pair object.

```
Pair[Int, String] p = (0, "z")
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b", "c" ]
Array[String] zs = [ "d", "e" ]

Array[Pair[Int, String]] crossed = cross(xs, zs) # i.e. crossed = [ (1, "d"), (1, "e"), (2, "d"), (2, "e"), (3, "d"), (3, "e") ]
```

## Array[Pair[X,Y]] as_pairs(Map[X,Y])

Given a Map, the `as_pairs` function returns an Array containing each element in the form of a Pair. The key will be the left element of the Pair and the value the right element. The order of the the Pairs in the resulting Array is the same as the order of the key/value pairs in the Map.

```
Map[String, Int] x = {"a": 1, "b": 2, "c": 3}
Map[String,Pair[File,File]] y = {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}

Array[Pair[String,Int]] xpairs = as_pairs(x) # [("a", 1), ("b", 2), ("c", 3)]
Array[Pair[String,Pair[File,File]]] ypairs = as_pairs(y) # [("a", ("a.bam", "a.bai")), ("b", ("b.bam", "b.bai"))]
```

## Map[X,Y] as_map(Array[Pair[X,Y]])

Given an Array consisting of Pairs, the `as_map` function returns a Map in which the left elements of the Pairs are the keys and the right elements the values. The left element of the Pairs passed to `as_map` must be a primitive type. The order of the key/value pairs in the resulting Map is the same as the order of the Pairs in the Array.

In cases where multiple Pairs would produce the same key, the workflow will fail.

```
Array[Pair[String,Int]] x = [("a", 1), ("b", 2), ("c", 3)]
Array[Pair[String,Pair[File,File]]] y = [("a", ("a.bam", "a.bai")), ("b", ("b.bam", "b.bai"))]

Map[String,Int] xmap = as_map(x) # {"a": 1, "b": 2, "c": 3}
Map[String,Pair[File,File]] ymap = as_map(y) # {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}
```

## Map[X,Array[Y]] collect_by_key(Array[Pair[X,Y]])

Given an Array consisting of Pairs, the `collect_by_key` function returns a Map in which the left elements of the Pairs are the keys and the right elements the values. The left element of the Pairs passed to `as_map` must be a primitive type. The values will be placed in an Array to allow for multiple Pairs to produce the same key. The order of the keys in the Map is the same as the order in the Array based on their first occurence. The order of the elements in the resulting Arrays is the same as their occurence in the given Array of Pairs.

```
Array[Pair[String,Int]] x = [("a", 1), ("b", 2), ("a", 3)]
Array[Pair[String,Pair[File,File]]] y = [("a", ("a_1.bam", "a_1.bai")), ("b", ("b.bam", "b.bai")), ("a", ("a_2.bam", "a_2.bai"))]

Map[String,Array[Int]] xmap = as_map(x) # {"a": [1, 3], "b": [2]}
Map[String,Array[Pair[File,File]]] ymap = as_map(y) # {"a": [("a_1.bam", "a_1.bai"), ("a_2.bam", "a_2.bai")], "b": [("b.bam", "b.bai")]}
```

## Integer length(Array[X])

Given an Array, the `length` function returns the number of elements in the Array as an Integer.

```
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b", "c" ]
Array[String] zs = [ ]

Integer xlen = length(xs) # 3
Integer ylen = length(ys) # 3
Integer zlen = length(zs) # 0
```

## Array[X] flatten(Array[Array[X]])

Given an array of arrays, the `flatten` function concatenates all the
member arrays in the order to appearance to give the result. It does not
deduplicate the elements. Arrays nested more deeply than 2 must be
flattened twice (or more) to get down to an unnested `Array[X]`.
For example:

```wdl
Array[Array[Integer]] ai2D = [[1, 2, 3], [1], [21, 22]]
Array[Integer] ai = flatten(ai2D)   # [1, 2, 3, 1, 21, 22]

Array[Array[File]] af2D = [["/tmp/X.txt"], ["/tmp/Y.txt", "/tmp/Z.txt"], []]
Array[File] af = flatten(af2D)   # ["/tmp/X.txt", "/tmp/Y.txt", "/tmp/Z.txt"]

Array[Array[Pair[Float,String]]] aap2D = [[(0.1, "mouse")], [(3, "cat"), (15, "dog")]]

Array[Pair[Float,String]] ap = flatten(aap2D) # [(0.1, "mouse"), (3, "cat"), (15, "dog")]
```

The last example (`aap2D`) is useful because `Map[X, Y]` can be coerced to `Array[Pair[X, Y]]`.

## Array[String] prefix(String, Array[X])

Given a String and an Array[X] where X is a primitive type, the `prefix` function returns an array of strings comprised
of each element of the input array prefixed by the specified prefix string.  For example:

```
Array[String] env = ["key1=value1", "key2=value2", "key3=value3"]
Array[String] env_param = prefix("-e ", env) # ["-e key1=value1", "-e key2=value2", "-e key3=value3"]

Array[Integer] env2 = [1, 2, 3]
Array[String] env2_param = prefix("-f ", env2) # ["-f 1", "-f 2", "-f 3"]
```

## X select_first(Array[X?])

Given an array of optional values, `select_first` will select the first defined value and return it. Note that this is a runtime check and requires that at least one defined value will exist: if no defined value is found when select_first is evaluated, the workflow will fail.

## Array[X] select_all(Array[X?])

Given an array of optional values, `select_all` will select only those elements which are defined.

## Boolean defined(X?)

This function will return `false` if the argument is an unset optional value. It will return `true` in all other cases.

## String basename(String)

- This function returns the basename of a file path passed to it: `basename("/path/to/file.txt")` returns `"file.txt"`.
- Also supports an optional parameter, suffix to remove: `basename("/path/to/file.txt", ".txt")` returns `"file"`.

## Int floor(Float), Int ceil(Float) and Int round(Float)

- These functions convert a Float value into an Int by:
  - floor: Round **down** to the next lower integer
  - ceil: Round **up** to the next higher integer
  - round: Round to the nearest integer based on standard rounding rules

# Data Types & Serialization

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
  input {
    Array[File] files
  }
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

Serializing primitive inputs into strings is intuitively easy because the value is just turned into a string and inserted into the command line.

Consider this example:

```wdl
task output_example {
  input {
    String s
    Int i
    Float f
  }

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

Compound types, like `Array` and `Map` must be converted to a primitive type before it can be used in the command.  There are many ways to turn a compound types into primitive types, as laid out in following sections

#### Array serialization

Arrays can be serialized in two ways:

* **Array Expansion**: elements in the list are flattened to a string with a separator character.
* **File Creation**: create a file with the elements of the array in it and passing that file as the parameter on the command line.

##### Array serialization by expansion

The array flattening approach can be done if a parameter is specified as `${sep=' ' my_param}`.  `my_param` must be declared as an `Array` of primitive types.  When the value of `my_param` is specified, then the values are joined together with the separator character (a space in this case).  For example:

```wdl
task test {
  input {
    Array[File] bams
  }
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

An array may be turned into a file with each element in the array occupying a line in the file.

```wdl
task test {
  input {
    Array[File] bams
  }
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

The array may be turned into a JSON document with the file path for the JSON file passed in as the parameter:

```wdl
task test {
  input {
    Array[File] bams
  }
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

Map types cannot be serialized on the command line directly and must be serialized through a file

##### Map serialization using write_map()

The map type can be serialized as a two-column TSV file and the parameter on the command line is given the path to that file, using the `write_map()` function:

```wdl
task test {
  input {
    Map[String, Float] sample_quality_scores
  }
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

The map type can also be serialized as a JSON file and the parameter on the command line is given the path to that file, using the `write_json()` function:

```wdl
task test {
  input {
    Map[String, Float] sample_quality_scores
  }
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

An object is a more general case of a map where the keys are strings and the values are of arbitrary types and treated as strings.  Objects can be serialized with either `write_object()` or `write_json()` functions:

##### Object serialization using write_object()

```wdl
task test {
  input {
    Object sample
  }
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

```wdl
task test {
  input {
    Object sample
  }
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

`Array[Object]` must guarantee that all objects in the array have the same set of attributes.  These can be serialized with either `write_objects()` or `write_json()` functions, as described in following sections.

##### Array[Object] serialization using write_objects()

an `Array[Object]` can be serialized using `write_objects()` into a TSV file:

```wdl
task test {
  input {
    Array[Object] sample
  }
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

an `Array[Object]` can be serialized using `write_json()` into a JSON file:

```wdl
task test {
  input {
    Array[Object] sample
  }
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

A task's command can only output data as files.  Therefore, every de-serialization function in WDL takes a file input and returns a WDL type

### Primitive Types

De-serialization of primitive types is done through a `read_*` function.  For example, `read_int("file/path")` and `read_string("file/path")`.

For example, if I have a task that outputs a `String` and an `Int`:

```wdl
task output_example {
  input {
    String param1
    String param2
  }
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

Tasks can also output to a file or stdout/stderr an `Array`, `Map`, or `Object` data structure in a two major formats:

* JSON - because it fits naturally with the types within WDL
* Text based / TSV - These are usually simple table and text-based encodings (e.g. `Array[String]` could be serialized by having each element be a line in a file)

#### Array deserialization

Maps are deserialized from:

* Files that contain a JSON Array as their top-level element.
* Any file where it is desirable to interpret each line as an element of the `Array`.

##### Array deserialization using read_lines()

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

Maps are deserialized from:

* Files that contain a JSON Object as their top-level element.
* Files that contain a two-column TSV file.

##### Map deserialization using read_map()

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

Objects are deserialized from files that contain a two-row, n-column TSV file.  The first row are the object attribute names and the corresponding entries on the second row are the values.

##### Object deserialization using read_object()

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

`Array[Object]` MUST assume that all objects in the array are homogeneous (they have the same attributes, but the attributes don't have to have the same values)

An `Array[Object]` is deserialized from files that contains at least 2 rows and a uniform n-column TSV file.  The first row are the object attribute names and the corresponding entries on the subsequent rows are the values

##### Object deserialization using read_objects()

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
