# Workflow Description Language (WDL)

This is version 1.1 of the Workflow Description Language (WDL) specification. It introduces a number of new features (denoted by the ✨ symbol) and clarifications to the [1.0](../1.0/SPEC.md) version of the specification. It also deprecates several aspects of the 1.0 specification that will be removed in the [next major WDL version](../development/SPEC.md) (denoted by the 🗑 symbol).

## Table of Contents

- [Workflow Description Language (WDL)](#workflow-description-language-wdl)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
    - [An Example WDL Workflow](#an-example-wdl-workflow)
    - [Executing a WDL Workflow](#executing-a-wdl-workflow)
    - [Advanced WDL Features](#advanced-wdl-features)
- [WDL Language Specification](#wdl-language-specification)
  - [Global Grammar Rules](#global-grammar-rules)
    - [Whitespace](#whitespace)
    - [Literals](#literals)
      - [Strings](#strings)
    - [Comments](#comments)
    - [Reserved Keywords](#reserved-keywords)
    - [Types](#types)
      - [Primitive Types](#primitive-types)
      - [Optional Types and None](#optional-types-and-none)
      - [Compound Types](#compound-types)
        - [Array[X]](#arrayx)
        - [Pair[X, Y]](#pairx-y)
        - [Map[P, Y]](#mapp-y)
        - [Custom Types (Structs)](#custom-types-structs)
        - [🗑 Object](#-object)
      - [Type Conversion](#type-conversion)
        - [Primitive Conversion to String](#primitive-conversion-to-string)
        - [Type Coercion](#type-coercion)
          - [Coercion of Optional Types](#coercion-of-optional-types)
          - [Struct/Object coercion from Map](#structobject-coercion-from-map)
    - [Declarations](#declarations)
    - [Expressions](#expressions)
      - [Built-in Operators](#built-in-operators)
        - [Unary Operators](#unary-operators)
        - [Binary Operators on Primitive Types](#binary-operators-on-primitive-types)
        - [Equality of Compound Types](#equality-of-compound-types)
        - [Equality and Inequality Comparison of Optional Types](#equality-and-inequality-comparison-of-optional-types)
      - [Operator Precedence Table](#operator-precedence-table)
      - [Member Access](#member-access)
      - [Ternary operator (if-then-else)](#ternary-operator-if-then-else)
      - [Function Calls](#function-calls)
      - [Expression Placeholders and String Interpolation](#expression-placeholders-and-string-interpolation)
        - [Expression Placeholder Coercion](#expression-placeholder-coercion)
        - [Concatenation of Optional Values](#concatenation-of-optional-values)
      - [🗑 Expression Placeholder Options](#-expression-placeholder-options)
        - [`sep`](#sep)
        - [`true` and `false`](#true-and-false)
        - [`default`](#default)
  - [WDL Documents](#wdl-documents)
  - [Versioning](#versioning)
  - [Import Statements](#import-statements)
  - [Task Definition](#task-definition)
    - [Task Inputs](#task-inputs)
      - [Task Input Localization](#task-input-localization)
        - [Special Case: Versioning Filesystem](#special-case-versioning-filesystem)
      - [Input Type Constraints](#input-type-constraints)
        - [Optional inputs with defaults](#optional-inputs-with-defaults)
    - [Private Declarations](#private-declarations)
    - [Command Section](#command-section)
      - [Expression Placeholders](#expression-placeholders)
      - [Stripping Leading Whitespace](#stripping-leading-whitespace)
    - [Task Outputs](#task-outputs)
      - [Files and Optional Outputs](#files-and-optional-outputs)
    - [Evaluation of Task Declarations](#evaluation-of-task-declarations)
    - [Runtime Section](#runtime-section)
      - [Units of Storage](#units-of-storage)
      - [Mandatory `runtime` attributes](#mandatory-runtime-attributes)
        - [`container`](#container)
        - [`cpu`](#cpu)
        - [`memory`](#memory)
        - [`gpu`](#gpu)
        - [`disks`](#disks)
        - [`maxRetries`](#maxretries)
        - [`returnCodes`](#returncodes)
      - [Reserved `runtime` hints](#reserved-runtime-hints)
      - [Conventions and Best Practices](#conventions-and-best-practices)
    - [Metadata Sections](#metadata-sections)
      - [Task Metadata Section](#task-metadata-section)
      - [Parameter Metadata Section](#parameter-metadata-section)
    - [Task Examples](#task-examples)
      - [Example 1: Simplest Task](#example-1-simplest-task)
      - [Example 2: Inputs/Outputs](#example-2-inputsoutputs)
      - [Example 3: Runtime/Metadata](#example-3-runtimemetadata)
      - [Example 4: BWA MEM](#example-4-bwa-mem)
      - [Example 5: Word Count](#example-5-word-count)
      - [Example 6: tmap](#example-6-tmap)
  - [Workflow Definition](#workflow-definition)
    - [Workflow Elements](#workflow-elements)
    - [Workflow Inputs](#workflow-inputs)
    - [Workflow Outputs](#workflow-outputs)
    - [Evaluation of Workflow Elements](#evaluation-of-workflow-elements)
    - [Fully Qualified Names & Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers)
    - [Call Statement](#call-statement)
      - [Computing Call Inputs](#computing-call-inputs)
    - [Scatter](#scatter)
    - [Conditional (`if` block)](#conditional-if-block)
  - [Struct Definition](#struct-definition)
    - [Struct Literals](#struct-literals)
    - [Struct Namespacing](#struct-namespacing)
    - [Struct Usage](#struct-usage)
- [Standard Library](#standard-library)
  - [Int floor(Float), Int ceil(Float) and Int round(Float)](#int-floorfloat-int-ceilfloat-and-int-roundfloat)
  - [✨ Int min(Int, Int), Float min(Float, Float), Float min(Int, Float), Float min(Float, Int)](#-int-minint-int-float-minfloat-float-float-minint-float-float-minfloat-int)
  - [✨ Int max(Int, Int), Float max(Float, Float), Float max(Int, Float), Float max(Float, Int)](#-int-maxint-int-float-maxfloat-float-float-maxint-float-float-maxfloat-int)
  - [String sub(String, String, String)](#string-substring-string-string)
  - [File stdout()](#file-stdout)
  - [File stderr()](#file-stderr)
  - [Array[File] glob(String)](#arrayfile-globstring)
    - [Non-standard Bash](#non-standard-bash)
  - [String basename(String|File, [String])](#string-basenamestringfile-string)
  - [Array[String] read_lines(String|File)](#arraystring-read_linesstringfile)
  - [Array[Array[String]] read_tsv(String|File)](#arrayarraystring-read_tsvstringfile)
  - [Map[String, String] read_map(String|File)](#mapstring-string-read_mapstringfile)
  - [🗑 Object read_object(String|File)](#-object-read_objectstringfile)
  - [🗑 Array[Object] read_objects(String|File)](#-arrayobject-read_objectsstringfile)
  - [R read_json(String|File)](#r-read_jsonstringfile)
  - [String read_string(String|File)](#string-read_stringstringfile)
  - [Int read_int(String|File)](#int-read_intstringfile)
  - [Float read_float(String|File)](#float-read_floatstringfile)
  - [Boolean read_boolean(String|File)](#boolean-read_booleanstringfile)
  - [File write_lines(Array[String])](#file-write_linesarraystring)
  - [File write_tsv(Array[Array[String]])](#file-write_tsvarrayarraystring)
  - [File write_map(Map[String, String])](#file-write_mapmapstring-string)
  - [🗑 File write_object(Object)](#-file-write_objectobject)
  - [🗑 File write_objects(Array[Object])](#-file-write_objectsarrayobject)
  - [File write_json(X)](#file-write_jsonx)
  - [Float size(File?|Array[File?], [String])](#float-sizefilearrayfile-string)
  - [Int length(Array[X])](#int-lengtharrayx)
  - [Array[Int] range(Int)](#arrayint-rangeint)
  - [Array[Array[X]] transpose(Array[Array[X]])](#arrayarrayx-transposearrayarrayx)
  - [Array[Pair[X,Y]] zip(Array[X], Array[Y])](#arraypairxy-ziparrayx-arrayy)
  - [✨ Pair[Array[X], Array[Y]] unzip(Array[Pair[X, Y]])](#-pairarrayx-arrayy-unziparraypairx-y)
  - [Array[Pair[X,Y]] cross(Array[X], Array[Y])](#arraypairxy-crossarrayx-arrayy)
  - [Array[X] flatten(Array[Array[X]])](#arrayx-flattenarrayarrayx)
  - [Array[String] prefix(String, Array[P])](#arraystring-prefixstring-arrayp)
  - [✨ Array[String] suffix(String, Array[P])](#-arraystring-suffixstring-arrayp)
  - [✨ Array[String] quote(Array[P])](#-arraystring-quotearrayp)
  - [✨ Array[String] squote(Array[P])](#-arraystring-squotearrayp)
  - [✨ String sep(String, Array[String])](#-string-sepstring-arraystring)
  - [✨ Array[Pair[P, Y]] as_pairs(Map[P, Y])](#-arraypairp-y-as_pairsmapp-y)
  - [✨ Map[P, Y] as_map(Array[Pair[P, Y]])](#-mapp-y-as_maparraypairp-y)
  - [✨ Array[P] keys(Map[P, Y])](#-arrayp-keysmapp-y)
  - [✨ Map[P, Array[Y]] collect_by_key(Array[Pair[P, Y]])](#-mapp-arrayy-collect_by_keyarraypairp-y)
  - [Boolean defined(X?)](#boolean-definedx)
  - [X select_first(Array[X?]+)](#x-select_firstarrayx)
  - [Array[X] select_all(Array[X?])](#arrayx-select_allarrayx)
- [Input and Output Formats](#input-and-output-formats)
  - [JSON Input Format](#json-input-format)
    - [Optional Inputs](#optional-inputs)
  - [JSON Output Format](#json-output-format)
  - [Specifying / Overriding Runtime Attributes](#specifying--overriding-runtime-attributes)
  - [JSON Serialization of WDL Types](#json-serialization-of-wdl-types)
    - [Primitive Types](#primitive-types-1)
    - [Array](#array)
    - [Pair](#pair)
    - [Map](#map)
    - [Struct and Object](#struct-and-object)
- [Appendix A: WDL Value Serialization and Deserialization](#appendix-a-wdl-value-serialization-and-deserialization)
  - [Primitive Values](#primitive-values)
  - [Compound Values](#compound-values)
    - [Array](#array-1)
      - [Array serialization by expansion](#array-serialization-by-expansion)
      - [Array serialization using write_lines()](#array-serialization-using-write_lines)
      - [Array serialization using write_json()](#array-serialization-using-write_json)
      - [Array deserialization using read_lines()](#array-deserialization-using-read_lines)
      - [Array deserialization using read_json()](#array-deserialization-using-read_json)
    - [Struct and Object](#struct-and-object-1)
      - [Struct serialization using write_json()](#struct-serialization-using-write_json)
    - [Map](#map-1)
      - [Map serialization using write_map()](#map-serialization-using-write_map)
      - [Map serialization using write_json()](#map-serialization-using-write_json)
      - [Map deserialization using read_map()](#map-deserialization-using-read_map)
      - [Map deserialization using read_json()](#map-deserialization-using-read_json)
    - [Pair](#pair-1)
- [Appendix B: WDL Namespaces and Scopes](#appendix-b-wdl-namespaces-and-scopes)
  - [Namespaces](#namespaces)
  - [Scopes](#scopes)
    - [Global Scope](#global-scope)
    - [Task Scope](#task-scope)
    - [Workflow Scope](#workflow-scope)
    - [Cyclic References](#cyclic-references)
    - [Namespaces without Scope](#namespaces-without-scope)
  - [Evaluation Order](#evaluation-order)

## Introduction

Workflow Description Language (WDL) is an open, standardized, *human readable and writable* language for expressing tasks and workflows. WDL is designed to be a general-purpose workflow language, but it is most widely used in the field of bioinformatics. There is a large community of WDL users who share their workflows and tasks on sites such as [Dockstore](https://dockstore.org/search?descriptorType=WDL&searchMode=files).

This document provides a detailed technical specification for WDL. Users who are new to WDL may appreciate a more gentle introduction, such as the [learn-wdl](https://github.com/openwdl/learn-wdl) repository.

Here is provided a short example of WDL, after which are several sections that provide the necessary details both for WDL users and for implementers of WDL execution engines:

* [Language Specification](#wdl-language-specification): a description of the WDL grammar and all the parts of the WDL document.
* [Standard Library](#standard-library): a catalog of the functions available to be called from within a WDL document.
* [Input and Output Formats](#input-and-output-formats): a description of the standard input and output formats that must be supported by all WDL implementations.
* [Appendices](#appendix-a-wdl-value-serialization-and-deserialization): Sections with more detailed information about various parts of the specification.

### An Example WDL Workflow

Below is the code for the "Hello World" workflow in WDL. This is just meant to give a flavor of WDL syntax and capabilities - all WDL elements are described in detail in the [Language Specification](#wdl-language-specification).

```wdl
task hello {
  input {
    File infile
    String pattern
  }

  command <<<
    egrep '~{pattern}' '~{infile}'
  >>>

  runtime {
    container: "my_image:latest"
  }

  output {
    Array[String] matches = read_lines(stdout())
  }
}

workflow wf {
  input {
    File infile
    String pattern
  }

  call hello {
    input: infile, pattern
  }

  output {
    Array[String] matches = hello.matches
  }
}
```

This WDL document describes a `task`, called `hello`, and a `workflow`, called `wf`.

* A `task` encapsulates a Bash script and a UNIX environment and presents them as a reusable function.
* A `workflow` encapsulates a (directed, acyclic) graph of task calls that transforms input data to the desired outputs.

Both workflows and tasks can accept input parameters and produce outputs. For example, `workflow wf` has two input parameters, `File infile` and `String pattern`, and one output parameter, `Array[String] matches`. This simple workflow calls `task hello`, passing through the workflow inputs to the task inputs, and using the results of `call hello` as the workflow output.

### Executing a WDL Workflow

To execute this workflow, a WDL execution engine must be used (sometimes called the "WDL runtime" or "WDL implementation"). Some popular WDL execution engines are listed in the [README](https://github.com/openwdl/wdl#execution-engines).

Along with the WDL file, the user must provide the execution engine with values for the two input parameters. While implementations may provide their own mechanisms for launching workflows, all implementations minimally accept [inputs as JSON format](#json-input-format), which requires that the input arguments be fully qualified according to the namespacing rules described in the [Fully Qualified Names & Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers) section. For example:

|Variable     |Value    |
|-------------|---------|
|wf.pattern   |^[a-z]+$ |
|wf.infile    |/file.txt|

Or, in JSON format:

```json
{
  "wf.pattern": "^[a-z]+$",
  "wf.infile": "/file.txt"
}
```

Running `workflow wf` with these inputs would yield the following command line from the call to `task hello`:

```sh
egrep '^[a-z]+$' '/file.txt'
```

And would result in (JSON) output that looks like:

```json
{
  "wf.matches": [
    "hello",
    "world"
  ]
}
```

### Advanced WDL Features

WDL also provides features for implementing more complex workflows. For example, `task hello` introduced in the previous example can be called in parallel across many different input files using the well-known [scatter-gather](https://en.wikipedia.org/wiki/Vectored_I/O#:~:text=In%20computing%2C%20vectored%20I%2FO,in%20a%20vector%20of%20buffers) pattern:

```wdl
workflow wf_parallel {
  input {
    Array[File] files
    String pattern
  }
  
  scatter (path in files) {
    call hello {
      input: 
        infile = path,
        pattern = pattern
    }
  }

  output {
    # WDL implicitly implements the 'gather' step, so
    # the output of a scatter is always an array with
    # elements in the same order as the input array
    Array[Array[String]] all_matches = hello.matches
  }
}
```

The inputs to this workflow might look like:

```json
{
  "wf_parallel.pattern": "^[a-z]+$",
  "wf_parallel.infile": ["/file1.txt", "/file2.txt"]
}
```

# WDL Language Specification

## Global Grammar Rules

WDL files are encoded in UTF-8, with no byte order mark (BOM).

### Whitespace

```txt
$ws = (0x20 | 0x09 | 0x0D | 0x0A)+
```

Whitespace may be used anywhere in a WDL document. Whitespace has no meaning in WDL, and is effectively ignored.

### Literals

```txt
$identifier = [a-zA-Z][a-zA-Z0-9_]*
$boolean = 'true' | 'false'
$integer = [1-9][0-9]*|0[xX][0-9a-fA-F]+|0[0-7]*
$float = (([0-9]+)?\.([0-9]+)|[0-9]+\.|[0-9]+)([eE][-+]?[0-9]+)?
$string = "([^\\\"\n]|\\[\\"\'nrbtfav\?]|\\[0-7]{1,3}|\\x[0-9a-fA-F]+|\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*"
$string = '([^\\\'\n]|\\[\\"\'nrbtfav\?]|\\[0-7]{1,3}|\\x[0-9a-fA-F]+|\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*'
```

Tasks and workflow inputs may be passed in from an external source, or they may be specified in the WDL document itself using literal values. Input, output, and other declaration values may also be constructed at runtime using [expressions](#expressions) that consist of literals, identifiers (references to [declarations](#declarations) or [call](#call-statement) outputs), built-in [operators](#operator-precedence-table), and [standard library functions](#standard-library).

#### Strings

A string literal may contain any unicode characters between single or double-quotes, with the exception of a few special characters that must be escaped:

| Escape Sequence | Meaning | \x Equivalent | Context |
|----|---|------|--|
|`\\`|`\`|`\x5C`||
|`\n`|newline|`\x0A`||
|`\t`|tab|`\x09`||
|`\'`|single quote|`\x22`|within a single-quoted string|
|`\"`|double quote|`\x27`|within a double-quoted string|

Strings can also contain the following types of escape sequences:

* An octal escape code starts with `\`, followed by 3 digits of value 0 through 7 inclusive.
* A hexadecimal escape code starts with `\x`, followed by 2 hexadecimal digits `0-9a-fA-F`. 
* A unicode code point starts with `\u` followed by 4 hexadecimal characters or `\U` followed by 8 hexadecimal characters `0-9a-fA-F`.

### Comments

Comments can be used to provide helpful information such as workflow usage, requirements, copyright, etc. A comment is prepended by `#` and can be placed at the start of a line or at the end of any line of WDL code. Any text following the `#` will be completely ignored by the execution engine, with one exception: within the `command` section, *ALL* text will be included in the evaluated script - even lines prepended by `#`.

There is no special syntax for multi-line comments - simply use a `#` at the start of each line.

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
    
  runtime {
    container: "my_image:latest"
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

### Reserved Keywords

The following language keywords are reserved and cannot be used to name declarations, calls, tasks, workflows, import namespaces, or struct types & aliases.

```
Array Boolean Float Int Map None Object Pair String

alias as call command else false if in import input 
left meta object output parameter_meta right runtime 
scatter struct task then true workflow
```

The following keywords should also be considered as reserved - they are not used in the current version of the specification, but they will be used in a future version:

* `Directory`
* `hints`

### Types

A [declaration](#declarations) is a name that the user reserves in a given [scope](#appendix-b-wdl-namespaces-and-scopes) to hold a value of a certain type. In WDL *all* declarations (including inputs and outputs) must be typed. This means that the information about the type of data that may be held by each declarations must be specified explicitly.

In WDL *all* types represent immutable values. For example, a `File` represent a logical "snapshot" of the file at the time when the value was created. It's impossible for a task to change an upstream value that has been provided as an input - even if it modifies its local copy, the original value is unaffected.

#### Primitive Types

The following primitive types exist in WDL:

* A `Boolean` represents a value of `true` or `false`.
* An `Int` represents a signed integer in the range \[-2^63, 2^63).
* A `Float` represents a finite 64-bit IEEE-754 floating point number.
* A `String` represents a unicode character string following the format described [above](#strings).
* A `File` represents a file (or file-like object).
  * A `File` declaration can have a string value indicating a relative or absolute path on the local file system.
  * Within a WDL file, literal values for files may only be local (relative or absolute) paths.
  * An execution engine may support other ways to specify [`File` inputs (e.g. as URIs)](#input-and-output-formats), but prior to task execution it must [localize inputs](#task-input-localization) so that the runtime value of a `File` variable is a local path.

Examples:

```wdl
Boolean b = true 
Int i = 0
Float f = 27.3
String s = "hello, world"
File f = "path/to/file"
```

#### Optional Types and None

A type may have a `?` postfix quantifier, which means that its value is allowed to be undefined without causing an error. It can only be used in calls or functions that accept optional values.

WDL has a special value `None` whose meaning is "an undefined value". The type of the `None` value is `Any`, meaning `None` can be assigned to an optional declaration of any type. The `None` value is the only value that can be of type `Any`.

An optional declaration has a default initialization of `None`, which indicates that it is undefined. An optional declaration may be initialized to any literal or expression of the correct type, including the special `None` value.

```wdl
Int certainly_five = 5      # an non-optional declaration
Int? maybe_five_and_is = 5  # a defined optional declaration

# the following are equivalent undefined optional declarations
String? maybe_five_but_is_not
String? maybe_five_but_is_not = None

Boolean test_defined = defined(maybe_five_but_is_not) # Evaluates to false
Boolean test_defined2 = defined(maybe_five_and_is)    # Evaluates to true
Boolean test_is_none = maybe_five_but_is_not == None  # Evaluates to true
Boolean test_not_none = maybe_five_but_is_not != None # Evaluates to false
```

For more details, see the sections on [Input Type Constraints](#input-type-constraints) and [Optional Inputs with Defaults](#optional-inputs-with-defaults).

#### Compound Types

A compound type is one that contains nested types, i.e. it is *parameterized* by other types. The following compound types can be constructed. In the examples below `P` represents any of the primitive types above, and `X` and `Y` represent any valid type (including nested compound types).

##### Array[X]

An `Array` represents an ordered list of elements that are all of the same type. An array is insertion ordered, meaning the order in which elements are added to the `Array` is preserved.

An array value can be initialized with an array literal - a comma-separated list of values in brackets (`[]`). A specific zero-based index of an `Array` can be accessed by placing the index in brackets after the declaration name. Accessing a non-existent index of an `Array` results in an error.

```wdl
Array[File] files = ["/path/to/file1", "/path/to/file2"]
File f = files[0]  # evaluates to "/path/to/file1"

Array[Int] empty = []
# this causes an error - trying to access a non-existent array element
Int i = empty[0]
```

An `Array` may have an empty value (i.e. an array of length zero), unless it is declared using `+`, the non-empty postfix quantifier, which represents a constraint that the `Array` value must contain one-or-more elements. For example, the following task operates on an `Array` of `File`s and it requires at least one file to function:

```wdl
task align {
  input {
    Array[File]+ fastqs
  }
  String sample_type = if length(fastqs) == 1 then "--single-end" else "--paired-end"
  command <<<
  ./align ~{sample_type} ~{sep(" ", fastqs)} > output.bam
  >>>
  output {
    File bam = "output.bam"
  }
}
```

Recall that a type may have an optional postfix quantifier (`?`), which means that its value may be undefined. The `+` and `?` postfix quantifiers can be combined to declare an `Array` that is either undefined or non-empty, i.e. it can have any value *except* the empty array.

Attempting to assign an empty array literal to a non-empty `Array` declaration results in an error. Otherwise, the non-empty assertion is only checked at runtime: binding an empty array to an `Array[T]+` input or function argument is a runtime error. 

```wdl
# array that must contain at least one Float
Array[Float]+ nonempty = [0.0]
# array that must contain at least one Int?
# (which may have an undefined value)
Array[Int?]+ nonempty2 = [None, 1]
# array that can be undefined or must contain
# at least one Int
Array[Int]+? nonempty4
Array[Int]+? nonempty5 = [0.0]

# these both cause an error - can't assign empty array value to non-empty Array type
Array[Boolean]+ nonempty3 = []
Array[Int]+? nonempty6 = [] 
```

For more details see the section on [Input Type Constraints](#input-type-constraints).

##### Pair[X, Y]

A `Pair` represents two associated values, which may be of different types. In other programming languages, a `Pair` might be called a "two-tuple".

A `Pair` can be initialized with a pair literal - a comma-separated pair of values in parentheses (`()`). The components of a `Pair` value are accessed using its `left` and `right` accessors.

```wdl
Pair[Int, Array[String]] data = (5, ["hello", "goodbye"])
Int five = p.left  # evaluates to 5
String hello = data.right[0]  # evaluates to "hello"
```

##### Map[P, Y]

A `Map` represents an associative array of key-value pairs. All of the keys must be of the same (primitive) type, and all of the values must be of the same type, but keys and values can be different types.

A `Map` can be initialized with a map literal - a comma-separated list of key-value pairs in braces (`{}`), where key-value pairs are delimited by `:`. The value of a specific key can be accessed by placing the key in brackets after the declaration name. Accessing a non-existent key of a `Map` results in an error.

```wdl
Map[Int, Int] int_to_int = {1: 10, 2: 11}
Map[String, Int] string_to_int = { "a": 1, "b": 2 }
Map[File, Array[Int]] file_to_ints = {
  "/path/to/file1": [0, 1, 2],
  "/path/to/file2": [9, 8, 7]
}
Int b = string_to_int["b"]  # evaluates to 2
Int c = string_to_int["c"]  # error - "c" is not a key in the map
```

A `Map` is insertion ordered, meaning the order in which elements are added to the `Map` is preserved, for example when [✨ converting a `Map` to an array of `Pair`s](#-arraypairp-y-as_pairsmapp-y).

```wdl
# declaration using a map literal
Map[Int, String] int_to_string = { 2: "hello", 1: "goodbye" }
# evaluates to [(2, "hello"), (1, "goodbye")]
Array[Pair[Int, String]] pairs = as_pairs(int_to_string)
```

##### Custom Types (Structs)

WDL provides the ability to define custom compound types called [structs](#struct-definition). `Struct` types are defined directly in the WDL document and are usable like any other type. A `struct` definition contains any number of declarations of any types, including other `Struct`s.

A struct is defined using the `struct` keyword, followed by a unique name, followed by member declarations within braces. A declaration with a custom type can be initialized with a struct literal, which begins with the `Struct` type name followed by a comma-separated list of key-value pairs in braces (`{}`), where name-value pairs are delimited by `:`. The member names in a struct literal are not quoted.

```wdl
# a struct is a user-defined type; it can contain members of any types
struct SampleBamAndIndex {
  String sample_name
  File bam
  File bam_index
}

SampleBamAndIndex b_and_i = SampleBamAndIndex {
  sample_name: "NA12878",
  bam: "NA12878.bam",
  bam_index: "NA12878.bam.bai" 
}
```

The value of a specific member of a `Struct` value can be accessed by placing a `.` followed by the member name after the identifier.

```wdl
File bam = b_and_i.bam
```

##### 🗑 Object

An `Object` is an unordered associative array of name-value pairs, where values may be of any type and are not specified explicitly.

An `Object` can be initialized using syntax similar to a struct literal, except that the `object` keyword is used in place of the `Struct` name. The value of a specific member of an `Object` value can be accessed by placing a `.` followed by the member name after the identifier.

```wdl
Object f = object {
  a: 10,
  b: "hello"
}
Int i = f.a
```

Due to the lack of explicitness in the typing of `Object` being at odds with the goal of being able to know the type information of all WDL declarations, **the `Object` type, the `object` literal syntax, and all of the [standard library functions](#-object-read_objectstringfile) with `Object` parameters or return values have been deprecated and will be removed in the next major version of the WDL specification**. All uses of `Object` can be replaced with [structs](#struct-definition).

#### Type Conversion

WDL has some limited facilities for converting a value of one type to another type. Some of these are explicitly provided by [standard library](#standard-library) functions, while others are [implicit](#type-coercion). When converting between types, it is best to be explicit whenever possible, even if an implicit conversion is allowed.

The execution engine is also responsible for converting (or "serializing") input values when constructing commands, as well as "deserializing" command outputs. For more information, see the [Command Section](#command-section) and the more extensive Appendix on [WDL Value Serialization and Deserialization](#appendix-a-wdl-value-serialization-and-deserialization).

##### Primitive Conversion to String 

Primitive types can always be converted to `String` using [string interpolation](#expression-placeholders-and-string-interpolation). See [Expression Placeholder Coercion](#expression-placeholder-coercion) for details.

```wdl
Int i = 5
String istring = "~{i}"
```

##### Type Coercion

There are some pairs of WDL types for which there is an obvious, unambiguous conversion from one to the other. In these cases, WDL provides an automatic conversion (called "coercion") from one type to the other, such that a value of one type typically can be used anywhere the other type is expected.

For example, file paths are always represented as strings, making the conversion from `String` to `File` obvious and unambiguous.

```wdl
String path = "/path/to/file"
# valid - String coerces unambiguously to File
File f = path
```

The table below lists all globally valid coercions. The "target" type is the type being coerced to (this is often called the "left-hand side" or "LHS" of the coercion) and the "source" type is the type being coerced from (the "right-hand side" or "RHS").

|Target Type |Source Type     |Notes/Constraints |
|------------|----------------|------------------|
|`File`|`String`||
|`Float`|`Int`|May cause overflow error|
|`Y?`|`X`|`X` must be coercible to `Y`|
|`Array[Y]`|`Array[X]`|`X` must be coercible to `Y`|
|`Map[X,Z]`|`Map[W,Y]`|`W` must be coercible to `X` and `Y` must be coercible to `Z`|
|`Pair[X,Z]`|`Pair[W,Y]`|`W` must be coercible to `X` and `Y` must be coercible to `Z`|
|`Struct`    |`Map[String,Y]`|`Map` keys must match `Struct` member names, and all `Struct` members types must be coercible from `Y`|
|`Map[String,Y]`|`Struct`|All `Struct` members must be coercible to `Y`|
|`Object`|`Map[String,Y]`|🗑|
|`Map[String,Y]`|`Object`|🗑 All object values must be coercible to `Y`|
|`Object`|`Struct`|🗑|
|`Struct`|`Object`|🗑 `Object` keys must match `Struct` member names, and `Object` values must be coercible to `Struct` member types|

###### Coercion of Optional Types

A non-optional type `T` can always be coerced to an optional type `T?`, but the reverse is not true - coercion from `T?` to `T` is not allowed because the latter cannot accept `None`.

This constraint propagates into compound types. For example, an `Array[T?]` can contain both optional and non-optional elements. This facilitates the common idiom [`select_first([expr, default])`](#x-select_firstarrayx), where `expr` is of type `T?` and `default` is of type `T`, for converting an optional type to a non-optional type. However, an `Array[T?]` could not be passed to the [`sep`](#-string-sepstring-arraystring) function, which requires an `Array[T]`.

There are two exceptions where coercion from `T?` to `T` is allowed:
* [String concatenation in expression placeholders](#concatenation-of-optional-values)
* [Equality and inequality comparisons](#equality-and-inequality-comparison-of-optional-types)

###### Struct/Object coercion from Map

`Struct`s and `Object`s can be coerced from map literals, but beware the following behavioral difference:

```wdl
String a = "beware"
String b = "key"
String c = "lookup"

struct Words {
  Int a
  Int b
  Int c
}

# What are the keys to this Struct?
Words literal_syntax = Words {
  a: 10,
  b: 11,
  c: 12
}

# What are the keys to this Struct?
Words map_coercion = {
  a: 10,
  b: 11,
  c: 12
}
```

- If a `Struct` (or `Object`) declaration is initialized using the struct-literal (or object-literal) syntax `Words literal_syntax = Words { a: ...` then the keys will be `"a"`, `"b"` and `"c"`.
- If a `Struct` (or `Object`) declaration is initialized using the map-literal syntax `Words map_coercion = { a: ...` then the keys are expressions, and thus `a` will be a variable reference to the previously defined `String a = "beware"`.

### Declarations

```txt
$declaration = $type $identifier ('=' $expression)?
```

A declaration reserves a name that can be referenced anywhere in the [scope](#appendix-b-wdl-namespaces-and-scopes) where it is declared. A declaration has a type, a name, and an optional initialization. Each declaration must be unique within its scope, and may not collide with a [reserved WDL keyword](#reserved-keywords) (e.g. `workflow`, or `input`).

Some examples of declarations:

```wdl
File x
String y = "abc"
Int i = 1 + 2
Float pi = 3 + .14
Map[String, String] m
```

A [task](#task-definition) or [workflow](#workflow-definition) may declare input parameters within its `input` section and output parameters within its `output` section. If a non-optional input declaration does not have an initialization, it is considered a "required" parameter, and its value must be provided by the user before the workflow or task may be run. Declarations may also appear in the body of a task or workflow. All non-input declarations must be initialized.

```wdl
task mytask {
  input {
    String s  # required input declaration
    Int? i    # optional input declaration
    Float f   # input delcaration with an initialization
  }

  Boolean b = true  # declaration in the task body

  # This is an error! f is not an input parameter and thus
  # must be initialized.
  File f

  ...

  output {
    Array[String] strarr = ["a", "b"] # output declaration
    File? optfile = "/path/to/file"   # optional output declaration
  } 
}
```

A declaration may be initialized with a literal value or an [expression](#expressions), which includes the ability to refer to elements that are outputs of tasks. For example:

```wdl
task test {
  input {
    String var
  }
  command <<<
    ./script ~{var}
  >>>
  output {
    String value = read_string(stdout())
  }
  runtime {
    container: "my_image:latest"
  }
}

task test2 {
  input {
    Array[String] array
  }
  command <<<
    ./script ~{write_lines(array)}
  >>>
  output {
    Int value = read_int(stdout())
  }
  runtime {
    container: "my_image:latest"
  }
}

workflow wf {
  call test as x {input: var="x"}
  call test as y {input: var="y"}
  Array[String] strs = [x.value, y.value]
  call test2 as z {input: array=strs}
}
```

In this example, `strs` would not be defined until both `call test as x` and `call test as y` have successfully completed. Before that's the case, `strs` is undefined. If any of the two tasks fail, then evaluation of `strs` should return an error to indicate that the `call test2 as z` operation should be skipped.

It must be possible to organize all of the statements within a scope into a directed acyclic graph (DAG); i.e. circular references between declarations are not allowed. The following example would result in an error due to the presence of a circular reference:

```wdl
task bad {
  Int i = j + 1
  Int j = i - 2
}
```

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
$expression = $expression '<=' $expression
$expression = $expression '>' $expression
$expression = $expression '>=' $expression
$expression = $expression '==' $expression
$expression = $expression '!=' $expression
$expression = $expression '&&' $expression
$expression = $expression '||' $expression
$expression = '{' ($expression ':' $expression (',' $expression ':' $expression )*)? '}'
$expression = object '{' ($identifier ':' $expression (',' $identifier ':' $expression )*)? '}'
$expression = '[' ($expression (',' $expression)*)? ']'
$expression = $string | $integer | $float | $boolean | $identifier
```

An expression is a compound statement that consists of literal values, identifiers (references to [declarations](#declarations) or [call](#call-statement) outputs), [built-in operators](#built-in-operators) (e.g. `+` or `>=`), and calls to [standard library functions](#standard-library).

A "simple" expression is one that does not make use of identifiers or any function that takes a `File` input or returns a `File` output; i.e. it is an expression that can be evaluated unambiguously without any knowledge of the runtime context. An execution engine may choose to replace simple expressions with their literal values.

```wdl
# simple expressions
Float f = 1 + 2.2
Boolean b = if 1 > 2 then true else false
Map[String, Int] = as_map(zip(["a", "b", "c"], [1, 2, 3]))

# non-simple expressions
Int i = x + 3  # requires knowing the value of x
# requires reading a file that might only exist at runtime
String s = read_string("/path/to/file")  
```

#### Built-in Operators

WDL provides the standard unary and binary mathematical and logical operators. The following table lists the valid operand and result type combinations for each operator. Using an operator with unsupported types results in an error.

In operations on mismatched numeric types (e.g. `Int` + `Float`), the `Int` type is first cast to a `Float`; the result type is always `Float`. This may result in loss of precision, for example if the `Int` is too large to be represented exactly by the `Float`. Note that a `Float` can be converted to an `Int` with the [`ceil`, `round`, or `floor`](#int-floorfloat-int-ceilfloat-and-int-roundfloat) functions.

##### Unary Operators

|Operator|RHS Type|Result|
|--------|--------|------|
|`-`|`Float`|`Float`|
|`-`|`Int`|`Int`|
|`!`|`Boolean`|`Boolean`|

##### Binary Operators on Primitive Types

|LHS Type|Operator|RHS Type|Result|Semantics|
|--------|--------|--------|------|---------|
|`Boolean`|`==`|`Boolean`|`Boolean`||
|`Boolean`|`!=`|`Boolean`|`Boolean`||
|`Boolean`|`\|\|`|`Boolean`|`Boolean`||
|`Boolean`|`&&`|`Boolean`|`Boolean`||
|🗑 `Boolean`|`>`|`Boolean`|`Boolean`|true is greater than false|
|🗑 `Boolean`|`>=`|`Boolean`|`Boolean`|true is greater than false|
|🗑 `Boolean`|`<`|`Boolean`|`Boolean`|true is greater than false|
|🗑 `Boolean`|`<=`|`Boolean`|`Boolean`|true is greater than false|
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
|🗑 `Int`|`+`|`String`|`String`||
|`Int`|`+`|`Float`|`Float`||
|`Int`|`-`|`Float`|`Float`||
|`Int`|`*`|`Float`|`Float`||
|`Int`|`/`|`Float`|`Float`||
|`Int`|`==`|`Float`|`Boolean`||
|`Int`|`!=`|`Float`|`Boolean`||
|`Int`|`>`|`Float`|`Boolean`||
|`Int`|`>=`|`Float`|`Boolean`||
|`Int`|`<`|`Float`|`Boolean`||
|`Int`|`<=`|`Float`|`Boolean`||
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
|🗑 `Float`|`+`|`String`|`String`||
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
|`String`|`+`|`String`|`String`|Concatenation|
|`String`|`+`|`File`|`File`||
|`String`|`==`|`String`|`Boolean`|Unicode comparison|
|`String`|`!=`|`String`|`Boolean`|Unicode comparison|
|`String`|`>`|`String`|`Boolean`|Unicode comparison|
|`String`|`>=`|`String`|`Boolean`|Unicode comparison|
|`String`|`<`|`String`|`Boolean`|Unicode comparison|
|`String`|`<=`|`String`|`Boolean`|Unicode comparison|
|🗑 `String`|`+`|`Int`|`String`||
|🗑 `String`|`+`|`Float`|`String`||
|`File`|`==`|`File`|`Boolean`||
|`File`|`!=`|`File`|`Boolean`||
|`File`|`==`|`String`|`Boolean`||
|`File`|`!=`|`String`|`Boolean`||
|🗑 `File`|`+`|`File`|`File`|append file paths - error if second path is not relative|
|🗑 `File`|`+`|`String`|`File`|append file paths - error if second path is not relative|

WDL `String`s are compared by the unicode values of their corresponding characters. Character `a` is less than character `b` if it has a lower unicode value.

Except for `String + File`, all concatenations between `String` and non-`String` types are deprecated and will be removed in WDL 2.0. The same effect can be achieved using [string interpolation](#expression-placeholders-and-string-interpolation).

##### Equality of Compound Types

|LHS Type|Operator|RHS Type|Result|
|--------|--------|--------|------|
|`Array`|`==`|`Array`|`Boolean`|
|`Array`|`!=`|`Array`|`Boolean`|
|`Map`|`==`|`Map`|`Boolean`|
|`Map`|`!=`|`Map`|`Boolean`|
|`Pair`|`==`|`Pair`|`Boolean`|
|`Pair`|`!=`|`Pair`|`Boolean`|
|`Struct`|`==`|`Struct`|`Boolean`|
|`Struct`|`!=`|`Struct`|`Boolean`|
|🗑`Object`|`==`|`Object`|`Boolean`|
|🗑`Object`|`!=`|`Object`|`Boolean`|

In general, two compound values are equal if-and-only-if all of the following are true:

1. They are of the same type.
2. They are the same length.
3. All of their contained elements are equal.

Since `Array`s and `Map`s are ordered, the order of their elements are also compared. For example:

```wdl
# arrays and maps with the same elements in the same order are equal
Boolean is_true1 = [1, 2, 3] == [1, 2, 3]
Boolean is_true2 = {"a": 1, "b": 2} == {"a": 1, "b": 2}

# arrays and maps with the same elements in different orders are not equal
Boolean is_false1 = [1, 2, 3] == [2, 1, 3]
Boolean is_false2 = {"a": 1, "b": 2} == {"b": 2, "a": 1}
```

Note that [type coercion](#type-coercion) can be employed to compare values of different but compatible types. For example:

```wdl
Array[Int] i = [1,2,3]
Array[Float] f = [1.0, 2.0, 3.0]
# Floats are not not automatically coerced to Ints for comparison
Boolean is_false = i == f

# instead, coerce i to an array of Float first
Array[Float] i_to_f = i
Boolean is_true = i_to_f == f
```

##### Equality and Inequality Comparison of Optional Types

The equality and inequality operators are exceptions to the general rules on [coercion of optional types](#coercion-of-optional-types). Either or both operands of an equality or inequality comparison can be optional, considering that `None` is equal to itself but no other value.

```wdl
Int i = 1
Int? j = 1
Int? k = None

# equal values of the same type are equal even if one is optional
Boolean is_true = i == j
# k is undefined (None), and so is only equal to None
Boolean is_true2 k == None
# these comparisons are valid and evaluate to false
Boolean is_false = i == k
Boolean is_false2 j == k
```

#### Operator Precedence Table

| Precedence | Operator type         | Associativity | Example              |
|------------|-----------------------|---------------|----------------------|
| 11         | Grouping              | n/a           | (x)                  |
| 10         | Member Access         | left-to-right | x.y                  |
| 9          | Index                 | left-to-right | x[y]                 |
| 8          | Function Call         | left-to-right | x(y,z,...)           |
| 7          | Logical NOT           | right-to-left | !x                   |
|            | Unary Negation        | right-to-left | -x                   |
| 6          | Multiplication        | left-to-right | x*y                  |
|            | Division              | left-to-right | x/y                  |
|            | Remainder             | left-to-right | x%y                  |
| 5          | Addition              | left-to-right | x+y                  |
|            | Subtraction           | left-to-right | x-y                  |
| 4          | Less Than             | left-to-right | x<y                  |
|            | Less Than Or Equal    | left-to-right | x<=y                 |
|            | Greater Than          | left-to-right | x>y                  |
|            | Greater Than Or Equal | left-to-right | x>=y                 |
| 3          | Equality              | left-to-right | x==y                 |
|            | Inequality            | left-to-right | x!=y                 |
| 2          | Logical AND           | left-to-right | x&&y                 |
| 1          | Logical OR            | left-to-right | x\|\|y               |

#### Member Access

The syntax `x.y` refers to member access. `x` must be a call in a workflow, or a `Struct` (or `Object`) value. A call can be thought of as a struct where the members are the outputs of the called task.

```wdl
# task foo has an output y
call foo
String x = foo.y

Stuct MyType {
  String b
}
MyType z = MyType { z: 'hello' }
String a = z.b
```

#### Ternary operator (if-then-else)

This is an operator that takes three arguments: a condition expression, an if-true expression, and an if-false expression. The condition is always evaluated. If the condition is true then the if-true value is evaluated and returned. If the condition is false, the if-false expression is evaluated and returned. The if-true and if-false expressions must return values of the same type, such that the value of the if-then-else is the same regardless of which side is evaluated.

Examples:

- Choose whether to say "good morning" or "good afternoon":
```wdl
task greet {
  input {
    Boolean morning
  }
  String greeting = "good ~{if morning then "morning" else "afternoon}"
}
```
- Choose how much memory to use for a task:
```wdl
task mytask {
  input {
    Array[String] array
  }
  Int array_length = length(array)
  Int memory = if array_length > 100 then "16GB" else "8GB"
}
```

#### Function Calls

WDL provides a [standard library](#standard-library) of functions. These functions can be called using the syntax `func(p1, p2, ...)`, where `func` is the function name and `p1` and `p2` are parameters to the function.

#### Expression Placeholders and String Interpolation

Any WDL string expression may contain one or more "placeholders" of the form `~{*expression*}`, each of which contains a single expression. Note that placeholders of the form `${*expression*}` may also be used interchangably, but their use is discouraged for reasons discussed in the [command section](#expression-placeholders) and may be deprecated in a future version of the specification.

When a string expression is evaluated, its placeholders are evaluated first, and their values are then substituted for the placeholders in the containing string.

```wdl
Int i = 3
String s = "~{1 + i}"  # s == "4"
```

As another example, consider how the following expression would be parsed:

```wdl
String command = "grep '~{start}...~{end}' ~{input}"
```

This command would be parsed as:

* `grep '` - literal string
* `~{start}` - identifier expression - replaced with the value of `start`
* `...` - literal string
* `~{end}` - identifier expression - replaced with the value of `end`
* `' ` - literal string
* `~{input}` - identifier expression - replaced with the value of `input`

Placeholders may contain other placeholders to any level of nesting, and placeholders are evaluated recursively in a depth-first manner. Placeholder expressions are anonymous - they have no name and thus cannot be referenced by other expressions, but they can reference declarations and call outputs.

```wdl
Int i = 3
Boolean b = true
# s evaluates to "4", but would be "0" if b were false
String s = "~{if b then '${1 + i}' else 0}"
```

##### Expression Placeholder Coercion

The expression result in a placeholder must ultimately be converted to a string in order to take the place of the placeholder in the command script. This is immediately possible for WDL primitive types due to automatic conversions ("coercions") that occur only within the context of string interpolation:

- `String` is substituted directly.
- `File` is substituted as if it were a `String`.
- `Int` is formatted without leading zeros (unless the value is `0`), and with a leading `-` if the value is negative.
- `Float` is printed in the style `[-]ddd.dddddd`, with 6 digits after the decimal point.
- `Boolean` is converted to the "stringified" version of its literal value, i.e. `true` or `false`.

```wdl
Boolean is_true1 = "~{"abc"}" == "abc"

File x = "hij"
Boolean is_true2 = "~{x}" == "hij"
 
Boolean is_true3 = "~{5}" == "5"

Boolean is_true4 = "~{3.141}" == "3.141000"
Boolean is_true5 = "~{3.141 * 1E-10}" == "0.000000"
Boolean is_true6 = "~{3.141 * 1E10}" == "31410000000.000000"
```

Compound types cannot be implicitly converted to strings. To convert an `Array` to a string, use the [`sep`](#-string-sepstring-arraystring) function: `~{sep(",", str_array)}`.

If an expression within a placeholder evaluates to `None`, then the placeholder is replaced by the empty string.

##### Concatenation of Optional Values

Within expression placeholders the string concatenation operator (`+`) gains the ability to operate on optional values, to facilitate formulation of command-line flags. When applied to two non-optional operands, the result is a non-optional `String`. However, if either operand has an optional type, then the concatenation has type `String?`, and the runtime result is `None` if either operand is `None` (which is then replaced with the empty string).

```wdl
String saluation = "hello"
String? name1
String? name2 = "Fred"

# since name1 is undefined, the evaluation of the
# expression in the placeholder fails, and the
# value of greeting1 = "nice to meet you!"
String greeting1 = "~{salutation + ' ' + name1 + ' '}nice to meet you!"

# since name2 is defined, the evaluation of the
# expression in the placeholder succeedes, and the
# value of greeting2 = "hello Fred, nice to meet you!"
String greeting2 = "~{salutation + ' ' + name2 + ', '}nice to meet you!"
```

To illustrate how this can be used, consider this task:

```wdl
task test {
  input {
    String? val
  }

  command <<<
    python script.py --val=~{val}
  >>>
}
```

Since `val` is optional, the command can be instantiated in two ways:

```
python script.py --val=foobar
```

Or

```
python script.py --val=
```

The latter case is very likely an error case, and this `--val=` part should be left off if a value for `val` is omitted. To solve this problem, modify the expression inside the template tag as follows:

```
python script.py ${"--val=" + val}
```
 
#### 🗑 Expression Placeholder Options

Expression placeholder options are `option="value"` pairs that precede the expression within an expression placeholder and customize the interpolation of the WDL value into the containing string expression.

The following options are available:

* [`sep`](#sep): convert an array to a string using a delimiter; e.g. `~{sep=", " array_value}`
* [`true` and `false`](#true-and-false): substitute a value depending on whether a boolean expression is `true` or `false`; e.g. `~{true="--yes" false="--no" boolean_value}`
* [`default`](#default): substitute a default value for an undefined expression; e.g. `~{default="foo" optional_value}`

Note that different options cannot be combined in the same expression placeholder.

**Expression placeholder options are deprecated and will be removed in WDL 2.0**. In the sections below, each type of placeholder option is described in more detail, including how to replicate its behavior using future-proof syntax.

##### `sep`

`sep` is interpreted as the separator string used to join multiple parameters together. `sep` is only valid if the expression evaluates to an `Array`.

For example, given a declaration `Array[Int] numbers = [1, 2, 3]`, the expression `"python script.py ~{sep=',' numbers}"` yields the value: `python script.py 1,2,3`.

Alternatively, if the command were `"python script.py ~{sep=' ' numbers}"` it would evaluate to: `python script.py 1 2 3`.

> *Requirements*:
>
> 1. `sep` MUST accept only a string as its value
> 2. `sep` is only allowed if the type of the expression is `Array[P]`

The `sep` option can be replaced with a call to the ✨ [`sep`](#-string-sepstring-arraystring) function:

```wdl
task sep_example {
  input {
    Array[String] str_array
    Array[Int] int_array
  }
  command <<<
    echo ~{sep(' ', str_array)}
    echo ${sep(',', quote(int_array))}
  >>>
}
```

##### `true` and `false`

`true` and `false` convert an expression that evaluates to a `Boolean` into a string literal when the result is `true` or `false`, respectively. 

For example, `"~{true='--enable-foo' false='--disable-foo' allow_foo}"` evaluates the expression `allow_foo` as an identifier and, depending on its value, replaces the entire expression placeholder with either `--enable-foo` or `--disable-foo`.

Both `true` and `false` cases are required. If one case should insert no value then an empty string literal is used, e.g. `"~{true='--enable-foo' false='' allow_foo}"`.

> *Requirements*:
>
> 1.  `true` and `false` values MUST be string literals.
> 2.  `true` and `false` are only allowed if the type of the expression is `Boolean`
> 3.  Both `true` and `false` cases are required.

The `true` and `false` options can be replaced with the use of an if-then-else expression:

```wdl
task tf_example {
  input {
    Boolean debug
  }
  command <<<
    ./my_cmd ~{if debug then "--verbose" else "--quiet"}
  >>>
}
```

##### `default`

The `default` option specifies a value to substitute for an optional-typed expression with an undefined value.

For example, this task takes an optional `String` parameter and, if a value is not specified, then the value `foobar` is used instead.

```wdl
task default_test {
  input {
    String? s
  }
  command <<<
    ./my_cmd ~{default="foobar" s}
  >>>
  ....
}
```

> *Requirements*:
>
> 1. The type of the default value must match the type of the expression
> 2. The type of the expression must be optional, i.e. it must have a `?` postfix quantifier

The `default` option can be replaced in several ways - most commonly with an if-then-else expression or with a call to the [`select_first`](#x-select_firstarrayx) function.

```wdl
task default_example {
  input {
    String? s
  }
  command <<<
    .my_cmd ~{if defined(s) then "--opt ${s}" else "foobar"}"foobar"}
    # OR
    .my_cmd ~{select_first([s, "foobar"])}
  >>>
}
```

## WDL Documents

A WDL document is a file that contains valid WDL definitions.

A WDL document must contain:

* A [`version` statement](#versioning) on the first non-comment line of the file.
* At least one [`task` definition](#task-definition), [`workflow` definition](#workflow-definition), or [`struct` definition](#struct-definition).

A WDL document may contain any combination of the following:

* Any number of [`import` statements](#import-statements).
* Any number of `task` definitions.
* Any number of `struct` definitions.
* A maximum of one `workflow` definition.

To execute a WDL workflow, the user must provide the execution engine with the location of a "primary" WDL file (which may import additional files as needed) and any input values needed to satisfy all required task and workflow input parameters, using a [standard input JSON file](#json-input-format) or some other execution engine-specific mechanism.

If a workflow appears in the primary WDL file, it is called the "top-level" workflow, and any workflows it calls via imports are "subworkflows". Typically, it is an error for the primary WDL file to not contain a workflow; however, an execution engine may choose to support executing individual tasks.

## Versioning

There are multiple versions of the WDL specification. Every WDL document must include a version statement to specify which version of the specification it adheres to. From `draft-3` forward, the first non-comment statement of all WDL files must be a `version` statement. For example:

```wdl
version 1.1
```

or

```wdl
#Licence header

version 1.1
```

A WDL file that does not have a `version` statement must be treated as `draft-2`.

## Import Statements

A WDL file may contain import statements to include WDL code from other sources.

```txt
$import = 'import' $ws+ $string ($ws+ $import_namespace)? ($ws+ $import_alias)*
$import_namespace = 'as' $ws+ $identifier
$import_alias = 'alias' $identifier $ws+ 'as' $ws+ $identifier
```

The `import` statement specifies a WDL document source as a string literal, which is interpreted as a URI. The execution engine is responsible for resolving the URI and downloading the contents.  The contents of the document in each URI must be WDL source code **of the same version as the importing document**.

Every imported WDL file requires a namespace, which can be specified using the `as $identifier` syntax. If a namespace identifier is not specified explicitly, then the default namespace is the filename of the imported WDL, minus the `.wdl` extension. For all imported WDL files, the tasks and workflows imported from that file will only be accessible through the assigned [namespace](#namespaces) - see [Fully Qualified Names & Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers) for details.

```wdl
import "http://example.com/lib/analysis_tasks" as analysis
import "http://example.com/lib/stdlib.wdl"

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

The execution engine must at least support the following protocols for import URIs:

* `http://`
* `https://`
* 🗑 `file://` - Using the `file://` protocol for local imports can be problematic. Its use is deprecated and will be removed in WDL 2.0.

In the event that there is no protocol specified, the import is resolved **relative to the location of the current document**. If a protocol-less import starts with `/` it will be interpreted as starting from the root of the host in the resolved URL.

Some examples of correct import resolution:

| Root Workflow Location                                | Imported Path                      | Resolved Path                                           |
|-------------------------------------------------------|------------------------------------|--------------------------------------------------------|
| /foo/bar/baz/qux.wdl                                  | some/task.wdl                      | /foo/bar/baz/some/task.wdl                               |
| http://www.github.com/openwdl/coolwdls/myWorkflow.wdl | subworkflow.wdl                    | http://www.github.com/openwdl/coolwdls/subworkflow.wdl  |
| http://www.github.com/openwdl/coolwdls/myWorkflow.wdl | /openwdl/otherwdls/subworkflow.wdl | http://www.github.com/openwdl/otherwdls/subworkflow.wdl |
| /some/path/hello.wdl                                  | /another/path/world.wdl            | /another/path/world.wdl                                  |

`Import` statements also support aliasing of structs using the `x as y` syntax. See [struct namespacing](#struct-namespacing) for details.

## Task Definition

A WDL task can be thought of as a template for running a set of commands - specifically, a UNIX Bash script - in a manner that is (ideally) independent of the execution engine and the runtime environment.

A task is defined using the `task` keyword, followed by a task name that is unique within its WDL document.

A task has a required [`command`](#command-section) that is a template for a Bash script.

Tasks explicitly define their [`input`s](#task-inputs) and [`output`s](#task-outputs), which is essential for building dependencies between tasks. The value of an input declaration may be supplied by the caller. All task declarations may be initialized with hard-coded literal values, or may have their values constructed from expressions. Declarations can be referenced in the command template.

A task may also specify [requirements for the runtime environment](#runtime-section) (such as the amount of RAM or number of CPU cores) that must be satisfied in order for its commands to execute properly.

There are two optional metadata sections: the [`meta`](#metadata-sections) section, for task-level metadata, and the [`parameter_meta`](#parameter-metadata-section) section, for parameter-level metadata.

The execution engine is responsible for "instantiating" the shell script (i.e. replacing all references with actual values) in an environment that meets all specified runtime requirements, localizing any input files into that environment, executing the script, and generating any requested outputs.

```wdl
task name {
  input {
    # task inputs are declared here
  }

  # other "private" declarations can be made here
 
  command <<<
    # the command template - this section is required
  >>>

  output {
    # task outputs are declared here
  }

  runtime {
    # runtime requirements are specified here
  }

  meta {
    # task-level metadata can go here
  }

  parameter_meta {
    # metadata about each input/output parameter can go here
  }
}
```

### Task Inputs

A task's `input` section declares its input parameters. The values for declarations within the input section may be specified by the caller of the task. An input declaration may be initialized to a default value or expression that will be used when the caller does not specify a value. Input declarations may also be optional, in which case a value may be specified but is not required. If an input declaration is not optional and does not have an initialization, then it is a required input, meaning the caller must specify a value.

```wdl
task t {
  input {
    Int i               # a required input parameter
    String s = "hello"  # an input parameter with a default value
    File? f             # an optional input parameter
  }

  # [... other task sections]
}
```

#### Task Input Localization

`File` inputs must be treated specially since they may require localization to the execution directory. For example, a file located on a remote web server that is provided to the execution engine as an `https://` URL must first be downloaded to the machine where the task is being executed.

- Files are localized into the execution directory prior to the task execution commencing.
- When localizing a `File`, the engine may choose to place the file wherever it likes so long as it adheres to these rules:
  - The original file name must be preserved even if the path to it has changed.
  - Two input files with the same name must be located separately, to avoid name collision.
  - Two input files that originated in the same storage directory must also be localized into the same directory for task execution (see the special case handling for Versioning Filesystems below).
- When a WDL author uses a `File` input in their [Command Section](#command-section), the fully qualified, localized path to the file is substituted when that declaration is referenced in the command template.

##### Special Case: Versioning Filesystem

Two or more versions of a file in a versioning filesystem might have the same name and come from the same directory. In that case, the following special procedure must be used to avoid collision:
  - The first file is always placed according to the rules above.
  - Subsequent files that would otherwise overwrite this file are instead placed in a subdirectory named for the version.

For example, imagine two versions of file `fs://path/to/A.txt` are being localized (labeled version `1.0` and `1.1`). The first might be localized as `/execution_dir/path/to/A.txt`. The second must then be placed in `/execution_dir/path/to/1.1/A.txt`

#### Input Type Constraints

Recall that a type may have a quantifier:
* `?` means that the parameter is optional. A user does not need to specify a value for the parameter in order to satisfy all the inputs to the workflow.
* `+` applies only to `Array` types and it represents a constraint that the `Array` value must contain one-or-more elements.

The following task has several inputs with type quantifiers:

```wdl
task test {
  input {
    Array[File]  a
    Array[File]+ b
    Array[File]? c
    # If the next line were uncommented it would cause an error
    # + only applies to Array, not File
    #File+ d
    # An optional array that, if defined, must contain at least one element
    Array[File]+? e
  }

  command <<<
    /bin/mycmd ~{sep=" " a}
    /bin/mycmd ~{sep="," b}
    /bin/mycmd ~{write_lines(c)}
  >>>
  
  runtime {
    container: "my_image:latest"
  }
}
```

If these input values are provided:

|input |value|
|------|-----|
|test.a|["1", "2", "3"]|
|test.b|[]|

It will result in an error, since `test.b` is required to have at least one element.

On the other hand, if these input values are provided:

|var   |value|
|------|-----|
|test.a|["1", "2", "3"]|
|test.b|["x"]|

The task will run successfully, because `test.c` is not required. Given these values, the command would be instantiated as:

```txt
/bin/mycmd 1 2 3
/bin/mycmd x
/bin/mycmd
```

If the inputs were:

|var   |value|
|------|-----|
|test.a|["1", "2", "3"]|
|test.b|["x","y"]|
|test.c|["a","b","c","d"]|

Then the command would be instantiated as:

```txt
/bin/mycmd 1 2 3
/bin/mycmd x,y
/bin/mycmd /path/to/c.txt
```

##### Optional inputs with defaults

It *is* possible to provide a default to an optional input type. This may be desirable in the case where you want to have a defined value by default, but you want the caller to be able to override the default and set the value to undefined (i.e. `None`).

```wdl
task say_hello {
  input {
    String name
    String? saluation = "hello"
  }
  command <<< >>>
  output {
    String greeting = if defined(saluation) then "${saluation} ${name}" else name
  }
}

workflow foo {
  input {
    String name
    Boolean use_salutation
  }
  
  if (use_salutation) {
    call say_hello { input: name = name }
  }

  if (!use_salutation) {
    call say_hello { 
      input: 
        name = name,
        salutation = None 
    }
  }
}
```

### Private Declarations

A task can have declarations that are intended as intermediate values rather than inputs. These private declarations may appear anywhere in the body of the task, and they must be initialized. Just like input declarations, private declarations may be initialized with literal values, or with expressions that may reference other declarations.

For example, this task takes an input and then performs a calculation, using a private declaration, that can then be referenced in the command template:

```wdl
task t {
  input {
    Int size
  }

  Int size_clamped = if size > 10 then 10 else size
  ...
}
```

The value of a private declaration may *not* be specified by the task caller, nor is it accessible outside of the task [scope](#task-scope).

```wdl
task test {
  input {
    Int i
  }
  String s = "hello"
  command <<< ... >>>
  output {
    File out = "/path/to/file"
  }
}

workflow wf {
  call test {
    input:
      i = 1,         # this is fine - "i" is in the input section
      s = "goodbye"  # error! "s" is private
  }
  output {
    File out = test.out # this is fine - "out" is in the output section
    String s = test.s   # error! "s" is private
  }
}
```

### Command Section

The `command` section is the only required task section. It defines the command template that is evaluated and executed when the task is called. Specifically, the commands are executed after all of the inputs are staged and before the outputs are evaluated.

There are two different syntaxes that can be used to define the command section:

```wdl
# HEREDOC style - this way is preferred
command <<< ... >>>

# older style - may be preferable in some cases
command { ... }
```

There may be any number of commands within a command section. Commands are not modified by the execution engine, with the following exceptions:
- Common leading whitespace is [stripped](#stripping-leading-whitespace)
- String interpolation is performed on the entire command section to replace [expression placeholders](#expression-placeholders) with their actual values.

#### Expression Placeholders

The body of the command section (i.e. the command "template") can be though of as a single string expression, which (like all string expressions) may contain placeholders.

There are two different syntaxes that can be used to define command expression placeholders, depending on which style of command section definition is used:

|Command Definition Style|Placeholder Style|
|---|---|
|`command <<< >>>`|`~{}` only|
|`command { ... }`|`~{}` (preferred) or `${}`|

Note that the `~{}` and `${}` styles may be used interchangably in other string expressions.

Any valid WDL expression may be used within a placeholder. For example, a command might reference an input to the task, like this:

```wdl
task test {
  input {
    File infile
  }
  command <<<
    cat ~{infile}
  >>>
  ....
}
```

In this case, `infile` within the `~{...}` is an identifier expression referencing the value of the `infile` input parameter that was specified at runtime. Since `infile` is a `File` declaration, the execution engine will have staged whatever file was referenced by the caller such that it is available on the local file system, and will have replaced the original value of the `infile` parameter with the path to the file on the local filesystem.

The expression can also be more complex, for example a function call: 

```wdl
task write_array {
  input {
    Array[String] str_array
  }
  command <<<
    # the "write_lines" function writes each string in an array
    # as a line in a temporary file, and returns the path to that
    # file, which can then be referenced by other commands such as 
    # the unix "cat" command
    cat ~{write_lines(str_array)}
  >>>
}
```

In most cases, the `~{}` style of placeholder is preferred, to avoid ambiguity between WDL placeholders and Bash variables, which are of the form `$name` or `${name}`. If the `command { ... }` style is used, then `${name}` is always interpreted as a WDL placeholder, so care must be taken to only use `$name` style Bash variables. If the `command <<< ... >>>` style is used, then only `~{name}` is interpreted as a WDL placeholder, so either style of Bash variable may be used.

```wdl
task test {
  input {
    File infile
  }
  command {
    # store value of WDL declaration "infile" to Bash variable "f"
    f=${infile}
    # cat the file referenced by Bash variable "f"
    cat $f
    # this causes an error since "f" is not a WDL declaration
    cat ${f}
  }
  ....
}
```

Keep in mind that the command section is still subject to the rules of [string interpolation](#expression-placeholders-and-string-interpolation): ultimately, the value of the placeholder must be converted to a string. This is immediately possible for primitive values, but compound values must be somehow converted to primitive values. In some cases, this is not possible, and the only available mechanism is to write the complex output to a file. See the guide on [WDL value serialization](#appendix-a-wdl-value-serialization-and-deserialization) for details.

#### Stripping Leading Whitespace

When a command template is evaluate, the execution engine first strips out all *common leading whitespace*.

For example, consider a task that calls the `python` interpreter with an in-line Python script:

```wdl
task heredoc {
  input {
    File infile
  }

  command<<<
  python <<CODE
    with open("~{in}") as fp:
      for line in fp:
        if not line.startswith('#'):
          print(line.strip())
  CODE
  >>>
  ....
}
```

Given an `infile` value of `/path/to/file`, the execution engine will produce the following Bash script, which has removed the two spaces that were common to the beginning of each line:

```sh
python <<CODE
  with open("/path/to/file") as fp:
    for line in fp:
      if not line.startswith('#'):
        print(line.strip())
CODE
```

If the user mixes tabs and spaces, the behavior is undefined. The execution engine should, at a minimum, issue a warning and leave the whitespace unmodified, though it may choose to raise an exception or to substitute e.g. 4 spaces per tab.

### Task Outputs

The `output` section contains declarations that are exposed as outputs of the task after a call to the task completes successfully. An output declaration must be initialized, and its value is evaluated only after the task's command completes successfully, enabling any files generated by the command to be used to determine its value.

For example a task's `output` section might looks like this:

```wdl
output {
  Int threshold = read_int("threshold.txt")
  Array[File]+ csvs = glob("*.csv")
  File? outfile = "path/to/outfile.txt"
}
```

After the command is executed, the following outputs are expected to be found in the task execution directory:
- A file called "threshold.txt", which contains one line that consists of only an integer and whitespace.
- One or more files (as indicated by the `+` postfix quantifier) with the `.csv` extension in the working directory that are collected into an array by the [`glob`](#arrayfile-globstring) function.
- There may or may not be an output file at `path/to/outfile.txt` (relative to the execution directory) - if the file does not exist, the value of `outfile` will be undefined.

See the [WDL Value Serialization](#appendix-a-wdl-value-serialization-and-deserialization) section for more details.

#### Files and Optional Outputs

File outputs are represented as string paths.

A common pattern is to use a placeholder in a string expression to construct a file name as a function of the task input. For example:

```wdl
task example {
  input {
    String prefix
    File bam
  }

  command <<<
    python analysis.py --prefix=~{prefix} ~{bam}
  >>>

  output {
    File analyzed = "~{prefix}.out"
    File bam_sibling = "~{bam}.suffix"
  }
  
  runtime {
    container: "quay.io/biocontainers/bwa:0.7.17--hed695b0_7"
  }
}
```

If prefix were specified as `"foobar"`, then `"~{prefix}.out"` would be evaluated to `"foobar.out"`.

Another common pattern is to use the [`glob`](#arrayfile-globstring) function to define outputs that might contain zero, one, or many files.

```wdl
output {
  Array[File] output_bams = glob("*.bam")
}
```

Relative paths are interpreted relative to the execution directory, whereas absolute paths are interpreted in a container-dependent way.

```wdl
# 'rel' is always at the given path relative to the execution dir
File rel = "my/path/to/something.txt"
# 'abs' may be in the root dir of the container file system if
# we're running in a Docker container, or it might be in the
# root dir of the host machine's file system if we're not
File abs = "/something.txt"
```

All file outputs are required to exist, otherwise the task will fail. However, an output may be declared as optional (e.g. `File?` or `Array[File?]`), in which case the value will be undefined if the file does not exist.

For example, executing the following task:

```wdl
task optional_output {
  command <<<
    touch example_exists.txt
    touch arr2.exists.txt
  >>>
  output {
    File example_exists = "example_exists.txt"
    File? example_optional = "example_optional.txt"
    Array[File?] array_optional = ["arr1.dne.txt", "arr2.exists.txt"]
  }
}
```

will generate the following outputs:

* `optional_output.example_exists` will resolve to a File
* `optional_output.example_optional` will resolve to `None`
* `optional_output.array_optional` will resolve to `[<File>, None]`

### Evaluation of Task Declarations

All non-output declarations (i.e. input and private declarations) must be evaluated prior to evaluating the command section.

Input and private declarations may appear in any order within their respective sections and they may reference each other so long as there are no circular references. Input and private declarations may *not* reference declarations in the output section.

Declarations in the output section may reference any input and private declarations, and may also reference other output declarations.

### Runtime Section

```txt
$runtime = 'runtime' $ws* '{' ($ws* $runtime_kv $ws*)* '}'
$runtime_kv = $identifier $ws* '=' $ws* $expression
```

The `runtime` section defines a set of key/value pairs that represent the minimum requirements needed to run a task and the conditions under which a task should be interpreted as a failure or success. 

During execution of a task, resource requirements within the `runtime` section must be enforced by the engine. If the engine is not able to provision the requested resources, then the task immediately fails. 

There are a set of reserved attributes (described below) that must be supported by the execution engine, and which have well-defined meanings and default values. Default values for all optional standard attributes are directly defined by the WDL specification in order to encourage portability of workflows and tasks; execution engines should NOT provide additional mechanisms to set _default_ values for when no runtime attributes are defined.

🗑 Additional arbitrary attributes may be specified in the `runtime` section, but these may be ignored by the execution engine. These non-standard attributes are called "hints". The use of hint attributes in the `runtime` section is deprecated; a later version of WDL will introduce a new `hints` section for arbitrary attributes and disallow non-standard attributes in the `runtime` section.

The value of a `runtime` attribute can be any expression that evaluates to the expected type - and in some cases matches the accepted format - for that attribute. Expressions in the `runtime` section may reference (non-output) declarations in the task:

```wdl
task test {
  input {
    String ubuntu_version
  }

  command <<<
    python script.py
  >>>
  
  runtime {
    container: ubuntu_version
  }
}
```

#### Units of Storage

Several of the `runtime` attributes can (and some [Standard Library](#standard-library) functions) accept a string value with an optional unit suffix, using one of the valid [SI or IEC abbreviations](https://en.wikipedia.org/wiki/Binary_prefix). At a minimum, execution engines must support the following suffices in a case-insensitive manner:

* B (bytes)
* Decimal: KB, MB, GB, TB
* Binary: KiB, MiB, GiB, TiB

An optional space is allowed between the number/expression and the suffix. For example: `6.2 GB`, `5MB`, `"~{ram}GiB"`.

The decimal and binary units may be shortened by omitting the trailing "B". For example, "K" and "KB" are both interpreted as "kilobytes".

#### Mandatory `runtime` attributes

The following attributes must be supported by the execution engine. The value for each of these attributes must be defined - if it is not specified by the user, then it must be set to the specified default value. 

##### `container`

* Accepted types:
    * `String`: A single container URI.
    * `Array[String]`: An array of container URIs.

The `container` key accepts a URI string that describes a location where the execution engine can attempt to retrieve a container image to execute the task.

The user is strongly suggested to specify a `container` for every task. There is no default value for `container`. If `container` is not specified, the execution behavior is determined by the execution engine. Typically, the task is simply executed in the host environment. 

🗑 The ability to omit `container` is deprecated. In WDL 2.0, `container` will be required.

The format of a container URI string is `protocol://location`, where protocol is one of the protocols supported by the execution engine. Execution engines must, at a minimum, support the `docker://` protocol, and if no protocol is specified, it is assumed to be `docker://`. An execution engine should ignore any URI with a protocol it does not support.

```wdl
task single_image_test {
  #....
  runtime {
    container: "ubuntu:latest"
  }
```

Container source locations should use the syntax defined by the individual container repository. For example an image defined as `ubuntu:latest` would conventionally refer a docker image living on `DockerHub`, while an image defined as `quay.io/bitnami/python` would refer to a `quay.io` repository.

The `container` key also accepts an array of URI strings. All of the locations must point to images that are equivalent, i.e. they must always produce the same final results when the task is run with the same inputs. It is the responsibility of the execution engine to define the specific image sources it supports, and to determine which image is the "best" one to use at runtime. The ordering of the array does not imply any implicit preference or ordering of the containers. All images are expected to be the same, and therefore any choice would be equally valid. Defining multiple images enables greater portability across a broad range of execution environments.

```wdl
task multiple_image_test {
  #.....
  runtime {
    container: ["ubuntu:latest", "https://gcr.io/standard-images/ubuntu:latest"]
  }
}
```

The execution engine must cause the task to fail immediately if none of the container URIs can be successfully resolved to a runnable image.

🗑 `docker` is supported as an alias for `container` with the exact same semantics. Exactly one of the `container` or `docker` is required. The `docker` alias will be dropped in WDL 2.0.

##### `cpu`

* Accepted types:
    * `Int`
    * `Float`
* Default value: `1`

The `cpu` attribute defines the _minimum_ number of CPU cores required for this task, which must be available prior to instantiating the command. The execution engine must provision at least the requested number of CPU cores, but it may provision more. For example, if the request is `cpu: 0.5` but only discrete values are supported, then the execution engine might choose to provision `1.0` CPU instead.

```wdl
task cpu_example {
  #....	
  runtime {
    cpu: 8
  }
}
```

##### `memory`

* Accepted types:
    * `Int`: Bytes of RAM.
    * `String`: A decimal value with, optionally with a unit suffix.
* Default value: `2 GiB`

The `memory` attribute defines the _minimum_ memory (RAM) required for this task, which must be available prior to instantiating the command. The execution engine must provision at least the requested amount of memory, but it may provision more. For example, if the request is `1 GB` but only blocks of `4 GB` are available, then the execution engine might choose to provision `4.0 GB` instead.

```wdl
task memory_test {
  #....
  runtime {
    memory: "2 GB"
  }
}
```

##### `gpu`

* Accepted type: `Boolean`
* Default value: `false`

The `gpu` attribute provides a way to accommodate modern workflows that are increasingly becoming reliant on GPU computations. This attribute simply indicates to the execution engine that a task requires a GPU to run to completion. A task with this flag set to `true` is guaranteed to only run if a GPU is a available within the runtime environment. It is the responsibility of the execution engine to check prior to execution whether a GPU is provisionable, and if not, preemptively fail the task.

This attribute *cannot* request any specific quantity or types of GPUs to make available to the task. Any such information should be provided using an execution engine-specific attribute.

```wdl
task gpu_test {
  #.....
  runtime {
    gpu: true
  }
}
```

##### `disks`

* Accepted types:
    * `Int`: Amount disk space to request, in `GiB`.
    * `String`: A disk specification - one of the following:
        * `"<size>"`: Amount disk space to request, in `GiB`.
        * `"<size> <suffix>"`: Amount disk space to request, with the given suffix.
        * `"<mount-point> <size>"`: A mount point and the amount disk space to request, in `GiB`.
        * `"<mount-point> <size> <suffix>"`: A mount point and the amount disk space to request, with the given suffix.
    * `Array[String]` - An array of disk specifications.
* Default value: `1 GiB`

The `disks` attribute provides a way to request one or more persistent volumes of at least a specific size and mounted at a specific location. When the `disks` attribute is provided, the execution engine must guarantee the requested resources are available or immediately fail the task prior to instantiating the command.

 ```wdl
task disks_test {
  #.....
  runtime {
    disks: 100
  }
}
```

This property does not specify exactly what type of persistent volume is being requested (e.g. SSD, HDD), but leaves this up to the engine to decide, based on what hardware is available or on another execution engine-specific attribute.

If a disk specification string is used to specify a mount point, then the mount point must be an absolute path to a location on the host machine. If the mount point is omitted, it is assumed to be a persistent volume mounted at the root of the execution directory within a task.

```wdl
task disks_test {
  #.....
  runtime {
    disks: "/mnt/outputs 500 GiB"
  }
}
```

If an array of disk specifications is used to specify multiple disk mounts, only one of them is allowed to omit the mount point.

```wdl
task disks_test {
  #.....
  runtime {
  	# The first value will be mounted at the execution root
    disks: ["500", "/mnt/outputs 500 GiB", "/mnt/tmp 5 TB"]
  }
}
```

##### `maxRetries`

* Accepted type: `Int`
* Default value: `0`

The `maxRetries` attribute provides a mechanism for a task to be retried in the event of a failure. If this attribute is defined, the execution engine must retry the task UP TO but not exceeding the number of attempts that it specifies.

The execution engine may choose to define an upper bound (>= 1) on the number of retry attempts that it permits.

A value of `0` means that the task as not retryable, and therefore any failure in the task should never result in a retry by the execution engine, and the final status of the task should remain the same.

```wdl
task maxRetries_test {
  #.....
  runtime {
    maxRetries: 4
  }
}
```

##### `returnCodes`

* Accepted types:
    * `"*"`: This special value indicates that ALL returnCodes should be considered a success.
    * `Int`: Only the specified return code should be considered a success.
    * `Array[Int]`: Any of the return codes specified in the array should be considered a success.
* Default value: `0`

The `returnCodes` attribute provides a mechanism to specify the return code, or set of return codes, that indicates a successful execution of a task. The engine must honor the return codes specified within the runtime block and set the tasks status appropriately. 

**Single return code**

```wdl
task maxRetries_test {
  #.....
  runtime {
    returnCodes: 1
  }
}
```

**Multiple return codes**

```wdl
task maxRetries_test {
  #.....
  runtime {
    returnCodes: [1,2,5,10]
  }
}
```

**All return codes**

```wdl
task maxRetries_test {
  #.....
  runtime {
    returnCodes: "*"
  }
}
```

#### Reserved `runtime` hints

The following attributes are considered "hints" rather than requirements. They are optional for execution engines to support. The purpose of reserving these attributes is to encourage interoperability of tasks and workflows between different execution engines.

In WDL 2.0, these attributes will move to the new `hints` section.

* `maxCpu`: Specifies the maximum CPU to be provisioned for a task. The value of this hint has the same specification as `runtime.cpu`.
* `maxMemory`: Specifies the maximum memory provisioned for a task. The value of this hint has the same specification as `runtime.memory`.
* `shortTask`: A `Boolean` value, for which `true` indicates that that this task is not expected to take long to execute. The execution engine can interpret this as permission to attempt to optimize the execution of the task - e.g. by batching together multiple `shortTask`s, or by using the cost-optimized instance types that many clouds provide, e.g. `preemptible` instances on `gcp` and `spot` instances on `aws`. "Short" is a bit relative, but should generally be interpreted as << 24h.
* `localizationOptional`: A `Boolean` value, for which `true` indicates that, if possible, the `File` type input declarations for this task should not be (immediately) localized. For example, a task that processes its input file once in linear fashion could have that input streamed (e.g. using a `fifo`) rather than requiring the input file to be fully localized prior to execution. This directive must not have any impact on the success or failure of a task (i.e. a task should run with or without localization).
* `inputs`: Provides input-specific hints in the form of a hints object. Each key within this hint should refer to an actual input defined for the current task.
  * `inputs.<key>.localizationOptional`: Tells the execution engine that a specific `File` input does not need to be localized for this task.
* `outputs`: Provides outputs specific hints in the form of a hints object. Each key within this hint should refer to an actual output defined for the current task
  
```wdl
task foo {
  input {
    File bar
  } 
  ...
  runtime {
    container: "ubuntu:latest"
    maxMemory: "36 GB"
    maxCpu: 24
    shortTask: true
    localizationOptional: false
    inputs: object {
      bar: object { 
        localizationOptional: true
      } 
    }
  }
}
```

#### Conventions and Best Practices

In order to encourage interoperable workflows, WDL authors and execution engine implementors should view hints strictly as an optimization that can be made for a specific task at runtime; hints should not be interpreted as requirements for that task. By following this principle, we can guarantee that a workflow is runnable on all platforms assuming the `runtime` block has the required parameters, regardless of whether it contains any additional hints.

The following guidelines should be followed when using hints:

* A hint should never be required.
* Less is more. Before adding a new hint key, ask yourself "do I really need another hint?", or "is there a better way to specify the behavior I require". If there is, then adding a hint is likely not the right way to achieve your aims.
* Complexity is killer. By allowing any arbitrary keys, it is possible that the `runtime` section can get quite unruly and complex. This should be discouraged, and instead a pattern of simplicity should be stressed.
* Sharing is caring. People tend to look for similar behavior between different execution engines. It is strongly encouraged that execution engines agree on common names and accepted values for hints that describe common usage patterns. A good example of hints that have conventions attached to them is cloud provider specific details:
    ```wdl
    task foo {
      .... 
      runtime {
        gcp: {
        ...
        }
        aws: {
        ...
        }
        azure: {
          ...
        }
        alibaba: {
          ...
        }
      }
    }
    ```
* Use objects to avoid collisions. If there are specific hints that are unlikely to ever be shared between execution engines, it is good practice to encapsulate these within their own execution engine-specific hints object:
    ```wdl
    task foo {
      .... 
      runtime {
        cromwell: {
          # cromwell specific 
          ...
        }
        miniwdl: {
          # miniwdl specific
          ...
        }
      }
    }
    ```

### Metadata Sections

```txt
$meta_kv = $identifier $ws* '=' $ws* $meta_value
$meta_value = $string | $number | $boolean | 'null' | $meta_object | $meta_array
$meta_object = '{}' | '{' $meta_kv (, $meta_kv)* '}'
$meta_array = '[]' |  '[' $meta_value (, $meta_value)* ']'
```

There are two purely optional sections that can be used to store metadata with the task: `meta` and `parameter_meta`. These sections are designed to contain metadata that is only of interest to human readers. The engine can ignore these sections with no loss of correctness. The extra information can be used, for example, to generate a user interface. Any attributes that may influence execution behavior should go in the `runtime` section.

Both of these sections can contain key/value pairs. Metadata values are different than in `runtime` and other sections:

* Only string, numeric, and boolean primitives are allowed.
* Only array and "meta object" compound values are allowed.
* The special value `null` is allowed for undefined attributes.
* Expressions are not allowed.

A meta object is similar to a struct literal, except:
* A `Struct` type name is not required.
* Its values must conform to the same metadata rules defined above.

```wdl
task {
  meta {
    authors: ["Jim", "Bob"]
    version: 1.1
    citation: {
      year: 2020,
      doi: "1234/10.1010"
    }
  }
}
```

Note that, unlike the WDL `Object` type, metadata objects are not deprecated and will continue to be supported in future versions.

#### Task Metadata Section

```txt
$meta = 'meta' $ws* '{' ($ws* $meta_kv $ws*)* '}'
```

This section contains task-level metadata. For example: author and contact email.

#### Parameter Metadata Section

```txt
$parameter_meta = 'parameter_meta' $ws* '{' ($ws* $meta_kv $ws*)* '}'
```

This section contains metadata specific to input and output parameters. Any key in this section *must* correspond to a task input or output.

```wdl
task wc {
  input {
    File infile
    Boolean lines_only = false
    String? region
  }

  parameter_meta {
    infile: {
      help: "Count the number of lines in this file"
    }
    lines_only: { 
      help: "Count only lines"
    }
    region: {
      help: "Cloud region",
      suggestions: ["us-west", "us-east", "asia-pacific", "europe-central"]
    }
  }

  command <<<
    wc ~{true="-l", false=' ' lines_only} ~{infile}
  >>>

  output {
     String retval = stdout()
  }

  runtime {
    container: "my_image:latest"
  }
}
```

### Task Examples

#### Example 1: Simplest Task

```wdl
task hello_world {
  command <<<
  echo "hello world"
  >>>
}
```

#### Example 2: Inputs/Outputs

```wdl
task one_and_one {
  input {
    String pattern
    File infile
  }
  command <<<
    grep ~{pattern} ~{infile}
  >>>
  output {
    File filtered = stdout()
  }
  runtime {
    container: "my_image:latest"
  }
}
```

#### Example 3: Runtime/Metadata

```wdl
task runtime_meta {
  input {
    Int memory_mb
    String sample_id
    String param
  }
  command <<<
    java -Xmx~{memory_mb}M -jar task.jar -id ~{sample_id} -param ~{param} -out ~{sample_id}.out
  >>>
  output {
    File results = "~{sample_id}.out"
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
  runtime {
    container: "my_image:latest"
    memory: "~{memory_mb + 256} MB"
  }
}
```

#### Example 4: BWA MEM

```wdl
task bwa_mem_tool {
  input {
    Int threads
    Int min_seed_length
    Array[Int]+ min_std_max_min
    File reference
    File reads
  }
  command <<<
    bwa mem -t ~{threads} \
            -k ~{min_seed_length} \
            -I ~{sep=',' min_std_max_min} \
            ~{reference} \
            ~{sep=' ' reads+} > output.sam
  >>>
  output {
    File sam = "output.sam"
  }
  runtime {
    container: "my_image:latest"
    cpu: threads
  }
}
```

#### Example 5: Word Count

```wdl
task wc2_tool {
  input {
    File file1
  }
  command <<<
    wc ~{file1}
  >>>
  output {
    Int count = read_int(stdout())
  }
  runtime {
    container: "my_image:latest"
  }
}

workflow count_lines4_wf {
  input {
    Array[File] files
  }
  scatter (f in files) {
    call wc2_tool {
      input: file1 = f
    }
  }
  output {
    wc2_tool.count
  }
}
```

#### Example 6: tmap

```wdl
task tmap_tool {
  input {
    Array[String] stages
    File reads
  }
  command <<<
    tmap mapall ~{sep=' ' stages} < ~{reads} > output.sam
  >>>
  output {
    File sam = "output.sam"
  }
  runtime {
    container: "my_image:latest"
  }
}
```

Given the following inputs:

|Variable|Value|
|--------|-----|
|reads   |/path/to/fastq|
|stages  |["stage1 map1 --min-seq-length 20 map2 --min-seq-length 20", "stage2 map1 --max-seq-length 20 --min-seq-length 10 --seed-length 16  map2 --max-seed-hits -1 --max-seq-length 20 --min-seq-length 10"]|

This task produces a command line like this:

```sh
tmap mapall \
stage1 map1 --min-seq-length 20 \
       map2 --min-seq-length 20 \
stage2 map1 --max-seq-length 20 --min-seq-length 10 --seed-length 16 \
       map2 --max-seed-hits -1 --max-seq-length 20 --min-seq-length 10
```

## Workflow Definition

A workflow can be thought of as a directed acyclic graph (DAG) of transformations that convert the input data to the desired outputs. Rather than explicitly specifying the sequence of operations, A WDL workflow instead describes the connections between the steps in the workflow (i.e. between the nodes in the graph). It is the responsibility of the execution engine to determine the proper ordering of the workflow steps, and to orchestrate the execution of the different steps.

A workflow is defined using the `workflow` keyword, followed by a workflow name that is unique within its WDL document, followed by any number of workflow elements within braces.

```wdl
workflow name {
  input {
    # workflow inputs are declared here
  }

  # other "private" declarations can be made here
 
  # there may be any number of (potentially nested) 
  # calls, scatter blocks, or conditional blocks
  call target { input: ... }
  scatter (i in collection) { ... }
  if (condition) { ... }

  output {
    # workflow outputs are declared here
  }

  meta {
    # workflow-level metadata can go here
  }

  parameter_meta {
    # metadata about each input/output parameter can go here
  }
}
```

Here is an example of a simple workflow that runs one task (not defined here):

```wdl
workflow wf {
  input {
    Array[File] files
    Int threshold
    Map[String, String] my_map
  }
  call analysis_job {
    input:
      search_paths = files,
      threshold = threshold,
      sex_lookup = my_map
  }
}
```

### Workflow Elements

Tasks and workflows have several elements in common. These sections have nearly the same usage in workflows as they do in tasks, so we just link to their earlier descriptions.

* [`input` section](#task-inputs)
* [Private declarations](#private-declarations)
* [`output` section](#task-outputs)
* [`meta` section](#metadata-sections)
* [`parameter_meta` section](#parameter-metadata-section)

In addition to these sections, a workflow may have any of the following elements that are specific to workflows:

* [`call`s](#call-statement) to tasks or subworkflows
* [`scatter`](#scatter) blocks, which are used to parallelize operations across collections
* [Conditional (`if`)](#conditional-if-block) blocks, which are only executed when a conditional expression evaluates to `true`

### Workflow Inputs

The workflow and [task `input` sections](#task-inputs) have identical semantics.

### Workflow Outputs

The workflow and [task `output` sections](#task-outputs) have identical semantics.

By default, if the `output {...}` section is omitted from a top-level workflow, then the workflow has no outputs. However, the execution engine may choose allow the user to specify that when the top-level output section is omitted, all outputs from all calls (including nested calls) should be returned.

If the `output {...}` section is omitted from a workflow that is called as a subworkflow, then that call must not have outputs. Formally defined outputs of subworkflows are required for the following reasons:

- To present the same interface when calling subworkflows as when calling tasks.
- To make it easy for callers of subworkflows to find out exactly what outputs the call is creating.
- In case of nested subworkflows, to give the outputs at the top level a simple fixed name rather than a long qualified name like `a.b.c.d.out` (which is liable to change if the underlying implementation of `c` changes, for example).

### Evaluation of Workflow Elements

As with tasks, workflow declarations can appear in the body of a workflow in any order. Expressions in workflows can reference the outputs of calls, including in input declarations. For example:

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

The control flow of this workflow changes depending on whether the value of `y` is provided as an input or it's initializer expression is evaluated:

* If an input value is provided for `y` then it receives that value immediately and `t2` may start running as soon as the workflow starts.
* In no input value is provided for `y` then it will need to wait for `t1` to complete before it is assigned.

### Fully Qualified Names & Namespaced Identifiers

```txt
$fully_qualified_name = $identifier ('.' $identifier)*
$namespaced_identifier = $identifier ('.' $identifier)*
```

A fully qualified name is the unique identifier of any particular call, input, or output, and has the following structure:

* For `call`s: `<parent namespace>.<call alias>`
* For inputs and outputs: `<parent namespace>.<input or output name>`
* For `Struct`s and `Object`s: `<parent namespace>.<member name>`

A [namespace](#namespaces) is a set of names, such that every name is unique within the namespace (but the same name could be used in two different namespaces). The `parent namespace` is the fully qualified name of the workflow containing the call, the workflow or task containing the input or output declaration, or the `Struct` or `Object` declaration containing the member. For the top-level workflow this is equal to the workflow name.

For example: `ns.ns2.mytask` is a fully-qualified name - `ns.ns2` is the parent namespace, and `mytask` is the task name being referred to within that namespace. Fully-qualified names are left-associative, meaning `ns.ns2.mytask` is interpreted as `((ns.ns2).mytask)`, meaning `ns.ns2` has to resolve to a namespace so that `.mytask` can be applied.

When a [call statement](#call-statement) needs to refer to a task or workflow in another namespace, then it must use the fully-qualified name of that task or workflow. When an [expression](#expressions) needs to refer to a declaration in another namespace, it must use a *namespaced identifier*, which is an identifier consisting of a fully-qualified name.

Consider this workflow:

`other.wdl`
```wdl
struct Result {
  String foo
}

task mytask {
  ...
  output {
    Result result
  }
}
```

`main.wdl`
```wdl
import "other.wdl" as ns

workflow wf {
  call ns.mytask

  output {
    String result = mytask.result.foo
  }
}
```

In this example, the call statement uses the fully-qualified name `ns.mytask` to refer to task `mytask` in namespace `ns`, which is the alias given to `other.wdl` when it is imported. We can then refer to the outputs of this call using its alias `mytask` (see the [Call Statement](#call-statement) section for details on call aliasing). `mytask.result.foo` is a namespaced identifier referring to the member `foo` of the `Struct`-typed output declaration `result` of the call `mytask`.

In the following more extensive example, all of the fully-qualified names that exist within the top-level workflow are listed exhaustively:

`other.wdl`
```wdl
task foobar {
  input {
    File infile
  }
  command <<<
    sh setup.sh ~{infile}
  >>>
  output {
    File results = stdout()
  }
  runtime {
    container: "my_image:latest"
  }
}

workflow other_workflow {
  input {
    Boolean bool
  }
  call foobar
}
```

`main.wdl`
```wdl
import "other.wdl" as other

task test {
  input {
    String my_var
  }
  command <<<
    ./script ~{my_var}
  >>>
  output {
    File results = stdout()
  }
  runtime {
    container: "my_image:latest"
  }
}

workflow wf {
  Array[String] arr = ["a", "b", "c"]
  call test
  call test as test2
  call other.foobar
  call other.other_workflow
  call other.other_workflow as other_workflow2
  output {
    test.results
    foobar.results
  }
  scatter(x in arr) {
    call test as scattered_test {
      input: my_var = x
    }
  }
}
```

The following fully-qualified names exist within `workflow wf` in main.wdl:

* `wf` - References top-level workflow
* `wf.test` - References the first call to task `test`
* `wf.test2` - References the second call to task `test` (aliased as test2)
* `wf.test.my_var` - References the `String` input of first call to task `test`
* `wf.test.results` - References the `File` output of first call to task `test`
* `wf.test2.my_var` - References the `String` input of second call to task `test`
* `wf.test2.results` - References the `File` output of second call to task `test`
* `wf.foobar.results` - References the `File` output of the call to `other.foobar`
* `wf.foobar.input` - References the `File` input of the call to `other.foobar`
* `wf.other_workflow` - References the first call to subworkflow `other.other_workflow`
* `wf.other_workflow.bool` - References the `Boolean` input of the first call to subworkflow `other.other_workflow`
* `wf.other_workflow.foobar.results` - References the `File` output of the call to `foobar` inside the first call to subworkflow `other.other_workflow`
* `wf.other_workflow.foobar.input` - References the `File` input of the call to `foobar` inside the first call to subworkflow `other.other_workflow`
* `wf.other_workflow2` - References the second call to subworkflow `other.other_workflow` (aliased as other_workflow2)
* `wf.other_workflow2.bool` - References the `Boolean` input of the second call to subworkflow `other.other_workflow`
* `wf.other_workflow2.foobar.results` - References the `File` output of the call to `foobar` inside the second call to subworkflow `other.other_workflow`
* `wf.other_workflow2.foobar.input` - References the `File` input of the call to `foobar` inside the second call to subworkflow `other.other_workflow`
* `wf.arr` - References the `Array[String]` declaration on the workflow
* `wf.scattered_test` - References the scattered version of `call test`
* `wf.scattered_test.my_var` - References an `Array[String]` for each element used as `my_var` when running the scattered version of `call test`.
* `wf.scattered_test.results` - References an `Array[File]` which are the accumulated results from scattering `call test`
* `wf.scattered_test.1.results` - References an `File` from the second invocation (0-indexed) of `call test` within the scatter block.  This particular invocation used value "b" for `my_var`

### Call Statement

A workflow calls other tasks/workflows via the `call` keyword. A `call` is followed by the name of the task or subworkflow to run. A call's target task may be defined in the current WDL document - using just the task name - or in an imported WDL - using its [fully-qualified name](#fully-qualified-names--namespaced-identifiers). Since a WDL workflow can never be in the same document as another workflow, a subworkflow must always be called in an imported WDL using its fully-qualified name.

A `call` statement must be uniquely identifiable. By default, the call's unique identifier is the task or subworkflow name (e.g. `call foo` would be referenced by name `foo`). However, if one were to `call foo` twice in a workflow, each subsequent `call` statement will need to alias itself to a unique name using the `as` clause, e.g. `call foo as bar`.

A `call` has an optional body in braces (`{}`). The only element that may appear in the call body is the `input:` keyword, followed by an optional, comma-delimited list of inputs to the call. A `call` must, at a minimum, provide values for all of the task/subworkflow's required inputs, and every input value/expression must match the type of the task/subworkflow's corresponding input parameter. If a task has no required parameters, then the call body may be empty or omitted.

```wdl
import "lib.wdl" as lib

task my_task {
  input {
    Int num
    String? opt_string
  }
  ...
}

workflow wf {
  input {
    String s
    Int i
  }

  # Calls my_task with one required input - it is okay to not
  # specify a value for my_task.opt_string since it is optional.
  call my_task { input: num = i }

  # Calls my_task a second time, this time with both inputs.
  # We need to give this one an alias to avoid name-collision.
  call my_task as my_task_alias {
    input:
      num = i,
      opt_string = s
  }

  # Calls a workflow imported from lib with no inputs.
  call lib.other_workflow
  # This call is also valid
  call lib.other_workflow as other_workflow2 {}
}
```

Note that there is no mechanism for a workflow to set a value for a nested input when calling a subworkflow. For example, the following workflow is invalid:

`sub.wdl`
```wdl
task mytask {
  input {
    Int x
  }
  ...
}

workflow sub {
  # error! missing required input
  call mytask
}
```

`main.wdl`
```wdl
workflow top {
  # error! can't specify a nested input
  call sub { input: sub.mytask.x = 5 }
}
```

If a call input has the same name as a declaration from the current scope, the name of the input may appear alone (without an expression) to implicitly bind the value of that declaration. In the following example, `{input: x, y=b, z}` is equivalent to `{input: x=x, y=b, z=z}`

```wdl
tash foo {
  input {
    Int x
    String y
    Float z
  }
  ...
}

workflow abbrev {
  input {
    Int x
    String b
    Float z
  }
  call foo { input: x, y=b, z }
}
```

Calls may be executed as soon as all their inputs are available. If `call x`'s inputs are based on `call y`'s outputs, this means that `call x` can be run as soon as `call y` has completed. 

As soon as the execution of a called task completes, the call outputs are available to be used as inputs to other calls in the workflow or as workflow outputs. Note that the only task declarations that are accessible outside of the task are its output declarations, i.e. call inputs cannot be referenced. To expose a call input, add an output to the task that simply copies the input:

```wdl
task copy_input {
  input {
    String greeting
  }
  command <<< echo "~{greeting}, nice to meet you!" >>>
  output {
    # expose the input to s as an output
    String greeting_out = greeting
    String msg = read_string(stdout())
  }
}

workflow test {
  input {
    String name
  }
  call copy_input { input: greeting = "hello ~{name}" }
  output {
    String greeting = copy_input.greeting_out
    String msg = copy_input.msg
  }
}
```

To add a dependency from x to y that isn't based on outputs, you can use the `after` keyword, such as `call x after y after z`. But note that this is only required if `x` doesn't already depend on an output from `y`.

```wdl
task my_task {
  input {
    Int input_num
  }
  ...
  output {
    Int output_num
  }
}

workflow wf {
  # Call my_task
  call my_task { input: input_num = 2 }

  # Call my_task again with the output from the first call.
  # This call will wait until my_task is finished.
  call my_task as my_task_alias {
    input: input_num = my_task.output_num
  }

  # Call my_task again. This call does not depend on the
  # output from an earlier call, but we explicitly
  # specify that this task should wait until my_task is
  # complete before executing this call.
  call my_task as my_task_alias2 after my_task {
    input: input_num = 5
  }
}
```

An input value may be any valid expression, not just a reference to another call output. For example:

```wdl
task my_task {
  input {
    File f
    Int disk_space_gb
  }

  command <<<
    python do_stuff.py ~{f}
  >>>

  output {
    File results = stdout()
  }
  
  runtime {
    container: "my_image:latest"
    disks: disk_space_gb
  }
} 

workflow wf {
  input {
    File f
  }

  call my_task {
    input:
      f = f,
      disk_space_gb = size(f, "GB")
  }
}
```

Here is a more complex example of calling a subworkflow:

`sub_wdl.wdl`
```wdl
task hello {
  input {
    String addressee
  }
  command <<<
    echo "Hello ~{addressee}!"
  >>>
  runtime {
    container: "ubuntu:latest"
  }
  output {
    String salutation = read_string(stdout())
  }
}

workflow wf_hello {
  input {
    String wf_hello_input
  }

  call hello {
    input: addressee = wf_hello_input 
  }

  output {
    String salutation = hello.salutation
  }
}
```

`main.wdl`
```wdl
import "sub_wdl.wdl" as sub

workflow main_workflow {
  call sub.wf_hello as sub_hello { 
    input: wf_hello_input = "sub world" 
  }

  output {
    String main_output = sub_hello.salutation
  }
}
```

#### Computing Call Inputs

Any required workflow inputs (i.e. those that are not initialized with a default value or expression) must have their values provided when invoking the workflow. Inputs may be specified for a workflow invocation using any mechanism supported by the execution engine, including the [standard JSON format](#json-input-format). 

By default, all calls to subworkflows and tasks must have values provided for all required inputs by the caller. However, the execution engine may allow the workflow to leave some subworkflow/task inputs undefined - to be specified by the user at runtime - by setting the `allowNestedInputs` flag to `true` in the `meta` section of the top-level workflow. For example:

```wdl
task mytask {
  input {
    String name
    File f
  }
  ...
}

workflow allows_nested_inputs {
  input {
    String s
  }
  
  meta {
    allowNestedInputs: true
  }

  # Required parameter "mytask.f" is not specified.
  # Typically this is an error, but "meta.allowNestedInputs"
  # is true so it is allowed, but the user must specify a 
  # value for "allows_nested_inputs.mytask.f" as a runtime 
  # input.
  call mytask { input: name = s }
}
```

Here is a more extensive example:

```wdl
task t1 {
  input {
    String s
    Int x
  }

  command <<<
    ./script --action=~{s} -x~{x}
  >>>

  output {
    Int count = read_int(stdout())
  }
  
  runtime {
    container: "my_image:latest"
  }
}

task t2 {
  input {
    String s
    Int? t
    Int x
  }

  command <<<
    ./script2 --action=~{s} -x~{x} ~{"--other=" + t}
  >>>

  output {
    Int count = read_int(stdout())
  }
  
  runtime {
    container: "my_image:latest"
  }
}

task t3 {
  input {
    Int y
    File ref_file # Do nothing with this
  }

  command <<<
    python -c "print(~{y} + 1)"
  >>>

  output {
    Int incr = read_int(stdout())
  }
  
  runtime {
    container: "my_image:latest"
  }
}

workflow wf {
  input {
    Int int_val
    Array[Int] my_ints
    File ref_file
    String t1s
    String t2s
  }

  meta {
    allowNestedInputs: true
  }

  String not_an_input = "hello"

  call t1 {
    input: 
        x = int_val,
        s = t1s
  }

  call t2 {
    input: 
        x = t1.count,
        s = t2s
  }

  scatter(i in my_ints) {
    call t3 {
      input: y=i, ref=ref_file
    }
  }
}
```

The inputs to `wf` will be:

* `wf.t1s` as a `String`
* `wf.t2s` as a `String`
* `wf.int_val` as an `Int`
* `wf.my_ints` as an `Array[Int]`
* `wf.ref_file` as a `File`
* `wf.t2.t` as an `Int?`

Note that the optional `t` input for task `t2` is left unsatisfied. This input can be specified at runtime as `wf.t2.t` because `allowNestedInputs` is set to `true`; if it were set to `false`, this input could not be specified at runtime. 

It is an error for the user to attempt to override a call input at runtime, even if nested inputs are allowed. For example, if the user tried to specify `allows_nested_inputs.mytask.name = "Fred"` in the input JSON, an error would be raised.

### Scatter

```txt
$scatter = 'scatter' $ws* '(' $ws* $scatter_iteration_statement $ws*  ')' $ws* $scatter_body
$scatter_iteration_statement = $identifier $ws* 'in' $ws* $expression
$scatter_body = '{' $ws* $workflow_element* $ws* '}'
```

Scatter-gather is a common parallelization pattern in computer science. Given a collection of inputs (such as an array), the "scatter" step executes a set of operations on each input in parallel. In the "gather" step, the outputs of all the individual scatter-tasks are collected into the final output.

WDL provides a mechanism for scatter-gather using the `scatter` block. A `scatter` block begins with the `scatter` keyword and has three essential pieces:

* An expression that evaluates to an `Array[X]` - the array to be scattered over.
* The scatter variable - an identifier that will hold the input value in each iteration of the scatter. The scatter variable is always of type `X`, where `X` is the item type of the `Array`.
* A body that contains any number of nested statements - declarations, calls, scatters, conditionals - that are executed for each value in the collection.

```wdl
workflow scatter_example {
  input {
    Array[String] name_array = ["Joe", "Bob", "Fred"]
    String salutation = "hello"
  }
  
  # 'name_array' is an identifier expression that evaluates
  #   to an Array of Strings.
  # 'name' is a String declaration that will have a 
  #   different value - one of the elements of name_array - 
  #   during each iteration
  scatter (name in name_array) {
    # these statements are evaluated for each different value
    # of 'name'
    String greeting = "~{salutation} ~{name}"
    call say_hello { input: greeting = greeting }
  }
}
```

In this example, the scatter body is evaluated three times - once for each value in `name_array`. On a multi-core computer, each of these evaluations might happen in a separate thread or subprocess; on a cloud platform, each of these evaluations might take place in a different virtual machine.

The scatter body is a nested scope in which `name` is accessible, along with all of the declarations and call outputs that are accessible in the enclosing scope. `name` is *not* accessible outside the scatter body - e.g. it would be an error to reference `name` in the workflow's output section. However, if there were another nested scatter, `name` would be accessible in that nested scatter's body.

```wdl
workflow scatter_example {
  input {
    Array[String] name_array = ["Joe", "Bob", "Fred"]
    Array[String] salutation_array = ["hello", "goodbye"]
  }

  scatter (name in name_array) {
    scatter (salutation in salutation_array)
      # both 'name' and 'saluation' are accessible here
      String greeting = "~{salutation} ~{name}"
    }
  }

  output {
    String scatter_name = name  # error! 'name' not accessible here
  }
}
```

Calls within the scatter body are able to depend on each other and reference each others' outputs. In the following example, `task2` depends on `task1`.

```wdl
scatter (i in integers) {
  call task1 { input: num=i }
  call task2 { input: num=task1.output }
}
```

After a scatter block is fully evaluated, *all* of the declarations and call outputs in the scatter body (except for the scatter variable) are "exported" to the enclosing context. However, because a scatter block represents an array of evaluations, the type of each exported declaration or call output is implicitly `Array[X]`, where `X` is the type of the declaration or call output within the scatter body. The ordering of the exported array(s) is guaranteed to match the ordering of the input array.

For example:

```wdl
task say_hello {
  input {
    String salutation
    String name
  }
  command <<< >>>
  output {
    String greeting = "~{salutation} ~{name}"
  }
}

workflow scope_example {
  input {
    Array[String] hobbit_array = ["Bilbo", "Frodo", "Merry"]
  }

  Array[Int] counter = range(length(hobbit_array))
  
  # the zip() function generates an array of pairs
  scatter (name_and_index in zip(hobbit_array, counter)) {
    # use a different saluation for even and odd items in the array
    String salutation = if name_and_index.right % 2 == 0 then "hello" else "g'day"
    
    call say_hello { 
      input:
        salutation = salutation,
        name = name_and_index.left
    }

    # within the scatter body, when we access the output of the
    # say_hello call, we get a String
    String greeting = say_hello.greeting
  }

  # Outside of the scatter body, we can access all of the names that
  # are inside the scatter body, but the types are now all Arrays.
  # Each of these outputs will be an array of length 3 (the same
  # length as 'hobbit_array').
  output {
    # the value of this Array is guaranteed to be: 
    # ["hello", "g'day", "hello"]
    Array[String] salutations = salutation

    # the value of this Array is guaranteed to be:
    # ["hello Bilbo", "g'day Frodo", "hello Merry"]
    Array[String] greetings = say_hello.greeting
  }
}
```

If scatter blocks are nested to multiple levels, the output types are also nested to the same number of levels. For example:

```wdl
workflow multi_level {
  scatter (i in [1, 2, 3]) {
    scatter (j in ["a", "b", "c"]) {
      String msg = "~{i} ~{j}"
    }
    # directly outside the scatter containing msg,
    # msg's type is an Array
    Array[String] msg_level_1 = msg
  }

  # here we are two levels of nesting away from msg, so
  # its type is an Array that is two levels deep
  Array[Array[String]] msg_level_2a = msg

  # these two arrays are identical
  Array[Array[String]] msg_level_2b = msg_level_1
}
```

### Conditional (`if` block)

```txt
$conditional = 'if' '(' $expression ')' '{' $workflow_element* '}'
```

A conditional block consists of the `if` keyword, followed by a `Boolean` expression and a body of nested statements. The conditional body is only evaluated if the conditional expression evaluates to `true`.

```wdl
workflow cond_test {
  input {
    Boolean b = false
  }
  
  # this block is not evaluated since 'b' is false
  if (b) {
    call say_hello
  }
  # this block is not evaluated since !b is true
  if (!b) {
    call say_goodbye
  }
}
```

The scoping rules for conditionals are similar to those for scatters. Any declarations or call outputs inside a conditional body are accessible within that conditional and any nested scatter or conditional blocks. After a conditional block has been evaluated, its declarations and call outputs are "exported" to the enclosing scope. However, because the statements within a conditional block may or may not be evaluated during any given execution of the workflow, the type of each exported declarations or call output is implicitly `X?`, where `X` is the type of the declaration or call output within the conditional body.

Note that, even though a conditional body is only evaluated if its conditional expression evaluates to `true`, all of the potential declarations and call outputs in the conditional body are always exported, regardless of the value of the conditional expression. In the case that the conditional expression evaluates to `false`, all of the exported declarations and call outputs are undefined (i.e. have a value of `None`).

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

  # Outside the if block, 'y' has an optional type:
  Int? y_out_maybe = y.out

  # Call 'z' which takes an optional Int input:
  call z { input: optional_int = y_out_maybe }
}
```

Also note that it is impossible to have a multi-level optional type, e.g. `Int??`; thus, the outputs of a conditional block are only ever single-level optionals, even when there are nested conditionals.

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

  # Even though it's within a nested conditional, x_out
  # has a type of Int? rather than Int??
  Int? x_out_maybe = x_out 

  # Call 'y' which takes an Int input.
  # The select_first produces an Int, not an Int?
  call y { input: int_input = select_first([x_out_maybe, 5]) } 
}
```

Remember that optional types can be coalesced by using the `select_all` and `select_first` functions. For example:

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

  # Because it was declared inside the scatter and the if-block, 
  # the type of x_out is different here:
  Array[Int?] x_out_maybes = x_out

  # We can select only the valid elements with select_all:
  Array[Int] x_out_valids = select_all(x_out_maybes)

  # Or we can select the first valid element:
  Int x_out_first = select_first(x_out_maybes)
}
```

## Struct Definition

A `Struct` type is a user-defined data type. Structs enable the creation of compound data types that bundle together related attributes in a more natural way than is possible using the general-purpose compound types like `Pair` or `Map`. Once defined, a `Struct` type can be used as the type of a declaration like any other data type.

A `struct` definition is a top-level WDL element, meaning it is defined at the same level as tasks and workflows, and it cannot be defined within a task or workflow body. A struct is defined using the `struct` keyword, followed by a name that is unique within the WDL document, and a body containing a set of member declarations. Declarations in a `struct` body differ from those in a `task` or `workflow` in that `struct` members cannot have default initializers. `Struct` members may be optional.

Valid `struct`:
```wdl
struct Person {
  String first_name
  String last_name
  Int age
  Float? income
}
```

Invalid `struct`:
```wdl
struct Invalid {
  String myString = "Cannot do this"
  Int myInt
}
```

A `struct` member may be of any type, including compound types and even other `Struct` types.

```wdl
struct Sample {
  String id
  Person donor
  Map[String, Array[File]] assay_data
}
```

### Struct Literals

A struct literal is an instance of a specific `Struct` type that provides values for all of the non-optional members and any of the optional members. The members of a struct literal are validated against the `Struct`'s definition at the time of creation. Members do not need to be specified in any specific order. Once a struct literal is created, it is immutable like any other WDL value.

A struct literal begins with the name of the `Struct` type, followed by name-value pairs for each of the members within braces.

```wdl
struct BankAccount {
  String account_number
  Int routing_number
  Float balance
  Array[Int]+ pin_digits
  String? username
}

task {
  input {
    # it's okay to leave out username since it's optional
    BankAccount account1 = BankAccount {
      account_number: "123456",
      routing_number: 300211325,
      balance: 3.50,
      pin_digits: [1, 2, 3, 4]
    }

    # error! missing required account_number
    BankAccount account2 = BankAccount {
      routing_number: 611325474,
      balance: 9.99,
      pin_digits: [5, 5, 5, 5]
    }

    # error! pin_digits is empty
    BankAccount account3 = BankAccount {
      account_number: "FATCAT42",
      routing_number: 880521345,
      balance: 50.01,
      pin_digits: []
    }
  }
}
```

🗑 It is also possible to assign an `Object` or `Map[String, X]` value to a `Struct` declaration. In the either case:
* The `Object`/`Map` must not have any members that are not declared for the struct.
* The value of each object/map member must be coercible to the declared type of the struct member.
* The `Object`/`Map` must at least contain values for all of the struct's non-optional members.

Note that the ability to assign non-`Struct` values to `Struct` declarations is deprecated and will be removed in WDL 2.0.

### Struct Namespacing

Although a `struct` is a top-level element, it is not considered a member of the WDL document's namespace the way that other top-level elements (`task`s and `workflow`s) are. Instead, when a WDL document is imported all of its `structs` are added to a global struct namespace. This enables structs to be used by their name alone, without the need for any `namespace.` prefix.

`structs.wdl`
```wdl
struct Foo {
  String s
  Int i
}
```

`main.wdl`
```wdl
import "structs.wdl"

task test {
  input {
    # here we can use type 'Foo' rather than 'structs.Foo'
    Foo f = Foo { s: "hello", i: 42 }
  }
}
```

It is valid to import the same `Struct` into the global namespace multiple times via different paths; however, if two `Struct`s with the same name but different members are imported into the global namespace there is a name collision resulting in an error. This means that care must be taken not to give identical names to two different `Struct`s that might be imported into the same WDL document tree. Alternatively, `Struct`s can be aliased at import time.

For example, if the current WDL defines a `struct Experiment` and an imported WDL defines a different `struct Experiment`, it can be aliased as follows:

```wdl
import "http://example.com/example.wdl" as ex alias Experiment as OtherExperiment
```

In order to resolve multiple `Struct`s, simply add additional alias statements:

```wdl
import "http://example.com/another_exampl.wdl" as ex2
  alias Parent as Parent2
  alias Child as Child2
  alias GrandChild as GrandChild2
```

A `Struct` can always be aliased even if its name does not conflict with another `Struct` in the global namespace. When a `Struct` is imported with an alias, it is added to the global namespace only under that alias. If aliases are used for some `Struct`s in an imported WDL but not others, the unaliased `Struct`s are still imported into the global namespace under their original names.

### Struct Usage

A `Struct`s members are [accessed](#member-access) using a `.` to separate the identifier from the member name. For example:

```wdl
struct Wizard {
  String name
  Int age
}

task my_task {
  input {
    Wizard w
  }

  command <<<
    echo "hello my name is ~{w.name} and I am ~{w.age} years old"
  >>>

  output {
    String wizard_name = "~{w.name} Potter"
    Int age_in_muggle_years = w.age * 2
  }
    
  runtime {
    container: "my_image:latest"
  }
}

workflow my_workflow {
  Wizard harry = Wizard { name: "Harry", age: 11 }
  
  call myTask { input: a = harry }
}
```

Access to elements of compound members can be chained into a single expression. For example:

```wdl
struct Experiment {
  Array[File] experimentFiles
  Map[String, String] experimentData
}
```

**Example 1:** Accessing the nth element of experimentFiles and any element in experimentData:

```wdl
workflow workflow_a {
  input {
    Experiment myExperiment
  }
  File firstFile = myExperiment.experimentFiles[0]
  String experimentName = myExperiment.experimentData["name"]
}
```

**Example 2:** The struct is an item in an Array:

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

# Standard Library

The following functions are available to be called in WDL expressions. The signature of each function is given as `R func_name(T1, T2, ...)`, where `R` is the return type and `T1`, `T2`, ... are the parameter types. All function parameters must be specified in order, and all function parameters are required, with the exception that the last parameter of some functions is optional (denoted by the type in brackets `[]`).

A function is called using the following syntax: `R' val = func_name(arg1, arg2, ...)`, where `R'` is a type that is coercible from `R`, and `arg1`, `arg2`, ... are expressions whose types are coercible to `T1`, `T2`, ...

Some functions accept arguments of multiple different types, denoted as a list of types separated by `|`.

Some functions are polymorphic, which means that they are actually multiple functions with the same name but different signatures. Such functions are defined with generic types (e.g. `X`, `Y`) instead of concrete types (e.g. `File` or `String`), and the bounds of each type parameter is specified in the function description.

Functions that are new in this version of the specification are denoted by ✨, and deprecated functions are denoted by 🗑.

## Int floor(Float), Int ceil(Float) and Int round(Float)

These functions convert a `Float` to an `Int` using different rounding methods:

- `floor`: Rounds **down** to the next lower integer.
- `ceil`: Rounds **up** to the next higher integer.
- `round`: Rounds to the nearest integer based on standard rounding rules ("round half up").

**Parameters**:

1. `Float`: the number to round.

**Returns**: An integer.

**Example**

```wdl
# all these expressions evaluate to true
Boolean all_true = [
  floor(1.0) == 1,
  floor(1.9) == 1,
  ceil(2.0) == 2,
  ceil(2.1) == 3,
  round(1.49) == 1,
  round(1.50) == 2
]
```

## ✨ Int min(Int, Int), Float min(Float, Float), Float min(Int, Float), Float min(Float, Int)

Returns the smaller of two values. If both values are `Int`s, the return value is an `Int`, otherwise it is a `Float`.

**Parameters**:

1. `Int|Float`: the first number to compare.
2. `Int|Float`: the second number to compare.

**Returns**: The smaller of the two arguments.

**Example**

```wdl
workflow min_test {
  input {
    Int value1
    Float value2
  }
  output {
    # these two expressions are equivalent
    Float min1 = if value1 < value2 then value1 else value2
    Float min2 = min(value1, value2)
  }
}
``` 

## ✨ Int max(Int, Int), Float max(Float, Float), Float max(Int, Float), Float max(Float, Int)

Returns the larger of two values. If both values are `Int`s, the return value is an `Int`, otherwise it is a `Float`.

**Parameters**:

1. `Int|Float`: the first number to compare.
2. `Int|Float`: the second number to compare.

**Returns**: The larger of the two arguments.

**Example**

```wdl
workflow max_test {
  input {
    Int value1
    Float value2
  }
  output {
    # these two expressions are equivalent
    Float max1 = if value1 > value2 then value1 else value2
    Float max2 = max(value1, value2)
  }
}
``` 

## String sub(String, String, String)

Given 3 String parameters `input`, `pattern`, `replace`, this function replaces all non-overlapping occurrences of `pattern` in `input` by `replace`. `pattern` is a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) that will be evaluated as a [POSIX Extended Regular Expression (ERE)](https://en.wikipedia.org/wiki/Regular_expression#POSIX_basic_and_extended).

Note that regular expressions are written using regular WDL strings, so backslash characters need to be double-escaped. For example:

```wdl
String s1 = "hello\tBob"
String s2 = sub(s1, "\\t", " ")
```

🗑 The option for execution engines to allow other regular expression grammars besides POSIX ERE is deprecated.

**Parameters**:

1. `String`: the input string.
2. `String`: the pattern to search for.
3. `String`: the replacement string.

**Returns**: the input string, with all occurrences of the pattern replaced by the replacement string.

**Example**

```wdl
String chocolike = "I like chocolate when it's late"

String chocolove = sub(chocolike, "like", "love") # I love chocolate when it's late
String chocoearly = sub(chocolike, "late", "early") # I like chocoearly when it's early
String chocolate = sub(chocolike, "late$", "early") # I like chocolate when it's early
String chocoearlylate = sub(chocolike, "[^ ]late", "early") # I like chocearly when it's late
String choco4 = sub(chocolike, " [:alpha:]{4} ", " 4444 ") # I 4444 chocolate 4444 it's late
```

Any arguments are allowed so long as they can be coerced to `String`s. For example, this can be useful to swap the extension of a filename:

```wdl
task example {
  input {
    File input_file = "my_input_file.bam"
    # the value of output_file_name is "my_input_file.index"
    String output_file_name = sub(input_file, "\\.bam$", ".index")
  }

  command <<<
    echo "I want an index instead" > ~{output_file_name}
  >>>

  output {
    File outputFile = output_file_name
  }
  
  runtime {
    container: "my_image:latest"
  }
}
```

## File stdout()

Returns the value of the executed command's standard output (stdout) as a `File`. The file should be given a random name and written in a temporary directory, so as not to conflict with any other task output files.

**Parameters**: None

**Returns**: A `File` reference to the stdout generated by the command of the task where the function is called.

**Restrictions**: Can only be used within the `output` section of a `task`.

**Example**

This task echos a message to standard out, and then returns a `File` containing that message.

```wdl
task echo {
  command <<< echo "hello world" >>>
  output {
    File message = stdout()
  }
}
```

## File stderr()

Returns the value of the executed command's standard error (stderr) as a `File`. The file should be given a random name and written in a temporary directory, so as not to conflict with any other task output files.

**Parameters**: None

**Returns**: A `File` reference to the stderr generated by the command of the task where the function is called.

**Restrictions**: Can only be used within the `output` section of a `task`.

**Example**

This task echos a message to standard error, and then returns a `File` containing that message.

```wdl
task echo {
  command <<< >&2 echo "hello world" >>>
  output {
    File message = stderr()
  }
}
```

## Array[File] glob(String)

Returns the Bash expansion of the [glob string](https://en.wikipedia.org/wiki/Glob_(programming)) relative to the task's execution directory, and in the same order.

`glob` finds all of the files (but not the directories) in the same order as would be matched by running `echo <glob>` in Bash from the task's execution directory.

At least in standard Bash, glob expressions are not evaluated recursively, i.e. files in nested directories are not included. 

**Parameters**:

1. `String`: The glob string.

**Returns**: A array of all files matched by the glob.

**Restrictions**: Can only be used within a `task`.

**Example**

```wdl
task gen_files {
  command <<<
    ./generate_files --num 4 --prefix "a"
  >>>

  output {
    Array[File] a_files = glob("a*")
  }
}
```

This command generates the following directory structure:

```txt
execution_directory
├── a1.txt
├── ab.txt
├── a_dir
│   ├── a_inner.txt
├── az.txt
```

Running `echo a*` in the execution directory would expand to `a1.txt`, `ab.txt`, `a_dir` and `az.txt`, in that order. Since `glob` ignores directories, `a_dir` is discarded and the result of the expression is `["a1.txt", "ab.txt", "az.txt"]`.

### Non-standard Bash

The runtime container may use a non-standard Bash shell that supports more complex glob strings, such as allowing expansions that include `a_inner.txt` in the example above. To ensure that a WDL is portable when using `glob`, a container image should be provided and the WDL author should remember that `glob` results depend on coordination with the Bash implementation provided in that container.

## String basename(String|File, [String])

Returns the "basename" of a file - the name after the last directory separator in the file's path. 

The optional second parameter specifies a literal suffix to remove from the file name.

**Parameters**

1. (`String`|`File`): Path of the file to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.
2. `[String]`: Suffix to remove from the file name.
 
**Returns**: The file's basename as a `String`.

**Example**

```wdl
Boolean is_true1 = basename("/path/to/file.txt") == "file.txt"`
Boolean is_true2 = basename("/path/to/file.txt", ".txt") == "file"
```

## Array[String] read_lines(String|File)

Reads each line of a file as a `String`, and returns all lines in the file as an `Array[String]`. Line endings (`\r` and `\n`) are removed from every line.

The order of the lines in the returned `Array[String]` must be the order in which the lines appear in the file.

If the entire contents of the file can not be read for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation-imposed file size limits.

**Parameters**

1. `String|File`: Path of the file to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.

**Returns**: An `Array[String]` representation of the lines in the file.

**Example**

This task `grep`s through a file and returns all strings that match the given pattern:

```wdl
task do_stuff {
  input {
    String pattern
    File file
  }

  command <<<
    grep '~{pattern}' ~{file}
  >>>

  output {
    Array[String] matches = read_lines(stdout())
  }
  
  runtime {
    container: "my_image:latest"
  }
}
```

## Array[Array[String]] read_tsv(String|File)

Reads a tab-separated value (TSV) file as an `Array[Array[String]]` representing a table of values. Line endings (`\r` and `\n`) are removed from every line.

There is no requirement that the rows of the table are all the same length.

If the entire contents of the file can not be read for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation-imposed file size limits.

**Parameters**

1. `String|File`: Path of the TSV file to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.

**Returns**: An `Array` of rows in the TSV file, where each row is an `Array[String]` of fields.

**Example**

The following task has a command that outputs a TSV file to `./results/file_list.tsv`. The output file is read and returned as a table.

```wdl
task do_stuff {
  input {
    File file
  }
  command <<<
    python do_stuff.py ~{file}
  >>>
  output {
    Array[Array[String]] output_table = read_tsv("./results/file_list.tsv")
  }
}
```

## Map[String, String] read_map(String|File)

Reads a tab-separated value (TSV) file representing a set of pairs. Every row must have exactly two columns, i.e. `col1\tcol2`. Line endings (`\r` and `\n`) are removed from every line.

Each pair is added to a `Map[String, String]` in order. The values in the first column must be unique; if there are any duplicate keys, an error is raised.

If the entire contents of the file can not be read for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation-imposed file size limits.

**Parameters**

1. `String|File`: Path of the two-column TSV file to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.

**Returns**: A `Map[String, String]`, with one element for each unique key in the TSV file.

**Example**

This task executes a command that writes a two-column TSV to standard out, and then reads that file into a `Map[String, String]`:

```wdl
task do_stuff {
  input {
    String flags
    File file
  }
  command <<<
    ./script --flags=~{flags} ~{file}
  >>>
  output {
    Map[String, String] mapping = read_map(stdout())
  }
}
```

## 🗑 Object read_object(String|File)

Reads a tab-separated value (TSV) file representing the names and values of the members of an `Object`. There must be two rows, and each row must have the same number of elements. Line endings (`\r` and `\n`) are removed from every line.

The first row specifies the object member names. The names in the first row must be unique; if there are any duplicate names, an error is raised.

The second row specifies the object member values corresponding to the names in the first row. All of the `Object`'s values are of type `String`.

If the entire contents of the file can not be read for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation-imposed file size limits.

**Parameters**

1. `String|File`: Path of the two-row TSV file to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.

**Returns**: An `Object`, with as many members as there are unique names in the TSV.

**Example**

This task writes a TSV file to standard out, then reads it into an `Object`.

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

The command outputs the following lines to stdout:

```
key_1\tkey_2\tkey_3
value_1\tvalue_2\tvalue_3
```

Which are read into an `Object` with the following members:

|Attribute|Value|
|---------|-----|
|key_1    |"value_1"|
|key_2    |"value_2"|
|key_3    |"value_3"|

## 🗑 Array[Object] read_objects(String|File)

Reads a tab-separated value (TSV) file representing the names and values of the members of any number of `Object`s. Line endings (`\r` and `\n`) are removed from every line.

There must be a header row with the names of the object members. The names in the first row must be unique; if there are any duplicate names, an error is raised.

There are any number of additional rows, where each additional row contains the values of an object corresponding to the member names. Every row in the file must have the same number of elements. All of the `Object`'s values are of type `String`.

If the entire contents of the file can not be read for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation-imposed file size limits.

**Parameters**

1. `String|File`: Path of the TSV file to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.

**Returns**: An `Array[Object]`, with N-1 elements, where N is the number of rows in the file.

**Example**

This task writes a TSV file to standard out, then reads it into an `Array[Object]`.

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

The command outputs the following lines to stdout:

```
key_1\tkey_2\tkey_3
value_1\tvalue_2\tvalue_3
value_1\tvalue_2\tvalue_3
value_1\tvalue_2\tvalue_3
```

Which are read into an `Array[Object]` with the following elements:

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

## R read_json(String|File)

Reads a JSON file into a WDL value whose type depends on the file's contents. The mapping of JSON type to WDL type is:

|JSON Type|WDL Type|
|---------|--------|
|object|`Object`|
|array|`Array[X]`|
|number|`Int` or `Float`|
|string|`String`|
|boolean|`Boolean`|
|null|`None`|

The return value must be used in a context where it can be coerced to the expected type, or an error is raised. For example, if the JSON file contains `null`, then the return type will be `None`, meaning the value can only be used in a context where an optional type is expected.

If the JSON file contains an array, then all the elements of the array must be of the same type or an error is raised.

Note that the `read_json` function doesn't have access to any WDL type information, so it cannot return an instance of a specific `Struct` type. Instead, it returns a generic `Object` value that must be coerced to the desired `Struct` type. For example:

`person.json`
```json
{
  "name": "John",
  "age": 42
}
```

```wdl
struct Person {
  String name
  Int age
}
File json_file = "person.json"
Person p = read_json(json_file)
```

If the entire contents of the file can not be read for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation-imposed file size limits.

**Parameters**

1. `String|File`: Path of the JSON file to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.

**Returns**: An value whose type is dependent on the contents of the JSON file.

**Example**

This task writes a JSON object to `./results/file_list.json` and then reads it into an `Object`, which is immediately coerced to a `Map[String, String]`.

```wdl
task do_stuff {
  input {
    File file
  }
  
  command <<<
    python do_stuff.py ~{file}
  >>>

  output {
    Map[String, String] output_table = read_json("./results/file_list.json")
  }
  
  runtime {
    container: "my_image:latest"
  }
}
```

## String read_string(String|File)

Reads an entire file as a string, with any trailing end-of-line characters (`\r` and `\n`) stripped off. If the file is empty, an empty string is returned.

Note that if the file contains any internal newline characters, they are left intact. For example:

```wdl
# this file will contain "this\nfile\nhas\nfive\nlines\n"
File f = write_lines(["this", "file", "has", "file", "lines"])

# s will contain "this\nfile\nhas\nfive\nlines"
String s = read_string(f)
```

If the entire contents of the file can not be read for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation-imposed file size limits.

**Parameters**

1. `String|File`: Path of the file to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.

**Returns**: A `String`.

## Int read_int(String|File)

Reads a file that contains a single line containing only an integer and (optional) whitespace. If the line contains a valid integer, that value is returned as an `Int`, otherwise an error is raised.

If the entire contents of the file can not be read for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation-imposed file size limits.

**Parameters**

1. `String|File`: Path of the file to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.

**Returns**: An `Int`.

## Float read_float(String|File)

Reads a file that contains a single line containing only an numeric value and (optional) whitespace. If the line contains a valid floating point number, that value is returned as a `Float`, otherwise an error is raised.

If the entire contents of the file can not be read for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation-imposed file size limits.

**Parameters**

1. `String|File`: Path of the file to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.

**Returns**: A `Float`.

## Boolean read_boolean(String|File)

Reads a file that contains a single line containing only an boolean value and (optional) whitespace. If the line contains "true" or "false", that value is returned as a `Boolean`, otherwise an error is raised.

If the entire contents of the file can not be read for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation-imposed file size limits.

**Parameters**

1. `String|File`: Path of the file to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.

**Returns**: A `Boolean`.

## File write_lines(Array[String])

Writes a file with one line for each element in a `Array[String]`. All lines are terminated by the newline (`\n`) character (following the [POSIX standard](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_206)). If the `Array` is empty, an empty file is written.

The generated file should be given a random name and written in a temporary directory, so as not to conflict with any other task output files.

If the entire contents of the file can not be written for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, insufficient disk space to write the file.

**Parameters**

1. `Array[String]`: Array of strings to write.

**Returns**: A `File`.

**Example**

This task writes an array of strings to a file, and then calls a script with that file as input.

```wdl
task example {
  input {
    Array[String] array = ["first", "second", "third"]
  }

  command <<<
    ./script --file-list=~{write_lines(array)}
  >>>
  
  runtime {
    container: "my_image:latest"
  }
}
```

The actual command line might look like:

```sh
./script --file-list=/local/fs/tmp/array.txt
```

And `/local/fs/tmp/array.txt` would contain:

`first\nsecond\nthird`

## File write_tsv(Array[Array[String]])

Writes a tab-separated value (TSV) file with one line for each element in a `Array[Array[String]]`. Each element is concatenated into a single tab-delimited string. All lines are terminated by the newline (`\n`) character. If the `Array` is empty, an empty file is written.

The generated file should be given a random name and written in a temporary directory, so as not to conflict with any other task output files.

If the entire contents of the file can not be written for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, insufficient disk space to write the file.

**Parameters**

1. `Array[Array[String]]`: An array of rows, where each row is an array of column values.

**Returns**: A `File`.

**Example**

This task writes a TSV file with two lines, and three columns in each line. It then calls a script using that file as input.

```wdl
task example {
  input {
    Array[Array[String]] array = [["one", "two", "three"], ["un", "deux", "trois"]]
  }

  command <<<
    ./script --tsv=~{write_tsv(array)}
  >>>
  
  runtime {
    container: "my_image:latest"
  }
}
```

The actual command line might look like:

```sh
./script --tsv=/local/fs/tmp/array.tsv
```

And `/local/fs/tmp/array.tsv` would contain:

```txt
one\ttwo\tthree
un\tdeux\ttrois
```

## File write_map(Map[String, String])

Writes a tab-separated value (TSV) file with one line for each element in a `Map[String, String]`. Each element is concatenated into a single tab-delimited string of the format `~{key}\t~{value}`. All lines are terminated by the newline (`\n`) character. If the `Map` is empty, an empty file is written.

Since `Map`s are ordered, the order of the lines in the file is guaranteed to be the same order that the elements were added to the `Map`.

The generated file should be given a random name and written in a temporary directory, so as not to conflict with any other task output files.

If the entire contents of the file can not be written for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, insufficient disk space to write the file.

**Parameters**

1. `Map[String, String]`: An `Map`, where each element will be a row in the generated file.

**Returns**: A `File`.

**Example**

This task writes a `Map[String, String]` to a file, and then calls a script with that file as input.

```wdl
task example {
  input {
    Map[String, String] map = {"key1": "value1", "key2": "value2"}
  }

  command <<<
    ./script --map=~{write_map(map)}
  >>>
  
  runtime {
    container: "my_image:latest"
  }
}
```

The actual command line might look like:

```sh
./script --tsv=/local/fs/tmp/map.tsv
```

And `/local/fs/tmp/map.tsv` would contain:

```txt
key1\tvalue1
key2\tvalue2
```

## 🗑 File write_object(Object)

Writes a tab-separated value (TSV) file with the contents of an `Object`. The file contains two tab-delimited lines. The first line is the names of the `Object` members, and the second line is the corresponding values. All lines are terminated by the newline (`\n`) character. The ordering of the columns is unspecified.

The `Object` values must be serializable to strings, meaning that only primitive types are supported. Attempting to write an `Object` that has a compound member value results in an error.

The generated file should be given a random name and written in a temporary directory, so as not to conflict with any other task output files.

If the entire contents of the file can not be written for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, insufficient disk space to write the file.

**Parameters**

1. `Object`: An object to write.

**Returns**: A `File`.

**Example**

This task writes an `Object` to a file, and then calls a script with that file as input.

```wdl
task test {
  input {
    Object obj
  }
  command <<<
    /bin/do_work --obj=~{write_object(obj)}
  >>>
  output {
    File results = stdout()
  }
}
```

The actual command line might look like:

```
/bin/do_work --obj=/path/to/input.tsv
```

If `obj` has the following members:

|Attribute|Value|
|---------|-----|
|key_1    |"value_1"|
|key_2    |"value_2"|
|key_3    |"value_3"|

Then `/path/to/input.tsv` will contain:

```
key_1\tkey_2\tkey_3
value_1\tvalue_2\tvalue_3
```

## 🗑 File write_objects(Array[Object])

Writes a tab-separated value (TSV) file with the contents of a `Array[Object]`. All `Object`s in the `Array` must have the same member names, or an error is raised.

The file contains N+1 tab-delimited lines terminated by a newline (`\n`), where N is the number of elements in the `Array`. The first line is the names of the `Object` members, and the subsequent lines are the corresponding values for each `Object`. All lines are terminated by the newline (`\n`) character. The lines are written in the same order as the `Object`s in the `Array`. The ordering of the columns is unspecified. If the `Array` is empty, an empty file is written.

The object values must be serializable to strings, meaning that only primitive types are supported. Attempting to write an `Object` that has a compound member value results in an error.

The generated file should be given a random name and written in a temporary directory, so as not to conflict with any other task output files.

If the entire contents of the file can not be written for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, insufficient disk space to write the file.

**Parameters**

1. `Array[Object]`: An array of objects to write.

**Returns**: A `File`.

**Example**

This task writes an array of objects to a file, and then calls a script with that file as input.

```wdl
task test {
  input {
    Array[Object] obj_array
  }
  command <<<
    /bin/do_work --obj=~{write_objects(obj_array)}
  >>>
  output {
    File results = stdout()
  }
}
```

The actual command line might look like:

```
/bin/do_work --obj=/path/to/input.tsv
```

If `obj_array` has the items:

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


The `/path/to/input.tsv` will contain:

```
key_1\tkey_2\tkey_3
value_1\tvalue_2\tvalue_3
value_4\tvalue_5\tvalue_6
value_7\tvalue_8\tvalue_9
```

## File write_json(X)

Writes a JSON file with the serialized form of a WDL value. The following WDL types can be serialized:

|WDL Type|JSON Type|
|--------|--------|
|`Struct`        |object |
|`Object`        |object |
|`Map[String, X]`|object |
|`Array[X]`      |array  |
|`Int`           |number |
|`Float`         |number |
|`String`        |string |
|`File`          |string |
|`Boolean`       |boolean|
|`None`          |null   |

When serializing compound types, all nested types must be serializable or an error is raised. For example the following value could not be written to JSON:

```wdl
Pair[Int, Map[Int, String]] x = (1, {2: "hello"})
# this fails with an error - Map with Int keys is not serializable
File f = write_json(x)  
```

**Parameters**

1. `X`: A WDL value of a supported type.

**Returns**: A `File`.

**Example**

This task writes a `Map[String, String]` to a JSON file, then calls a script with that file as input.

```wdl
task example {
  input {
    Map[String, String] map = {"key1": "value1", "key2": "value2"}
  }

  command <<<
    ./script --map=~{write_json(map)}
  >>>
  
  runtime {
    container: "my_image:latest"
  }
}
```

The actual command line might look like:

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

## Float size(File?|Array[File?], [String])

Determines the size of a file, or the sum total sizes of an array of files. By default, the size is returned in bytes unless the optional second argument is specified with a [unit](#units-of-storage).

There are four supported types for the first parameter:
- `File`: Returns the size of the file.
- `File?`: Returns the size of the file if it is defined, or 0.0 otherwise.
- `Array[File]`: Returns the sum of sizes of the files in the array, or 0.0 if the array is empty.
- `Array[File?]`: Returns the sum of sizes of all defined files in the array, or 0.0 if the array contains no defined files.

If the size can not be represented in the specified unit because the resulting value is too large to fit in a `Float`, an error is raised. It is recommended to use a unit that will always be large enough to handle any expected inputs without numerical overflow.

**Parameters**

1. `File|File?|Array[File]|Array[File?]`: A file, or array of files, for which to determine the size.
2. `[String]` The unit of storage; defaults to 'B'.

**Returns**: The size of the file(s) as a `Float`.

**Example**

```wdl
task example {
  input {
    Array[File] input_files
  }

  command <<<
    echo "this file is 22 bytes" > created_file
  >>>

  output {
    Float input_files_gb = size(input_files, "GB")
    Float created_file_bytes = size("created_file") # 22.0
    Float created_file_kb = size("created_file", "K") # 0.022
  }
  
  runtime {
    container: "my_image:latest"
  }
}
```

## Int length(Array[X])

Returns the number of elements in an array as an `Int`.

**Parameters**

1. `Array[X]`: An array with any element type.

**Returns**: The length of the array as an `Int`.

**Example**

```wdl
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b", "c" ]
Array[String] zs = [ ]

Int xlen = length(xs) # 3
Int ylen = length(ys) # 3
Int zlen = length(zs) # 0
```

## Array[Int] range(Int)

Creates an array of the given length containing sequential integers starting from 0.

**Parameters**

1. `Int`: The length of array to create.

**Returns**: An `Array[Int]` containing integers `0..(N-1)`.

**Example**

```wdl
workflow wf {
  input {
    Int i
  }
  Array[Int] indexes = range(i)
  scatter (idx in indexes) {
    call do_stuff { input: n = idx }
  }
}
```

## Array[Array[X]] transpose(Array[Array[X]])

Transposes a two-dimensional array according to the standard matrix transposition rules, i.e. each row of the input array becomes a column of the output array. The input array must be square - i.e. every row must have the same number of elements - or an error is raised.

**Parameters**

1. `Array[Array[X]]`: A `M*N` two-dimensional array.

**Returns**: A `N*M` two-dimensional array (`Array[Array[X]]`) containing the transposed input array.

**Example**

```wdl
# input array is 2 rows * 3 columns
Array[Array[Int]] input_array = [[0, 1, 2], [3, 4, 5]]

# output array is 3 rows * 2 columns
Array[Array[Int]] expected_output_array = [[0, 3], [1, 4], [2, 5]]

Boolean is_true = transpose(input_array) == expected_output_array
``` 

## Array[Pair[X,Y]] zip(Array[X], Array[Y])

Creates an array of `Pair`s containing the [dot product](https://en.wikipedia.org/wiki/Dot_product) of two input arrays, i.e. the elements at the same indices in each array `Xi` and `Yi` are combined together into (`Xi`, `Yi`) for each `i` in `range(length(array))`. The input arrays must have the same lengths or an error is raised.

**Parameters**

1. `Array[X]`: The first array of length `M`.
2. `Array[Y]`: The second array of length `N`.

**Returns**: An `Array[Pair[X, Y]]` of length `N`.

**Example**

```wdl
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b", "c" ]
Array[String] zs = [ "d", "e" ]

Array[Pair[Int, String]] zipped = zip(xs, ys) 
Boolean is_true = zipped == [ (1, "a"), (2, "b"), (3, "c") ]

# this fails with an error - xs and zs are not the same length
Array[Pair[Int, String]] bad = zip(xs, zs)
```

## ✨ Pair[Array[X], Array[Y]] unzip(Array[Pair[X, Y]])

Creates a `Pair` of `Arrays`, the first containing the elements from the `left` members of an `Array` of `Pair`s, and the second containing the `right` members. This is the inverse of the `zip` function.

**Parameters**

1. `Array[Pair[X, Y]]`: The `Array` of `Pair`s of length `N` to unzip.

**Returns**: A `Pair[Array[X], Array[Y]]` where each `Array` is of length `N`.

**Example**

```wdl
Array[Pair[Int, String]] int_str_arr = [(0, "hello"), (42, "goodbye")]
Boolean is_true = unzip(int_str_arr) == ([0, 42], ["hello", "goodbye"])

Map[String, Int] m = {"a": 0, "b": 1, "c": 2}
Pair[Array[X], Pair[Array[Y]] keys_and_values = unzip(as_pairs(map))
Boolean is_true2 = keys_and_values.left == ["a", "b", "c"]
Boolean is_true3 = keys_and_values.right == [0, 1, 2]
```

## Array[Pair[X,Y]] cross(Array[X], Array[Y])

Creates an array of `Pair`s containing the [cross product](https://en.wikipedia.org/wiki/Cross_product) of two input arrays, i.e. each element in the first array is paired with each element in the second array.

Given arrays `X` of length `M`, and `Y` of length `N`, the cross product is an array `Z` of length `M*N` with the following elements: `[(X0, Y0), (X0, Y1), ..., (X0, Yn-1), (X1, Y0), ..., (X1, Yn-1), ..., (Xm-1, Yn-1)]`.

**Parameters**

1. `Array[X]`: The first array of length `M`.
2. `Array[Y]`: The second array of length `N`.

**Returns**: An `Array[Pair[X, Y]]` of length `M*N`.

**Example**

```wdl
Array[Int] xs = [ 1, 2, 3 ]
Array[String] ys = [ "a", "b" ]

Array[Pair[Int, String]] crossed = cross(xs, ys)
Boolean is_true = crossed == [ (1, "a"), (1, "b"), (2, "a"), (2, "b"), (3, "a"), (3, "b") ]
```

## Array[X] flatten(Array[Array[X]])

Flattens a nested `Array[Array[X]]` by concatenating all of the element arrays, in order, into a single array. The function is not recursive - e.g. if the input is `Array[Array[Array[Int]]]` then the output will be `Array[Array[Int]]`. The elements in the concatenated array are not deduplicated.

**Parameters**

1. `Array[Array[X]]`: A nested array to flatten.

**Returns**: An `Array[X]` containing the concatenated elements of the input array.

**Example**

```wdl
Array[Array[Int]] ai2D = [[1, 2, 3], [1], [21, 22]]
Boolean is_true = flatten(ai2D) == [1, 2, 3, 1, 21, 22]

Array[Array[File]] af2D = [["/tmp/X.txt"], ["/tmp/Y.txt", "/tmp/Z.txt"], []]
Boolean is_true2 = flatten(af2D) == ["/tmp/X.txt", "/tmp/Y.txt", "/tmp/Z.txt"]

Array[Array[Pair[Float, String]]] aap2D = [[(0.1, "mouse")], [(3, "cat"), (15, "dog")]]
Boolean is_true3 = flatten(aap2D) == [(0.1, "mouse"), (3, "cat"), (15, "dog")]
# we can use as_map to turn this into a Map[Float, String]
Map[Float, String] f2s = as_map(flatten(aap2D))

Array[Array[Array[Int]]] ai3D = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
Boolean is_true4 = flatten(ai3D) == [[1, 2], [3, 4], [5, 6], [7, 8]]
```

## Array[String] prefix(String, Array[P])

Adds a prefix to each element of the input array of primitive values. Equivalent to evaluating `"~{prefix}~{array[i]}"` for each `i` in `range(length(array))`.

**Parameters**

1. `String`: The prefix to prepend to each element in the array.
2. `Array[P]`: Array with a primitive element type.

**Returns**: An `Array[String]` the prefixed elements of the input array.

**Example**

```wdl
Array[String] env = ["key1=value1", "key2=value2", "key3=value3"]
prefix("-e ", env) == ["-e key1=value1", "-e key2=value2", "-e key3=value3"]

Array[Int] env2 = [1, 2, 3]
Array[String] env2_param = prefix("-f ", env2) # ["-f 1", "-f 2", "-f 3"]

Array[Array[String]] env3 = [["a", "b], ["c", "d"]]
# this fails with an error - env3 element type is not primitive
Array[String] bad = prefix("-x ", env3)
```

## ✨ Array[String] suffix(String, Array[P])

Adds a suffix to each element of the input array of primitive values. Equivalent to evaluating `"~{array[i]}~{suffix}"` for each `i` in `range(length(array))`.

**Parameters**

1. `String`: The suffix to append to each element in the array.
2. `Array[P]`: Array with a primitive element type.

**Returns**: An `Array[String]` the suffixed elements of the input array.

**Example**

```wdl
Array[String] env = ["key1=value1", "key2=value2", "key3=value3"]
Boolean is_true = suffix(".txt ", env) == ["key1=value1.txt", "key2=value2.txt", "key3=value3.txt"]

Array[Int] env2 = [1, 2, 3]
Boolean is_true2 = suffix(".0", env2) == ["1.0", "2.0", "3.0"]

Array[Array[String]] env3 = [["a", "b], ["c", "d"]]
# this fails with an error - env3 element type is not primitive
Array[String] bad = suffix("-z", env3)  
```

## ✨ Array[String] quote(Array[P])

Adds double-quotes (`"`) around each element of the input array of primitive values. Equivalent to evaluating `'"~{array[i]}"'` for each `i` in `range(length(array))`.

**Parameters**

1. `Array[P]`: Array with a primitive element type.

**Returns**: An `Array[String]` the double-quoted elements of the input array.

**Example**

```wdl
Array[String] env = ["key1=value1", "key2=value2", "key3=value3"]
Array[String] env_quoted = quote(env) # ['"key1=value1"', '"key2=value2", '"key3=value3"']

Array[Int] env2 = [1, 2, 3]
Array[String] env2_quoted = quote(env2) # ['"1"', '"2"', '"3"']
``` 

## ✨ Array[String] squote(Array[P])

Adds single-quotes (`'`) around each element of the input array of primitive values. Equivalent to evaluating `"'~{array[i]}'"` for each `i` in `range(length(array))`.

**Parameters**

1. `Array[P]`: Array with a primitive element type.

**Returns**: An `Array[String]` the single-quoted elements of the input array.

**Example**

```wdl
Array[String] env = ["key1=value1", "key2=value2", "key3=value3"]
Array[String] env_quoted =  squote(env) # ["'key1=value1'", "'key2=value2'", "'key3=value3'"]

Array[Int] env2 = [1, 2, 3]
Array[String] env2_quoted = squote(env2) # ["'1'", "'2'", "'3'"]
``` 

## ✨ String sep(String, Array[String])

Concatenates the elements of an array together into a string with the given separator between consecutive elements. There are always `N-1` separators in the output string, where `N` is the length of the input array. A separator is never added after the last element.

**Parameters**

1. `String`: Separator string. 
2. `Array[String]`: Array of strings to concatenate.

**Returns**: A `String` with the concatenated elements of the array delimited by the separator string.

**Example**

```wdl
Array[String] a = ["file_1", "file_2"]
# these all evaluate to true
Boolean all_true = [
  sep(' ', prefix('-i ', a)) == "-i file_1 -i file_2",
  sep("", ["a, "b", "c"]) == "abc",
  sep(' ', ["a", "b", "c"]) == "a b c",
  sep(',', [1]) == "1"
]
```

## ✨ Array[Pair[P, Y]] as_pairs(Map[P, Y])

Converts a `Map` with primitive keys into an `Array` of `Pair`s. Since `Map`s are ordered, the output array will always have elements in the same order they were added to the `Map`.

**Parameters**

1. `Map[P, Y]`: `Map` to convert to `Pair`s.

**Returns**: Ordered `Array` of `Pair`s, where each pair contains the key (left) and value (right) of a `Map` element.

**Example**

```wdl
workflow foo {
  Map[String, Int] x = {"a": 1, "c": 3, "b": 2}
  Boolean is_true = as_pairs(x) == [("a", 1), ("c", 3), ("b", 2)]

  Map[String, Pair[File, File]] y = {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}
  scatter (item in as_pairs(y)) {
    String s = item.left
    Pair[File, File] files = item.right
    Pair[File, String] bams = (files.left, s)
  }
  Boolean is_true2 = bams == [("a.bam", "a"), ("b.bam", "b")]
  Map[File, String] bam_to_name = as_map(bams)
}
```

## ✨ Map[P, Y] as_map(Array[Pair[P, Y]])

Converts an `Array` of `Pair`s into a `Map` in which the left elements of the `Pair`s are the (primitive) keys and the right elements the values. All the keys must be unique, or an error is raised. The order of the key/value pairs in the output `Map` is the same as the order of the `Pair`s in the `Array`.

**Parameters**

1. `Array[Pair[P, Y]]`: Array of `Pair`s to convert to a `Map`.

**Returns**: `Map[P, Y]` of the elements in the input array.

**Example**

```wdl
Array[Pair[String, Int]] x = [("a", 1), ("c", 3), ("b", 2)]
Boolean is_true = as_map(x) == {"a": 1, "c": 3, "b": 2}

Array[Pair[String, Pair[File,File]]] y = [("a", ("a.bam", "a.bai")), ("b", ("b.bam", "b.bai"))
Boolean is_true2 = as_map(y) == {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}

# this fails with an error - the "a" key is duplicated
Boolean bad = as_map([("a", 1), ("a", 2)])  
```

## ✨ Array[P] keys(Map[P, Y])

Creates an `Array` of the keys from the input `Map`, in the same order as the elements in the map.

**Parameters**

1. `Map[P, Y]`: `Map` from which to extract keys.

**Returns**: `Array[P]` of the input `Map`s keys.

**Example**

```wdl
workflow foo {
  Map[String,Int] x = {"a": 1, "b": 2, "c": 3}
  Boolean is_true = keys(x) == ["a", "b", "c"]

  Map[String, Pair[File, File]] str_to_files = {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}
  scatter (item in str_to_files) {
    String key = item.left
  }
  Array[String] str_to_files_keys = key
  Boolean is_truew = str_to_files_keys == keys(str_to_files)
}
```

## ✨ Map[P, Array[Y]] collect_by_key(Array[Pair[P, Y]])

Given an `Array` of `Pair`s, creates a `Map` in which the right elements of the `Pair`s are grouped by the left elements. In other words, the input `Array` may have multiple `Pair`s with the same (primitive) key - rather than causing an error (as would happen with [`as_map`](#-mapp-y-as_maparraypairp-y)), all the values with the same key are grouped together into an `Array`.

The order of the keys in the output `Map` is the same as the order of their first occurrence in the input `Array`. The order of the elements in the `Map` values is the same as their order of occurrence in the input `Array`.

**Parameters**

1. `Array[Pair[P, Y]]`: `Array` of `Pair`s to group.

**Returns**: `Map` of keys to `Array`s of values.

**Example**

```wdl
Array[Pair[String, Int]] x = [("a", 1), ("b", 2), ("a", 3)]
Boolean is_true = as_map(x) == {"a": [1, 3], "b": [2]}

Array[Pair[String, Pair[File, File]]] y = [
  ("a", ("a_1.bam", "a_1.bai")), ("b", ("b.bam", "b.bai")), ("a", ("a_2.bam", "a_2.bai"))
]
Boolean is_true2 = as_map(y) == {
  "a": [("a_1.bam", "a_1.bai"), ("a_2.bam", "a_2.bai")], 
  "b": [("b.bam", "b.bai")]
}
```

## Boolean defined(X?)

Tests whether the given optional value is defined, i.e. has a non-`None` value.

**Parameters**

1. `X?`: optional value of any type.

**Returns**: `false` if the input value is `None`, otherwise `true`.

**Example**

```wdl
task say_hello {
  input {
    String name
  }
  command <<< echo ~{name} >>>
}

workflow wf {
  input {
    String? s
  }
  if (defined(s)) {
    call say_hello { input: name = select_first([s]) }
  }
}
```

## X select_first(Array[X?]+)

Selects the first - i.e. left-most - non-`None` value from an `Array` of optional values. It is an error if the array is empty, or if the array only contains `None` values. 

**Parameters**

1. `Array[X?]+`: non-empty `Array` of optional values.

**Returns**: the first non-`None` value in the input array.

**Example**

```wdl
workflow SelectFirst {
  input {
    Int? maybe_five = 5
    Int? maybe_four_but_is_not = None
    Int? maybe_three = 3
  }
  # both of these statements evaluate to 5
  Int five = select_first([maybe_five, maybe_four_but_is_not, maybe_three])
  Int five = select_first([maybe_four_but_is_not, maybe_five, maybe_three])

  select_first([maybe_four_but_is_not])  # error! array contains only None values
  select_first([])  # error! array is empty
}
```

## Array[X] select_all(Array[X?])

Filters the input `Array` of optional values by removing all `None` values. The elements in the output `Array` are in the same order as the input `Array`. If the input array is empty or contains only `None` values, an empty array is returned.

**Parameters**

1. `Array[X?]`: `Array` of optional values.

**Returns**: an `Array` of all non-`None` values in the input array.

**Example**

```wdl
workflow SelectAll {
  input {
    Int? maybe_five = 5
    Int? maybe_four_but_is_not = None
    Int? maybe_three = 3
  }
  Array[Int] fivethree = select_all([maybe_five, maybe_four_but_is_not, maybe_three])
  Boolean is_true = fivethree == [5, 3]
}
```

# Input and Output Formats

WDL uses [JSON](https://www.json.org) as its native serialization format for task and workflow inputs and outputs. The specifics of these formats are described below.

All WDL implementations are required to support the standard JSON input and output formats. WDL compliance testing is performed using test cases whose inputs and expected outputs are given in these formats. A WDL implementation may choose to support any additional input and output mechanisms so long as they are documented, and or tools are provided to interconvert between engine-specific input and the standard JSON format, to foster interoperability between tools in the WDL ecosystem.

## JSON Input Format

The inputs for a workflow invocation may be specified as a single JSON object that contains one member for each top-level workflow, subworkflow, or task input. The name of the object member is the [fully-qualified name](#fully-qualified-names--namespaced-identifiers) of the input parameter, and the value is the [serialized form]() of the WDL value.

Here is an example JSON workflow input file:

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

WDL implementations are only required to support workflow execution, and not necessarily task execution, so a JSON input format for tasks is not specified. However, it is strongly suggested that if an implementation does support task execution, that it also supports this JSON input format for tasks. It is left to the discretion of the WDL implementation whether it is required to prefix the task input with the task name, i.e. `mytask.infile` vs. `infile`.

### Optional Inputs

If a workflow has an optional input, its value may or may not be specified in the JSON input. It is also valid to explicitly set the value of an optional input to be undefined using JSON `null`.

For example, given this workflow:

```wdl
workflow foo {
  input {
    File? x
    Int? y = 5
  }
}
```

The following would all be valid JSON inputs:

```json
# no input
{}

# only x
{
  "x": 100
}

# only y
{
  "x": null,
  "y": "/path/to/file"
}

# x and y
{
  "x": 1000,
  "y": "/path/to/file"
}

# override y default and set it to None
{
  "y": null
}
```

## JSON Output Format

The outputs from a workflow invocation may be specified as a single JSON object that contains one member for each top-level workflow output; sub-workflow and task outputs are not provided. The name of the object member is the [fully-qualified name](#fully-qualified-names--namespaced-identifiers) of the output parameter, and the value is the [serialized form]() of the WDL value.

Every WDL implementation must support the ability to output this standard output. It is suggested that WDL implementations make the standard format be the default output format.

For example, given this workflow:

```wdl
workflow example {
  ...
  output {
    String foo = cafeteria.inn
    File analysis_results = analysis.results
    Int read_count = readcounter.result
    Float kessel_run_parsecs = trip_to_space.distance
    Boolean sample_swap_detected = array_concordance.concordant
    Array[File] sample_variants = variant_calling.vcfs
    Map[String, Int] droids = escape_pod.cargo
  }
}
```

The output JSON will look like:

```json
{
  "example.foo": "bar",
  "example.analysis_results": "/path/to/my/analysis/results.txt",
  "example.read_count": 50157187,
  "example.kessel_run_parsecs": 11.98,
  "example.sample_swap_detected": false,
  "example.sample_variants": ["/data/patient1.vcf", "/data/patient2.vcf"],
  "example.droids": {"C": 3, "D": 2, "P": 0, "R": 2}
}
```

It is recommended (but not required) that JSON outputs be "pretty printed" to be more human-readable.

## Specifying / Overriding Runtime Attributes

In addition to specifying workflow input in JSON, the user can also specify (or override) runtime attributes. Input values for standardized runtime attributes must adhere to the [supported types and formats](#runtime-section). Runtime values provided as inputs always supersede values supplied directly in the WDL. Any runtime attributes that are not supported by the execution engine are ignored.

To differentiate runtime attributes from task inputs, the `runtime` namespace is added after the task name. For example:

```json
{
  "wf.t1.runtime.memory": "16 GB",
  "wf.t2.runtime.cpu": 2,
  "wf.t2.runtime.disks": "100",
  "wf.t2.runtime.container": "mycontainer:latest"
}
```

## JSON Serialization of WDL Types

### Primitive Types

All primitive WDL types serialize naturally to JSON values:

|WDL Type        |JSON Type|
|----------------|---------|
|`Int`           |number   |
|`Float`         |number   |
|`Boolean`       |boolean  |
|`String`        |string   |
|`File`          |string   |
|`None`          |null     |

JSON has a single numeric type - it does not differentiate between integral and floating point values. A JSON `number` is always deserialized to a WDL `Float`, which may then be coerced to an `Int` if necessary.

JSON also does not have a specific type for filesystem paths, but a WDL `String` may be coerced to a `File` if necessary.

### Array

Arrays are represented naturally in JSON using the `array` type. Each array element is serialized recursively into its JSON format.

When a JSON `array` is deserialized to WDL, each element of the array must be coercible to a common type.

### Pair

`Pair`s are not directly serializable to JSON, because there is no way to represent them unambiguously. Instead, a `Pair` must first be converted to a serializable type, such as using one of the following suggested methods. Attempting to serialize a `Pair` in an error.

**Suggested Conversion 1: `Array`**

To make a `Pair[X, X]` serializable, simply convert it to a two-element array:

```wdl
Pair[Int, Int] p = (1, 2)
Array[Int] a = [p.left, p.right]

# after deserialization, we can convert back to Pair
Pair[Int, Int] p2 = (a[0], a[1])
```

**Suggested Conversion 2: `Struct`**

When a `Pair`'s left and right members are of different types, it can be converted to a `Struct` with members of the correct types:

```wdl
struct StringIntPair {
  String left
  Int right
}
Pair[String, Int] p = ("hello", 42)
StringIntPair s = StringIntPair {
  left: p.left,
  right: p.right
}

# after deserialization, we can convert back to Pair
Pair[String, Int] p2 = (s.left, s.right)
```

### Map

A `Map[String, X]` may be serialized to a JSON `object` by the same mechanism as a WDL `Struct` or `Object`. This value will be deserialized to a WDL `Object`, after which it may be coerced to a `Map`.

Serialization of `Map`s with other key types is problematic, because there is no way to represent them in JSON unambiguously. Thus, a `Map` with non-`String` keys must first be converted to a serializable type, e.g. by using the following suggested method. Attempting to serialize a `Map` with a non-`String` key type results in an error.

**Suggested Conversion**

Convert the `Map[X, Y]` into a `Struct` with two array members: `Array[X] keys` and `Array[Y] values`.

```wdl
struct IntStringMap {
  Array[Int] keys
  Array[String] values
}
Map[Int, String] m = {0: "a", 1: "b"}
Pair[Array[Int], Array[String]] u = unzip(m)
IntStringMap i = IntStringMap {
  keys: u.left,
  values: u.right
}

# after deserialization, we can convert back to Map
Map[Int, String] m2 = as_map(zip(i.keys, i.values))
```

### Struct and Object

`Struct`s and `Object`s are represented naturally in JSON using the `object` type. Each WDL `Struct` or `Object` member value is serialized recursively into its JSON format.

A JSON `object` is deserialized to a WDL `Object` value, and each member value is deserialized to its most likely WDL type. The WDL `Object` may then be coerced to a `Map` or `Struct` type if necessary.

# Appendix A: WDL Value Serialization and Deserialization

This section provides suggestions for ways to deal with primitive and compound values in the task [command section](#command-section). When a WDL execution engine instantiates a command specified in the `command` section of a `task`, it must evaluate all expression placeholders (`~{...}` and `${...}`) in the command and coerce their values to strings. There are multiple different ways that WDL values can be communicated to the command(s) being called in the command section, and the best method will vary by command.

For example, a task that wraps a tool that operates on an `Array` of FASTQ files has several ways that it can specify the list of files to the tool:

* A file containing one file path per line, e.g. `Rscript analysis.R --files=fastq_list.txt`
* A file containing a JSON list, e.g. `Rscript analysis.R --files=fastq_list.json`
* Enumerated on the command line, e.g. `Rscript analysis.R 1.fastq 2.fastq 3.fastq`

On the other end, command line tools will output results in files or to standard output, and these output data need to be converted to WDL values to be used as task outputs. For example, the FASTQ processor task mentioned above outputs a mapping of the input files to the number of reads in each file. This output might be represented as a two-column TSV or as a JSON object, both of which would need to be deserialized to a WDL `Map[File, Int]` value.

The various methods for serializing and deserializing primitive and compound values are enumerated below.

## Primitive Values

WDL primitive values are naturally converted to string values. This is described in detail in the [string interpolation](#expression-placeholders-and-string-interpolation) section.

De-serialization of primitive values is done through the `read_*` functions, which deserialize primitive values written to a file by a task command.

For example, this task's command writes a `String` to one file and an `Int` to another:

```wdl
task output_example {
  input {
    String param1
    String param2
  }

  command <<<
    python do_work.py ~{param1} ~{param2} --out1=int_file --out2=str_file
  >>>

  output {
    Int my_int = read_int("int_file")
    String my_str = read_string("str_file")
  }
  
  runtime {
    container: "my_image:latest"
  }
}
```

Both files `int_file` and `str_file` must contain one line with the value on that line. This value is read as a string and then coerced to the appropriate type. If `int_file` contains a line with the text "foobar", calling `read_int` on that file results in an error.

## Compound Values

Compound values, like `Array` and `Map` must be converted to a primitive value before they can be used in the command. Similarly, compound values generated by the command must be deserialized to be used in WDL. Task commands will generally use one of two formats to write outputs that can be deserialized by WDL:

* JSON: Most WDL values convert naturally to JSON values, and vice-versa
* Text based / tab-separated-values (TSV): Simple table and text-based encodings (e.g. `Array[String]` could be serialized by having each element be a line in a file)

The various ways to turn compound values into primitive values and vice-versa are described below.

### Array

Arrays can be serialized in two ways:

* **Array Expansion**: elements in the list are flattened to a string with a separator character.
* **File Creation**: create a file with the elements of the array in it and passing that file as the parameter on the command line.

#### Array serialization by expansion

The array flattening approach can be done if a parameter is specified as `~{sep=' ' my_param}`.  `my_param` must be declared as an `Array` of primitive values. When the value of `my_param` is specified, then the values are joined together with the separator character (a space in this case).  For example:

```wdl
task test {
  input {
    Array[File] bams
  }

  command <<<
    python script.py --bams=~{sep=',' bams}
  >>>
  
  runtime {
    container: "my_image:latest"
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

#### Array serialization using write_lines()

An array may be turned into a file with each element in the array occupying a line in the file.

```wdl
task test {
  input {
    Array[File] bams
  }

  command <<<
    sh script.sh ~{write_lines(bams)}
  >>>
  
  runtime {
    container: "my_image:latest"
  }
}
```

If `bams` is given this array:

|Element       |
|--------------|
|/path/to/1.bam|
|/path/to/2.bam|
|/path/to/3.bam|

Then, the resulting command line might be:

```sh
sh script.sh /jobs/564758/bams
```

Where `/jobs/564758/bams` would contain:

```txt
/path/to/1.bam
/path/to/2.bam
/path/to/3.bam
```

#### Array serialization using write_json()

The array may be turned into a JSON document with the file path for the JSON file passed in as the parameter:

```wdl
task test {
  input {
    Array[File] bams
  }

  command <<<
    sh script.sh ~{write_json(bams)}
  >>>
  
  runtime {
    container: "my_image:latest"
  }
}
```

If `bams` is given this array:

|Element       |
|--------------|
|/path/to/1.bam|
|/path/to/2.bam|
|/path/to/3.bam|

Then, the resulting command line might look like:

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

#### Array deserialization using read_lines()

`read_lines()` will return an `Array[String]` where each element in the array is a line in the file.

This return value can be auto converted to other `Array` values.  For example:

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
  
  runtime {
    container: "my_image:latest"
  }
}
```

`my_ints` would contain ten random integers ranging from 0 to 10.

#### Array deserialization using read_json()

`read_json()` will return whatever data value resides in that JSON file.

```wdl
task test {
  command <<<
    echo '["foo", "bar"]'
  >>>

  output {
    Array[String] my_array = read_json(stdout())
  }
  
  runtime {
    container: "my_image:latest"
  }
}
```

This task would assign the array with elements `"foo"` and `"bar"` to `my_array`.

If the echo statement was instead `echo '{"foo": "bar"}'`, the engine MUST fail the task for a type mismatch.

### Struct and Object

`Struct`s and `Object`s are serialized identically. A JSON object is always deserialized to a WDL `Object`, which can then be coerced to a `Struct` type if necessary.

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
  
  runtime {
    container: "my_image:latest"
  }
}
```

If `p` is provided as:

```wdl
Person {
  name: "John",
  age: 5,
  friends: ["James", "Jim"]
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

### Map

`Map` types cannot be serialized on the command line directly and must be serialized through a file

#### Map serialization using write_map()

The `Map` value can be serialized as a two-column TSV file, and the parameter on the command line is given the path to that file, using the `write_map()` function:

```wdl
task test {
  input {
    Map[String, Float] sample_quality_scores
  }

  command <<<
    sh script.sh ~{write_map(sample_quality_scores)}
  >>>
  
  runtime {
    container: "my_image:latest"
  }
}
```

If `sample_quality_scores` were a `Map` with these members:

|Key    |Value |
|-------|------|
|sample1|98    |
|sample2|95    |
|sample3|75    |

Then, the resulting command line might look like:

```sh
sh script.sh /jobs/564757/sample_quality_scores.tsv
```

Where `/jobs/564757/sample_quality_scores.tsv` would contain:

```txt
sample1\t98
sample2\t95
sample3\t75
```

#### Map serialization using write_json()

The `Map` value can also be serialized as a JSON `object` in a file, and the parameter on the command line is given the path to that file, using the `write_json()` function:

```wdl
task test {
  input {
    Map[String, Float] sample_quality_scores
  }

  command <<<
    sh script.sh ~{write_json(sample_quality_scores)}
  >>>
  
  runtime {
    container: "my_image:latest"
  }
}
```

If `sample_quality_scores` were a `Map` with these members:

|Key    |Value |
|-------|------|
|sample1|98    |
|sample2|95    |
|sample3|75    |

Then, the resulting command line might look like:

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

#### Map deserialization using read_map()

`read_map()` will return a `Map[String, String]` where the keys are the first column in the TSV input file and the corresponding values are the second column.

This return value can be coerced to other `Map` types. For example:

```wdl
task test {
  command <<<
    python <<CODE
    for i in range(3):
      print("key_{idx}\t{idx}".format(idx=i))
    CODE
  >>>

  output {
    Map[String, Int] my_ints = read_map(stdout())
  }
  
  runtime {
    container: "my_image:latest"
  }
}
```

`my_ints` will be a `Map[String, Int]` with members:

|Key  |Value |
|-----|------|
|key_0|0     |
|key_1|1     |
|key_2|2     |

#### Map deserialization using read_json()

`read_json()` will return whatever data type resides in the JSON file. If the file contains a JSON `object`, it is deserialized as an `Object` value, which can be coerced to a `Map[String, X]` so long as all values are coercible to `X`.

```wdl
task test {
  command <<<
    echo '{"foo":"bar"}'
  >>>

  output {
    Map[String, String] my_map = read_json(stdout())
  }
  
  runtime {
    container: "my_image:latest"
  }
}
```

`my_map` will be a `Map[String, String]` with members:

|Key |Value |
|----|------|
|foo |bar   |

Note that using `write_json`/`read_json` to serialize to/from a `Map` can cause suble issues due to the fact that `Map` is ordered whereas `Object` is not. For example:

```wdl
Map[String, Int] s2i = {"b": 2, "a": 1}
File f = write_json(s2i)

# Object is not ordered - coercion to Map may
# result in either of two values:
# {"a": 1, "b": 2} or {"b": 2, "a": 1}
Map[String, Int] deserialized_s2i = read_json(f)

# is_equal is non-deterministic - it may be
# true or false, depending on how the members
# are ordered in the Object
Boolean is_equal = s2i == deserialized_s2i
```

### Pair

There are no functions to directly serialize and deserialize `Pair`s. Instead, the left and right values should be passed to the command independently.

In this script, `myscript` writes two files, `int.txt` containing an `Int`, and `str.txt` containing a `String`.

```wdl
task pair_test {
  input {
    Pair[Int, String] p
  }

  command <<<
  ./myscript -i ~{p.left} -s ~{p.right}
  >>>

  output {
    Pair[Int, String] out = (read_int("int.txt"), read_string("str.txt")) 
  }
}
```

Alternatively, a `Struct` (or `Object`) can be created with `left` and `right` members and then serialized by the appropriate function.

```wdl
struct IntStringPair {
  Int left
  String right
}

task pair_test_obj {
  input {
    Pair[Int, String] p
  }
  IntStringPair serializable = IntStringPair {
    left: p.left,
    right: p.right
  }
  command <<<
  ./myscript --json ~{write_json(serializable)}
  >>>
}
```

# Appendix B: WDL Namespaces and Scopes

Namespaces and scoping in WDL are somewhat complex topics, and some aspects are counter-intuitive for users coming from backgrounds in other programming languages. This section goes into deeper details on these topics.

## Namespaces

The following WDL namespaces exist:

* [WDL document](#wdl-documents)
  * The namespace of an [imported](#import-statements) document equals that of the basename of the imported file by default, but may be aliased using the `as identifier` syntax.
  * A WDL document may contain a `workflow` and/or `task`s, which are names within the document's namespace.
  * A WDL document may contain `struct`s, which are added to a [global namespace](#struct-usage).
  * A WDL document may contain other namespaces via `import`s.
* A [WDL `task`](#task-definition) is a namespace consisting of:
  * The `task` `input` declarations
  * The `task` `output` declarations
  * A [`runtime`](#runtime-section) namespace that contains all the runtime attributes
* A [WDL `workflow`](#workflow-definition) is a namespace consisting of:
  * The `workflow` `input` declarations
  * The `workflow` `output` declarations
  * The [`call`s](#call-statement) made to tasks and subworkflows within the body of the workflow.
    * A call is itself a namespace that equals the name of the called task or subworkflow by default, but may be aliased using the `as $identifier` syntax.
    * A call namespace contains the output declarations of the called task or workflow.
    * A call to a subworkflow also contains the names of calls made in the body of that workflow.
* A [`struct` instance](#struct-definition): is a namespace consisting of the members defined in the `Struct`. This also applies to `Object` instances.

All members of a namespace must be unique within that namespace. For example:

* Two workflows cannot be imported while they have the same namespace identifier - at least one of them would need to be aliased.
* A workflow and a namespace both named `foo` cannot exist inside a common namespace.
* There cannot be a call `foo` in a workflow also named `foo`.
 
However, two sub-namespaces imported into the same parent namespace are allowed to contain the same names. For example, two workflows with different namespace identifiers `foo` and `bar` can both have a task named `baz`, because the [fully-qualified names](#fully-qualified-names--namespaced-identifiers) of the two tasks would be different: `foo.baz` and `bar.baz`.

## Scopes

A "scope" is associated with a level of nesting within a namespace. The visibility of workflow elements is governed by their scope, and by WDL's scoping rules, which are explained in this section.

### Global Scope

A WDL document is the top-level (or "outermost") scope. All elements defined within a document that are not nested inside other elements are in the global scope and accessible from anywhere in the document. The elements that may be in a global scope are:

* Namespaces (via imports)
* `struct`s (including all `struct`s defined in the document and in any imported documents)
* `task`s
* A `workflow`

### Task Scope

A task scope consists of all the declarations in the task `input` section and in the body of the task. The `input` section is used only to delineate which declarations are visible outside the task (i.e. are part of the task's namespace) and which are private to the task. Input declarations may reference private declarations, and vice-versa. Declarations in the task scope are reachable from all sections of the task (i.e. `command`, `runtime`, `output` - `meta` and `parameter_meta` are excluded because they cannot have expressions).

The `output` section can be considered a nested scope within the task. Expressions in the output scope may reference declarations in the task scope, but the reverse is not true. This is because declarations in the task scope are evaluated when a task is invoked (i.e. before it's command is evaluated and executed), while declarations in the output scope are not evaluated until after execution of the command is completed.

Example:

```wdl
task my_task {
  input {
    Int x
    File f
  }

  Int y = x + 1

  command <<<
    my_cmd --integer1=~{x} --integer2=~{y} ~{f}
  >>>

  output {
    Int z = read_int(stdout())
    Int z_plus_one = z + 1
  }
}
```

* `x` and `f` are `input` values that will be evaluated when the task is invoked.
* `y` is an private declaration with a dependency on the input `x`.
* The `command` section is able to access all `input` and private declarations.
  * The `command` section is *not* able to reference `output` declarations.
* `z` is an `output` declaration - it cannot be accessed except by the other declaration in the `output` section.
* `z_plus_one` is another `output` declaration.

### Workflow Scope

A workflow scope consists of all of the:

* Declarations in the workflow `input` section.
* Declarations in the body of the workflow.
* Calls in the workflow.
* Declarations and call outputs that are exported from nested scopes within the workflow (i.e. `scatter` and `if` blocks).
 
Just like in the task scope, all declarations in the workflow scope can reference each other, and the `output` section is a nested scope that has access to - but cannot be accessed from - the workflow scope.

Example: this workflow calls the `my_task` task from the previous example.

```wdl
workflow my_workflow {
  input {
    File file
    Int x = 2
  }

  call my_task { 
    input:
      x = x,
      f = file
  }

  output {
    Int z = my_task.z
  }
}
```

* `file` and `x` are `input` declarations that will be evaluated when the workflow is invoked.
* The call block provides inputs for the task values `x` and `f`. Note that `x` is used twice in the line `x = x`:
    * First: to name the value in the task being provided. This must reference an input declaration in the namespace of the called `task`.
    * Second: as part of the input expression. This expression may reference any values in the current `workflow` scope.
* `z` is an output declaration that depends on the output from the `call` to `my_task`. It is not accessible from elsewhere outside the `output` section.

Workflows can have block constructs - scatters and conditionals - that define nested scopes. A nested scope can have declarations, calls, and block constructs (which create another level of nested scope). The declarations and calls in a nested scope are visible within that scope and within any sub-scopes, recursively.

Every nested scope implicitly "exports" all of its declarations and call outputs in the following manner:

* A scatter scope exports its declarations and calls with the same names they have inside the scope, but with their types modified, such that the exported types are all `Array[X]`, where `X` is the type of the declaration within the scope.
  * A scatter scope *does not* export its scatter variable. For example, if a block is defined as `scatter (x in array)`, `x` is not accessible outside of the scatter scope - it is only accessible from within the scatter scope and any nested scopes.
* A conditional scope exports its declarations and calls with the same names they have inside the scope, but with their types modified, such that the exported types are all `X?`, where `X` is the type of the declaration within the scope.

Example: this workflow scatters over the `my_task` task from the previous examples.

```wdl
workflow my_workflow {
  input {
    File file
    Array[Int] xs = [1, 2, 3]
  }

  scatter (x in xs) {
    call my_task { input:
      x = x,
      f = file
    }

    Int z = my_task.z
  }

  output {
    Array[Int] zs = z
  }
}
```

* The expression for `Int z = ...` accesses `my_task.z` from within the same scatter.
* The output `zs` references `z` even though it was declared in a sub-section. However, because `z` is declared within a `scatter` block, the type of `zs` is `Array[Int]` outside of that scatter block.

The concept of a single name within a workflow having different types depending on where it appears can be confusing at first, and it helps to think of these as two different variables. When the user makes a declaration within a nested scope, they are essentially reserving that name in all of the higher-level scopes so that it cannot be reused. For example, the following workflow is invalid:

```wdl
workflow invalid {
  Boolean b = true
  
  scatter {
    String x = "hello"
  }
  
  # the scatter block exports x to the top-level scope - 
  # there is an implicit declaration here that is 
  # reserved to hold the exported value and cannot be 
  # used by any other declaration in this scope
  # Array[String] x
  
  if (b) {
    # error! x is already reserved in the top-level
    # scope to hold the exported value of x from the
    # scatter block, so we cannot reserve it here
    Float x = 1.0
  }

  # error! x is already reserved
  Int x = 5
}
```

### Cyclic References

In addition to following the scoping rules, all references to declarations must be acyclic. In other words, if each declarations in a scope were placed as a node in a graph with directed edges to all of the declarations referenced in its initializer expression, then the WDL would only be valid if there were no cycles in that graph.

For example, this is an example of an invalid workflow due to cyclic references:

```wdl
task mytask {
  input {
    Int inp
  }
  command <<< >>>
  output {
    Int out = inp * 2
  }
}

workflow cyclic {
  input {
    Int i = j + 1
  }

  Int j = mytask.out - 2

  call mytask { input: inp = i }
}
```

Here, `i` references `j` in its initializer expression; `j` references the output of `mytask` in its initializer expression; and the call to `mytask` requires the value of `i`. The graph would be cyclic:

```txt
i -> j -> mytask
^            |
|____________|
```

Since `i` cannot be evaluated until `j` is evaluated, and `j` cannot be evaluated until the call to `mytask` completes, and the call to `mytask` cannot be invoked until the value of `i` is available, trying to execute this workflow would result in a deadlock.

Cycles can be tricky to detect, for example when they occur between declarations in different blocks of a workflow. For example, here is a workflow with one block that references a declaration that originates in another block:

```wdl
workflow my_workflow {
  input {
    Array[Int] as
    Array[Int] bs
  }

  scatter (a in as) {
    Int x_a = a
  }

  scatter (b in bs) {
    Array[Int] x_b = x_a
  }

  output {
    Array[Array[Int]] xs_output = x_b
  }
}
```

* The declaration for `x_b` is able to access the value for `x_a` even though the declaration is in another sub-section of the `workflow`.
* Because the declaration for `x_b` is outside the `scatter` in which `x_a` was declared, the type is `Array[Int]`

The following change introduces a cyclic dependency between the scatter blocks:

```wdl
workflow my_workflow {
  input {
    Array[Int] as
    Array[Int] bs
  }

  scatter (a in as) {
    Int x_a = a
    Array[Int] y_a = y_b
  }

  scatter (b in bs) {
    Array[Int] x_b = x_a
    Int x_b = b
  }

  output {
    Array[Array[Int]] xs_output = x_b
    Array[Array[Int]] ys_output = y_a
  }
}
```

The dependency graph now has to criss-cross between the `scatter (a in as)` block and the `scatter (b in bs)` block. This is **not** allowed. To avoid this criss-crossing between sub-sections, scatters may be split into separate `scatter` blocks over the same input array:

```wdl
workflow my_workflow {
  input {
    Array[Int] as
    Array[Int] bs
  }

  scatter (a in as) {
    Int x_a = a
  }

  scatter (b in bs) {
    Array[Int] x_b = x_a
    Int x_b = b
  }
  
  scatter (a2 in as) {
    Array[Int] y_a = y_b
  }

  output {
    Array[Array[Int]] xs_output = x_b
    Array[Array[Int]] ys_output = y_a
  }
}
```

### Namespaces without Scope

Elements such as `struct`s and task `runtime` sections are namespaces, but they lack scope because their members cannot reference each other. For example, one member of a `struct` cannot reference another member in that struct, nor can a `runtime` attribute reference another attribute.

## Evaluation Order

A key concept in WDL is: **the order in which statements are evaluated depends on the availability of their dependencies, not on the order of the statements in the document.**

All values in tasks and workflows *can* be evaluated as soon as - but not before - their expression inputs are available; beyond this, it is up to the WDL implementation to determine when to evaluate each value.

Remember that, in tasks, the `command` section implicitly depends on all the input and private declarations in the task, and the `output` section implicitly depends on the `command` section, i.e. the `command` section cannot be instantiated until all input and private declarations are evaluated, and the `output` section cannot be evaluated until the command successfully completes execution. This is true even for private declarations that follow the `command` block positionally in the file.

A "forward reference" occurs when an expression refers to a declaration that occurs at a later position in the WDL file. Given the above cardinal rule of evaluation order, forward references are allowed, so long as all declarations can ultimately be processed as an acyclic graph. For example:

```wdl
workflow my_workflow {
  input {
    File file
    Int x = 2
    String s = my_task.out2
  }

  call my_task {
    input:
      x = x_modified,
      f = file
  }

  Int x_modified = x

  output {
    Array[String] out = [my_task.out1, s]
  }
}
```

The dependencies are:

```txt
* x_modified -> x
* my_task -> (x_modified, f)
* s -> my_task
* out -> (my_task, s)
```

There are no cycles in this dependency graph; thus, this workflow is valid, although perhaps not as readable as it could be with better organization.
