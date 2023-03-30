# Workflow Description Language (WDL)

This is version 1.1.1 of the Workflow Description Language (WDL) specification. It describes WDL `version 1.1`. It introduces a number of new features (denoted by the ✨ symbol) and clarifications to the [1.0](https://github.com/openwdl/wdl/blob/main/versions/1.0/SPEC.md) version of the specification. It also deprecates several aspects of the 1.0 specification that will be removed in the [next major WDL version](https://github.com/openwdl/wdl/blob/wdl-2.0/SPEC.md) (denoted by the 🗑 symbol).

## Revisions

Revisions to this specification are made periodically in order to correct errors, clarify language, or add additional examples. Revisions are released as "patches" to the specification, i.e., the third number in the specification version is incremented. No functionality is added or removed after the initial revision of the specification is ratified.

* [1.1.1](https://github.com/openwdl/wdl/tree/release-1.1.1/SPEC.md): TODO
* [1.1.0](https://github.com/openwdl/wdl/tree/release-1.1.0/SPEC.md): 2021-01-29
 
## Table of Contents

- [Workflow Description Language (WDL)](#workflow-description-language-wdl)
  - [Revisions](#revisions)
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
        - [Array\[X\]](#arrayx)
        - [Pair\[X, Y\]](#pairx-y)
        - [Map\[P, Y\]](#mapp-y)
        - [Custom Types (Structs)](#custom-types-structs)
        - [🗑 Object](#-object)
      - [Hidden Types](#hidden-types)
        - [Union](#union)
      - [Type Conversion](#type-conversion)
        - [Primitive Conversion to String](#primitive-conversion-to-string)
        - [Type Coercion](#type-coercion)
          - [Order of Precedence](#order-of-precedence)
          - [Coercion of Optional Types](#coercion-of-optional-types)
          - [Struct/Object coercion from Map](#structobject-coercion-from-map)
          - [🗑 Limited exceptions](#-limited-exceptions)
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
    - [Static Analysis and Dynamic Evaluation](#static-analysis-and-dynamic-evaluation)
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
    - [Fully Qualified Names \& Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers)
    - [Call Statement](#call-statement)
      - [Computing Call Inputs](#computing-call-inputs)
    - [Scatter](#scatter)
    - [Conditional (`if` block)](#conditional-if-block)
  - [Struct Definition](#struct-definition)
    - [Struct Literals](#struct-literals)
    - [Struct Namespacing](#struct-namespacing)
    - [Struct Usage](#struct-usage)
- [Standard Library](#standard-library)
  - [Numeric Functions](#numeric-functions)
    - [`floor`](#floor)
    - [`ceil`](#ceil)
    - [`round`](#round)
    - [✨ `min`](#-min)
    - [✨ `max`](#-max)
  - [String Functions](#string-functions)
    - [`sub`](#sub)
  - [File Functions](#file-functions)
    - [`basename`](#basename)
    - [`glob`](#glob)
      - [Non-standard Bash](#non-standard-bash)
    - [`size`](#size)
    - [`stdout`](#stdout)
    - [`stderr`](#stderr)
    - [`read_string`](#read_string)
    - [`read_int`](#read_int)
    - [`read_float`](#read_float)
    - [`read_boolean`](#read_boolean)
    - [`read_lines`](#read_lines)
    - [`write_lines`](#write_lines)
    - [`read_tsv`](#read_tsv)
    - [`write_tsv`](#write_tsv)
    - [`read_map`](#read_map)
    - [`write_map`](#write_map)
    - [`read_json`](#read_json)
    - [`write_json`](#write_json)
    - [`read_object`](#read_object)
    - [`read_objects`](#read_objects)
    - [`write_object`](#write_object)
    - [`write_objects`](#write_objects)
  - [String Array Functions](#string-array-functions)
    - [`prefix`](#prefix)
    - [✨ `suffix`](#-suffix)
    - [✨ `quote`](#-quote)
    - [✨ `squote`](#-squote)
    - [✨ `sep`](#-sep)
  - [Generic Array Functions](#generic-array-functions)
    - [`length`](#length)
    - [`range`](#range)
    - [`transpose`](#transpose)
    - [`cross`](#cross)
    - [`zip`](#zip)
    - [✨ `unzip`](#-unzip)
    - [`flatten`](#flatten)
    - [`select_first`](#select_first)
    - [`select_all`](#select_all)
  - [Map Functions](#map-functions)
    - [✨ `as_pairs`](#-as_pairs)
    - [✨ `as_map`](#-as_map)
    - [✨ `keys`](#-keys)
    - [✨ `collect_by_key`](#-collect_by_key)
  - [Other Functions](#other-functions)
    - [`defined`](#defined)
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
      - [Array serialization using write\_lines()](#array-serialization-using-write_lines)
      - [Array serialization using write\_json()](#array-serialization-using-write_json)
      - [Array deserialization using read\_lines()](#array-deserialization-using-read_lines)
      - [Array deserialization using read\_json()](#array-deserialization-using-read_json)
    - [Struct and Object](#struct-and-object-1)
      - [Struct serialization using write\_json()](#struct-serialization-using-write_json)
    - [Map](#map-1)
      - [Map serialization using write\_map()](#map-serialization-using-write_map)
      - [Map serialization using write\_json()](#map-serialization-using-write_json)
      - [Map deserialization using read\_map()](#map-deserialization-using-read_map)
      - [Map deserialization using read\_json()](#map-deserialization-using-read_json)
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

<details>
  <summary>
  Example: hello.wdl
      
  ```wdl
  version 1.1

  task hello_task {
    input {
      File infile
      String pattern
    }

    command <<<
      egrep '~{pattern}' '~{infile}'
    >>>

    runtime {
      container: "ubuntu:latest"
    }

    output {
      Array[String] matches = read_lines(stdout())
    }
  }

  workflow hello {
    input {
      File infile
      String pattern
    }

    call hello_task {
      input: infile, pattern
    }

    output {
      Array[String] matches = hello_task.matches
    }
  }
  ```
  </summary>
  <p>
  Example input:

  ```json
  {
    "hello.infile": "greetings.txt",
    "hello.pattern": "hello.*"
  }
  ```
   
  Example output:

  ```json
  {
    "hello.matches": ["hello world", "hello nurse"]
  }
  ``` 
  </p>
</details>

*Note*: you can click the arrow next to the name of any example to expand it and see supplementary information, such as example inputs and outputs.

This WDL document describes a `task`, called `hello_task`, and a `workflow`, called `hello`.

* A `task` encapsulates a Bash script and a UNIX environment and presents them as a reusable function.
* A `workflow` encapsulates a (directed, acyclic) graph of task calls that transforms input data to the desired outputs.

Both workflows and tasks can accept input parameters and produce outputs. For example, `workflow hello` has two input parameters, `File infile` and `String pattern`, and one output parameter, `Array[String] matches`. This simple workflow calls `task hello_task`, passing through the workflow inputs to the task inputs, and using the results of `call hello_task` as the workflow output.

### Executing a WDL Workflow

To execute this workflow, a WDL execution engine must be used (sometimes called the "WDL runtime" or "WDL implementation"). Some popular WDL execution engines are listed in the [README](https://github.com/openwdl/wdl#execution-engines).

Along with the WDL file, the user must provide the execution engine with values for the two input parameters. While implementations may provide their own mechanisms for launching workflows, all implementations minimally accept [inputs as JSON format](#json-input-format), which requires that the input arguments be fully qualified according to the namespacing rules described in the [Fully Qualified Names & Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers) section. For example:

| Variable      | Value         |
| ------------- | ------------- |
| hello.pattern | hello.*       |
| hello.infile  | greetings.txt |

Running the `hello` workflow with these inputs would yield the following command line from the call to `hello_task`:

```sh
egrep 'hello.*' 'greetings.txt'
```

### Advanced WDL Features

WDL also provides features for implementing more complex workflows. For example, `hello_task` introduced in the previous example can be called in parallel across many different input files using the well-known [scatter-gather](https://en.wikipedia.org/wiki/Vectored_I/O#:~:text=In%20computing%2C%20vectored%20I%2FO,in%20a%20vector%20of%20buffers) pattern:

<details>
  <summary>
  Example: hello_parallel.wdl
  
  ```wdl
  version 1.1
  
  import "hello.wdl"

  workflow hello_parallel {
    input {
      Array[File] files
      String pattern
    }
    
    scatter (path in files) {
      call hello.hello_task {
        input: 
          infile = path,
          pattern = pattern
      }
    }

    output {
      # WDL implicitly implements the 'gather' step, so the output of 
      # a scatter is always an array with the elements in the same 
      # order as the input array. Since hello_task.matches is an array,
      # all the results will be gathered into an array-of-arrays.
      Array[Array[String]] all_matches = hello_task.matches
    }
  }
  ```
  </summary>
  <p>
  Example input:
  
  ```json
  {
    "hello_parallel.pattern": "^[a-z_]+$",
    "hello_parallel.infile": ["/greetings.txt", "greetings2.txt"]
  }
  ```
  
  Example output:
  
  ```json
  {
    "hello.matches": [["hi_world"], ["hi_pal"]]
  }
  ```
  </p>
</details>

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

Task and workflow inputs may be passed in from an external source, or they may be specified in the WDL document itself using literal values. Input, output, and other declaration values may also be constructed at runtime using [expressions](#expressions) that consist of literals, identifiers (references to [declarations](#declarations) or [call](#call-statement) outputs), built-in [operators](#operator-precedence-table), and [standard library functions](#standard-library).

#### Strings

A string literal may contain any unicode characters between single or double-quotes, with the exception of a few special characters that must be escaped:

| Escape Sequence | Meaning      | \x Equivalent | Context                       |
| --------------- | ------------ | ------------- | ----------------------------- |
| `\\`            | `\`          | `\x5C`        |                               |
| `\n`            | newline      | `\x0A`        |                               |
| `\t`            | tab          | `\x09`        |                               |
| `\'`            | single quote | `\x22`        | within a single-quoted string |
| `\"`            | double quote | `\x27`        | within a double-quoted string |
| `~`             | tilde        | `\x7E`        | literal `"~{"`                |
| `$`             | dollar sign  | `\x24`        | literal `"${"`                |

Strings can also contain the following types of escape sequences:

* An octal escape code starts with `\`, followed by 3 digits of value 0 through 7 inclusive.
* A hexadecimal escape code starts with `\x`, followed by 2 hexadecimal digits `0-9a-fA-F`. 
* A unicode code point starts with `\u` followed by 4 hexadecimal characters or `\U` followed by 8 hexadecimal characters `0-9a-fA-F`.

### Comments

Comments can be used to provide helpful information such as workflow usage, requirements, copyright, etc. A comment is prepended by `#` and can be placed at the start of a line or at the end of any line of WDL code. Any text following the `#` will be completely ignored by the execution engine, with one exception: within the `command` section, *ALL* text will be included in the evaluated script - even lines prepended by `#`.

There is no special syntax for multi-line comments - simply use a `#` at the start of each line.

<details>
  <summary>
  Example: workflow_with_comments.wdl
  
  ```wdl
  # Comments are allowed before version
  version 1.1

  # This is how you
  # write a long
  # multiline
  # comment

  task task_with_comments {
    input {
      Int number  # This comment comes after a variable declaration
    }

    # This comment will not be included within the command
    command <<<
      # This comment WILL be included within the command after it has been parsed
      cat ~{number * 2}
    >>>

    output {
      Int result = read_int(stdout())
    }
      
    runtime {
      container: "ubuntu:latest"
    }
  }

  workflow workflow_with_comments {
    input {
      Int number
    }

    # You can have comments anywhere in the workflow
    call task_with_comments { input: number }
    
    output { # You can also put comments after braces
      Int result = task_with_comments.result
    }
  }
  ```
  </summary>
  <p>
  Example input:
  
  ```json
  {
    "workflow_with_comments.number": 1
  }
  ```
  
  Example output:
  
  ```json
  {
    "workflow_with_comments.result": 2
  }
  ```
  </p>
</details>

### Reserved Keywords

The following (case-sensitive) language keywords are reserved and cannot be used to name declarations, calls, tasks, workflows, import namespaces, struct types, or aliases.

```
Array
Boolean
File
Float
Int
Map
None
Object
Pair
String
alias
as
call
command
else
false
if
in
import
input 
left
meta
object
output
parameter_meta
right
runtime 
scatter
struct
task
then
true
version
workflow
```

The following keywords should also be considered as reserved - they are not used in the current version of the specification, but they will be used in a future version:

```
Directory
hints
requirements
```

### Types

A [declaration](#declarations) is a name that the user reserves in a given [scope](#appendix-b-wdl-namespaces-and-scopes) to hold a value of a certain type. In WDL *all* declarations (including inputs and outputs) must be typed. This means that the information about the type of data that may be held by each declarations must be specified explicitly.

In WDL *all* types represent immutable values. For example, a `File` represents a logical "snapshot" of the file at the time when the value was created. It is impossible for a task to change an upstream value that has been provided as an input - even if it modifies its local copy, the original value is unaffected.

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

<details>
  <summary>
  Example: primitive_literals.wdl
  
  ```wdl
  version 1.1

  task write_file_task {
    command <<<
    echo "hello" > hello.txt
    >>>

    output {
      File x = "hello.txt"
    }
  }

  workflow primitive_literals {
    call write_file_task

    output {
      Boolean b = true 
      Int i = 0
      Float f = 27.3
      String s = "hello, world"
      File x = write_file_task.x
    }  
  }
  ```
  </summary>
  <p>
  Example input:
  
  ```json
  {}
  ```
  
  Example output:
  
  ```json
  {
    "primitive_literals.b": true,
    "primitive_literals.i": 0,
    "primitive_literals.f": 27.3,
    "primitive_literals.s": "hello, world",
    "primitive_literals.x": "hello.txt"
  }
  ```
  </p>
</details>

#### Optional Types and None

A type may have a `?` postfix quantifier, which means that its value is allowed to be undefined without causing an error. A declaration with an optional type can only be used in calls or functions that accept optional values.

WDL has a special value `None` whose meaning is "an undefined value". The `None` value has the (hidden) type [`Union`](#hidden-types), meaning `None` can be assigned to an optional declaration of any type.

An optional declaration has a default initialization of `None`, which indicates that it is undefined. An optional declaration may be initialized to any literal or expression of the correct type, including the special `None` value.

<details>
  <summary>
  Example: optionals.wdl
  
  ```wdl
  version 1.1

  workflow optionals {
    input {
      Int certainly_five = 5      # an non-optional declaration
      Int? maybe_five_and_is = 5  # a defined optional declaration

      # the following are equivalent undefined optional declarations
      String? maybe_five_but_is_not
      String? also_maybe_five_but_is_not = None
    }

    output {
      Boolean test_defined = defined(maybe_five_but_is_not) # Evaluates to false
      Boolean test_defined2 = defined(maybe_five_and_is)    # Evaluates to true
      Boolean test_is_none = maybe_five_but_is_not == None  # Evaluates to true
      Boolean test_not_none = maybe_five_but_is_not != None # Evaluates to false
    }
  }
  ```
  </summary>
  <p>
  Example input:
  
  ```json
  {}
  ```
  
  Example output:
  
  ```json
  {
    "optionals.test_defined": false,
    "optionals.test_defined2": true,
    "optionals.test_is_none": true,
    "optionals.test_not_none": false,
  }
  ```
  </p>
</details>

For more details, see the sections on [Input Type Constraints](#input-type-constraints) and [Optional Inputs with Defaults](#optional-inputs-with-defaults).

#### Compound Types

A compound type is one that contains nested types, i.e. it is *parameterized* by other types. The following compound types can be constructed. In the examples below `P` represents any of the primitive types above, and `X` and `Y` represent any valid type (including nested compound types).

##### Array[X]

An `Array` represents an ordered list of elements that are all of the same type. An array is insertion ordered, meaning the order in which elements are added to the `Array` is preserved.

An array value can be initialized with an array literal - a comma-separated list of values in brackets (`[]`). A specific zero-based index of an `Array` can be accessed by placing the index in brackets after the declaration name. Accessing a non-existent index of an `Array` results in an error.

<details>
  <summary>
  Example: array_access.wdl
  
  ```wdl
  version 1.1

  workflow array_access {
    input {
      Array[String] strings
      Int index
    }

    output {
      String s = strings[index]
    }
  }
  ```
  </summary>
  <p>
  Example input:
  
  ```json
  {
    "array_access.strings": ["hello", "world"],
    "array_access.index": 0
  }
  ```
  
  Example output:
  
  ```json
  {
    "array_access.s": "hello"
  }
  ```
  </p>
</details>

<details>
  <summary>
  Example: empty_array_fail.wdl
  
  ```wdl
  version 1.1
  
  workflow empty_array_fail {
    Array[Int] empty = []
    
    output {
      # this causes an error - trying to access a non-existent array element
      Int i = empty[0]
    }

    meta {
     test_config: "fail"
    }
  }
  ```
  </summary>
  <p>
  Example input:
  
  ```json
  {}
  ```
  
  Example output:
  
  ```json
  ```
  </p>
</details>

An `Array` may have an empty value (i.e. an array of length zero), unless it is declared using `+`, the non-empty postfix quantifier, which represents a constraint that the `Array` value must contain one-or-more elements. For example, the following task operates on an `Array` of `File`s and it requires at least one file to function:

<details>
<summary>
Example: sum_task.wdl

```wdl
version 1.1

task sum {
  input {
    Array[Int]+ ints
  }
  
  command <<<
  echo ~{sep(" ", ints)} | awk '{tot=0; for(i=1;i<=NF;i++) tot+=$i; print tot}'
  >>>
  
  output {
    Int total = read_int(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{
  "sum.ints": [0, 1, 2]
}
```

Example output:

```json
{
  "sum.total": 3
}
```
</p>
</details>

Recall that a type may have an optional postfix quantifier (`?`), which means that its value may be undefined. The `+` and `?` postfix quantifiers can be combined to declare an `Array` that is either undefined or non-empty, i.e. it can have any value *except* the empty array.

Attempting to assign an empty array literal to a non-empty `Array` declaration results in an error. Otherwise, the non-empty assertion is only checked at runtime: binding an empty array to an `Array[T]+` input or function argument is a runtime error. 


<details>
<summary>
Example: non_empty_optional.wdl

```wdl
version 1.1

workflow non_empty_optional {
  output {
    # array that must contain at least one Float
    Array[Float]+ nonempty1 = [0.0]
    # array that must contain at least one Int? (which may have an undefined value)
    Array[Int?]+ nonempty2 = [None, 1]
    # array that can be undefined or must contain at least one Int
    Array[Int]+? nonempty3
    Array[Int]+? nonempty4 = [0.0]
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "non_empty_optional.nonempty1": [0.0],
  "non_empty_optional.nonempty2": [null, 1],
  "non_empty_optional.nonempty3": [],
  "non_empty_optional.nonempty4": [0.0],
}
```
</p>
</details>

<details>
<summary>
Example: non_empty_optional_fail.wdl

```wdl
version 1.1

workflow non_empty_optional_fail {
  # these both cause an error - can't assign empty array value to non-empty Array type
  Array[Boolean]+ nonempty3 = []
  Array[Int]+? nonempty6 = [] 

  meta {
    test_config: "fail"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{}
```
</p>
</details>

For more details see the section on [Input Type Constraints](#input-type-constraints).

##### Pair[X, Y]

A `Pair` represents two associated values, which may be of different types. In other programming languages, a `Pair` might be called a "two-tuple".

A `Pair` can be initialized with a pair literal - a comma-separated pair of values in parentheses (`()`). The components of a `Pair` value are accessed using its `left` and `right` accessors.

<details>
<summary>
Example: test_pairs.wdl

```wdl
verison 1.1

workflow test_pairs {
  Pair[Int, Array[String]] data = (5, ["hello", "goodbye"])
  output {
    Int five = p.left  # evaluates to 5
    String hello = data.right[0]  # evaluates to "hello"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_pairs.five": 5,
  "test_pairs.hello": "hello"
}
```
</p>
</details>

##### Map[P, Y]

A `Map` represents an associative array of key-value pairs. All of the keys must be of the same (primitive) type, and all of the values must be of the same type, but keys and values can be different types.

A `Map` can be initialized with a map literal - a comma-separated list of key-value pairs in braces (`{}`), where key-value pairs are delimited by `:`. The value of a specific key can be accessed by placing the key in brackets after the declaration name. Accessing a non-existent key of a `Map` results in an error.

<details>
<summary>
Example: test_map.wdl

```wdl
verison 1.1

workflow test_map {
  Map[Int, Int] int_to_int = {1: 10, 2: 11}
  Map[String, Int] string_to_int = { "a": 1, "b": 2 }
  Map[File, Array[Int]] file_to_ints = {
    "/path/to/file1": [0, 1, 2],
    "/path/to/file2": [9, 8, 7]
  }

  output {
    Int ten = int_to_int[1]  # evaluates to 10
    Int b = string_to_int["b"]  # evaluates to 2
    Array[Int] ints = file_to_ints["/path/to/file1"]  # evaluates to [0, 1, 2]
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_map.ten": 10,
  "test_map.b": 2,
  "test_map.ints": [0, 1, 2]
}
```
</p>
</details>

<details>
<summary>
Example: test_map_fail.wdl

```wdl
verison 1.1

workflow test_map_fail {
  Map[String, Int] string_to_int = { "a": 1, "b": 2 }
  Int c = string_to_int["c"]  # error - "c" is not a key in the map

  meta {
    test_config: "fail"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{}
```
</p>
</details>

A `Map` is insertion-ordered, meaning the order in which elements are added to the `Map` is preserved, for example when [✨ converting a `Map` to an array of `Pair`s](#-as_pairs).

<details>
<summary>
Example: test_map_ordering.wdl

```wdl
verison 1.1

workflow test_map_ordering {
  # declaration using a map literal
  Map[Int, Int] int_to_int = { 2: 5, 1: 10 }

  scatter (ints in as_pairs(int_to_int)) {
    Array[Int] i = [ints.left, ints.right]
  }

  output {
    # evaluates to [[2, 5], [1, 10]]
    Array[Array[Int]] ints = i
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_map_ordering.ints": [[2, 5], [1, 10]]
}
```
</p>
</details>

##### Custom Types (Structs)

WDL provides the ability to define custom compound types called [structs](#struct-definition). `Struct` types are defined directly in the WDL document and are usable like any other type. A `struct` definition contains any number of declarations of any types, including other `Struct`s.

A struct is defined using the `struct` keyword, followed by a unique name, followed by member declarations within braces. A declaration with a custom type can be initialized with a struct literal, which begins with the `Struct` type name followed by a comma-separated list of name-value pairs in braces (`{}`), where name-value pairs are delimited by `:`. The member names in a struct literal are not quoted.

The value of a specific member of a `Struct` value can be accessed by placing a `.` followed by the member name after the identifier.

<details>
<summary>
Example: test_struct.wdl

```wdl
version 1.1

struct Person {
  String name
  Phone? phone
}

struct Phone {
  Int exchange
  Int number
  Int? extension
}

workflow test_struct {
  output {
    Person person = Person {
      name: "John",
      phone: {
        exchange: 123,
        number: 4567890
      }
    }
    Boolean has_extension = defined(person.extension)
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_struct.person": {
    "name": "John",
    "phone": {
      "exchange": 123,
      "number": 4567890
    }
  },
  "test_struct.has_extension": false
}
```
</p>
</details>

##### 🗑 Object

An `Object` is an unordered associative array of name-value pairs, where values may be of any type and are not defined explicitly.

An `Object` can be initialized using syntax similar to a struct literal, except that the `object` keyword is used in place of the `Struct` name. The value of a specific member of an `Object` value can be accessed by placing a `.` followed by the member name after the identifier.

<details>
<summary>
Example: test_object.wdl

```wdl
version 1.1

workflow test_object {
  output {
    Object obj = object {
      a: 10,
      b: "hello"
    }
    Int i = f.a
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_object.obj": {
    "a": 10,
    "b": "hello"
  },
  "test_object.i": 10
}
```
</p>
</details>

Due to the lack of explicitness in the typing of `Object` being at odds with the goal of being able to know the type information of all WDL declarations, the use of the `Object` type and the `object` literal syntax have been deprecated. In WDL 2.0, `Object` will become a [hidden type](#hidden-types) that may only be instantiated by the runtime engine. `Object` declarations can be replaced with use of [structs](#struct-definition).

#### Hidden Types

A hidden type is one that may only be instantiated by the runtime engine, and cannot be used in a declaration within a WDL file. There is currently only one hidden type, `Union`; however, in WDL 2.0, `Object` will also become a hidden type.

##### Union

The `Union` type is used for a value that may have any one of several concrete types. A `Union` value must always be coerced to a concrete type. The `Union` type is used in two contexts:

* It is the type of the special [`None`](#optional-types-and-none) value.
* It is the return type of some standard library functions, such as [`read_json`](#read_json).

#### Type Conversion

WDL has some limited facilities for converting a value of one type to another type. Some of these are explicitly provided by [standard library](#standard-library) functions, while others are [implicit](#type-coercion). When converting between types, it is best to be explicit whenever possible, even if an implicit conversion is allowed.

The execution engine is also responsible for converting (or "serializing") input values when constructing commands, as well as "deserializing" command outputs. For more information, see the [Command Section](#command-section) and the more extensive Appendix on [WDL Value Serialization and Deserialization](#appendix-a-wdl-value-serialization-and-deserialization).

##### Primitive Conversion to String 

Primitive types can always be converted to `String` using [string interpolation](#expression-placeholders-and-string-interpolation). See [Expression Placeholder Coercion](#expression-placeholder-coercion) for details.

<details>
<summary>
Example: primitive_to_string.wdl

```wdl
version 1.1

workflow primitive_to_string {
  input {
    Int i = 5
  }

  output {
    String istring = "~{i}"
  }
}
```
</summary>
<p>
Example input:

```json
{
  "primitive_to_string.i": 3
}
```

Example output:

```json
{
  "primitive_to_string.istring": "3"
}
```
</p>
</details>

##### Type Coercion

There are some pairs of WDL types for which there is an obvious, unambiguous conversion from one to the other. In these cases, WDL provides an automatic conversion (called "coercion") from one type to the other, such that a value of one type typically can be used anywhere the other type is expected.

For example, file paths are always represented as strings, making the conversion from `String` to `File` obvious and unambiguous.

<details>
<summary>
Example: string_to_file.wdl

```wdl
version 1.1

workflow string_to_file {
  String path1 = "/path/to/file"
  File path2 = "/path/to/file"

  # valid - String coerces unambiguously to File
  File path3 = path1

  output {
    Boolean string_equals_path = path1 == path2
    Boolean paths_equal = path2 == path3
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "string_to_file.string_equals_path": true,
  "string_to_file.paths_equal": true
}
```
</p>
</details>

The table below lists all globally valid coercions. The "target" type is the type being coerced to (this is often called the "left-hand side" or "LHS" of the coercion) and the "source" type is the type being coerced from (the "right-hand side" or "RHS").

| Target Type      | Source Type      | Notes/Constraints                                                                                              |
| ---------------- | ---------------- | -------------------------------------------------------------------------------------------------------------- |
| `File`           | `String`         |                                                                                                                |
| `Float`          | `Int`            | May cause overflow error                                                                                       |
| `Y?`             | `X`              | `X` must be coercible to `Y`                                                                                   |
| `Array[Y]`       | `Array[X]`       | `X` must be coercible to `Y`                                                                                   |
| `Array[Y]`       | `Array[X]+`      | `X` must be coercible to `Y`                                                                                   |
| `Map[X, Z]`      | `Map[W, Y]`      | `W` must be coercible to `X` and `Y` must be coercible to `Z`                                                  |
| `Pair[X, Z]`     | `Pair[W, Y]`     | `W` must be coercible to `X` and `Y` must be coercible to `Z`                                                  |
| `Struct`         | `Map[String, Y]` | `Map` keys must match `Struct` member names, and all `Struct` members types must be coercible from `Y`         |
| `Map[String, Y]` | `Struct`         | All `Struct` members must be coercible to `Y`                                                                  |
| `Object`         | `Map[String, Y]` |                                                                                                                |
| `Map[String, Y]` | `Object`         | All object values must be coercible to `Y`                                                                     |
| `Object`         | `Struct`         |                                                                                                                |
| `Struct`         | `Object`         | `Object` keys must match `Struct` member names, and `Object` values must be coercible to `Struct` member types |

The [`read_lines`](#read_lines) function presents a special case in which the `Array[String]` value it returns may be immediately coerced into other `Array[P]` values, where `P` is a primitive type. See [Appendix A](#array-deserialization-using-read_lines) for details and best practices.

###### Order of Precedence

During string interpolation, there are some operators for which it is possible to coerce the same arguments in multiple different ways. For such operators, it is necessary to define the order of precedence so that a single function prototype can be selected from among the available options for any given set of arguments.

The `+` operator is overloaded for both numeric addition and `String` concatenation. This can lead to the following kinds of situations:

```
String s = "1.0"
Float f = 2.0
String x = "~{s + f}"
```

There are two possible ways to evaluate the `s + f` expression:

1. Coerce `s` to `Float` and perform floating point addition, then coerce to `String` with the result being `x = "3.0"`.
2. Coerce `f` to `String` and perform string concatenation with result being `x = "1.02.0"`.

Similarly, the equality/inequality operators can be applied to any primitive type.

The order of precedence is:

1. `Int`, `Float`: `Int` coerces to `Float`
2. `X`, `Y`: For any primitive types `X` != `Y`, both are coerced to `String`
3. If applying `+` to two values of the same type that cannot otherwise be summed/concatenated (i.e., `Boolean`, `File`, `Directory`), both values are first coerced to `String`

###### Coercion of Optional Types

A non-optional type `T` can always be coerced to an optional type `T?`, but the reverse is not true - coercion from `T?` to `T` is not allowed because the latter cannot accept `None`.

This constraint propagates into compound types. For example, an `Array[T?]` can contain both optional and non-optional elements. This facilitates the common idiom [`select_first([expr, default])`](#select_first), where `expr` is of type `T?` and `default` is of type `T`, for converting an optional type to a non-optional type. However, an `Array[T?]` could not be passed to the [`sep`](#-sep) function, which requires an `Array[T]`.

There are two exceptions where coercion from `T?` to `T` is allowed:

* [String concatenation in expression placeholders](#concatenation-of-optional-values)
* [Equality and inequality comparisons](#equality-and-inequality-comparison-of-optional-types)

###### Struct/Object coercion from Map

`Struct`s and `Object`s can be coerced from map literals, but beware the difference between `Map` keys (expressions) and `Struct`/`Object` member names.

<details>
<summary>
Example: map_to_struct.wdl

```wdl
version 1.1

struct Words {
  Int a
  Int b
  Int c
}

workflow map_to_struct {
  String a = "beware"
  String b = "key"
  String c = "lookup"

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
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "map_to_struct.literal_syntax": {
    "a": 10,
    "b": 11,
    "c": 12
  },
  "map_to_struct.map_coercion": {
    "beware": 10,
    "key": 11,
    "lookup": 12
  }
}
```
</p>
</details>

- If a `Struct` (or `Object`) declaration is initialized using the struct-literal (or object-literal) syntax `Words literal_syntax = Words { a: ...` then the keys will be `"a"`, `"b"` and `"c"`.
- If a `Struct` (or `Object`) declaration is initialized using the map-literal syntax `Words map_coercion = { a: ...` then the keys are expressions, and thus `a` will be a variable reference to the previously defined `String a = "beware"`.

###### 🗑 Limited exceptions

Implementers may choose to allow limited exceptions to the above rules, with the understanding that workflows depending on these exceptions may not be portable. These exceptions are provided for backward-compatibility, are considered deprecated, and will be removed in a future version of WDL.

* `Float` to `Int`, when the coercion can be performed with no loss of precision, e.g. `1.0 -> 1`.
* `String` to `Int`/`Float`, when the coercion can be performed with no loss of precision.
* `X?` may be coerced to `X`, and an error is raised if the value is undefined.
* `Array[X]` to `Array[X]+`, when the array is non-empty (an error is raised otherwise).
* `Map[W, X]` to `Array[Pair[Y, Z]]`, in the case where `W` is coercible to `Y` and `X` is coercible to `Z`.
* `Array[Pair[W, X]]` to `Map[Y, Z]`, in the case where `W` is coercible to `Y` and `X` is coercible to `Z`.
* `Map` to `Object`, in the case of `Map[String, X]`.
* `Map` to struct, in the case of `Map[String, X]` where all members of the struct have type `X`.
* `Object` to `Map[String, X]`, in the case where all object values are of (or are coercible to) the same type.

### Declarations

```txt
$declaration = $type $identifier ('=' $expression)?
```

A declaration reserves a name that can be referenced anywhere in the [scope](#appendix-b-wdl-namespaces-and-scopes) where it is declared. A declaration has a type, a name, and an optional initialization. Each declaration must be unique within its scope, and may not collide with a [reserved WDL keyword](#reserved-keywords) (e.g., `workflow`, or `input`).

A [task](#task-definition) or [workflow](#workflow-definition) may declare input parameters within its `input` section and output parameters within its `output` section. If a non-optional input declaration does not have an initialization, it is considered a "required" parameter, and its value must be provided by the user before the workflow or task may be run. Declarations may also appear in the body of a task or workflow. All non-input declarations must be initialized.

<details>
<summary>
Example: declarations.wdl

```wdl
version 1.1

workflow declarations {
  input {
    # these "unbound" declarations are only allowed in the input section
    File? x  # optional - defaults to None
    Map[String, String] m  # required
    # this is a "bound" declaration
    String y = "abc"  
  }

  Int i = 1 + 2  # Private declarations must be bound

  output {
    Float pi = i + .14  # output declarations must also be bound
  }
}
```
</summary>
<p>
Example input:

```json
{
  "declarations.m": {"a": "b"}
}
```

Example output:

```json
{
  "declarations.pi": 3.14
}
```
</p>
</details>

A declaration may be initialized with a literal value or an [expression](#expressions), which includes the ability to refer to elements that are outputs of tasks.

<details>
<summary>
Example: task_outputs.wdl

```wdl
version 1.1

task greet {
  input {
    String name
  }
  
  command <<<
    echo "Hello ~{name}"
  >>>

  output {
    String greeting = read_string(stdout())
  }
}

task count_lines {
  input {
    Array[String] array
  }

  command <<<
    wc -l ~{write_lines(array)}
  >>>
  
  output {
    Int line_count = read_int(stdout())
  }
}

workflow task_outputs {
  call greet as x {
    input: name="John"
  }
  
  call greet as y {
    input: name="Sarah"
  }

  Array[String] greetings = [x.greeting, y.greeting]
  call count_lines {
    input: array=greetings
  }

  output {
    Int num_greetings = count_lines.line_count
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "task_outputs.num_greetings": 2
}
```
</p>
</details>

In this example, `greetings` is undefined until both `call greet as x` and `call greet as y` have successfully completed, at which point it is assigned the result of evaluating its expression. If either of the two tasks fail, the workflow would also fail and `greetings` would never be initialized.

It must be possible to organize all of the statements within a scope into a directed acyclic graph (DAG); thus, circular references between declarations are not allowed. The following example would result in an error due to the presence of a circular reference.

<details>
<summary>
Example: circular.wdl

```wdl
version 1.1

workflow circular {
  Int i = j + 1
  Int j = i - 2

  meta {
    test_config: "fail"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{}
```
</p>
</details>

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

An expression is a compound statement that consists of literal values, identifiers (references to [declarations](#declarations) or [call](#call-statement) outputs), [built-in operators](#built-in-operators) (e.g., `+` or `>=`), and calls to [standard library functions](#standard-library).

A "simple" expression is one that does not make use of identifiers or any function that takes a `File` input or returns a `File` output; i.e., it is an expression that can be evaluated unambiguously without any knowledge of the runtime context. An execution engine may choose to replace simple expressions with their literal values.

<details>
<summary>
Example: expressions_task.wdl

```wdl
version 1.1

task expressions {
  input {
    Int x
  }

  command <<<
  echo -n "hello" > hello.txt
  >>>

  output {
    # simple expressions
    Float f = 1 + 2.2
    Boolean b = if 1 > 2 then true else false
    Map[String, Int] m = as_map(zip(["a", "b", "c"], [1, 2, 3]))

    # non-simple expressions
    Int i = x + 3  # requires knowing the value of x
    # requires reading a file that might only exist at runtime
    String s = read_string("hello.txt")
  }
}
```
</summary>
<p>
Example input:

```json
{
  "expressions.x": 5
}
```

Example output:

```json
{
  "expressions.f": 3.2,
  "expressions.b": false,
  "expressions.m": {
    "a": 1,
    "b": 2,
    "c": 3
  },
  "expressions.i": 8,
  "expressions.s": "hello"
}
```
</p>
</details>

#### Built-in Operators

WDL provides the standard unary and binary mathematical and logical operators. The following tables list the valid operand and result type combinations for each operator. Using an operator with unsupported types results in an error.

In operations on mismatched numeric types (e.g., `Int` + `Float`), the `Int` is first coerced to `Float`, and the result type is `Float`. This may result in loss of precision, for example if the `Int` is too large to be represented exactly by a `Float`. A `Float` can be converted to `Int` with the [`ceil`](#ceil), [`round`](#round), or [`floor`](#floor) functions.

##### Unary Operators

| Operator | RHS Type  | Result    |
| -------- | --------- | --------- |
| `-`      | `Float`   | `Float`   |
| `-`      | `Int`     | `Int`     |
| `!`      | `Boolean` | `Boolean` |

##### Binary Operators on Primitive Types

| LHS Type    | Operator | RHS Type  | Result    | Semantics                                                |
| ----------- | -------- | --------- | --------- | -------------------------------------------------------- |
| `Boolean`   | `==`     | `Boolean` | `Boolean` |                                                          |
| `Boolean`   | `!=`     | `Boolean` | `Boolean` |                                                          |
| `Boolean`   | `\|\|`   | `Boolean` | `Boolean` |                                                          |
| `Boolean`   | `&&`     | `Boolean` | `Boolean` |                                                          |
| 🗑 `Boolean` | `>`      | `Boolean` | `Boolean` | true is greater than false                               |
| 🗑 `Boolean` | `>=`     | `Boolean` | `Boolean` | true is greater than false                               |
| 🗑 `Boolean` | `<`      | `Boolean` | `Boolean` | true is greater than false                               |
| 🗑 `Boolean` | `<=`     | `Boolean` | `Boolean` | true is greater than false                               |
| `Int`       | `+`      | `Int`     | `Int`     |                                                          |
| `Int`       | `-`      | `Int`     | `Int`     |                                                          |
| `Int`       | `*`      | `Int`     | `Int`     |                                                          |
| `Int`       | `/`      | `Int`     | `Int`     | Integer division                                         |
| `Int`       | `%`      | `Int`     | `Int`     | Integer division, return remainder                       |
| `Int`       | `==`     | `Int`     | `Boolean` |                                                          |
| `Int`       | `!=`     | `Int`     | `Boolean` |                                                          |
| `Int`       | `>`      | `Int`     | `Boolean` |                                                          |
| `Int`       | `>=`     | `Int`     | `Boolean` |                                                          |
| `Int`       | `<`      | `Int`     | `Boolean` |                                                          |
| `Int`       | `<=`     | `Int`     | `Boolean` |                                                          |
| 🗑 `Int`     | `+`      | `String`  | `String`  |                                                          |
| `Int`       | `+`      | `Float`   | `Float`   |                                                          |
| `Int`       | `-`      | `Float`   | `Float`   |                                                          |
| `Int`       | `*`      | `Float`   | `Float`   |                                                          |
| `Int`       | `/`      | `Float`   | `Float`   |                                                          |
| `Int`       | `==`     | `Float`   | `Boolean` |                                                          |
| `Int`       | `!=`     | `Float`   | `Boolean` |                                                          |
| `Int`       | `>`      | `Float`   | `Boolean` |                                                          |
| `Int`       | `>=`     | `Float`   | `Boolean` |                                                          |
| `Int`       | `<`      | `Float`   | `Boolean` |                                                          |
| `Int`       | `<=`     | `Float`   | `Boolean` |                                                          |
| `Float`     | `+`      | `Float`   | `Float`   |                                                          |
| `Float`     | `-`      | `Float`   | `Float`   |                                                          |
| `Float`     | `*`      | `Float`   | `Float`   |                                                          |
| `Float`     | `/`      | `Float`   | `Float`   |                                                          |
| `Float`     | `%`      | `Float`   | `Float`   |                                                          |
| `Float`     | `==`     | `Float`   | `Boolean` |                                                          |
| `Float`     | `!=`     | `Float`   | `Boolean` |                                                          |
| `Float`     | `>`      | `Float`   | `Boolean` |                                                          |
| `Float`     | `>=`     | `Float`   | `Boolean` |                                                          |
| `Float`     | `<`      | `Float`   | `Boolean` |                                                          |
| `Float`     | `<=`     | `Float`   | `Boolean` |                                                          |
| 🗑 `Float`   | `+`      | `String`  | `String`  |                                                          |
| `Float`     | `+`      | `Int`     | `Float`   |                                                          |
| `Float`     | `-`      | `Int`     | `Float`   |                                                          |
| `Float`     | `*`      | `Int`     | `Float`   |                                                          |
| `Float`     | `/`      | `Int`     | `Float`   |                                                          |
| `Float`     | `%`      | `Int`     | `Float`   |                                                          |
| `Float`     | `==`     | `Int`     | `Boolean` |                                                          |
| `Float`     | `!=`     | `Int`     | `Boolean` |                                                          |
| `Float`     | `>`      | `Int`     | `Boolean` |                                                          |
| `Float`     | `>=`     | `Int`     | `Boolean` |                                                          |
| `Float`     | `<`      | `Int`     | `Boolean` |                                                          |
| `Float`     | `<=`     | `Int`     | `Boolean` |                                                          |
| `String`    | `+`      | `String`  | `String`  | Concatenation                                            |
| `String`    | `+`      | `File`    | `File`    |                                                          |
| `String`    | `==`     | `String`  | `Boolean` | Unicode comparison                                       |
| `String`    | `!=`     | `String`  | `Boolean` | Unicode comparison                                       |
| `String`    | `>`      | `String`  | `Boolean` | Unicode comparison                                       |
| `String`    | `>=`     | `String`  | `Boolean` | Unicode comparison                                       |
| `String`    | `<`      | `String`  | `Boolean` | Unicode comparison                                       |
| `String`    | `<=`     | `String`  | `Boolean` | Unicode comparison                                       |
| 🗑 `String`  | `+`      | `Int`     | `String`  |                                                          |
| 🗑 `String`  | `+`      | `Float`   | `String`  |                                                          |
| `File`      | `==`     | `File`    | `Boolean` |                                                          |
| `File`      | `!=`     | `File`    | `Boolean` |                                                          |
| `File`      | `==`     | `String`  | `Boolean` |                                                          |
| `File`      | `!=`     | `String`  | `Boolean` |                                                          |
| 🗑 `File`    | `+`      | `File`    | `File`    | append file paths - error if second path is not relative |
| 🗑 `File`    | `+`      | `String`  | `File`    | append file paths - error if second path is not relative |

WDL `String`s are compared by the unicode values of their corresponding characters. Character `a` is less than character `b` if it has a lower unicode value.

Except for `String + File`, all concatenations between `String` and non-`String` types are deprecated and will be removed in WDL 2.0. The same effect can be achieved using [string interpolation](#expression-placeholders-and-string-interpolation).

##### Equality of Compound Types

| LHS Type | Operator | RHS Type | Result    |
| -------- | -------- | -------- | --------- |
| `Array`  | `==`     | `Array`  | `Boolean` |
| `Array`  | `!=`     | `Array`  | `Boolean` |
| `Map`    | `==`     | `Map`    | `Boolean` |
| `Map`    | `!=`     | `Map`    | `Boolean` |
| `Pair`   | `==`     | `Pair`   | `Boolean` |
| `Pair`   | `!=`     | `Pair`   | `Boolean` |
| `Struct` | `==`     | `Struct` | `Boolean` |
| `Struct` | `!=`     | `Struct` | `Boolean` |
| `Object` | `==`     | `Object` | `Boolean` |
| `Object` | `!=`     | `Object` | `Boolean` |

In general, two compound values are equal if-and-only-if all of the following are true:

1. They are of the same type.
2. They are the same length.
3. All of their contained elements are equal.

Since `Array`s and `Map`s are ordered, the order of their elements are also compared. For example:

<details>
<summary>
Example: array_map_equality.wdl

```wdl
version 1.1

workflow array_map_equality {
  output {
    # arrays and maps with the same elements in the same order are equal
    Boolean is_true1 = [1, 2, 3] == [1, 2, 3]
    Boolean is_true2 = {"a": 1, "b": 2} == {"a": 1, "b": 2}

    # arrays and maps with the same elements in different orders are not equal
    Boolean is_false1 = [1, 2, 3] == [2, 1, 3]
    Boolean is_false2 = {"a": 1, "b": 2} == {"b": 2, "a": 1}
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "array_map_equality.is_true1": true,
  "array_map_equality.is_true2": true,
  "array_map_equality.is_false1": true,
  "array_map_equality.is_false2": true,
}
```
</p>
</details>

[Type coercion](#type-coercion) can be employed to compare values of different but compatible types.

<details>
<summary>
Example: compare_coerced.wdl

```wdl
version 1.1

workflow compare_coerced {
  Array[Int] i = [1, 2, 3]
  Array[Float] f = [1.0, 2.0, 3.0]

  output {
    # Ints are automatically coerced to Floats for comparison
    Boolean is_true = i == f
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "compare_coerced.is_true": true
}
```
</p>
</details>

##### Equality and Inequality Comparison of Optional Types

The equality and inequality operators are exceptions to the general rules on [coercion of optional types](#coercion-of-optional-types). Either or both operands of an equality or inequality comparison can be optional, considering that `None` is equal to itself but no other value.

<details>
<summary>
Example: compare_optionals.wdl

```wdl
version 1.1

workflow compare_optionals {
  Int i = 1
  Int? j = 1
  Int? k = None

  output {
    # equal values of the same type are equal even if one is optional
    Boolean is_true1 = i == j
    # k is undefined (None), and so is only equal to None
    Boolean is_true2 k == None
    # these comparisons are valid and evaluate to false
    Boolean is_false1 = i == k
    Boolean is_false2 j == k
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "compare_optionals.is_true1": true,
  "compare_optionals.is_true2": true,
  "compare_optionals.is_false1": false,
  "compare_optionals.is_false2": false,
}
```
</p>
</details>

#### Operator Precedence Table

| Precedence | Operator type         | Associativity | Example      |
| ---------- | --------------------- | ------------- | ------------ |
| 11         | Grouping              | n/a           | `(x)`        |
| 10         | Member Access         | left-to-right | `x.y`        |
| 9          | Index                 | left-to-right | `x[y]`       |
| 8          | Function Call         | left-to-right | `x(y,z,...)` |
| 7          | Logical NOT           | right-to-left | `!x`         |
|            | Unary Negation        | right-to-left | `-x`         |
| 6          | Multiplication        | left-to-right | `x*y`        |
|            | Division              | left-to-right | `x/y`        |
|            | Remainder             | left-to-right | `x%y`        |
| 5          | Addition              | left-to-right | `x+y`        |
|            | Subtraction           | left-to-right | `x-y`        |
| 4          | Less Than             | left-to-right | `x<y`        |
|            | Less Than Or Equal    | left-to-right | `x<=y`       |
|            | Greater Than          | left-to-right | `x>y`        |
|            | Greater Than Or Equal | left-to-right | `x>=y`       |
| 3          | Equality              | left-to-right | `x==y`       |
|            | Inequality            | left-to-right | `x!=y`       |
| 2          | Logical AND           | left-to-right | `x&&y`       |
| 1          | Logical OR            | left-to-right | `x\|\|y`     |

#### Member Access

The syntax `x.y` refers to member access. `x` must be a `Struct` or `Object` value, or a call in a workflow. A call can be thought of as a struct where the members are the outputs of the called task.


<details>
<summary>
Example: member_access.wdl

```wdl
version 1.1

struct MyType {
  String s
}

task foo {
  output {
    String bar = "bar"
  }
}

workflow member_access {
  # task foo has an output y
  call foo
  MyType my = MyType { s: "hello" }

  output {
    String bar = foo.bar
    String hello = my.s
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "member_access.bar": "bar",
  "member_access.hello": "hello"
}
```
</p>
</details>

#### Ternary operator (if-then-else)

This operator takes three arguments: a condition expression, an if-true expression, and an if-false expression. The condition is always evaluated. If the condition is true then the if-true value is evaluated and returned. If the condition is false, the if-false expression is evaluated and returned. The if-true and if-false expressions must return values of the same type, such that the value of the if-then-else is the same regardless of which side is evaluated.

<details>
<summary>
Example: ternary.wdl

```wdl
version 1.1

task mem {
  input {
    Array[String] array
  }
  Int array_length = length(array)
  # choose how much memory to use for a task
  String memory = if array_length > 100 then "2GB" else "1GB"

  command <<<
  >>>

  runtime {
    memory: memory
  }
}

workflow ternary {
  input {
    Boolean morning
  }

  call mem { input: ["x", "y", "z"] }

  output {
    # Choose whether to say "good morning" or "good afternoon"
    String greeting = "good ~{if morning then "morning" else "afternoon}"
  }
}
```
</summary>
<p>
Example input:

```json
{
  "ternary.morning": true
}
```

Example output:

```json
{
  "ternary.greeting": "good morning"
}
```
</p>
</details>

#### Function Calls

WDL provides a [standard library](#standard-library) of functions. These functions can be called using the syntax `func(p1, p2, ...)`, where `func` is the function name and `p1` and `p2` are parameters to the function.

#### Expression Placeholders and String Interpolation

Any WDL string expression may contain one or more "placeholders" of the form `~{*expression*}`, each of which contains a single expression. Placeholders of the form `${*expression*}` may also be used interchangably, but their use is discouraged for reasons discussed in the [command section](#expression-placeholders) and may be deprecated in a future version of the specification.

When a string expression is evaluated, its placeholders are evaluated first, and their values are then substituted for the placeholders in the containing string.

<details>
<summary>
Example: placeholders.wdl

```wdl
version 1.1

workflow placeholders {
  input {
    Int i = 3
    String start
    String end
    String input
  }

  output {
    String s = "~{1 + i}"
    String command = "grep '~{start}...~{end}' ~{input}"
  }
}
```
</summary>
<p>
Example input:

```json
{
  "placeholders.start": "h",
  "placeholders.end": "o",
  "placeholders.input": "hello"
}
```

Example output:

```json
{
  "placeholders.command": "grep 'h...o' hello"
}
```
</p>
</details>

In the above example, `command` would be parsed and evaluated as:

1. `grep '`: literal string
2. `~{start}`: identifier expression, replaced with the value of `start`
3. `...`: literal string
4. `~{end}`: identifier expression, replaced with the value of `end`
5. `' `: literal string
6. `~{input}`: identifier expression, replaced with the value of `input`
7. Final string value created by concatenating 1-6

Placeholders may contain other placeholders to any level of nesting, and placeholders are evaluated recursively in a depth-first manner. Placeholder expressions are anonymous, i.e., they have no name and thus cannot be referenced by other expressions, but they can reference declarations and call outputs.

<details>
<summary>
Example: nested_placeholders.wdl

```wdl
version 1.1

workflow nested_placeholders {
  input {
    Int i
    Boolean b
  }

  output {
    String s = "~{if b then '~{1 + i}' else '0'}"
  }
}
```
</summary>
<p>
Example input:

```json
{
  "nested_placeholders.i": 3,
  "nested_placeholders.b": true
}
```

Example output:

```json
{
  "nested_placeholders.s": "4"
}
```
</p>
</details>

##### Expression Placeholder Coercion

The result of evaluating an expression in a placeholder must ultimately be converted to a string in order to take the place of the placeholder in the command script. This is immediately possible for WDL primitive types due to automatic conversions ("coercions") that occur only within the context of string interpolation:

- `String` is substituted directly.
- `File` is substituted as if it were a `String`.
- `Int` is formatted without leading zeros (unless the value is `0`), and with a leading `-` if the value is negative.
- `Float` is printed in the style `[-]ddd.dddddd`, with 6 digits after the decimal point.
- `Boolean` is converted to the "stringified" version of its literal value, i.e., `true` or `false`.

Compound types cannot be implicitly converted to strings. To convert an `Array` to a string, use the [`sep`](#-sep) function: `~{sep(",", str_array)}`.

If an expression within a placeholder evaluates to `None`, then the placeholder is replaced by the empty string.

<details>
<summary>
Example: placeholder_coercion.wdl

```wdl
version 1.1

workflow placeholder_coercion {
  File x = "/hij"
  Int? i = None

  output {
    Boolean is_true1 = "~{"abc"}" == "abc"
    Boolean is_true2 = "~{x}" == "/hij"
    Boolean is_true3 = "~{5}" == "5"
    Boolean is_true4 = "~{3.141}" == "3.141000"
    Boolean is_true5 = "~{3.141 * 1E-10}" == "0.000000"
    Boolean is_true6 = "~{3.141 * 1E10}" == "31410000000.000000"
    Boolean is_true7 = "~{i}" == ""
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "placeholder_coercion.is_true1": true,
  "placeholder_coercion.is_true2": true,
  "placeholder_coercion.is_true3": true,
  "placeholder_coercion.is_true4": true,
  "placeholder_coercion.is_true5": true,
  "placeholder_coercion.is_true6": true,
  "placeholder_coercion.is_true7": true,
}
```
</p>
</details>

##### Concatenation of Optional Values

Within expression placeholders the string concatenation operator (`+`) gains the ability to operate on optional values. When applied to two non-optional operands, the result is a non-optional `String`. However, if either operand has an optional type, then the concatenation has type `String?`, and the runtime result is `None` if either operand is `None` (which is then replaced with the empty string).

<details>
<summary>
Example: concat_optional.wdl

```wdl
version 1.1

workflow concat_optional {
  input {
    String saluation = "hello"
    String? name1
    String? name2 = "Fred"
  }

  output {
    # since name1 is undefined, the evaluation of the expression in the placeholder fails, and the
    # value of greeting1 = "nice to meet you!"
    String greeting1 = "~{salutation + ' ' + name1 + ' '}nice to meet you!"

    # since name2 is defined, the evaluation of the expression in the placeholder succeeds, and the
    # value of greeting2 = "hello Fred, nice to meet you!"
    String greeting2 = "~{salutation + ' ' + name2 + ', '}nice to meet you!"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "concat_optional.greeting1": "nice to meet you!",
  "concat_optional.greeting2": "hello Fred, nice to meet you!"
}
```
</p>
</details>

Among other uses, concatenation of optionals can be used to facilitate the formulation of command-line flags. 

<details>
<summary>
Example: flags_task.wdl

```wdl
version 1.1

task flags {
  input {
    File input
    String pattern
    Int? max_matches
  }

  command <<<
    # If `max_matches` is `None`, the command
    # grep -m ~{max_matches} ~{pattern} ~{input}
    # would evaluate to
    # 'grep -m <pattern> <input>', which would be an error.

    # Instead, make both the flag and the value conditional on `max_matches`
    # being defined.
    grep ~{"-m " + max_matches} ~{pattern} ~{input} | wc -l
  >>>

  output {
    String num_matches = read_int(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{
  "flags.input": "greetings.txt",
  "flags.pattern": "world"
}
```

Example output:

```json
{
  "flags.num_matches": 2
}
```
</p>
</details>

#### 🗑 Expression Placeholder Options

Expression placeholder options are `option="value"` pairs that precede the expression within an expression placeholder and customize the interpolation of the WDL value into the containing string expression.

There are three options available. An expression placeholder may have at most one option.

* [`sep`](#sep): convert an array to a string using a delimiter; e.g., `~{sep=", " array_value}`.
* [`true` and `false`](#true-and-false): substitute a value depending on whether a boolean expression is `true` or `false`; e.g., `~{true="--yes" false="--no" boolean_value}`.
* [`default`](#default): substitute a default value for an undefined expression; e.g., `~{default="foo" optional_value}`.

**Expression placeholder options are deprecated and will be removed in WDL 2.0**. In the sections below, each type of placeholder option is described in more detail, including how to replicate its behavior using future-proof syntax.

##### `sep`

`sep` is interpreted as the separator string used to join together the elements of an array. `sep` is only valid if the expression evaluates to an `Array`.

For example, given a declaration `Array[Int] numbers = [1, 2, 3]`, the expression `"python script.py ~{sep=',' numbers}"` yields the value: `python script.py 1,2,3`.

Alternatively, if the command were `"python script.py ~{sep=' ' numbers}"` it would evaluate to: `python script.py 1 2 3`.

Requirements:

* `sep` MUST accept only a string as its value
* `sep` is only allowed if the type of the expression is `Array[P]`

The `sep` option can be replaced with a call to the ✨ [`sep`](#-sep) function:

<details>
<summary>
Example: sep_option_to_function.wdl

```wdl
version 1.1

workflow sep_option_to_function {
  input {
    Array[String] str_array
    Array[Int] int_array
  }
  
  output {
    Boolean is_true1 = "~{sep(' ', str_array)}" == "~{sep=' ' str_array}"
    Boolean is_true2 = "~{sep(',', quote(int_array))}" == "~{sep=',' quote(int_array)}"
  }
}
```
</summary>
<p>
Example input:

```json
{
  "sep_option_to_function.str_array": ["A", "B", "C"],
  "sep_option_to_function.int_array": [1, 2, 3]
}
```

Example output:

```json
{
  "sep_option_to_function.is_true1": true,
  "sep_option_to_function.is_true2": true,
}
```
</p>
</details>

##### `true` and `false`

`true` and `false` convert an expression that evaluates to a `Boolean` into a string literal when the result is `true` or `false`, respectively. 

For example, `"~{true='--enable-foo' false='--disable-foo' allow_foo}"` evaluates the expression `allow_foo` as an identifier and, depending on its value, replaces the entire expression placeholder with either `--enable-foo` or `--disable-foo`.

Both `true` and `false` cases are required. If one case should insert no value then an empty string literal is used, e.g. `"~{true='--enable-foo' false='' allow_foo}"`.

Requirements:

* `true` and `false` values MUST be string literals.
* `true` and `false` are only allowed if the type of the expression is `Boolean`
* Both `true` and `false` cases are required.

The `true` and `false` options can be replaced with the use of an if-then-else expression:

<details>
<summary>
Example: true_false_ternary.wdl

```wdl
version 1.1

workflow true_false_ternary {
  input {
    String message
    Boolean newline
  }

  command <<<
    # these two commands have the same result
    echo ~{true="-n" false="" newline} "~{message}" > result1
    echo ~{if newline then "-n" else ""} "~{message}" > result2
  >>>

  output {
    Boolean is_true = read_string("result1") == read_string("result2")
  }
}
```
</summary>
<p>
Example input:

```json
{
  "true_false_ternary.message": "hello world",
  "true_false_ternary.newline": false
}
```

Example output:

```json
{
  "true_false_ternary.is_true": true
}
```
</p>
</details>

##### `default`

The `default` option specifies a value to substitute for an optional-typed expression with an undefined value.

Requirements:

* The type of the default value must match the type of the expression
* The type of the expression must be optional, i.e., it must have a `?` postfix quantifier

The `default` option can be replaced in several ways - most commonly with an `if-then-else` expression or with a call to the [`select_first`](#select_first) function.

<details>
<summary>
Example: default_option_task.wdl

```wdl
version 1.1

task default_option {
  input {
    String? s
  }

  command <<<
    echo ~{default="foobar" s} > result1
    echo ~{if defined(s) then "~{select_first([s])}" else "foobar"} > result2
    echo ~{select_first([s, "foobar"])} > result3
  >>>
  
  output {
    Boolean is_true1 = read_string("result1") == read_string("result2")
    Boolean is_true2 = read_string("result1") == read_string("result3")
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "default_option.is_true1": true,
  "default_option.is_true2": true
}
```
</p>
</details>

### Static Analysis and Dynamic Evaluation

As with any strongly typed programming language, WDL is processed in two distinct phases by the implementation: static analysis and dynamic evaluation.

* Static analysis is the process of parsing the WDL document and performing type inference - that is, making sure the WDL is syntactically correct, and that there is compatibility between the expected and actual types of all declarations, expressions, and calls.
* Dynamic evaluation is the process of evaluating all WDL expressions and calls at runtime, when all of the user-specified inputs are available.

An implementation should raise an error as early as possible when processing a WDL document. For example, in the following task the `sub` function is being called with an `Int` argument rather than a `String`. This function call cannot be evaluated successfully, so the implementation should raise an error during static analysis, rather than waiting until runtime.

```wdl
task bad_sub {
  Int i = 111222333
  String s = sub(i, "2", "4")
}
```

On the other hand, in the following example all of the types are compatible, but if the `hello.txt` file does not exist at runtime (when the implementation instantiates the command and tries to evaluate the call to `read_lines`), then an error will be raised.

```wdl
task missing_file {
  File f = "hello.txt"

  command <<<
  echo "~{sep(","), read_lines(f)}"
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

Because patches to the WDL specification do not change any functionality, all revisions that carry the same major and minor version numbers are considered equivalent. For example, `version 1.1` is used for a WDL document that adheres to the `1.1.x` specification, regardless of the value of `x`.

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
| ----------------------------------------------------- | ---------------------------------- | ------------------------------------------------------- |
| /foo/bar/baz/qux.wdl                                  | some/task.wdl                      | /foo/bar/baz/some/task.wdl                              |
| http://www.github.com/openwdl/coolwdls/myWorkflow.wdl | subworkflow.wdl                    | http://www.github.com/openwdl/coolwdls/subworkflow.wdl  |
| http://www.github.com/openwdl/coolwdls/myWorkflow.wdl | /openwdl/otherwdls/subworkflow.wdl | http://www.github.com/openwdl/otherwdls/subworkflow.wdl |
| /some/path/hello.wdl                                  | /another/path/world.wdl            | /another/path/world.wdl                                 |

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

`File` inputs must be treated specially since they may require localization to the execution environment. For example, a file located on a remote web server that is provided to the execution engine as an `https://` URL must first be downloaded to the machine where the task is being executed.

- Files are localized into the execution environment prior to the task execution commencing.
- When localizing a `File`, the engine may choose to place the file wherever it likes so long as it adheres to these rules:
  - The original file name must be preserved even if the path to it has changed.
  - Two input files with the same name must be located separately, to avoid name collision.
  - Two input files that have the same parent location must be localized into the same directory for task execution. For example, `http://foo.com/bar/a.txt` and `http://foo.com/bar/b.txt` have the same parent (`http://foo.com/bar/`), so they must be localized into the same directory. See below for special-case handling for Versioning Filesystems.
- When a WDL author uses a `File` input in their [Command Section](#command-section), the fully qualified, localized path to the file is substituted when that declaration is referenced in the command template.

The above rules do *not* guarantee that two files will be localized to the same directory *unless* they originate from the same parent location. If you are writing a task for a tool that assumes two files will be co-located, then it is safest to manually co-locate them prior to running the tool. For example, the following task runs a variant caller (`varcall`) on a BAM file and expects the BAM's index file (`.bai` extension) to be in the same directory as the BAM file.

```wdl
task call_variants_safe {
  input {
    File bam
    File bai
  }
  
  String prefix = basename(bam, ".bam")

  command <<<
  mkdir workdir
  ln -s ~{bam} workdir/~{prefix}.bam
  ln -s ~{bai} workdir/~{prefix}.bam.bai
  varcall --bam workdir/~{prefix}.bam > ~{prefix}.vcf
  >>>

  output {
    File vcf = "~{prefix}.vcf"
  }
}
```

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

| input  | value           |
| ------ | --------------- |
| test.a | ["1", "2", "3"] |
| test.b | []              |

It will result in an error, since `test.b` is required to have at least one element.

On the other hand, if these input values are provided:

| var    | value           |
| ------ | --------------- |
| test.a | ["1", "2", "3"] |
| test.b | ["x"]           |

The task will run successfully, because `test.c` is not required. Given these values, the command would be instantiated as:

```txt
/bin/mycmd 1 2 3
/bin/mycmd x
/bin/mycmd
```

If the inputs were:

| var    | value             |
| ------ | ----------------- |
| test.a | ["1", "2", "3"]   |
| test.b | ["x","y"]         |
| test.c | ["a","b","c","d"] |

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
    String greeting = if defined(saluation) then "~{saluation} ~{name}" else name
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

| Command Definition Style | Placeholder Style          |
| ------------------------ | -------------------------- |
| `command <<< >>>`        | `~{}` only                 |
| `command { ... }`        | `~{}` (preferred) or `${}` |

Note that the `~{}` and `${}` styles may be used interchangeably in other string expressions.

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

Like any other WDL string, the command section is subject to the rules of [string interpolation](#expression-placeholders-and-string-interpolation): all placeholders must contain expressions that are valid when analyzed statically, and that can be converted to a `String` value when evaluated dynamically. However, the evaluation of placeholder expressions during command instantiation is more lenient than typical dynamic evaluation as described in [Expression Placeholder Coercion](#expression-placeholder-coercion).

The implementation is *not* responsible for interpreting the contents of the command section to check that it is a valid Bash script, ignore comment lines, etc. For example, in the following task the `greeting` declaration is commented out, so `greeting` is not a valid identifier in the task's scope. However, the placeholder in the command section refers to `greeting`, so the implementation will raise an error during static analysis. The fact that the placeholder occurs in a commented line of the Bash script doesn't matter.

```wdl
task missing_declaration {
  # String greeting = "hello"

  command <<<
  # echo "~{greeting} John!"
  >>>
}
```

#### Stripping Leading Whitespace

When a command template is evaluated, the execution engine first strips out all *common leading whitespace*.

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
- One or more files (as indicated by the `+` postfix quantifier) with the `.csv` extension in the working directory that are collected into an array by the [`glob`](#glob) function.
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

Another common pattern is to use the [`glob`](#glob) function to define outputs that might contain zero, one, or many files.

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

| Variable | Value                                                                                                                                                                                                 |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| reads    | /path/to/fastq                                                                                                                                                                                        |
| stages   | ["stage1 map1 --min-seq-length 20 map2 --min-seq-length 20", "stage2 map1 --max-seq-length 20 --min-seq-length 10 --seed-length 16  map2 --max-seed-hits -1 --max-seq-length 20 --min-seq-length 10"] |

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

In the following more extensive example, all of the fully-qualified names that exist within the top-level workflow are listed exhaustively.

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
    File test_results = test.results
    File foobar_results = foobar.results
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
* `wf.foobar.infile` - References the `File` input of the call to `other.foobar`
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

There is no mechanism for a workflow to set a value for a nested input when calling a subworkflow. For example, the following workflow is invalid:

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

As soon as the execution of a called task completes, the call outputs are available to be used as inputs to other calls in the workflow or as workflow outputs. The only task declarations that are accessible outside of the task are its output declarations, i.e. call inputs cannot be referenced. To expose a call input, add an output to the task that simply copies the input:

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

To add a dependency from x to y that isn't based on outputs, you can use the `after` keyword, such as `call x after y after z`. However, this is only required if `x` doesn't already depend on an output from `y`.

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

Even though a conditional body is only evaluated if its conditional expression evaluates to `true`, all of the potential declarations and call outputs in the conditional body are always exported, regardless of the value of the conditional expression. In the case that the conditional expression evaluates to `false`, all of the exported declarations and call outputs are undefined (i.e. have a value of `None`).

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

It is impossible to have a multi-level optional type, e.g. `Int??`; thus, the outputs of a conditional block are only ever single-level optionals, even when there are nested conditionals.

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
  Array[File] experiment_files
  Map[String, String] experiment_data
}
```

**Example 1:** Accessing the nth element of experimentFiles and any element in experimentData:

```wdl
workflow workflow_a {
  input {
    Experiment my_experiment
  }
  File first_file = my_experiment.experiment_files[0]
  String experiment_name = my_experiment.experiment_data["name"]
}
```

**Example 2:** The struct is an item in an Array:

```wdl
workflow workflow_a {
  input {
    Array[Experiment] my_experiments
  }

  File first_file_from_first_experiment = my_experiments[0].experiment_files[0]
  File experiment_name_from_first_experiment = my_experiments[0].experiment_data["name"]
  ....
}
```

# Standard Library

The following functions are available to be called in WDL expressions. The signature of each function is given as `R func_name(T1, T2, ...)`, where `R` is the return type and `T1`, `T2`, ... are the parameter types. All function parameters must be specified in order, and all function parameters are required, with the exception that the last parameter(s) of some functions is optional (denoted by the type in brackets `[]`).

A function is called using the following syntax: `R' val = func_name(arg1, arg2, ...)`, where `R'` is a type that is coercible from `R`, and `arg1`, `arg2`, ... are expressions whose types are coercible to `T1`, `T2`, ...

A function may be generic, which means that one or more of its parameters and/or its return type are generic. These functions are defined using letters (e.g. `X`, `Y`) for the type parameters, and the bounds of each type parameter is specified in the function description.

A function may be polymorphic, which means it is actually multiple functions ("variants") with the same name but different signatures. Such a function may be defined using `|` to denote the set of alternative valid types for one or more of its parameters, or it may have each variant defined separately.

Functions are grouped by their argument types and restrictions. Some functions may be restricted as to where they may be used. An unrestricted function may be used in any expression.

Functions that are new in this version of the specification are denoted by ✨, and deprecated functions are denoted by 🗑.

## Numeric Functions

These functions all operate on numeric types.

**Restrictions**: None

### `floor`

```
Int floor(Float)
```

Rounds a floating point number **down** to the next lower integer.

**Parameters**:

1. `Float`: the number to round.

**Returns**: An integer.

<details>
<summary>
Example: test_floor.wdl

```wdl
verison 1.1

workflow test_floor {
  input {
    Int i1
  }

  Int i2 = i1 - 1
  Float f1 = i1
  Float f2 = i - 0.1
  
  output {
    Boolean all_true = [floor(f1) == i1, floor(f2) == i2]
  }
}
```
</summary>
<p>
Example input:

```json
{
  "test_floor.i1": 2
}

```
Example output:

```json
{
  "test_floor.all_true": true
}
```
</p>
</details>

### `ceil`

```
Int ceil(Float)
```

Rounds a floating point number **up** to the next higher integer.

**Parameters**:

1. `Float`: the number to round.

**Returns**: An integer.

<details>
<summary>
Example: test_ceil.wdl

```wdl
verison 1.1

workflow test_ceil {
  input {
    Int i1
  }

  Int i2 = i1 + 1
  Float f1 = i1
  Float f2 = i + 0.1
  
  output {
    Boolean all_true = [ceil(f1) == i1, ceil(f2) == i2]
  }
}
```
</summary>
<p>
Example input:

```json
{
  "test_ceil.i1": 2
}
```

Example output:

```json
{
  "test_ceil.all_true": true
}
```
</p>
</details>

### `round`

```
Int round(Float)
```

Rounds a floating point number to the nearest integer based on standard rounding rules ("round half up").

**Parameters**:

1. `Float`: the number to round.

**Returns**: An integer.

<details>
<summary>
Example: test_round.wdl

```wdl
verison 1.1

workflow test_round {
  input {
    Int i1
  }

  Int i2 = i1 + 1
  Float f1 = i1 + 0.49
  Float f2 = i1 + 0.50
  
  output {
    Boolean all_true = [round(f1) == i1, round(f2) == i2]
  }
}
```
</summary>
<p>
Example input:

```json
{
  "test_round.i1": 2
}
```

Example output:

```json
{
  "test_round.all_true": true
}
```
</p>
</details>

### ✨ `min`

This function has four variants:

```
* Int min(Int, Int)
* Float min(Int, Float)
* Float min(Float, Int)
* Float min(Float, Float)
```

Returns the smaller of two values. If both values are `Int`s, the return value is an `Int`, otherwise it is a `Float`.

**Parameters**:

1. `Int|Float`: the first number to compare.
2. `Int|Float`: the second number to compare.

**Returns**: The smaller of the two arguments.

<details>
<summary>
Example: test_min.wdl

```wdl
verison 1.1

workflow test_min {
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
</summary>
<p>
Example input:

```json
{
  "test_min.value1": 1,
  "test_min.value2": 2.0
}
```

Example output:

```json
{
  "test_min.min1": 1.0,
  "test_min.min2": 1.0
}
```
</p>
</details>

### ✨ `max`

This function has four variants:

```
* Int max(Int, Int)
* Float max(Int, Float)
* Float max(Float, Int)
* Float max(Float, Float)
```

Returns the larger of two values. If both values are `Int`s, the return value is an `Int`, otherwise it is a `Float`.

**Parameters**:

1. `Int|Float`: the first number to compare.
2. `Int|Float`: the second number to compare.

**Returns**: The larger of the two arguments.

<details>
<summary>
Example: test_max.wdl

```wdl
verison 1.1

workflow test_max {
  input {
    Int value1
    Float value2
  }

  output {
    # these two expressions are equivalent
    Float min1 = if value1 > value2 then value1 else value2
    Float min2 = max(value1, value2)
  }
}
```
</summary>
<p>
Example input:

```json
{
  "test_max.value1": 1,
  "test_max.value2": 2.0
}
```

Example output:

```json
{
  "test_max.min1": 1.0,
  "test_max.min2": 1.0
}
```
</p>
</details>

## String Functions

These functions operate on `String` arguments.

**Restrictions**: None

### `sub`

```
String sub(String, String, String)
```

Given 3 String parameters `input`, `pattern`, and `replace`, this function replaces all non-overlapping occurrences of `pattern` in `input` by `replace`. `pattern` is a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) that will be evaluated as a [POSIX Extended Regular Expression (ERE)](https://en.wikipedia.org/wiki/Regular_expression#POSIX_basic_and_extended).

Regular expressions are written using regular WDL strings, so backslash characters need to be double-escaped (e.g., `"\\t"`).

🗑 The option for execution engines to allow other regular expression grammars besides POSIX ERE is deprecated.

**Parameters**:

1. `String`: the input string.
2. `String`: the pattern to search for.
3. `String`: the replacement string.

**Returns**: the input string, with all occurrences of the pattern replaced by the replacement string.

<details>
<summary>
Example: test_sub.wdl

```wdl
verison 1.1

workflow test_sub {
  String chocolike = "I like chocolate when\nit's late"

  output {
    String chocolove = sub(chocolike, "like", "love") # I love chocolate when\nit's late
    String chocoearly = sub(chocolike, "late", "early") # I like chocoearly when\nit's early
    String chocolate = sub(chocolike, "late$", "early") # I like chocolate when\nit's early
    String chocoearlylate = sub(chocolike, "[^ ]late", "early") # I like chocearly when\nit's late
    String choco4 = sub(chocolike, " [:alpha:]{4} ", " 4444 ") # I 4444 chocolate 4444\nit's late
    String no_newline = sub(chocolike, "\\n", " ") "I like chocolate when it's late"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_sub.chocolove": "I love chocolate when\nit's late",
  "test_sub.chocoearly": "I like chocoearly when\nit's early",
  "test_sub.chocolate": "I like chocolate when\nit's early",
  "test_sub.chocoearlylate": "I like chocearly when\nit's late",
  "test_sub.choco4": "I 4444 chocolate 4444\nit's late"
  "test_sub.no_newline": "I like chocolate when it's late"
}
```
</p>
</details>

Any arguments are allowed so long as they can be coerced to `String`s. For example, this can be useful to swap the extension of a filename:

<details>
<summary>
Example: change_extension_task.wdl

```wdl
verison 1.1

task change_extension {
  input {
    String prefix
  }

  command <<<
    echo "data" > ~{prefix}.data
    echo "index" > ~{prefix}.index
  >>>

  output {
    String data = read_string("~{prefix}.data")
    String index = read_string(sub(data_file, "\\.data$", ".index"))
  }

  runtime {
    container: "ubuntu:latest"
  }
}
```
</summary>
<p>
Example input:

```json
{
  "change_extension.prefix": "foo"
}
```

Example output:

```json
{
  "change_extension.data": "data",
  "change_extension.index": "index"
}
```
</p>
</details>

## File Functions

These functions have a `File` as an input and/or output. Due to [type coercion](#type-coercion), `File` arguments may be specified as `String` values.

For functions that read from or write to the file system, if the entire contents of the file cannot be read/written for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having appropriate permissions, resource limitations (e.g., memory) when reading the file, and implementation-imposed file size limits.

For functions that write to the file system, the implementatuion should generate a random file name in a temporary directory so as not to conflict with any other task output files.

**Restrictions**

1. A function that only manipulates a path (i.e., doesn't require reading any of the file's attributes or contents) may be called anywhere, whether or not the file exists.
2. A function that *reads* a file or its attributes may only be called in a context where the input file exists. If the file is an input to a task or workflow, then it may be read anywhere in that task or worklow. If the file is created by a task, then it may only be read after it is created. For example, if the file is written during the execution of the `command`, then it may only be read in the task's `output` section. This includes functions like `stdout` and `stderr` that read a task's output stream.
3. A function that *writes* a file may be called anywhere. However, writing a file in a workflow is discouraged since it may have the side-effect of creating a permanent output file that is not named in the output section. For example, calling [`write_lines`](#write_lines) in a workflow and then passing the resulting `File` as input to a task may require the engine to persist that file to cloud storage.

### `basename`

```
String basename(File, [String])
```

Returns the "basename" of a file - the name after the last directory separator in the file's path. 

The optional second parameter specifies a literal suffix to remove from the file name.

**Parameters**

1. `File`: Path of the file to read.
2. `String`: (Optional) Suffix to remove from the file name.
 
**Returns**: The file's basename as a `String`.

<details>
<summary>
Example: test_basename.wdl

```wdl
verison 1.1

workflow test_basename {
  output {
    Boolean is_true1 = basename("/path/to/file.txt") == "file.txt"`
    Boolean is_true2 = basename("/path/to/file.txt", ".txt") == "file"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_basename.is_true1": true,
  "test_basename.is_true2": true
}
```
</p>
</details>

### `glob`

```
Array[File] glob(String)
```

Returns the Bash expansion of the [glob string](https://en.wikipedia.org/wiki/Glob_(programming)) relative to the task's execution directory, and in the same order.

`glob` finds all of the files (but not the directories) in the same order as would be matched by running `echo <glob>` in Bash from the task's execution directory.

At least in standard Bash, glob expressions are not evaluated recursively, i.e., files in nested directories are not included. 

**Parameters**:

1. `String`: The glob string.

**Returns**: A array of all files matched by the glob.

<details>
<summary>
Example: gen_files_task.wdl

```wdl
verison 1.1

task gen_files {
  input {
    Int num_files
  }

  command <<<
    for i in 1..~{num_files}; do
      echo ~{i} > a_file_~{i}.txt
    done
    mkdir a_dir
    touch a_dir/a_inner.txt
  >>>

  Array[File] files = glob("a_*")

  output {  
    Int glob_len = length(files)
  }
}
```
</summary>
<p>
Example input:

```json
{
  "gen_files.num_files": 2
}
```

Example output:

```json
{
  "gen_files.glob_len": 2
}
```
</p>
</details>

This command generates the following directory structure:

```txt
<workdir>
├── a_dir
│   └─ a_inner.txt
├── a_file_1.txt
└── a_file_2.txt
```

Running `echo a_*` in the execution directory would expand to `a_dir`, `a_file_1.txt`, and `a_file_2.txt`, in that order. Since `glob` ignores directories, `a_dir` is discarded and the result of the expression is `["a_file_1.txt", "a_file_2.txt"]`.

#### Non-standard Bash

The runtime container may use a non-standard Bash shell that supports more complex glob strings, such as allowing expansions that include `a_inner.txt` in the example above. To ensure that a WDL task is portable when using `glob`, a container image should be provided and the WDL author should remember that `glob` results depend on coordination with the Bash implementation provided in that container.

### `size`

```
Float size(File?|Array[File?], [String])
```

Determines the size of a file, or the sum total of the sizes of files in an array. The files may be optional values; `None` values have a size of `0.0`. By default, the size is returned in bytes unless the optional second argument is specified with a [unit](#units-of-storage).

If the size cannot be represented in the specified unit because the resulting value is too large to fit in a `Float`, an error is raised. It is recommended to use a unit that will always be large enough to handle any expected inputs without numerical overflow.

**Parameters**

1. `File?|Array[File?]`: A file, or array of files, for which to determine the size.
2. `String`: (Optional) The unit of storage; defaults to 'B'.

**Returns**: The size of the file(s) as a `Float`.

<details>
<summary>
Example: file_sizes_task.wdl

```wdl
verison 1.1

task file_sizes {
  command <<<
    echo "this file is 22 bytes" > created_file
  >>>

  File? missing_file = None

  output {
    Float missing_file_bytes = size(missing_file) # 0.0
    Float created_file_bytes = size("created_file", "B") # 22.0
    Float multi_file_kb = size(["created_file", missing_file], "K") # 0.022
  }
  
  runtime {
    container: "ubuntu:latest"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "file_sizes.missing_file_bytes": 0.0,
  "file_sizes.created_file_bytes": 22.0,
  "file_sizes.multi_file_kb": 0.022
}
```
</p>
</details>

### `stdout`

```
File stdout()
```

Returns the value of the executed command's standard output (stdout) as a `File`. The engine should give the file a random name and write it in a temporary directory, so as not to conflict with any other task output files.

**Parameters**: None

**Returns**: A `File` whose contents are the stdout generated by the command of the task where the function is called.

<details>
<summary>
Example: echo_stdout.wdl

```wdl
verison 1.1

task echo_stdout {
  command <<< echo "hello world" >>>

  output {
    File message = read_string(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "echo_stdout.message": "hello world"
}
```
</p>
</details>

### `stderr`

```
File stderr()
```

Returns the value of the executed command's standard error (stderr) as a `File`. The file should be given a random name and written in a temporary directory, so as not to conflict with any other task output files.

**Parameters**: None

**Returns**: A `File` whose contents are the stderr generated by the command of the task where the function is called.

<details>
<summary>
Example: echo_stderr.wdl

```wdl
verison 1.1

task echo_stderr {
  command <<< >&2 echo "hello world" >>>

  output {
    File message = read_string(stderr())
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "echo_stderr.message": "hello world"
}
```
</p>
</details>

### `read_string`

```
String read_string(File)
```

Reads an entire file as a `String`, with any trailing end-of-line characters (`\r` and `\n`) stripped off. If the file is empty, an empty string is returned.

If the file contains any internal newline characters, they are left in tact.

**Parameters**

1. `File`: Path of the file to read.

**Returns**: A `String`.

<details>
<summary>
Example: read_string_task.wdl

```wdl
verison 1.1

task read_string {
  # this file will contain "this\nfile\nhas\nfive\nlines\n"
  File f = write_lines(["this", "file", "has", "file", "lines"])

  output {
    # s will contain "this\nfile\nhas\nfive\nlines"
    String s = read_string(f)
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "read_string.s": "this\nfile\nhas\nfive\nlines"
}
```
</p>
</details>

### `read_int`

```
Int read_int(File)
```

Reads a file that contains a single line containing only an integer and (optional) whitespace. If the line contains a valid integer, that value is returned as an `Int`, otherwise an error is raised.

**Parameters**

1. `File`: Path of the file to read.

**Returns**: An `Int`.

<details>
<summary>
Example: read_int_task.wdl

```wdl
verison 1.1

task read_int {
  command <<<
  echo "  1  \n" > int_file
  >>>

  output {
    Int i = read_int("int_file")
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "read_int.i": 1
}
```
</p>
</details>

### `read_float`

```
Float read_float(File)
```

Reads a file that contains only a numeric value and (optional) whitespace. If the line contains a valid floating point number, that value is returned as a `Float`, otherwise an error is raised.

**Parameters**

1. `File`: Path of the file to read.

**Returns**: A `Float`.

<details>
<summary>
Example: read_float_task.wdl

```wdl
verison 1.1

task read_float {
  command <<<
  echo "  1  \n" > int_file
  echo "  2.0  \n" > float_file
  >>>

  output {
    Float f1 = read_float("int_file")
    Float f2 = read_float("float_file")
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "read_float.f1": 1.0,
  "read_float.f2": 2.0
}
```
</p>
</details>

### `read_boolean`

```
Boolean read_boolean(File)
```

Reads a file that contains a single line containing only a boolean value and (optional) whitespace. If the line contains "true" or "false", that value is returned as a `Boolean`, otherwise an error is raised.

**Parameters**

1. `File`: Path of the file to read.

**Returns**: A `Boolean`.

<details>
<summary>
Example: read_bool_task.wdl

```wdl
verison 1.1

task read_bool {
  command <<<
  echo "  true  \n" > true_file
  echo "  FALSE  \n" > false_file
  >>>

  output {
    Boolean b1 = read_boolean("true_file")
    Boolean b2 = read_boolean("false_file")
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "read_bool.b1": true,
  "read_bool.b2": false
}
```
</p>
</details>

### `read_lines`

```
Array[String] read_lines(File)
```

Reads each line of a file as a `String`, and returns all lines in the file as an `Array[String]`. Trailing end-of-line characters (`\r` and `\n`) are removed from each line.

The order of the lines in the returned `Array[String]` is the order in which the lines appear in the file.

**Parameters**

1. `File`: Path of the file to read.

**Returns**: An `Array[String]` representation of the lines in the file.

<details>
<summary>
Example: grep_task.wdl

```wdl
verison 1.1

task grep {
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
    container: "ubuntu:latest"
  }
}
```
</summary>
<p>
Example input:

```json
{
  "grep.pattern": "world",
  "grep.file": "greetings.txt"
}
```

Example output:

```json
{
  "grep.matches": [
    "hello world",
    "hi_world"
  ]
}
```
</p>
</details>

### `write_lines`

```
File write_lines(Array[String])
```

Writes a file with one line for each element in a `Array[String]`. All lines are terminated by the newline (`\n`) character (following the [POSIX standard](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_206)). If the `Array` is empty, an empty file is written.

**Parameters**

1. `Array[String]`: Array of strings to write.

**Returns**: A `File`.

<details>
<summary>
Example: write_lines_task.wdl

```wdl
verison 1.1

task write_lines {
  input {
    Array[String] array = ["first", "second", "third"]
  }

  command <<<
    paste -s -d'\t' ~{write_lines(array)}
  >>>

  output {
    String s = read_string(stdout())
  }
  
  runtime {
    container: "ubuntu:latest"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "write_lines.s": "first\tsecond\tthird"
}
```
</p>
</details>

The actual command line might look like:

```sh
paste -s -d'\t' /local/fs/tmp/array.txt
```

And `/local/fs/tmp/array.txt` would contain:

`first\nsecond\nthird`

### `read_tsv`

```
Array[Array[String]] read_tsv(File)
```

Reads a tab-separated value (TSV) file as an `Array[Array[String]]` representing a table of values. Trailing end-of-line characters (`\r` and `\n`) are removed from each line.

There is no requirement that the rows of the table are all the same length.

**Parameters**

1. `File`: Path of the TSV file to read.

**Returns**: An `Array` of rows in the TSV file, where each row is an `Array[String]` of fields.

<details>
<summary>
Example: read_tsv_task.wdl

```wdl
verison 1.1

task read_tsv {
  command <<<
    echo "row1\tvalue1" >> data.tsv
    echo "row2\tvalue2" >> data.tsv
    echo "row3\tvalue3" >> data.tsv
  >>>

  output {
    Array[Array[String]] output_table = read_tsv("data.tsv")
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "read_tsv.output_table": [
    ["row1", "value1"],
    ["row2", "value2"],
    ["row3", "value3"]
  ]
}
```
</p>
</details>

### `write_tsv`

```
File write_tsv(Array[Array[String]])
```

Writes a tab-separated value (TSV) file with one line for each element in a `Array[Array[String]]`. Each element is concatenated into a single tab-delimited string. Each line is terminated by the newline (`\n`) character. If the `Array` is empty, an empty file is written.

**Parameters**

1. `Array[Array[String]]`: An array of rows, where each row is an array of column values.

**Returns**: A `File`.

<details>
<summary>
Example: write_tsv_task.wdl

```wdl
verison 1.1

task write_tsv {
  input {
    Array[Array[String]] array = [["one", "two", "three"], ["un", "deux", "trois"]]
  }

  command <<<
    cut -f 1 ~{write_tsv(array)}
  >>>

  output {
    Array[String] ones = read_lines(stdout())
  }
  
  runtime {
    container: "ubuntu:latest"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "write_tsv.ones": ["one", "un"]
}
```
</p>
</details>

The actual command line might look like:

```sh
cut -f 1 /local/fs/tmp/array.tsv
```

And `/local/fs/tmp/array.tsv` would contain:

```txt
one\ttwo\tthree
un\tdeux\ttrois
```

### `read_map`

```
Map[String, String] read_map(File)
```

Reads a tab-separated value (TSV) file representing a set of pairs. Each row must have exactly two columns, e.g., `col1\tcol2`. Trailing end-of-line characters (`\r` and `\n`) are removed from each line.

Each pair is added to a `Map[String, String]` in order. The values in the first column must be unique; if there are any duplicate keys, an error is raised.

**Parameters**

1. `File`: Path of the two-column TSV file to read.

**Returns**: A `Map[String, String]`, with one element for each row in the TSV file.

<details>
<summary>
Example: read_map_task.wdl

```wdl
verison 1.1

task read_map {
  command <<<
    echo "key1\tvalue1" >> map_file
    echo "key2\tvalue2" >> map_file
  >>>
  
  output {
    Map[String, String] mapping = read_map(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "read_map.mapping": {
    "key1": "value1",
    "key2": "value2"
  }
}
```
</p>
</details>

### `write_map`

```
File write_map(Map[String, String])
```

Writes a tab-separated value (TSV) file with one line for each element in a `Map[String, String]`. Each element is concatenated into a single tab-delimited string of the format `~{key}\t~{value}`. Each line is terminated by the newline (`\n`) character. If the `Map` is empty, an empty file is written.

Since `Map`s are ordered, the order of the lines in the file is guaranteed to be the same order that the elements were added to the `Map`.

**Parameters**

1. `Map[String, String]`: A `Map`, where each element will be a row in the generated file.

**Returns**: A `File`.

<details>
<summary>
Example: write_map_task.wdl

```wdl
verison 1.1

task write_map {
  input {
    Map[String, String] map = {"key1": "value1", "key2": "value2"}
  }

  command <<<
    cut -f 1 ~{write_map(map)}
  >>>
  
  output {
    Array[String] keys = read_lines(stdout())
  }

  runtime {
    container: "ubuntu:latest"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "write_map.keys": ["key1", "key2"]
}
```
</p>
</details>

The actual command line might look like:

```sh
cut -f 1 /local/fs/tmp/map.tsv
```

And `/local/fs/tmp/map.tsv` would contain:

```txt
key1\tvalue1
key2\tvalue2
```

### `read_json`

```
Union read_json(File)
```

Reads a JSON file into a WDL value whose type depends on the file's contents. The mapping of JSON type to WDL type is:

| JSON Type | WDL Type         |
| --------- | ---------------- |
| object    | `Object`         |
| array     | `Array[X]`       |
| number    | `Int` or `Float` |
| string    | `String`         |
| boolean   | `Boolean`        |
| null      | `None`           |

The return value is of type [`Union`](#union) and must be used in a context where it can be coerced to the expected type, or an error is raised. For example, if the JSON file contains `null`, then the return value will be `None`, meaning the value can only be used in a context where an optional type is expected.

If the JSON file contains an array, then all the elements of the array must be coercible to the same type, or an error is raised.

The `read_json` function does not have access to any WDL type information, so it cannot return an instance of a specific `Struct` type. Instead, it returns a generic `Object` value that must be coerced to the desired `Struct` type.

**Parameters**

1. `File`: Path of the JSON file to read.

**Returns**: A value whose type is dependent on the contents of the JSON file.

<details>
<summary>
Example: read_person.wdl

```wdl
verison 1.1

struct Person {
  String name
  Int age
}

workflow read_person {
  input {
    File json_file
  }

  output {
    Person p = read_json(json_file)
  }
}
```
</summary>
<p>
Example input:

```json
{
  "read_person.json_file": "person.json"
}
```

Example output:

```json
{
  "read_person.p": {
    "name": "John",
    "age": 42
  }
}
```
</p>
</details>

### `write_json`

```
File write_json(X)
```

Writes a JSON file with the serialized form of a WDL value. The following WDL types can be serialized:

| WDL Type         | JSON Type |
| ---------------- | --------- |
| `Struct`         | object    |
| `Object`         | object    |
| `Map[String, X]` | object    |
| `Array[X]`       | array     |
| `Int`            | number    |
| `Float`          | number    |
| `String`         | string    |
| `File`           | string    |
| `Boolean`        | boolean   |
| `None`           | null      |

When serializing compound types, all nested types must be serializable or an error is raised.

**Parameters**

1. `X`: A WDL value of a supported type.

**Returns**: A `File`.

<details>
<summary>
Example: write_json_fail.wdl

```wdl
verison 1.1

workflow write_json_fail {
  Pair[Int, Map[Int, String]] x = (1, {2: "hello"})
  # this fails with an error - Map with Int keys is not serializable
  File f = write_json(x)
  
  meta {
    test_config: "fail"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{}
```
</p>
</details>

<details>
<summary>
Example: write_json_task.wdl

```wdl
verison 1.1

task write_json {
  input {
    Map[String, String] map = {"key1": "value1", "key2": "value2"}
  }

  command <<<
    python <<CODE
    import json
    with open("~{write_json(map)}") as js:
      d = json.load(js)
      print(list(d.keys()))
    CODE
  >>>

  output {
    Array[String] keys = read_json(stdout())
  }
  
  runtime {
    container: "python:latest"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "write_json.keys": ["key1", "key2"]
}
```
</p>
</details>

The actual command line might look like:

```sh
python <<CODE
import json
with open("local/fs/tmp/map.json") as js:
  d = json.load(js)
  print(list(d.keys()))
CODE
```

And `/local/fs/tmp/map.json` would contain:

```json
{
  "key1": "value1",
  "key2": "value2"
}
```

### `read_object`

```
Object read_object(File)
```

Reads a tab-separated value (TSV) file representing the names and values of the members of an `Object`. There must be two rows, and each row must have the same number of elements. Trailing end-of-line characters (`\r` and `\n`) are removed from each line.

The first row specifies the object member names. The names in the first row must be unique; if there are any duplicate names, an error is raised.

The second row specifies the object member values corresponding to the names in the first row. All of the `Object`'s values are of type `String`.

**Parameters**

1. `File`: Path of the two-row TSV file to read.

**Returns**: An `Object`, with as many members as there are unique names in the TSV.

<details>
<summary>
Example: read_object_task.wdl

```wdl
verison 1.1

task read_object {
  command <<<
    python <<CODE
    print('\t'.join(["key_{}".format(i) for i in range(3)]))
    print('\t'.join(["value_{}".format(i) for i in range(3)]))
    CODE
  >>>

  output {
    Object my_obj = read_object(stdout())
  }

  runtime {
    container: "python:latest"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "read_object.my_obj": {
    "key_0": "value_0",
    "key_1": "value_1",
    "key_2": "value_2",
  }
}
```
</p>
</details>

The command outputs the following lines to stdout:

```
key_0\tkey_1\tkey_2
value_0\tvalue_1\tvalue_2
```

Which are read into an `Object` with the following members:

| Attribute | Value     |
| key_0     | "value_0" |
| key_1     | "value_1" |
| key_2     | "value_2" |

### `read_objects`

```
Array[Object] read_objects(File)
```

Reads a tab-separated value (TSV) file representing the names and values of the members of any number of `Object`s. Trailing end-of-line characters (`\r` and `\n`) are removed from each line.

There must be a header row with the names of the object members. The names in the first row must be unique; if there are any duplicate names, an error is raised.

There are any number of additional rows, where each additional row contains the values of an object corresponding to the member names. Each row in the file must have the same number of fields as the header row. All of the `Object`'s values are of type `String`.

**Parameters**

1. `File`: Path of the TSV file to read.

**Returns**: An `Array[Object]`, with `N-1` elements, where `N` is the number of rows in the file.

<details>
<summary>
Example: read_objects_task.wdl

```wdl
verison 1.1

task read_objects {
  command <<<
    python <<CODE
    print('\t'.join(["key_{}".format(i) for i in range(3)]))
    print('\t'.join(["value_A{}".format(i) for i in range(3)]))
    print('\t'.join(["value_B{}".format(i) for i in range(3)]))
    print('\t'.join(["value_C{}".format(i) for i in range(3)]))
    CODE
  >>>

  output {
    Array[Object] my_obj = read_objects(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "read_objects.my_obj": [
    {
      "key_0": "value_A0",
      "key_1": "value_A1",
      "key_2": "value_A2",
    },
    {
      "key_0": "value_B0",
      "key_1": "value_B1",
      "key_2": "value_B2",
    },
    {
      "key_0": "value_C0",
      "key_1": "value_C1",
      "key_2": "value_C2",
    }
  ]
}
```
</p>
</details>

The command outputs the following lines to stdout:

```
key_0\tkey_1\tkey_3
value_A0\tvalue_A1\tvalue_A2
value_B0\tvalue_B1\tvalue_B2
value_C0\tvalue_C1\tvalue_C2
```

Which are read into an `Array[Object]` with the following elements:

| Index | Attribute | Value      |
| ----- | --------- | ---------- |
| 0     | key_0     | "value_A0" |
|       | key_1     | "value_A1" |
|       | key_2     | "value_A2" |
| 1     | key_0     | "value_B0" |
|       | key_1     | "value_B1" |
|       | key_2     | "value_B2" |
| 2     | key_0     | "value_C0" |
|       | key_1     | "value_C1" |
|       | key_2     | "value_C2" |

### `write_object`

```
File write_object(Struct|Object)
```

Writes a tab-separated value (TSV) file with the contents of a `Object` or `Struct`. The file contains two tab-delimited lines. The first line is the names of the members, and the second line is the corresponding values. Each line is terminated by the newline (`\n`) character. The ordering of the columns is unspecified.

The member values must be serializable to strings, meaning that only primitive types are supported. Attempting to write a `Struct` or `Object` that has a compound member value results in an error.

**Parameters**

1. `Struct|Object`: An object to write.

**Returns**: A `File`.

<details>
<summary>
Example: write_object_task.wdl

```wdl
verison 1.1

task write_object {
  input {
    Object obj
  }

  command <<<
    cut -f 1 ~{write_object(obj)}
  >>>
  
  output {
    Array[String] results = read_lines(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{
  "write_object": {
    "key_1": "value_1",
    "key_2": "value_2",
    "key_3": "value_3",
  }
}
```

Example output:

```json
{
  "write_object": ["key_1", "value_1"]
}
```
</p>
</details>

The actual command line might look like:

```sh
cut -f 1 /path/to/input.tsv
```

If `obj` has the following members:

| Attribute | Value     |
| --------- | --------- |
| key_1     | "value_1" |
| key_2     | "value_2" |
| key_3     | "value_3" |

Then `/path/to/input.tsv` will contain:

```
key_1\tkey_2\tkey_3
value_1\tvalue_2\tvalue_3
```

### `write_objects`

```
File write_objects(Array[Struct|Object])
```

Writes a tab-separated value (TSV) file with the contents of a `Array[Struct]` or `Array[Object]`. All elements of the `Array` must have the same member names, or an error is raised.

The file contains `N+1` tab-delimited lines, where `N` is the number of elements in the `Array`. The first line is the names of the `Struct`/`Object` members, and the subsequent lines are the corresponding values for each element. Each line is terminated by a newline (`\n`) character. The lines are written in the same order as the elements in the `Array`. The ordering of the columns is the same as the order in which the `Struct`'s members are defined; the column ordering for `Object`s is unspecified. If the `Array` is empty, an empty file is written.

The member values must be serializable to strings, meaning that only primitive types are supported. Attempting to write a `Struct` or `Object` that has a compound member value results in an error.

**Parameters**

1. `Array[Struct|Object]`: An array of objects to write.

**Returns**: A `File`.

<details>
<summary>
Example: write_objects_task.wdl

```wdl
verison 1.1

task write_objects {
  input {
    Array[Object] obj_array
  }

  command <<<
    cut -f 1 ~{write_objects(obj_array)}
  >>>
  
  output {
    Array[String] results = read_lines(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{
  "write_objects.obj_array": [
    {
      "key_1": "value_1",
      "key_2": "value_2",
      "key_3": "value_3",
    },
    {
      "key_1": "value_4",
      "key_2": "value_5",
      "key_3": "value_6",
    },
    {
      "key_1": "value_7",
      "key_2": "value_8",
      "key_3": "value_9",
    },
  ]
}
```

Example output:

```json
{
  "write_objects.results": ["key_1", "value_1", "value_4", "value_7"]
}
```
</p>
</details>

The actual command line might look like:

```sh
cut -f 1 /path/to/input.tsv
```

If `obj_array` has the items:

| Index | Attribute | Value     |
| ----- | --------- | --------- |
| 0     | key_1     | "value_1" |
|       | key_2     | "value_2" |
|       | key_3     | "value_3" |
| 1     | key_1     | "value_4" |
|       | key_2     | "value_5" |
|       | key_3     | "value_6" |
| 2     | key_1     | "value_7" |
|       | key_2     | "value_8" |
|       | key_3     | "value_9" |

The `/path/to/input.tsv` will contain:

```
key_1\tkey_2\tkey_3
value_1\tvalue_2\tvalue_3
value_4\tvalue_5\tvalue_6
value_7\tvalue_8\tvalue_9
```

## String Array Functions

These functions take an `Array` as input and return a `String` or `Array[String]`. Due to type coercion, the `Array` argument may be of any primitive type (denoted by `P`).

**Restrictions**: None

### `prefix`

```
Array[String] prefix(String, Array[P])
```

Adds a prefix to each element of the input array of primitive values. Equivalent to evaluating `"~{prefix}~{array[i]}"` for each `i` in `range(length(array))`.

**Parameters**

1. `String`: The prefix to prepend to each element in the array.
2. `Array[P]`: Array with a primitive element type.

**Returns**: An `Array[String]` with the prefixed elements of the input array.

<details>
<summary>
Example: test_prefix.wdl

```wdl
verison 1.1

workflow test_prefix {
  Array[String] env1 = ["key1=value1", "key2=value2", "key3=value3"]
  Array[Int] env2 = [1, 2, 3]

  output {
    Array[String] env_prefixed = prefix("-e ", env1)
    Array[String] env2_prefixed = prefix("-f ", env2)
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_prefix.env1_prefixed": ["-e key1=value1", "-e key2=value2", "-e key3=value3"],
  "test_prefix.env2_prefixed": ["-f 1", "-f 2", "-f 3"]
}
```
</p>
</details>

<details>
<summary>
Example: test_prefix_fail.wdl

```wdl
verison 1.1

workflow test_prefix_fail {
  Array[Array[String]] env3 = [["a", "b], ["c", "d"]]
  # this fails with an error - env3 element type is not primitive
  Array[String] bad = prefix("-x ", env3)

  meta {
    test_config: "fail"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{}
```
</p>
</details>

### ✨ `suffix`

```
Array[String] suffix(String, Array[P])
```

Adds a suffix to each element of the input array of primitive values. Equivalent to evaluating `"~{array[i]}~{suffix}"` for each `i` in `range(length(array))`.

**Parameters**

1. `String`: The suffix to append to each element in the array.
2. `Array[P]`: Array with a primitive element type.

**Returns**: An `Array[String]` the suffixed elements of the input array.

<details>
<summary>
Example: test_suffix.wdl

```wdl
verison 1.1

workflow test_suffix {
  Array[String] env1 = ["key1=value1", "key2=value2", "key3=value3"]
  Array[Int] env2 = [1, 2, 3]

  output {
    Array[String] env1_suffix = suffix(".txt ", env1)
    Array[String] env2_suffix = suffix(".0", env2)
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_suffix.env1_suffix": ["key1=value1.txt", "key2=value2.txt", "key3=value3.txt"],
  "test_suffix.env2_suffix": ["1.0", "2.0", "3.0"]
}
```
</p>
</details>

<details>
<summary>
Example: test_suffix_fail.wdl

```wdl
verison 1.1

workflow test_suffix_fail {
  Array[Array[String]] env3 = [["a", "b], ["c", "d"]]
  # this fails with an error - env3 element type is not primitive
  Array[String] bad = suffix("-z", env3)
  
  meta {
    test_config: "fail"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{}
```
</p>
</details>

### ✨ `quote`

```
Array[String] quote(Array[P])
```

Adds double-quotes (`"`) around each element of the input array of primitive values. Equivalent to evaluating `'"~{array[i]}"'` for each `i` in `range(length(array))`.

**Parameters**

1. `Array[P]`: Array with a primitive element type.

**Returns**: An `Array[String]` the double-quoted elements of the input array.

<details>
<summary>
Example: test_quote.wdl

```wdl
verison 1.1

workflow test_quote {
  Array[String] env1 = ["key1=value1", "key2=value2", "key3=value3"]
  Array[Int] env2 = [1, 2, 3]

  output {
    Array[String] env1_quoted = quote(env1)
    Array[String] env2_quoted = quote(env2)
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_quote.env1_quoted": ["\"key1=value1\"", "\"key2=value2\"", "\"key3=value3\""],
  "test_quote.env2_quoted": ["\"1\"", "\"2\"", "\"3\""]
}
```
</p>
</details>

### ✨ `squote`

```
Array[String] squote(Array[P])
```

Adds single-quotes (`'`) around each element of the input array of primitive values. Equivalent to evaluating `"'~{array[i]}'"` for each `i` in `range(length(array))`.

**Parameters**

1. `Array[P]`: Array with a primitive element type.

**Returns**: An `Array[String]` the single-quoted elements of the input array.

<details>
<summary>
Example: test_squote.wdl

```wdl
verison 1.1

workflow test_squote {
  Array[String] env1 = ["key1=value1", "key2=value2", "key3=value3"]
  Array[Int] env2 = [1, 2, 3]
  
  output {
    Array[String] env1_quoted =  squote(env)
    Array[String] env2_quoted = squote(env2)
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_squote.env1_quoted": ["'key1=value1'", "'key2=value2'", "'key3=value3'"],
  "test_squote.env2_quoted": ["'1'", "'2'", "'3'"]
}
```
</p>
</details>

### ✨ `sep`

```
String sep(String, Array[P])
```

Concatenates the elements of an array together into a string with the given separator between consecutive elements. There are always `N-1` separators in the output string, where `N` is the length of the input array. A separator is never added after the last element. Returns an empty string if the array is empty.

**Parameters**

1. `String`: Separator string. 
2. `Array[P]`: Array of strings to concatenate.

**Returns**: A `String` with the concatenated elements of the array delimited by the separator string.

<details>
<summary>
Example: test_sep.wdl

```wdl
verison 1.1

workflow test_sep {
  Array[String] a = ["file_1", "file_2"]

  output {
    # these all evaluate to true
    Boolean all_true = [
      sep(' ', prefix('-i ', a)) == "-i file_1 -i file_2",
      sep("", ["a, "b", "c"]) == "abc",
      sep(' ', ["a", "b", "c"]) == "a b c",
      sep(',', [1]) == "1"
    ]
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_sep.all_true: [true, true, true, true]
}
```
</p>
</details>

## Generic Array Functions

These functions are generic and take an `Array` as input and/or return an `Array`.

**Restrictions**: None

### `length`

```
Int length(Array[X])```

Returns the number of elements in an array as an `Int`.

**Parameters**

1. `Array[X]`: An array with any element type.

**Returns**: The length of the array as an `Int`.

<details>
<summary>
Example: test_length.wdl

```wdl
verison 1.1

workflow test_length {
  Array[Int] xs = [1, 2, 3]
  Array[String] ys = ["a", "b", "c"]
  Array[String] zs = []

  output {
    Int xlen = length(xs) # 3
    Int ylen = length(ys) # 3
    Int zlen = length(zs) # 0
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_length.xlen": 3,
  "test_length.ylen": 3,
  "test_length.zlen": 0
}
```
</p>
</details>

### `range`

```
Array[Int] range(Int)
```

Creates an array of the given length containing sequential integers starting from 0. The length must be >= `0`. If the length is `0`, an empty array is returned.

**Parameters**

1. `Int`: The length of array to create.

**Returns**: An `Array[Int]` containing integers `0..(N-1)`.

<details>
<summary>
Example: test_range.wdl

```wdl
verison 1.1

task double {
  input {
    Int n
  }

  output {
    Int d = n * n
  }
}

workflow test_range {
  input {
    Int i
  }

  Array[Int] indexes = range(i)
  scatter (idx in indexes) {
    call double { input: n = idx }
  }

  output {
    Array[Int] result = double.d
  }
}
```
</summary>
<p>
Example input:

```json
{
  "test_range.n": 5
}
```

Example output:

```json
{
  "test_range.result": [0, 2, 4, 6, 8]
}
```
</p>
</details>

### `transpose`

```
Array[Array[X]] transpose(Array[Array[X]])
```

Transposes a two-dimensional array according to the standard matrix transposition rules, i.e. each row of the input array becomes a column of the output array. The input array must be square - i.e., every row must have the same number of elements - or an error is raised. If either the inner or the outer array is empty, an empty array is returned.

**Parameters**

1. `Array[Array[X]]`: A `M*N` two-dimensional array.

**Returns**: A `N*M` two-dimensional array (`Array[Array[X]]`) containing the transposed input array.

<details>
<summary>
Example: test_transpose.wdl

```wdl
verison 1.1

workflow test_transpose {
  # input array is 2 rows * 3 columns
  Array[Array[Int]] input_array = [[0, 1, 2], [3, 4, 5]]
  # output array is 3 rows * 2 columns
  Array[Array[Int]] expected_output_array = [[0, 3], [1, 4], [2, 5]]
  
  output {
    Boolean is_true = transpose(input_array) == expected_output_array
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_transpose.is_true": true
}
```
</p>
</details>

### `cross`

```
Array[Pair[X,Y]] cross(Array[X], Array[Y])
```

Creates an array of `Pair`s containing the [cross product](https://en.wikipedia.org/wiki/Cross_product) of two input arrays, i.e., each element in the first array is paired with each element in the second array.

Given `Array[X]` of length `M`, and `Array[Y]` of length `N`, the cross product is `Array[Pair[X, Y]]` of length `M*N` with the following elements: `[(X0, Y0), (X0, Y1), ..., (X0, Yn-1), (X1, Y0), ..., (X1, Yn-1), ..., (Xm-1, Yn-1)]`. If either of the input arrays is empty, an empty array is returned.

**Parameters**

1. `Array[X]`: The first array of length `M`.
2. `Array[Y]`: The second array of length `N`.

**Returns**: An `Array[Pair[X, Y]]` of length `M*N`.

<details>
<summary>
Example: test_cross.wdl

```wdl
verison 1.1

workflow test_cross {
  Array[Int] xs = [1, 2, 3]
  Array[String] ys = ["a", "b"]
  Array[Pair[Int, String]] expected = [
    (1, "a"), (1, "b"), (2, "a"), (2, "b"), (3, "a"), (3, "b")
  ]
  
  output {
    Boolean is_true = cross(xs, ys) == expected
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_cross.is_true": true
}
```
</p>
</details>

### `zip`

```
Array[Pair[X,Y]] zip(Array[X], Array[Y])
```

Creates an array of `Pair`s containing the [dot product](https://en.wikipedia.org/wiki/Dot_product) of two input arrays, i.e., the elements at the same indices in each array `X[i]` and `Y[i]` are combined together into (`X[i]`, `Y[i]`) for each `i` in `range(length(X))`. The input arrays must have the same lengths or an error is raised. If the input arrays are empty, an empty array is returned.

**Parameters**

1. `Array[X]`: The first array of length `N`.
2. `Array[Y]`: The second array of length `N`.

**Returns**: An `Array[Pair[X, Y]]` of length `N`.

<details>
<summary>
Example: test_zip.wdl

```wdl
verison 1.1

workflow test_zip {
  Array[Int] xs = [1, 2, 3]
  Array[String] ys = ["a", "b", "c"]
  Array[Pair[Int, String]] expected = [(1, "a"), (2, "b"), (3, "c")]
  
  output {
    Boolean is_true = zip(xs, ys) == expected
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_zip.is_true": true
}
```
</p>
</details>

<details>
<summary>
Example: test_zip_fail.wdl

```wdl
verison 1.1

workflow test_zip_fail {
  Array[Int] xs = [1, 2, 3]
  Array[String] zs = ["d", "e"]
  # this fails with an error - xs and zs are not the same length
  Array[Pair[Int, String]] bad = zip(xs, zs)

  meta {
    test_config: "fail"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{}
```
</p>
</details>

### ✨ `unzip`

```
Pair[Array[X], Array[Y]] unzip(Array[Pair[X, Y]])
```

Creates a `Pair` of `Arrays`, the first containing the elements from the `left` members of an `Array` of `Pair`s, and the second containing the `right` members. If the array is empty, a pair of empty arrays is returned. This is the inverse of the `zip` function.

**Parameters**

1. `Array[Pair[X, Y]]`: The `Array` of `Pair`s of length `N` to unzip.

**Returns**: A `Pair[Array[X], Array[Y]]` where each `Array` is of length `N`.

<details>
<summary>
Example: test_unzip.wdl

```wdl
verison 1.1

workflow test_unzip {
  Array[Pair[Int, String]] int_str_arr = [(0, "hello"), (42, "goodbye")]
  Map[String, Int] m = {"a": 0, "b": 1, "c": 2}
  Pair[Array[X], Pair[Array[Y]]] keys_and_values = unzip(as_pairs(map))

  output {
    Boolean is_true1 = unzip(int_str_arr) == ([0, 42], ["hello", "goodbye"])
    Boolean is_true2 = keys_and_values.left == ["a", "b", "c"]
    Boolean is_true3 = keys_and_values.right == [0, 1, 2]
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_unzip.is_true1": true,
  "test_unzip.is_true2": true,
  "test_unzip.is_true3": true
}
```
</p>
</details>

### `flatten`

```
Array[X] flatten(Array[Array[X]])
```

Flattens a nested `Array[Array[X]]` by concatenating all of the element arrays, in order, into a single array. The function is not recursive - e.g. if the input is `Array[Array[Array[Int]]]` then the output will be `Array[Array[Int]]`. The elements in the concatenated array are *not* deduplicated.

**Parameters**

1. `Array[Array[X]]`: A nested array to flatten.

**Returns**: An `Array[X]` containing the concatenated elements of the input array.

<details>
<summary>
Example: test_flatten.wdl

```wdl
verison 1.1

workflow test_flatten {
  Array[Array[Int]] ai2D = [[1, 2, 3], [1], [21, 22]]
  Array[Array[File]] af2D = [["/tmp/X.txt"], ["/tmp/Y.txt", "/tmp/Z.txt"], []]
  Array[Array[Pair[Float, String]]] aap2D = [[(0.1, "mouse")], [(3, "cat"), (15, "dog")]]
  Map[Float, String] f2s = as_map(flatten(aap2D))
  Array[Array[Array[Int]]] ai3D = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]

  output {
    Boolean is_true1 = flatten(ai2D) == [1, 2, 3, 1, 21, 22]
    Boolean is_true2 = flatten(af2D) == ["/tmp/X.txt", "/tmp/Y.txt", "/tmp/Z.txt"]
    Boolean is_true3 = flatten(aap2D) == [(0.1, "mouse"), (3, "cat"), (15, "dog")]
    Boolean is_true4 = flatten(ai3D) == [[1, 2], [3, 4], [5, 6], [7, 8]]
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_flatten.is_true1": true,
  "test_flatten.is_true2": true,
  "test_flatten.is_true3": true,
  "test_flatten.is_true4": true
}
```
</p>
</details>

### `select_first`

```
X select_first(Array[X?]+)
```

Selects the first - i.e. left-most - non-`None` value from an `Array` of optional values. It is an error if the array is empty, or if the array only contains `None` values. 

**Parameters**

1. `Array[X?]+`: Non-empty `Array` of optional values.

**Returns**: The first non-`None` value in the input array.

<details>
<summary>
Example: test_select_first.wdl

```wdl
verison 1.1

workflow test_select_first {
  input {
    Int? maybe_five = 5
    Int? maybe_four_but_is_not = None
    Int? maybe_three = 3
  }

  output {
    # both of these statements evaluate to 5
    Int five1 = select_first([maybe_five, maybe_four_but_is_not, maybe_three])
    Int five2 = select_first([maybe_four_but_is_not, maybe_five, maybe_three])
  }

  select_first([maybe_four_but_is_not])  # error! array contains only None values
  select_first([])  # error! array is empty
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_select_first.five1": 5,
  "test_select_first.five2": 5,
}
```
</p>
</details>

<details>
<summary>
Example: select_first_only_none_fail.wdl

```wdl
verison 1.1

workflow select_first_only_none_fail {
  Int? maybe_four_but_is_not = None
  select_first([maybe_four_but_is_not])  # error! array contains only None values
  
  meta {
    test_config: "fail"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{}
```
</p>
</details>

<details>
<summary>
Example: select_first_empty_fail.wdl

```wdl
verison 1.1

workflow select_first_empty_fail {
  select_first([])  # error! array is empty
  
  meta {
    test_config: "fail"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{}
```
</p>
</details>

### `select_all`

```
Array[X] select_all(Array[X?])
```

Filters the input `Array` of optional values by removing all `None` values. The elements in the output `Array` are in the same order as the input `Array`. If the input array is empty or contains only `None` values, an empty array is returned.

**Parameters**

1. `Array[X?]`: `Array` of optional values.

**Returns**: an `Array` of all non-`None` values in the input array.

<details>
<summary>
Example: test_select_all.wdl

```wdl
verison 1.1

workflow test_select_all {
  input {
    Int? maybe_five = 5
    Int? maybe_four_but_is_not = None
    Int? maybe_three = 3
  }

  Array[Int] fivethree = select_all([maybe_five, maybe_four_but_is_not, maybe_three])

  output {
    Boolean is_true = fivethree == [5, 3]
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_select_all.is_true": true
}
```
</p>
</details>

## Map Functions

These functions are generic and take a `Map` as input and/or return a `Map`.

**Restrictions**: None

### ✨ `as_pairs`

```
Array[Pair[P, Y]] as_pairs(Map[P, Y])
```

Converts a `Map` into an `Array` of `Pair`s. Since `Map`s are ordered, the output array will always have elements in the same order they were added to the `Map`.

**Parameters**

1. `Map[P, Y]`: `Map` to convert to `Pair`s.

**Returns**: Ordered `Array` of `Pair`s, where each pair contains the key (left) and value (right) of a `Map` element.

<details>
<summary>
Example: test_as_pairs.wdl

```wdl
verison 1.1

workflow test_as_pairs {
  Map[String, Int] x = {"a": 1, "c": 3, "b": 2}
  Map[String, Pair[File, File]] y = {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}
  
  scatter (item in as_pairs(y)) {
    String s = item.left
    Pair[File, File] files = item.right
    Pair[File, String] bams = (files.left, s)
  }
  
  Map[File, String] bam_to_name = as_map(bams)

  output {
    Boolean is_true1 = as_pairs(x) == [("a", 1), ("c", 3), ("b", 2)]
    Boolean is_true2 = bams == [("a.bam", "a"), ("b.bam", "b")]
    Boolean is_true3 = bam_to_name == {"a.bam": "a", "b.bam": "b"}
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_as_pairs.is_true1": true,
  "test_as_pairs.is_true2": true,
  "test_as_pairs.is_true3": true
}
```
</p>
</details>

### ✨ `as_map`

```
Map[P, Y] as_map(Array[Pair[P, Y]])
```

Converts an `Array` of `Pair`s into a `Map` in which the left elements of the `Pair`s are the keys and the right elements the values. All the keys must be unique, or an error is raised. The order of the key/value pairs in the output `Map` is the same as the order of the `Pair`s in the `Array`.

**Parameters**

1. `Array[Pair[P, Y]]`: Array of `Pair`s to convert to a `Map`.

**Returns**: `Map[P, Y]` of the elements in the input array.

<details>
<summary>
Example: test_as_map.wdl

```wdl
verison 1.1

workflow test_as_map {
  Array[Pair[String, Int]] x = [("a", 1), ("c", 3), ("b", 2)]
  Array[Pair[String, Pair[File,File]]] y = [("a", ("a.bam", "a.bai")), ("b", ("b.bam", "b.bai"))]

  output {
    Boolean is_true1 = as_map(x) == {"a": 1, "c": 3, "b": 2}
    Boolean is_true2 = as_map(y) == {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_as_map.is_true1": true,
  "test_as_map.is_true2": true
}
```
</p>
</details>

<details>
<summary>
Example: test_as_map_fail.wdl

```wdl
verison 1.1

workflow test_as_map_fail {
  # this fails with an error - the "a" key is duplicated
  Boolean bad = as_map([("a", 1), ("a", 2)])

  meta {
    test_config: "fail"
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{}
```
</p>
</details>

### ✨ `keys`

```
Array[P] keys(Map[P, Y])
```

Creates an `Array` of the keys from the input `Map`, in the same order as the elements in the map.

**Parameters**

1. `Map[P, Y]`: `Map` from which to extract keys.

**Returns**: `Array[P]` of the input `Map`s keys.

<details>
<summary>
Example: test_keys.wdl

```wdl
verison 1.1

workflow test_keys {
  Map[String,Int] x = {"a": 1, "b": 2, "c": 3}
  Map[String, Pair[File, File]] str_to_files = {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}

  scatter (item in str_to_files) {
    String key = item.left
  }

  Array[String] str_to_files_keys = key

  output {
    Boolean is_true1 = keys(x) == ["a", "b", "c"]
    Boolean is_true2 = str_to_files_keys == keys(str_to_files)
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_keys.is_true1": true,
  "test_keys.is_true2": true
}
```
</p>
</details>

### ✨ `collect_by_key`

```
Map[P, Array[Y]] collect_by_key(Array[Pair[P, Y]])
```

Given an `Array` of `Pair`s, creates a `Map` in which the right elements of the `Pair`s are grouped by the left elements. In other words, the input `Array` may have multiple `Pair`s with the same key. Rather than causing an error (as would happen with [`as_map`](#✨-as_map)), all the values with the same key are grouped together into an `Array`.

The order of the keys in the output `Map` is the same as the order of their first occurrence in the input `Array`. The order of the elements in the `Map` values is the same as their order of occurrence in the input `Array`.

**Parameters**

1. `Array[Pair[P, Y]]`: `Array` of `Pair`s to group.

**Returns**: `Map` of keys to `Array`s of values.

<details>
<summary>
Example: test_collect_by_key.wdl

```wdl
verison 1.1

workflow test_collect_by_key {
  Array[Pair[String, Int]] x = [("a", 1), ("b", 2), ("a", 3)]
  Array[Pair[String, Pair[File, File]]] y = [
    ("a", ("a_1.bam", "a_1.bai")), 
    ("b", ("b.bam", "b.bai")), 
    ("a", ("a_2.bam", "a_2.bai"))
  ]

  output {
    Boolean is_true1 = collect_by_key(x) == {"a": [1, 3], "b": [2]}
    Boolean is_true2 = collect_by_key(y) == {
      "a": [("a_1.bam", "a_1.bai"), ("a_2.bam", "a_2.bai")], 
      "b": [("b.bam", "b.bai")]
    }
  }
}
```
</summary>
<p>
Example input:

```json
{}
```

Example output:

```json
{
  "test_collect_by_key.is_true1": true,
  "test_collect_by_key.is_true2": true
}
```
</p>
</details>

## Other Functions

### `defined`

```
Boolean defined(X?)
```

Tests whether the given optional value is defined, i.e., has a non-`None` value.

**Parameters**

1. `X?`: optional value of any type.

**Returns**: `false` if the input value is `None`, otherwise `true`.

<details>
<summary>
Example: is_defined.wdl

```wdl
verison 1.1

workflow is_defined {
  input {
    String? name
  }

  if (defined(s)) {
    call say_hello { input: name = select_first([name]) }
  }

  output {
    String? greeting = say_hello.greeting
  }
}

task say_hello {
  input {
    String name
  }

  command <<< echo "Hello ~{name}" >>>

  output {
    String greeting = read_string(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{
  "is_defined.name": "John"
}
```

Example output:

```json
{
  "is_defined.greeting": "Hello John"
}
```
</p>
</details>

# Input and Output Formats

WDL uses [JSON](https://www.json.org) as its native serialization format for task and workflow inputs and outputs. The specifics of these formats are described below.

All WDL implementations are required to support the standard JSON input and output formats. WDL compliance testing is performed using test cases whose inputs and expected outputs are given in these formats. A WDL implementation may choose to support any additional input and output mechanisms so long as they are documented, and or tools are provided to interconvert between engine-specific input and the standard JSON format, to foster interoperability between tools in the WDL ecosystem.

## JSON Input Format

The inputs for a workflow invocation may be specified as a single JSON object that contains one member for each top-level workflow, subworkflow, or task input. The name of the object member is the [fully-qualified name](#fully-qualified-names--namespaced-identifiers) of the input parameter, and the value is the [serialized form](#appendix-a-wdl-value-serialization-and-deserialization) of the WDL value.

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

The outputs from a workflow invocation may be specified as a single JSON object that contains one member for each top-level workflow output; sub-workflow and task outputs are not provided. The name of the object member is the [fully-qualified name](#fully-qualified-names--namespaced-identifiers) of the output parameter, and the value is the [serialized form](#appendix-a-wdl-value-serialization-and-deserialization) of the WDL value.

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

| WDL Type  | JSON Type |
| --------- | --------- |
| `Int`     | number    |
| `Float`   | number    |
| `Boolean` | boolean   |
| `String`  | string    |
| `File`    | string    |
| `None`    | null      |

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

| Element        |
| -------------- |
| /path/to/1.bam |
| /path/to/2.bam |
| /path/to/3.bam |

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

| Element        |
| -------------- |
| /path/to/1.bam |
| /path/to/2.bam |
| /path/to/3.bam |

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

| Element        |
| -------------- |
| /path/to/1.bam |
| /path/to/2.bam |
| /path/to/3.bam |

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

This return value can be immediately coerced to an `Array[P]` value, where `P` is another primitive type. For example:

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

It is strongly recommended to instead use `read_json` to read a JSON file containing an array, as described in the next section.

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

| Key     | Value |
| ------- | ----- |
| sample1 | 98    |
| sample2 | 95    |
| sample3 | 75    |

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

| Key     | Value |
| ------- | ----- |
| sample1 | 98    |
| sample2 | 95    |
| sample3 | 75    |

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

| Key   | Value |
| ----- | ----- |
| key_0 | 0     |
| key_1 | 1     |
| key_2 | 2     |

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

| Key | Value |
| --- | ----- |
| foo | bar   |

Using `write_json`/`read_json` to serialize to/from a `Map` can lead to subtle issues due to the fact that `Map` is ordered whereas `Object` is not. For example:

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
