# Workflow Description Language

## Table of Contents

* [Workflow Description Language](#workflow-description-language)
  * [Introduction](#introduction)
* [Language Specification](#language-specification)
  * [Global Grammar Rules](#global-grammar-rules)
    * [Whitespace, Strings, Identifiers, Constants](#whitespace-strings-identifiers-constants)
    * [Comments](#comments)
    * [Types](#types)
      * [Custom  Types](#custom--types)
    * [Fully Qualified Names &amp; Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers)
    * [Declarations](#declarations)
    * [Expressions](#expressions)
      * [If then else](#if-then-else)
    * [Operator Precedence Table](#operator-precedence-table)
    * [Member Access](#member-access)
    * [Map and Array Indexing](#map-and-array-indexing)
    * [Pair Indexing](#pair-indexing)
    * [Function Calls](#function-calls)
    * [Array Literals](#array-literals)
    * [Map Literals](#map-literals)
    * [Pair Literals](#pair-literals)
    * [Optional Literals](#optional-literals)
    * [Keywords](#keywords)
  * [Versioning](#versioning)
  * [Import Statements](#import-statements)
  * [Task Definition](#task-definition)
    * [Task Sections](#task-sections)
    * [Task Inputs](#task-inputs)
      * [Task Input Declaration](#task-input-declaration)
      * [Task Input Localization](#task-input-localization)
        * [Special Case: Versioning Filesystems](#special-case-versioning-filesystems)
    * [Non-Input Declarations](#non-input-declarations)
    * [Command Section](#command-section)
      * [Expression Placeholders](#expression-placeholders)
      * [Expression Placeholder Options](#expression-placeholder-options)
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
      * [Omitting Workflow Outputs](#omitting-workflow-outputs)
  * [Struct Definition](#struct-definition)
    * [Struct Declarations](#struct-declarations)
      * [Optional and non Empty Struct Values](#optional-and-non-empty-struct-values)
    * [Using a Struct](#using-a-struct)
      * [Struct Assignment from Map Literal](#struct-assignment-from-map-literal)
    * [Struct Member Access](#struct-member-access)
    * [Importing Structs](#importing-structs)
* [Namespaces](#namespaces)
* [Scope](#scope)
* [Optional Parameters &amp; Type Constraints](#optional-parameters--type-constraints)
  * [Prepending a String to an Optional Parameter](#prepending-a-string-to-an-optional-parameter)
* [Scatter / Gather](#scatter--gather)
* [Variable Resolution](#variable-resolution)
  * [Task-Level Resolution](#task-level-resolution)
  * [Workflow-Level Resolution](#workflow-level-resolution)
* [Computing Inputs](#computing-inputs)
  * [Computing Task Inputs](#computing-task-inputs)
  * [Computing Workflow Inputs](#computing-workflow-inputs)
  * [Specifying Workflow Inputs](#specifying-workflow-inputs)
    * [Cromwell-style inputs](#cromwell-style-inputs)
  * [Optional Inputs](#optional-inputs)
  * [Declared Inputs: Defaults and Overrides](#declared-inputs-defaults-and-overrides)
    * [Optional Inputs with Defaults](#optional-inputs-with-defaults)
  * [Call Input Blocks](#call-input-blocks)
* [Type Coercion](#type-coercion)
* [Standard Library](#standard-library)
  * [File stdout()](#file-stdout)
  * [File stderr()](#file-stderr)
  * [Array[String] read_lines(String|File)](#arraystring-read_linesstringfile)
  * [Array[Array[String]] read_tsv(String|File)](#arrayarraystring-read_tsvstringfile)
  * [Map[String, String] read_map(String|File)](#mapstring-string-read_mapstringfile)
  * [mixed read_json(String|File)](#mixed-read_jsonstringfile)
  * [Int read_int(String|File)](#int-read_intstringfile)
  * [String read_string(String|File)](#string-read_stringstringfile)
  * [Float read_float(String|File)](#float-read_floatstringfile)
  * [Boolean read_boolean(String|File)](#boolean-read_booleanstringfile)
  * [File write_lines(Array[String])](#file-write_linesarraystring)
  * [File write_tsv(Array[Array[String]])](#file-write_tsvarrayarraystring)
  * [File write_map(Map[String, String])](#file-write_mapmapstring-string)
  * [File write_json(mixed)](#file-write_jsonmixed)
  * [Float size(File, [String])](#float-sizefile-string)
    * [Acceptable compound input types](#acceptable-compound-input-types)
  * [String sub(String, String, String)](#string-substring-string-string)
  * [Array\[Int\] range(Int)](#arrayint-rangeint)
  * [Array\[Array\[X\]\] transpose(Array\[Array\[X\]\])](#arrayarrayx-transposearrayarrayx)
  * [Array\[Pair(X,Y)\] zip(Array\[X\], Array\[Y\])](#arraypairxy-ziparrayx-arrayy)
  * [Array\[Pair(X,Y)\] cross(Array\[X\], Array\[Y\])](#arraypairxy-crossarrayx-arrayy)
  * [Array\[Pair(X,Y)\] as_pairs(Map\[X,Y\])](#arraypairxy-as_pairsmapxy)
  * [Map\[X,Y\] as_map(Array\[Pair(X,Y)\])](#mapxy-as_maparraypairxy)
  * [Array\[X\] keys(Map\[X,Y\])](#arrayx-keysmapxy)
  * [Map\[X,Array\[Y\]\] collect_by_key(Array\[Pair(X,Y)\])](#mapxarrayy-collect_by_keyarraypairxy)
  * [Int length(Array\[X\])](#int-lengtharrayx)
  * [Array\[X\] flatten(Array\[Array\[X\]\])](#arrayx-flattenarrayarrayx)
  * [Array\[String\] prefix(String, Array\[X\])](#arraystring-prefixstring-arrayx)
  * [X select_first(Array\[X?\])](#x-select_firstarrayx)
  * [Array\[X\] select_all(Array\[X?\])](#arrayx-select_allarrayx)
  * [Boolean defined(X?)](#boolean-definedx)
  * [String basename(String)](#string-basenamestring)
  * [Int floor(Float), Int ceil(Float) and Int round(Float)](#int-floorfloat-int-ceilfloat-and-int-roundfloat)
* [Data Types &amp; Serialization](#data-types--serialization)
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
      * [Struct serialization](#struct-serialization)
      * [Struct serialization using write_json()](#struct-serialization-using-write_json)
  * [De-serialization of Task Outputs](#de-serialization-of-task-outputs)
    * [Primitive Types](#primitive-types-1)
    * [Compound Types](#compound-types-1)
      * [Array deserialization](#array-deserialization)
        * [Array deserialization using read_lines()](#array-deserialization-using-read_lines)
        * [Array deserialization using read_json()](#array-deserialization-using-read_json)
      * [Map deserialization](#map-deserialization)
        * [Map deserialization using read_map()](#map-deserialization-using-read_map)
        * [Map deserialization using read_json()](#map-deserialization-using-read_json)

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

The user must provide a value for these two parameters in order for this task to be runnable.  Implementations of WDL should accept their [inputs as JSON format](#specifying-workflow-inputs-in-json). The inputs described in such a JSON file should be fully qualified according to the namespacing rules described in the [Fully Qualified Names & Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers) section. For example, the above task needs values for two parameters: `String pattern` and `File in`:

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

```sh
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

# Language Specification

## Global Grammar Rules

WDL files are encoded in UTF-8, with no BOM.

### Whitespace, Strings, Identifiers, Constants

These are common among many of the following sections

```txt
$ws = (0x20 | 0x09 | 0x0D | 0x0A)+
$identifier = [a-zA-Z][a-zA-Z0-9_]+
$boolean = 'true' | 'false'
$integer = [1-9][0-9]*|0[xX][0-9a-fA-F]+|0[0-7]*
$float = (([0-9]+)?\.([0-9]+)|[0-9]+\.|[0-9]+)([eE][-+]?[0-9]+)?
```

`$string` can accept the following between single or double-quotes:

* Any character not in set: `\`, `"` (or `'` for single-quoted string), `\n`
* An escape sequence starting with `\`, followed by one of the following characters: `\nt"'`
* An escape sequence starting with `\`, followed by 3 digits of value 0 through 7 inclusive.  This specifies an octal escape code.
* An escape sequence starting with `\x`, followed by 2 hexadecimal digits `0-9a-fA-F`.  This specifies a hexadecimal escape code.
* An escape sequence starting with `\u` followed by 4 hexadecimal characters or `\U` followed by 8 hexadecimal characters `0-9a-fA-F`.  This specifies a unicode code point.

|Escape Sequence|Meaning|\x Equivalent|
|-|-|-|
|`\\`|`\`|`\x5C`|
|`\n`|newline|`\x0A`|
|`\t`|tab|`\x09`|
|`\'`|single quote|`\x22`|
|`\"`|double quote|`\x27`|

### Comments

Comments are a useful way of providing helpful information such as workflow usage, requirements, copyright etc directly within the wdl file. Comments can be added anywhere within the `WDL` document and are used to indicate text which should be ignored by an engine implementation. The one caveat to be aware of, is that within the `command` section, *ALL* text will be included in the underlying command and any lines prepended by `#` will be included.

A comment is started with the hash symbol `#`. Any text following the number sign will be completely ignored, regardless of its content by an engine. Comments can be placed at the start of a new line or after any declarations within the WDL itself. At the moment, there is no special syntax for multi-line comments, instead simply use a `#` at the start of each line.

```wdl
# Comments are allowed before versions

version 1.0

# This is how you would
# write a long
# multiline
# comment

task test {

    #This comment will not be included within the command
    command <<<
        #This comment WILL be included within the command after it has been parsed
        echo 'Hello World'
    >>>

    output {
        String result = read_string(stdout())
    }
}


workflow wf {
  input {
    Int number  #This comment comes after a variable declaration
  }

  #You can have comments anywhere in the workflow
  call test

  output { #You can also put comments after braces
    String result = test.result
  }

}
```

### Types

In WDL *all* types represent immutable values.

* Even types like `File` and `Directory` represent logical "snapshots" of the file or directory at the time when the value was created.
* It's impossible for a task to change an upstream value which has been provided as an input: even if it makes changes to its local copy the original value is unaffected.

All inputs and outputs must be typed. The following primitive types exist in WDL:

```wdl
Int i = 0                  # An integer value
Float f = 27.3             # A floating point number
Boolean b = true           # A boolean true/false
String s = "hello, world"  # A string value
File f = "path/to/file"    # A file
Directory d = "/path/to/"  # The contents of a directory (including sub-directories)
```

In addition, the following compound types can be constructed, parameterized by other types. In the examples below `P` represents any of the primitive types above, and `X` and `Y` represent any valid type (even nested compound types):

```wdl
Array[X] xs = [x1, x2, x3]                    # An array of Xs
Map[P,Y] p_to_y = { p1: y1, p2: y2, p3: y3 }  # An ordered map from Ps to Ys
Pair[X,Y] x_and_y = (x, y)                    # A pair of one X and one Y

struct BamAndIndex {
    File bam
    File bam_index
}
BamAndIndex b_and_i = {"bam":"NA12878.bam", "bam_index":"NA12878.bam.bai"}
BamAndIndex b_and_i_2 = object {bam:"NA12878.bam", bam_index:"NA12878.bam.bai"}
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

#### Numeric Behavior

`Int` and `Float` are the numeric types.
`Int` can be used to hold a signed Integer in the range \[-2^63, 2^63).
`Float` is a finite 64-bit IEEE-754 floating point number.

#### Custom Types

WDL provides the ability to define custom compound types called `Structs`. `Structs` are defined directly in the WDL and are usable like any other type.
For more information on their usage, see the section on [Structs](#struct-definition)

### Fully Qualified Names & Namespaced Identifiers

```txt
$fully_qualified_name = $identifier ('.' $identifier)*
$namespaced_identifier = $identifier ('.' $identifier)*
```

A fully qualified name is the unique identifier of any particular call, input or output. These follow the following structure:
* For calls: `<parent namespace>.<call alias>`
  * For calls to workflows the following structure is also permitted and is considered an alias to the above mentioned structure:  
    `<parent namespace>.<call alias>.<workflow name>`. Using this structure is not recommended as it will likely be deprecated in the future.
* For inputs and outputs: `<parent namespace>.<input or output name>`

The `parent namespace` here will equal the fully qualified name of the call containing the call, input or output. For the top-level workflow this is equal to the workflow name, as it lacks a call alias.

For example:

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

workflow otherWorkflow {
    input {
        Boolean bool
    }
    call foobar
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
  call other.otherWorkflow
  call other.otherWorkflow as otherWorkflow2
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
* `wf.otherWorkflow` - References the first call to subworkflow `other.otherWorkflow`
* `wf.otherWorkflow.bool` - References the `Boolean` input of the first call to subworkflow `other.otherWorkflow`
* `wf.otherWorkflow.foobar.results` - References the `File` output of the call to `foobar` inside the first call to subworkflow `other.otherWorkflow`
* `wf.otherWorkflow.foobar.input` - References the `File` input of the call to `foobar` inside the first call to subworkflow `other.otherWorkflow`
* `wf.otherWorkflow2` - References the second call to subworkflow `other.otherWorkflow` (aliased as otherWorkflow2)
* `wf.otherWorkflow2.bool` - References the `Boolean` input of the second call to subworkflow `other.otherWorkflow`
* `wf.otherWorkflow2.foobar.results` - References the `File` output of the call to `foobar` inside the second call to subworkflow `other.otherWorkflow`
* `wf.otherWorkflow2.foobar.input` - References the `File` input of the call to `foobar` inside the second call to subworkflow `other.otherWorkflow`
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

```txt
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

```txt
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
|`Boolean`|`||`|`Boolean`|`Boolean`||
|`Boolean`|`&&`|`Boolean`|`Boolean`||
|`File`|`==`|`File`|`Boolean`||
|`File`|`!=`|`File`|`Boolean`||
|`Float`|`+`|`Float`|`Float`||
|`Float`|`-`|`Float`|`Float`||
|`Float`|`*`|`Float`|`Float`||
|`Float`|`/`|`Float`|`Float`||
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
|`Float`|`>`|`Int`|`Boolean`||
|`Float`|`>=`|`Int`|`Boolean`||
|`Float`|`<`|`Int`|`Boolean`||
|`Float`|`<=`|`Int`|`Boolean`||
|`Int`|`+`|`Float`|`Float`||
|`Int`|`-`|`Float`|`Float`||
|`Int`|`*`|`Float`|`Float`||
|`Int`|`/`|`Float`|`Float`||
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
|`String`|`+`|`String`|`String`|Concatenation|
|`String`|`==`|`String`|`Boolean`||
|`String`|`!=`|`String`|`Boolean`||
|`String`|`>`|`String`|`Boolean`||
|`String`|`>=`|`String`|`Boolean`||
|`String`|`<`|`String`|`Boolean`||
|`String`|`<=`|`String`|`Boolean`||
||`-`|`Float`|`Float`||
||`-`|`Int`|`Int`||
||`!`|`Boolean`|`Boolean`||

Note: In expressions using an operator with mismatched numeric types,
the `Int` will be cast to `Float` and the result will be `Float`.
This will cause loss of precision if the `Int` is too large to be represented exactly by the `Float`.
The `Float` can be converted to `Int` with the `ceil`, `round` or `floor` functions if needed.

#### If then else

This is an operator that takes three arguments, a condition expression, an if-true expression and an if-false expression. The condition is always evaluated. If the condition is true then the if-true value is evaluated and returned. If the condition is false, the if-false expression is evaluated and returned. The return type of the if-then-else should be the same, regardless of which side is evaluated or runtime problems might occur.

Examples:

* Choose whether to say "good morning" or "good afternoon":

```wdl
Boolean morning = ...
String greeting = "good " + if morning then "morning" else "afternoon"
```

* Choose how much memory to use for a task:

```wdl
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

### Member Access

The syntax `x.y` refers to member access. `x` must be a task in a workflow, or struct. A Task can be thought of as a struct where the attributes are the outputs of the task.

```wdl
call foo
String x = foo.y

Struct z
String a = z.b
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

```wdl
Array[String] a = ["a", "b", "c"]
Array[Int] b = [0,1,2]
```

### Map Literals

Map values can be specified using a similar Python-like syntax:

```wdl
Map[Int, Int] = {1: 10, 2: 11}
Map[String, Int] = {"a": 1, "b": 2}
String a = "one"
Map[String, Int] = {a: 1, "not " + a: 2}
```

### Object Literals

Similar to Map literals, however object literal keys are unquoted strings.
This makes them well suited for assigning to `Structs`.
Beware the behaviour difference with Map literals

```wdl
Map[String, Int] map_1 = object {a: 1, b: 2}
String a = "one"
String b = "two"
# map_2 != map_1
Map[String, Int] map_2 = {a: 1, b: 2}
```

map_1 has the keys 'a' and 'b'.
map_2 has the keys 'one' and 'two'.

### Pair Literals

Pair values can be specified inside of a WDL using another Python-like syntax, as follows:

```wdl
Pair[Int, String] twenty_threes = (23, "twenty-three")
```

Pair values can also be specified within the [workflow inputs JSON](https://github.com/openwdl/wdl/blob/develop/SPEC.md#specifying-workflow-inputs-in-json) with a `Left` and `Right` value specified using JSON style syntax. For example, given a workflow `wf_hello` and workflow-level variable `twenty_threes`, it could be declared in the workflow inputs JSON as follows:

```json
{
  "wf_hello.twenty_threes": { "Left": 23, "Right": "twenty-three" }
}
```

### Optional literals

Any non-optional value can be stored into an optional variable by assigning it to an optional variable.
This does not change the value, but it changes the type of the value:

```wdl
Int? maybe_five = 5
```

The `None` literal is the value that an optional has when it is not defined.

```wdl
Int? maybe_five_but_is_not = None
# maybe_five_but_is_not is an undefined optional
Int? maybe_five_and_is = 5
# maybe_five_and_is is a defined optional
Int certainly_five = 5
# Certainly five is not an optional

Boolean test_defined = defined(maybe_five_but_is_not) # Evaluates to false
Boolean test_defined2 = defined(maybe_five_and_is) # Evaluates to true
Boolean test_is_none = maybe_five_but_is_not == None # Evaluates to true, same as !definedmaybe_five_but_is_not)
Boolean test_not_none = maybe_five_but_is_not != None # Evaluates to false, same as defined(maybe_five_but_is_not )
```

### Keywords

The following language keywords cannot be used as the names of values, calls, tasks, workflows, import namespaces, or struct types & aliases.

```txt
Array Float Int Map None Pair String
alias as call command else false if
import input left meta object output
parameter_meta right runtime scatter
struct task then true workflow
```

## Versioning

For portability purposes it is critical that WDL documents be versioned so an engine knows how to process it. From `draft-3` forward, the first non-comment statement of all WDL files must be a `version` statement, for example

```wdl
version draft-3
```

or

```wdl
#Licence header

version draft-3
```

Any WDL files which do not have a `version` field must be treated as `draft-2`.  All WDL files used by a workflow must have the same version.

## Import Statements

A WDL file may contain import statements to include WDL code from other sources

```txt
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
* No protocol (see below)

In the event that there is no protocol the import is resolved **relative** to the location of the current document. If a protocol-less import starts with `/` it will be interpreted as starting from the root of the host in the resolved URL. It is up to the implementation to provide a mechanism which allows these imports to be resolved correctly.

Some examples of correct import resolution:

| Root Workflow Location                                | Imported Path                      | Resolved Path                                           |
|-------------------------------------------------------|------------------------------------|---------------------------------------------------------|
| `file://foo/bar/baz/qux.wdl`                            | `some/task.wdl`                      | `file://foo/bar/baz/some/task.wdl`                        |
| `http://www.github.com/openwdl/coolwdls/myWorkflow.wdl` | `subworkflow.wdl`                    | `http://www.github.com/openwdl/coolwdls/subworkflow.wdl`  |
| `http://www.github.com/openwdl/coolwdls/myWorkflow.wdl` | `/openwdl/otherwdls/subworkflow.wdl` | `http://www.github.com/openwdl/otherwdls/subworkflow.wdl` |
| `file://some/path/hello.wdl`                            | `/another/path/world.wdl`            | `file:///another/path/world.wdl`                          |

## Task Definition

A task is a declarative construct with a focus on constructing a command from a template.  The command specification is interpreted in an engine and backend agnostic way. The command is a UNIX bash command line which will be run (ideally in a Docker image).

Tasks explicitly define their inputs and outputs which is essential for building dependencies between tasks.

To declare a task, use `task name { ... }`.  Inside the curly braces are the following sections:

### Task Sections

The task may have the following component sections:

* An `input` section (required if the task will have inputs)
* Non-input declarations (as many as needed, optional)
* A `command` section (required)
* A `runtime` section (optional)
* An `output` section (required if the task will have outputs)
* A `meta` section (optional)
* A `parameter_meta` section (optional)

### Task Inputs

#### Task Input Declaration

Tasks declare inputs within the task block. For example:

```wdl
task t {
  input {
    Int i
    File f
    Directory d
  }

  # [... other task sections]
}
```

#### Task Input Localization

`File` and `Directory` inputs must be treated specially since they require localization to within the execution directory:

* Files and directories are localized into the execution directory prior to the task execution commencing.
* When localizing a `File`, the engine may choose to place the file wherever it likes so long as it accords to these rules:
  * The original file name must be preserved even if the path to it has changed.
  * Two input files with the same name must be located separately, to avoid name collision.
  * Two input files which originated in the same storage directory must also be localized into the same directory for task execution (see the special case handling for Versioning Filesystems below).
* When localizing a `Directory`, the engine follows the same set of rules as for Files:
  * The original directory name must be preserved even if the path to it has changed.
  * Two input directories with the same name must be located separately, to avoid name collision.
  * Two input directories which originated in the same parent storage directory must be localized into the same parent directory for task execution.
  * The internal structure of files and sub-directories in the directory is preserved within the new directory location.
* When a WDL author uses a `File` input in their [Command Section](#command-section), the fully qualified, localized path to the file is substituted into the command string.
* When a WDL author uses a `Directory` input in their [Command Section](#command-section), the fully qualified localized path to the directory (with no trailing '/') is substituted into the command string.

##### Special Case: Versioning Filesystems

Two or more versions of a file in a versioning filesystem might have the same name and come from the same directory. In that case the following special procedure must be used to avoid collision:

* The first file is always placed as normal according to the usual rules.
* Subsequent files that would otherwise overwrite this file are instead placed in a subdirectory named for the version.

For example imagine two versions of file `fs://path/to/A.txt` are being localized (labeled version `1.0` and `1.1`). The first might be localized as `/execution_dir/path/to/A.txt`. The second must then be placed in `/execution_dir/path/to/1.1/A.txt`

### Non-Input Declarations

A task can have declarations which are intended as intermediate values rather than inputs. These declarations can be based on input values and can be used within the command section.

For example, this task takes an input, but performs some calculation which can then be used by the command:

```wdl
task t {
  input {
    Int size
  }
  size_clamped = if size > 10 then 10 else size

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
This is immediately possible for WDL primitive types (e.g. not `Array`, `Map`, or `Struct`).
To place an array into the command block a separator character must be specified using `sep` (eg `${sep=", " int_array}`).

As another example, consider how the parser would parse the following command:

```sh
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

```sh
python script.py 1,2,3
```

Alternatively, if the command were `python script.py ${sep=' ' numbers}` it would parse to:

```sh
python script.py 1 2 3
```

> *Additional requirements*: sep MUST accept only a string as its value

##### true and false

'true' and 'false' are available for expressions which evaluate to `Boolean`s. They specify a string literal to insert into the command block when the result is true or false respectively.

For example, `${true='--enable-foo' false='--disable-foo' allow_foo}` would evaluate the expression `allow_foo` as a variable lookup and depending on its value would either insert the string `--enable-foo` or `--disable-foo` into the command.

Both `true` and `false` cases are required. If one case should insert no value then an empty string literal should be used, eg `${true='--enable-foo' false='' allow_foo}`

1. `true` and `false` values MUST be string literals.
2. `true` and `false` are only allowed if the type is `Boolean`
3. Both `true` and `false` cases are required.
4. Consider using the expression `${if allow_foo then "--enable-foo" else "--disable-foo"}` as a more readable alternative which allows full expressions (rather than string literals) for the true and false cases.

##### default

This specifies the default value if no other value is specified for this parameter.

```wdl
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

> *Additional requirements*:
>
> 1. The type of the expression must match the type of the parameter
> 2. If 'default' is specified, the `$type_postfix_quantifier` for the variable's type MUST be `?`

#### Alternative heredoc syntax

Sometimes a command is sufficiently long enough or might use `{` characters that using a different set of delimiters would make it more clear.  In this case, enclose the command in `<<<`...`>>>`, as follows:

```wdl
task heredoc {
  input {
    File in
  }

  command<<<
  python <<CODE
    with open("~{in}") as fp:
      for line in fp:
        if not line.startswith('#'):
          print(line.strip())
  CODE
  >>>
}
```

Parsing of this command should be the same as the prior section describes.  As noted earlier in the [Expression Placeholders](#command-parts) section, it is important to remember that string interpolation within `<<<`...`>>>` blocks must be done using the syntax `~{expression}`.

#### Stripping Leading Whitespace

Any text inside of the `command` section, after instantiated, should have all *common leading whitespace* removed.  In the `task heredoc` example in the previous section, if the user specifies a value of `/path/to/file` as the value for `File in`, then the command should be:

```sh
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

```wdl
output {
  Int threshold = read_int("threshold.txt")
}
```

The task is expecting that a file called "threshold.txt" will exist in the current working directory after the command is executed. Inside that file must be one line that contains only an integer and whitespace.  See the [Data Types & Serialization](#data-types--serialization) section for more details.

As with other string literals in a task definition, Strings in the output section may contain interpolations (see the [String Interpolation](#string-interpolation) section below for more details). Here's an example:

```wdl
output {
  Array[String] quality_scores = read_lines("${sample_id}.scores.txt")
}
```

Note that for this to work, `sample_id` must be declared as an input to the task.

As with inputs, the outputs can reference previous outputs in the same block. The only requirement is that the output being referenced must be specified *before* the output which uses it.

```wdl
output {
  String a = "a"
  String ab = a + "b"
}
```

#### File Outputs

Individual `File` outputs can be declared using a String path relative to the execution directory. For example:

```wdl
output {
  File f = "created_file"
}
```

Notes:

* When a file is output, the name and contents are considered part of the output but the local path is not.
* If the specified file is a hard- or soft- link then it shall be resolved into a regular file for the WDL `File` output.

#### Directory Outputs

A `Directory` can be declared as an output just like a `File`. For example:

```wdl
output {
  Directory d = "created/directory"
}
```

Notes:

* When a directory is output, the name and contents (including subdirectories) are considered part of the output but the path is not.
* Any hard- or soft- links within the execution directory shall be resolved into separate, regular files in the WDL `Directory` value produced as the output.

##### Soft link resolution example

For example imagine a task which produces:

```txt
dir/
 - a           # a file, 10 MB
 - b -> a      # a softlink to 'a'
```

As a WDL directory this would manifest as:

```txt
dir/
 - a           # a file, 10 MB
 - b           # another file, 10 MB
```

And therefore if used as an input to a subsequent task:

```txt
dir/
 - a           # a file, 10 MB
 - b           # another file, 10 MB
```

#### Globs

Globs can be used to define outputs which might contain zero, one, or many files. The glob function therefore returns an array of File outputs:

```wdl
output {
  Array[File] output_bams = glob("*.bam")
}
```

The array of `File`s returned is the set of files found by the bash expansion of the glob string relative to the task's execution directory and in the same order. It's evaluated in the context of the bash shell installed in the docker image running the task.

In other words, you might think of `glob()` as finding all of the files (but not the directories) in the same order as would be matched by running `echo <glob>` in bash from the task's execution directory.

Note that this usually will not include files in nested directories. For example say you have an output `Array[File] a_files = glob("a*")` and the end result of running your command has produced a directory structure like this:

```txt
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

Any `${expression}` or `~{expression}` inside of a string literal must be replaced with the value of the expression.  If prefix were specified as `"foobar"`, then `"${prefix}.out"` would be evaluated to `"foobar.out"`.

Different types for the expression are formatted in different ways.
`String` is substituted directly.
`File` is substituted as if it were a `String`.
`Int` is formatted without leading zeros (unless the value is `0`), with a leading `-` if the value is negative.
`Float` is printed in the style `[-]ddd.ddd`, with 6 digits after the decimal point.
The expression cannot have the value of any other type.

```wdl
"${"abc"}" == "abc"

File def = "hij"
"${def}" == "hij"

"${5}" == "5"

"${3.141}" == "3.141000"
"${3.141 * 1E-10}" == "0.000000"
"${3.141 * 1E10}" == "31410000000.000000"
```

### Runtime Section

```txt
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

```txt
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
    f : { help: "Count the number of lines in this file" }
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

```txt
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
    Array[Int]+ min_std_max_min
    File reference
    Array[File]+ reads
  }
  command {
    bwa mem -t ${threads} \
            -k ${min_seed_length} \
            -I ${sep=',' min_std_max_min} \
            ${reference} \
            ${sep=' ' reads} > output.sam
  }
  output {
    File sam = "output.sam"
  }
  runtime {
    docker: "broadinstitute/baseimg"
  }
}
```

One notable piece in this example is `${sep=',' min_std_max_min}` which specifies that min_std_max_min will be flattened by combining the elements with the separator character (`sep=','`).

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

```sh
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

For this particular case where the command line is *itself* a mini DSL, The best option at that point is to allow the user to type in the rest of the command line, which is what `${sep=' ' stages}` is for.  This allows the user to specify an array of strings as the value for `stages` and then it concatenates them together with a space character

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

* No inputs:

```json
{ }
```

* Only x:

```json
{
  "x": 100
}
```

* Only y:

```json
{
  "x": null,
  "y": "/path/to/file"
}
```

* x and y:

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

A workflow calls other tasks/workflows via the `call` keyword.  A `call` is followed by the name of the task or subworkflow to run.  Most commonly that's simply the name of a task (see examples below), but it can also use `.` as a namespace resolver.

See the section on [Fully Qualified Names & Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers) for details about how the identifier ought to be interpreted.

All `call` statements must be uniquely identifiable.  By default, the call's unique identifier is the task name (e.g. `call foo` would be referenced by name `foo`).  However, if one were to `call foo` twice in a workflow, each subsequent `call` statement will need to alias itself to a unique name using the `as` clause: `call foo as bar`.

A `call` statement may reference a workflow too (e.g. `call other_workflow`).  In this case, the inputs section specifies the workflow's inputs by name.

Calls can be run as soon as their inputs are available. If `call x`'s inputs are based on `call y`'s outputs, this means that `call x` can be run as soon as `call y` has completed.

To add a dependency from x to y that isn't based on outputs, you can use the `after` keyword, such as `call x after y after z`. But note that this is only required if `x` doesn't already depend on an output from `y`.

Here are some examples:

```wdl
import "lib.wdl" as lib
workflow wf {
  # Calls my_task
  call my_task

  # Calls it another time straight away.
  # We need to give this one an alias to avoid name-collision
  call my_task as my_task_alias

  # Call it a third time
  # This time, wait until the first my_task has completed before running it.
  call my_task as my_task_alias2 after my_task {
    input: threshold=2
  }

  # Call a task imported from lib:
  call lib.other_task
}
```

The call inputs block (eg `{ input: x=a, y=b, z=c } `) is optional and specifies how to satisfy a subset of the the task or workflow's input parameters. An empty call inputs block of the form `call no_input_task { }` is valid and has the same meaning as `call no_input_task`.

Each variable mapping in the call inputs block maps input parameters in the task to expressions from the workflow.  These expressions usually reference outputs of other tasks, but they can be arbitrary expressions.

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

```wdl
import "sub_wdl.wdl" as sub

workflow main_workflow {

    call sub.wf_hello { input: wf_hello_input = "sub world" }

    output {
        String main_output = wf_hello.salutation
    }
}
```

`sub_wdl.wdl`

```wdl
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

```txt
$scatter = 'scatter' $ws* '(' $ws* $scatter_iteration_statement $ws*  ')' $ws* $scatter_body
$scatter_iteration_statement = $identifier $ws* 'in' $ws* $expression
$scatter_body = '{' $ws* $workflow_element* $ws* '}'
```

A "scatter" clause defines that everything in the body (`$scatter_body`) can be run in parallel.  The clause in parentheses (`$scatter_iteration_statement`) declares which collection to scatter over and what to call each element.

The `$scatter_iteration_statement` has two parts: the "item" and the "collection".  For example, `scatter(x in y)` would define `x` as the item, and `y` as the collection.  The item is always an identifier, while the collection is an expression that MUST evaluate to an `Array` type.  The item will represent each item in that expression.  For example, if `y` evaluated to an `Array[String]` then `x` would be a `String`.

The `$scatter_body` defines a set of scopes that will execute in the context of this scatter block.

For example, if `$expression` is an array of integers of size 3, then the body of the scatter clause can be executed 3-times in parallel.  `$identifier` would refer to each integer in the array.

```wdl
scatter(i in integers) {
  call task1{input: num=i}
  call task2{input: num=task1.output}
}
```

In this example, `task2` depends on `task1`.  Variable `i` has an implicit `index` attribute to make sure we can access the right output from `task1`.  Since both task1 and task2 run N times where N is the length of the array `integers`, any scalar outputs of these tasks is now an array.

### Conditionals

```txt
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

```txt
$wf_parameter_meta = 'parameter_meta' $ws* '{' ($ws* $wf_parameter_meta_kv $ws*)* '}'
$wf_parameter_meta_kv = $identifier $ws* '=' $ws* $meta_value
```

This purely optional section contains key/value pairs where the keys are names of parameters and the values are JSON like expressions that describe those parameters.

> *Additional requirement*: Any key in this section MUST correspond to a workflow input or output.

As an example:

```wdl
  parameter_meta {
    memory_mb: "Amount of memory to allocate to the JVM"
    param: "Some arbitrary parameter"
    sample_id: "The ID of the sample in format foo_bar_baz"
  }
```

### Metadata

```txt
$wf_meta = 'meta' $ws* '{' ($ws* $wf_meta_kv $ws*)* '}'
$wf_meta_kv = $identifier $ws* '=' $ws* $meta_value
```

This purely optional section contains key/value pairs for any additional meta data that should be stored with the workflow.  For example, perhaps author or contact email.

As an example:

```wdl
  meta {
    author: "Joe Somebody"
    email: "joe@company.org"
  }
```

### Outputs

Each `workflow` definition can specify an `output` section.  This section lists outputs as `Type name = expression`, just like task outputs.

Workflow outputs also follow the same syntax rules as task outputs. They are expressions which can reference all call outputs, workflow inputs, intermediate values and previous workflow outputs.
e.g:

```wdl
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

```wdl
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

* To present the same interface when calling subworkflows as when calling tasks.
* To make it easy for callers of subworkflows to find out exactly what outputs the call is creating.
* In case of nested subworkflows, to give the outputs at the top level a simple fixed name rather than a long qualified name like `a.b.c.d.out` (which is liable to change if the underlying implementation of `c` changes, for example).

## Struct Definition

A struct enables the user to create a new type that packages different types together.
This is also known as struct in some C-like languages, and tuple in others.
Once defined structs can be used just like any other normal type.
`Map`s and `Array`s are similar, but they are for packaging identical types together,
and in unlimited number.

Structs are declared separately from any other constructs, and cannot be declared within any `workflow` or `task` definition. They belong to the namespace of the WDL
file which they are written in and are therefore accessible globally within that WDL. Additionally, all structs must be evaluated prior to their use within a `task`,
`workflow` or another `struct`.

### Struct Declarations

Structs may be defined using the `struct` keyword and have a single section consisting of typed declarations.
Declarations can be any other type, and are defined
the same way as they are in any other section. The one caveat to this is that declarations within a struct do not allow an `=` and expression statement after
the `type` and name declaration. Once defined all structs are added to a global namespace accessible from any other construct within the WDL.

For example the following is a valid struct definition

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

Structs should be declared with Object literals, as the keys can be checked
for correctness before run time.
Assignment is also possible from `Maps`, other `Structs`.
As `Map` literals can contain arbitrary expressions for the keys,
their use for defining `Structs` is discouraged.
If the expression assigned to the `Struct` is not compatible with the
`Struct` fields, the workflow should error.

For example, if I have a struct like the following:

```wdl
struct Person {
    String name
    Int age
}
```

then usage of the struct in a workflow would look like the following:

```wdl
task myTask {
    input {
      Person a
    }
    command <<<
        echo "hello my name is ~{a.name} and I am ~{a.age} years old"
    >>>
    output {
      String name = a.name + "Potter"
      Int age = a.age * 2
    }
}

workflow myWorkflow {
    Person harry = object {name: "Harry", age: 11}
    call myTask {
        input:
            a = harry
    }
}
```

### Struct Member Access

In order to access members within a struct, use member access notation; ie `myStruct.name`. If the underlying member is a complex type which supports member access,
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
  input {
    Experiment myExperiment
  }
  File firstFile = myExperiment.experimentFiles[0]
  String experimentName = myExperiment.experimentData["name"]
}
```

**Example 2:**
If the struct itself is a member of an Array or another type, yo

```wdl
workflow workflow_a {
    input {
        Array[Experiment] myExperiments
    }

    File firstFileFromFirstExperiment = myExperiments[0].experimentFiles[0]
    File experimentNameFromFirstExperiment = myExperiments[0].experimentData["name"]
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

* Note: Alias can be used even when no conflicts are encountered to uniquely identify any struct.

# Namespaces

Import statements can be used to pull in tasks/workflows from other locations as well as to create namespaces.  In the simplest case, an import statement adds the tasks/workflows that are imported into the specified namespace.  For example:

tasks.wdl

```wdl
task x {
  command { python script.py }
}
task y {
  command { python script2.py }
}
```

workflow.wdl

```wdl
import "tasks.wdl" as pyTasks

workflow wf {
  call pyTasks.x
  call pyTasks.y
}
```

Tasks `x` and `y` are inside the namespace `pyTasks`, which is different from the `wf` namespace belonging to the primary workflow.  However, if no namespace is specified for tasks.wdl:

workflow.wdl

```wdl
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

* `?` means that the parameter is optional, potentially `None` at runtime. A user does not need to specify a value for the parameter in order to satisfy all the inputs to the workflow.
* `+` applies only to `Array` types and it represents a constraint that the `Array` value must contain one-or-more elements.

```wdl
task test {
  input {
    Array[File]  a
    Array[File]+ b
    Array[File]? c
    #File+ d <-- can't do this, + only applies to Arrays
    Array[File]+? e  # An optional array that, if defined, must contain at least one element
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

```sh
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

```sh
/bin/mycmd 1 2 3
/bin/mycmd x,y
/bin/mycmd /path/to/c.txt
```

It's invalid (a static validation error) to supply an expression of optional type `T?` for a non-optional input or variable of type `T`, as the latter cannot accept `None`. (The idiom `select_first([expr, default])` coerces `expr : T?` to `T` by substituting `default : T` when `expr` is undefined; if `default` is omitted, then the coercion fails at runtime.) This constraint propagates into compound types, so for example an `Array[T?]` expression doesn't satisfy an `Array[T]` input. It also applies to function arguments, with exceptions for string concatenation, described below, and the equality/inequality operators `==` and `!=`, which can compare two values of types differing only in their quantifiers, considering `None` equal to itself but no other value.

The nonempty array quantifier `Array[T]+` isn't statically validated in the same way, but rather as a runtime assertion: binding an empty array to an `Array[T]+` input or function argument is a runtime error. An array type can be both non-empty and optional, `Array[T]+?`, such that the value can be `None` or a non-empty array, but not the empty array.

## Interpolating and concatenating optional strings

Interpolations with `~{}` and `${}` accept optional string expressions and substitute the empty string for `None` at runtime.

Within interpolations, string concatenation with the `+` operator has special typing properties to facilitate formulation of command-line flags. When applied to two non-optional operands, the result is a non-optional `String`. However, if either operand has an optional type, then the concatenation has type `String?`, and the runtime result is `None` if either operand is `None`. To illustrate how this can be used, consider this task:

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

```sh
python script.py --val=foobar
```

Or

```sh
python script.py --val=
```

The latter case is very likely an error case, and this `--val=` part should be left off if a value for `val` is omitted.  To solve this problem, modify the expression inside the template tag as follows:

```sh
python script.py ${"--val=" + val}
```

The `+` operator cannot accept optional operands outside of interpolations.

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

Running this workflow (which needs no inputs), would yield a value of `[2,3,4,5,6]` for `wf.inc.incremented`.  While `task inc` itself returns an `Int`, when it is called inside a scatter block, that type becomes an `Array[Int]`.

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
  call sum {input: ints = inc.incremented}
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
  call sum {input: ints = inc2.incremented}
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

## Specifying Workflow Inputs

Once workflow inputs are computed (see previous section), the value for each of the fully-qualified names needs to be specified per invocation of the workflow. The format of workflow inputs is implementation specific.

### Cromwell-style Inputs

The "Cromwell-style" input format is widely supported by WDL implementations and recommended for portability purposes. In the Cromwell-style format, workflow inputs are specified as key/value pairs in JSON or YAML. The mapping to WDL values is codified in the [serialization of task inputs](#serialization-of-task-inputs) section.

In JSON, the inputs to the workflow in the previous section might be:

```json
{
  "wf.t1.s": "some_string",
  "wf.t2.s": "some_string",
  "wf.int_val": 3,
  "wf.my_ints": [5,6,7,8],
  "wf.ref_file": "/path/to/file.txt",
  "wf.some_struct": {
    "fieldA": "some_string",
    "fieldB": 42,
    "fieldC": "/path/to/file.txt"
  }
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
|         |`File`|May be removed in the future. Note that `Directory` to String is NOT a supported coercion.|
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

If when the file is read, the types cannot be converted into the type declared by
output_table, an error will be reported.

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

```sh
./script --file-list=/local/fs/tmp/array.txt
```

And `/local/fs/tmp/array.txt` would contain:

```txt
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

```sh
./script --tsv=/local/fs/tmp/array.tsv
```

And `/local/fs/tmp/array.tsv` would contain:

```tsv
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

```sh
./script --tsv=/local/fs/tmp/map.tsv
```

And `/local/fs/tmp/map.tsv` would contain:

```tsv
key1\tvalue1
key2\tvalue2
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

```sh
./script --tsv=/local/fs/tmp/map.json
```

And `/local/fs/tmp/map.json` would contain:

```json
{
  "key1": "value1",
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

* `Float size(File?, [String])`: Returns the size of the file, if specified, or 0.0 otherwise.
* `Float size(Array[File], [String])`: Returns the sum of sizes of the files in the array.
* `Float size(Array[File?], [String])`: Returns the sum of sizes of all specified files in the array.

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

Given a two dimensional array argument, the `transpose` function transposes the two dimensional array according to the standard matrix transpose rules. For example `transpose( [[0, 1, 2], [3, 4, 5]] )` will return the rotated two-dimensional array: `[[0, 3], [1, 4], [2, 5]]`.

## Array[Pair[X,Y]] zip(Array[X], Array[Y])

Return the dot product of the two arrays. If the arrays have different length
it is an error.

```wdl
Pair[Int, String] p = (0, "z")
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b", "c" ]
Array[String] zs = [ "d", "e" ]

Array[Pair[Int, String]] zipped = zip(xs, ys)     # i.e.  zipped = [ (1, "a"), (2, "b"), (3, "c") ]
```

## Array[Pair[X,Y]] cross(Array[X], Array[Y])

Return the cross product of the two arrays. Array[Y][1] appears before
Array[X][1] in the output.

```wdl
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b" ]

Array[Pair[Int, String]] crossed = cross(xs, ys) # i.e. crossed = [ (1, "a"), (1, "b"), (2, "a"), (2, "b") ]
```

## Array[Pair[X,Y]] as_pairs(Map[X,Y])

Given a Map, the `as_pairs` function returns an Array containing each element in the form of a Pair. The key will be the left element of the Pair and the value the right element. The order of the the Pairs in the resulting Array is the same as the order of the key/value pairs in the Map.

```wdl
Map[String, Int] x = {"a": 1, "b": 2, "c": 3}
Map[String,Pair[File,File]] y = {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}

Array[Pair[String,Int]] xpairs = as_pairs(x) # [("a", 1), ("b", 2), ("c", 3)]
Array[Pair[String,Pair[File,File]]] ypairs = as_pairs(y) # [("a", ("a.bam", "a.bai")), ("b", ("b.bam", "b.bai"))]
```

## Map[X,Y] as_map(Array[Pair[X,Y]])

Given an Array consisting of Pairs, the `as_map` function returns a Map in which the left elements of the Pairs are the keys and the right elements the values. The left element of the Pairs passed to `as_map` must be a primitive type. The order of the key/value pairs in the resulting Map is the same as the order of the Pairs in the Array.

In cases where multiple Pairs would produce the same key, the workflow will fail.

```wdl
Array[Pair[String,Int]] x = [("a", 1), ("b", 2), ("c", 3)]
Array[Pair[String,Pair[File,File]]] y = [("a", ("a.bam", "a.bai")), ("b", ("b.bam", "b.bai"))]

Map[String,Int] xmap = as_map(x) # {"a": 1, "b": 2, "c": 3}
Map[String,Pair[File,File]] ymap = as_map(y) # {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}
```

## Array[X] keys(Map[X,Y])

Given a Map, the `keys` function returns an Array consisting of the keys in the Map. The order of the keys in the resulting Array is the same as the order of the Pairs in the Map.

In cases where multiple Pairs would produce the same key, the workflow will fail.

```wdl
Map[String,Int] x = {("a", 1), ("b", 2), ("c", 3)}
Map[String,Pair[File,File]] y = {("a", ("a.bam", "a.bai")), ("b", ("b.bam", "b.bai"))}

Array[String] xmap = keys(x) # ["a", "b", "c"]
Array[String] ymap = keys(y) # ["a", "b"]
```

## Map[X,Array[Y]] collect_by_key(Array[Pair[X,Y]])

Given an Array consisting of Pairs, the `collect_by_key` function returns a Map in which the left elements of the Pairs are the keys and the right elements the values. The left element of the Pairs passed to `as_map` must be a primitive type. The values will be placed in an Array to allow for multiple Pairs to produce the same key. The order of the keys in the Map is the same as the order in the Array based on their first occurence. The order of the elements in the resulting Arrays is the same as their occurence in the given Array of Pairs.

```wdl
Array[Pair[String,Int]] x = [("a", 1), ("b", 2), ("a", 3)]
Array[Pair[String,Pair[File,File]]] y = [("a", ("a_1.bam", "a_1.bai")), ("b", ("b.bam", "b.bai")), ("a", ("a_2.bam", "a_2.bai"))]

Map[String,Array[Int]] xmap = as_map(x) # {"a": [1, 3], "b": [2]}
Map[String,Array[Pair[File,File]]] ymap = as_map(y) # {"a": [("a_1.bam", "a_1.bai"), ("a_2.bam", "a_2.bai")], "b": [("b.bam", "b.bai")]}
```

## Int length(Array[X])

Given an Array, the `length` function returns the number of elements in the Array as an Int.

```wdl
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b", "c" ]
Array[String] zs = [ ]

Int xlen = length(xs) # 3
Int ylen = length(ys) # 3
Int zlen = length(zs) # 0
```

## Array[X] flatten(Array[Array[X]])

Given an array of arrays, the `flatten` function concatenates all the
member arrays in the order to appearance to give the result. It does not
deduplicate the elements. Arrays nested more deeply than 2 must be
flattened twice (or more) to get down to an unnested `Array[X]`.
For example:

```wdl
Array[Array[Int]] ai2D = [[1, 2, 3], [1], [21, 22]]
Array[Int] ai = flatten(ai2D)   # [1, 2, 3, 1, 21, 22]

Array[Array[File]] af2D = [["/tmp/X.txt"], ["/tmp/Y.txt", "/tmp/Z.txt"], []]
Array[File] af = flatten(af2D)   # ["/tmp/X.txt", "/tmp/Y.txt", "/tmp/Z.txt"]

Array[Array[Pair[Float,String]]] aap2D = [[(0.1, "mouse")], [(3, "cat"), (15, "dog")]]

Array[Pair[Float,String]] ap = flatten(aap2D) # [(0.1, "mouse"), (3, "cat"), (15, "dog")]
```

The last example (`aap2D`) is useful because `Map[X, Y]` can be coerced to `Array[Pair[X, Y]]`.

## Array[String] prefix(String, Array[X])

Given a String and an Array[X] where X is a primitive type, the `prefix` function returns an array of strings comprised
of each element of the input array prefixed by the specified prefix string.  For example:

```wdl
Array[String] env = ["key1=value1", "key2=value2", "key3=value3"]
Array[String] env_param = prefix("-e ", env) # ["-e key1=value1", "-e key2=value2", "-e key3=value3"]

Array[Int] env2 = [1, 2, 3]
Array[String] env2_param = prefix("-f ", env2) # ["-f 1", "-f 2", "-f 3"]
```

## X select_first(Array[X?])

Given an array of optional values, `select_first` will select the first defined value and return it. Note that this is a runtime check and requires that at least one defined value will exist: if no defined value is found when select_first is evaluated, the workflow will fail.

```wdl
version 1.0
workflow SelectFirst {
  input {
    Int? maybe_five = 5
    Int? maybe_four_but_is_not = None
    Int? maybe_three = 3
  }
  Int five = select_first([maybe_five, maybe_four_but_is_not, maybe_three]) # This evaluates to 5
  Int five = select_first([maybe_four_but_is_not, maybe_five, maybe_three]) # This also evaluates to 5
}
```

## Array[X] select_all(Array[X?])

Given an array of optional values, `select_all` will select only those elements which are defined.

```wdl
version 1.0
workflow SelectFirst {
  input {
    Int? maybe_five = 5
    Int? maybe_four_but_is_not = None
    Int? maybe_three = 3
  }
  Array[Int] fivethree = select_all([maybe_five, maybe_four_but_is_not, maybe_three]) # This evaluates to [5, 3]
}
```

## Boolean defined(X?)

This function will return `false` if the argument is an unset optional value. It will return `true` in all other cases.

## String basename(String)

* This function returns the basename of a file path passed to it: `basename("/path/to/file.txt")` returns `"file.txt"`.
* Also supports an optional parameter, suffix to remove: `basename("/path/to/file.txt", ".txt")` returns `"file"`.

## Int floor(Float), Int ceil(Float) and Int round(Float)

* These functions convert a Float value into an Int by:
  * floor: Round **down** to the next lower integer
  * ceil: Round **up** to the next higher integer
  * round: Round to the nearest integer based on standard rounding rules

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
* Pair
* Struct

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

```sh
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

```sh
sh script.sh /jobs/564758/bams
```

Where `/jobs/564758/bams` would contain:

```txt
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

```sh
sh script.sh /jobs/564758/bams.json
```

Where `/jobs/564758/bams.json` would contain:

```json
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

```sh
sh script.sh /jobs/564757/sample_quality_scores.tsv
```

Where `/jobs/564757/sample_quality_scores.tsv` would contain:

```tsv
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

```sh
sh script.sh /jobs/564757/sample_quality_scores.json
```

Where `/jobs/564757/sample_quality_scores.json` would contain:

```json
{
  "sample1": 98,
  "sample2": 95,
  "sample3": 75
}
```

#### Struct serialization

A struct can be serialized by treating it like a `Map` with `String` keys
and differently typed values.

#### Struct serialization using write_json()

```wdl
struct Person {
    String name
    Int age
    Array[String] friends
}

task process_person {
  input {
    Person p
  }
  command <<<
    perl script.py ~{write_json(p)}
  >>>
}
```

If `p` is provided as:

```json
{
  "name", "John"
  "age", 5
  "friends": ["James", "Jim"]
}
```

Then, the resulting command line might look like:

```sh
perl script.pl /jobs/564759/sample.json
```

Where `/jobs/564759/sample.json` would contain:

```json
{
  "name": "John",
  "age": 5,
  "friends": ["James", "Jim"]
}
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

Both files `int_file` and `str_file` should contain one line with the value on that line.  This value is then validated against the type of the variable.  If `int_file` contains a line with the text "foobar", the workflow must fail this task with an error.

### Compound Types

Tasks can also output to a file or stdout/stderr an `Array`, `Map`, or `Struct` data structure in a two major formats:

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
