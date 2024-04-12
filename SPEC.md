# Workflow Description Language (WDL)

This is version 1.1.2 of the Workflow Description Language (WDL) specification. It describes WDL `version 1.1`. It introduces a number of new features (denoted by the ✨ symbol) and clarifications to the [1.0](https://github.com/openwdl/wdl/blob/main/versions/1.0/SPEC.md) version of the specification. It also deprecates several aspects of the 1.0 specification that will be removed in the [next major WDL version](https://github.com/openwdl/wdl/blob/wdl-2.0/SPEC.md) (denoted by the 🗑 symbol).

## Revisions

Revisions to this specification are made periodically in order to correct errors, clarify language, or add additional examples. Revisions are released as "patches" to the specification, i.e., the third number in the specification version is incremented. No functionality is added or removed after the initial revision of the specification is ratified.

* [1.1.2](https://github.com/openwdl/wdl/tree/release-1.1.2/SPEC.md): 2024-04-12
* [1.1.1](https://github.com/openwdl/wdl/tree/release-1.1.1/SPEC.md): 2023-10-04
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
    - [Comments](#comments)
    - [Reserved Keywords](#reserved-keywords)
    - [Literals](#literals)
    - [Types](#types)
      - [Primitive Types](#primitive-types)
        - [Strings](#strings)
      - [Optional Types and None](#optional-types-and-none)
      - [Compound Types](#compound-types)
        - [Array\[X\]](#arrayx)
        - [Pair\[X, Y\]](#pairx-y)
        - [Map\[P, Y\]](#mapp-y)
        - [🗑 Object](#-object)
        - [Custom Types (Structs)](#custom-types-structs)
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
  - [Struct Definition](#struct-definition)
  - [Import Statements](#import-statements)
    - [Import URIs](#import-uris)
    - [Importing and Aliasing Structs](#importing-and-aliasing-structs)
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
        - [`maxCpu`](#maxcpu)
        - [`maxMemory`](#maxmemory)
        - [`shortTask`](#shorttask)
        - [`localizationOptional`](#localizationoptional)
        - [`inputs`](#inputs)
        - [`outputs`](#outputs)
      - [Conventions and Best Practices](#conventions-and-best-practices)
    - [Metadata Sections](#metadata-sections)
      - [Task Metadata Section](#task-metadata-section)
      - [Parameter Metadata Section](#parameter-metadata-section)
    - [Advanced Task Examples](#advanced-task-examples)
      - [Example 1: HISAT2](#example-1-hisat2)
      - [Example 2: GATK Haplotype Caller](#example-2-gatk-haplotype-caller)
  - [Workflow Definition](#workflow-definition)
    - [Workflow Elements](#workflow-elements)
    - [Workflow Inputs](#workflow-inputs)
    - [Workflow Outputs](#workflow-outputs)
    - [Evaluation of Workflow Elements](#evaluation-of-workflow-elements)
    - [Fully Qualified Names \& Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers)
    - [Call Statement](#call-statement)
      - [Computing Call Inputs](#computing-call-inputs)
    - [Scatter Statement](#scatter-statement)
    - [Conditional Statement](#conditional-statement)
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
    - [Specifying / Overriding Runtime Attributes](#specifying--overriding-runtime-attributes)
  - [JSON Output Format](#json-output-format)
  - [JSON Serialization of WDL Types](#json-serialization-of-wdl-types)
    - [Primitive Types](#primitive-types-1)
    - [Array](#array)
    - [Struct and Object](#struct-and-object)
    - [Pair](#pair)
      - [Pair to Array](#pair-to-array)
      - [Pair to Struct](#pair-to-struct)
    - [Map](#map)
      - [Map to Struct](#map-to-struct)
      - [Map to Array](#map-to-array)
- [Appendix A: WDL Value Serialization and Deserialization](#appendix-a-wdl-value-serialization-and-deserialization)
  - [Primitive Values](#primitive-values)
  - [Compound Values](#compound-values)
    - [Array](#array-1)
      - [Array serialization by delimitation](#array-serialization-by-delimitation)
      - [Array serialization/deserialization using `write_lines()`/`read_lines()`](#array-serializationdeserialization-using-write_linesread_lines)
      - [Array serialization/deserialization using `write_json()`/`read_json()`](#array-serializationdeserialization-using-write_jsonread_json)
    - [Pair](#pair-1)
      - [Homogeneous Pair serialization/deserialization as Array](#homogeneous-pair-serializationdeserialization-as-array)
      - [Pair serialization/deserialization using `read_json`/`write_json`](#pair-serializationdeserialization-using-read_jsonwrite_json)
    - [Map](#map-1)
      - [Map serialization by delimitation](#map-serialization-by-delimitation)
      - [Map serialization/deserialization using `write_map()`/`read_map()`](#map-serializationdeserialization-using-write_mapread_map)
      - [Map serialization/deserialization using `write_json()`/`read_json()`](#map-serializationdeserialization-using-write_jsonread_json)
    - [Struct and Object serialization/deserialization](#struct-and-object-serializationdeserialization)
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
      grep -E '~{pattern}' '~{infile}'
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

This WDL document describes a task, called `hello_task`, and a workflow, called `hello`.

* A task encapsulates a Bash script and a UNIX environment and presents them as a reusable function.
* A workflow encapsulates a (directed, acyclic) graph of task calls that transforms input data to the desired outputs.

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
grep -E 'hello.*' 'greetings.txt'
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
    "hello_parallel.files": ["/greetings.txt", "greetings2.txt"]
  }
  ```
  
  Example output:
  
  ```json
  {
    "hello.all_matches": [["hi_world"], ["hi_pal"]]
  }
  ```
  </p>
</details>

# WDL Language Specification

## Global Grammar Rules

WDL files are encoded in UTF-8, with no byte order mark (BOM).

### Whitespace

Whitespace may be used anywhere in a WDL document. Whitespace has no meaning in WDL, and is effectively ignored.

The following characters are treated as whitespace:

| Name  | Dec | Hex    |
| ----- | --- | ------ |
| Space | 32  | `\x20` |
| Tab   | 9   | `\x09` |
| CR    | 13  | `\x0D` |
| LF    | 10  | `\x0A` |

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

### Literals

Task and workflow inputs may be passed in from an external source, or they may be specified in the WDL document itself using literal values. Input, output, and other declaration values may also be constructed at runtime using [expressions](#expressions) that consist of literals, identifiers (references to [declarations](#declarations) or [call](#call-statement) outputs), built-in [operators](#operator-precedence-table), and [standard library functions](#standard-library).

### Types

A [declaration](#declarations) is a name that the user reserves in a given [scope](#appendix-b-wdl-namespaces-and-scopes) to hold a value of a certain type. In WDL *all* declarations (including inputs and outputs) must be typed. This means that the information about the type of data that may be held by each declarations must be specified explicitly.

In WDL *all* types represent immutable values. For example, a `File` represents a logical "snapshot" of the file at the time when the value was created. It is impossible for a task to change an upstream value that has been provided as an input - even if it modifies its local copy, the original value is unaffected.

#### Primitive Types

The following primitive types exist in WDL:

* A `Boolean` represents a value of `true` or `false`.
* An `Int` represents a signed 64-bit integer (in the range `[-2^63, 2^63)`).
* A `Float` represents a finite 64-bit IEEE-754 floating point number.
* A `String` represents a unicode character string following the format described [below](#strings).
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
    printf "hello" > hello.txt
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

##### Strings

A string literal may contain any unicode characters between single or double-quotes, with the exception of a few special characters that must be escaped:

| Escape Sequence | Meaning      | \x Equivalent | Context                       |
| --------------- | ------------ | ------------- | ----------------------------- |
| `\\`            | `\`          | `\x5C`        |                               |
| `\n`            | newline      | `\x0A`        |                               |
| `\t`            | tab          | `\x09`        |                               |
| `\'`            | single quote | `\x22`        | within a single-quoted string |
| `\"`            | double quote | `\x27`        | within a double-quoted string |
| `\~`            | tilde        | `\x7E`        | literal `"~{"`                |
| `\$`            | dollar sign  | `\x24`        | literal `"${"`                |

Strings can also contain the following types of escape sequences:

* An octal escape code starts with `\`, followed by 3 digits of value 0 through 7 inclusive.
* A hexadecimal escape code starts with `\x`, followed by 2 hexadecimal digits `0-9a-fA-F`. 
* A unicode code point starts with `\u` followed by 4 hexadecimal characters or `\U` followed by 8 hexadecimal characters `0-9a-fA-F`.

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
      Boolean test_non_equal = maybe_five_but_is_not == also_maybe_five_but_is_not
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
    "optionals.test_not_none": false
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

  Test config:

  ```json
  {
    "fail": true
  }
  ```
  </p>
</details>

An `Array` may have an empty value (i.e. an array of length zero), unless it is declared using `+`, the non-empty postfix quantifier, which represents a constraint that the `Array` value must contain one-or-more elements. For example, the following task operates on an `Array` of `String`s and it requires at least one string to function:

<details>
<summary>
Example: sum_task.wdl

```wdl
version 1.1

task sum {
  input {
    Array[String]+ ints
  }
  
  command <<<
  printf ~{sep(" ", ints)} | awk '{tot=0; for(i=1;i<=NF;i++) tot+=$i; print tot}'
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
  "sum.ints": ["0", "1", "2"]
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
    Array[Int]+? nonempty3 = None
    Array[Int]+? nonempty4 = [0]
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
  "non_empty_optional.nonempty4": [0.0]
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

Test config:

```json
{
  "fail": true
}
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
version 1.1

workflow test_pairs {
  Pair[Int, Array[String]] data = (5, ["hello", "goodbye"])

  output {
    Int five = data.left  # evaluates to 5
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
version 1.1

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
version 1.1

workflow test_map_fail {
  Map[String, Int] string_to_int = { "a": 1, "b": 2 }
  Int c = string_to_int["c"]  # error - "c" is not a key in the map
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

Test config:

```json
{
  "fail": true
}
```
</p>
</details>

A `Map` is insertion-ordered, meaning the order in which elements are added to the `Map` is preserved, for example when [✨ converting a `Map` to an array of `Pair`s](#-as_pairs).

<details>
<summary>
Example: test_map_ordering.wdl

```wdl
version 1.1

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

##### 🗑 Object

An `Object` is an unordered associative array of name-value pairs, where values may be of any type and are not defined explicitly.

An `Object` can be initialized using an object literal value, which begins with the `object` keyword followed by a comma-separated list of name-value pairs in braces (`{}`), where name-value pairs are delimited by `:`. The member names in an object literal are not quoted. The value of a specific member of an `Object` value can be accessed by placing a `.` followed by the member name after the identifier.

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

Due to the lack of explicitness in the typing of `Object` being at odds with the goal of being able to know the type information of all WDL declarations, the use of the `Object` type and the `object` literal syntax have been deprecated. In WDL 2.0, `Object` will become a [hidden type](#hidden-types) that may only be instantiated by the execution engine. `Object` declarations can be replaced with use of [structs](#struct-definition).

##### Custom Types (Structs)

WDL provides the ability to define custom compound types called [structs](#struct-definition). `Struct` types are defined directly in the WDL document and are usable like any other type. A struct is defined using the `struct` keyword, followed by a unique name, followed by member declarations within braces. A struct definition contains any number of declarations of any types, including other `Struct`s.

A declaration with a custom type can be initialized with a struct literal, which begins with the `Struct` type name followed by a comma-separated list of name-value pairs in braces (`{}`), where name-value pairs are delimited by `:`. The member names in a struct literal are not quoted. A struct literal must provide values for all of the struct's non-optional members, and may provide values for any of the optional members. The members of a struct literal are validated against the struct's definition at the time of creation. Members do not need to be in any specific order. Once a struct literal is created, it is immutable like any other WDL value.

The value of a specific member of a struct value can be [accessed](#member-access) by placing a `.` followed by the member name after the identifier.

<details>
<summary>
Example: test_struct.wdl

```wdl
version 1.1

struct BankAccount {
  String account_number
  Int routing_number
  Float balance
  Array[Int]+ pin_digits
  String? username
}

struct Person {
  String name
  BankAccount? account
}

workflow test_struct {
  output {
    Person john = Person {
      name: "John",
      # it's okay to leave out username since it's optional
      account: BankAccount {
        account_number: "123456",
        routing_number: 300211325,
        balance: 3.50,
        pin_digits: [1, 2, 3, 4]
      }
    }
    Boolean has_account = defined(john.account)
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
    "account": {
      "account_number": "123456",
      "routing_number": 300211325,
      "balance": 3.5,
      "pin_digits": [1, 2, 3, 4]
    }
  },
  "test_struct.has_account": true
}
```
</p>
</details>

<details>
<summary>
Example: incomplete_struct_fail.wdl

```wdl
version 1.1

# importing a WDL automatically imports all its structs into
# the current namespace
import "test_struct.wdl"

workflow incomplete_struct {
  output {
    # error! missing required account_number
    Person fail1 = Person {
      "name": "Sam",
      "account": BankAccount {
        routing_number: 611325474,
        balance: 9.99,
        pin_digits: [5, 5, 5, 5]
      }
    }
    # error! pin_digits is empty
    Person fail2 = Person {
      "name": "Bugs",
      "account": BankAccount {
        account_number: "FATCAT42",
        routing_number: 880521345,
        balance: 50.01,
        pin_digits: []
      }
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
{}
```
</p>
</details>

🗑 It is also possible to assign an `Object` or `Map[String, X]` value to a `Struct` declaration. In the either case:

* The `Object`/`Map` must not have any members that are not declared for the struct.
* The value of each object/map member must be coercible to the declared type of the struct member.
* The `Object`/`Map` must at least contain values for all of the struct's non-optional members.

Note that the ability to assign values to `Struct` declarations other than struct literals is deprecated and will be removed in WDL 2.0.

#### Hidden Types

A hidden type is one that may only be instantiated by the execution engine, and cannot be used in a declaration within a WDL file. There is currently only one hidden type, `Union`; however, in WDL 2.0, `Object` will also become a hidden type.

##### Union

The `Union` type is used for a value that may have any one of several concrete types. A `Union` value must always be coerced to a concrete type. The `Union` type is used in the following contexts:

* It is the type of the special [`None`](#optional-types-and-none) value.
* It is the return type of some standard library functions, such as [`read_json`](#read_json).
* It is the type of some reserved [`runtime`](#runtime-section) attributes.

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

```wdl
String s = "1.0"
Float f = 2.0
String x = "~{s + f}"
```

There are two possible ways to evaluate the `s + f` expression:

1. Coerce `s` to `Float` and perform floating point addition, then coerce to `String` with the result being `x = "3.0"`.
2. Coerce `f` to `String` and perform string concatenation with result being `x = "1.02.0"`.

Similarly, the equality/inequality operators can be applied to any primitive values.

When applying `+`, `=`, or `!=` to primitive operands (`X`, `Y`), the order of precedence is:

1. (`Int`, `Int`) or (`Float`, `Float`): perform numeric addition/comparison
2. (`Int`, `Float`): coerce `Int` to `Float`, then perform numeric addition/comparison
3. (`String`, `String`): perform string concatenation/comparison
4. (`String`, `Y`): coerce `Y` to `String`, then perform string concatenation/comparison
5. Others: coerce `X` and `Y` to `String`, then perform string concatenation/comparison

Examples:

```wdl
# Evaluates to `"3.0"`: `1` is coerced to Float (`1.0`), then numeric addition
# is performed, and the result is converted to a string
String s1 = "~{1 + 2.0}"
# Evaluates to `"3.01"`: `1` is coerced to String, then concatenated with the 
# value of `s1`
String s2 = "~{s1 + 1}"
# Evaluates to `true`: `1` is coerced to Float (`1.0`), then numeric comparison 
# is performed
Boolean b1 = 1 == 1.0
# Evaluates to `true`: `true` is coerced to String, then string comparison is 
# performed
Boolean b2 = true == "true"
# Evaluates to `false`: `1` and `true` are both coerced to String, then string 
# comparison is performed
Boolean b3 = 1 == true
```

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

A declaration may be initialized with an [expression](#expressions), which includes the ability to refer to elements that are outputs of tasks.

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
    printf "Hello ~{name}"
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

Test config:

```json
{
  "fail": true
}
```
</p>
</details>

### Expressions

An expression is a compound statement that consists of literal values, identifiers (references to [declarations](#declarations) or [call](#call-statement) outputs), [built-in operators](#built-in-operators) (e.g., `+` or `>=`), and calls to [standard library functions](#standard-library).

A "literal" expression is one that consists only of a literal value. For example, `"foo"` is a literal `String` expression and `[1, 2, 3]` is a literal `Array[Int]` expression.

A "simple" expression is one that can be evaluated unambiguously without any knowledge of the runtime context. Literal expressions, operations on literals (e.g., `1 + 2`), and function calls with literal arguments (excluding any functions that read or create `File`s) are all simple expressions. A simple expression cannot refer to any declarations (i.e., it cannot contain identifiers). An execution engine may choose to replace a simple expression with its literal value during static analysis.

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
  printf "hello" > hello.txt
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

Boolean operator evaluation is minimal (or "short-circuiting"), meaning that:

1. For `A && B`, if `A` evalutes to `false` then `B` is not evaluated
2. For `A || B`, if `A` evaluates to `true` then `B` is not evaluated.

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
  "array_map_equality.is_false2": true
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
  Array[Float] f1 = i
  Array[Float] f2 = [1.0, 2.0, 3.0]

  output {
    # Ints are automatically coerced to Floats for comparison
    Boolean is_true = f1 == f2
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
    Boolean is_true2 = k == None
    # these comparisons are valid and evaluate to false
    Boolean is_false1 = i == k
    Boolean is_false2 = j == k
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
  "compare_optionals.is_false2": false
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
  command <<<
  printf "bar"
  >>>

  output {
    String bar = read_string(stdout())
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

Access to elements of compound members can be chained into a single expression.

<details>
<summary>
Example: nested_access.wdl

```wdl
version 1.1

struct Experiment {
  String id
  Array[String] variables
  Map[String, Float] data
}

workflow nested_access {
  input {
    Array[Experiment]+ my_experiments
  }

  Experiment first_experiment = my_experiments[0]
  
  output {
    # these are equivalent
    String first_var = first_experiment.variables[0]
    String first_var_from_first_experiment = my_experiments[0].variables[0]

    # these are equivalent
    String subject_name = first_experiment.data["name"]
    String subject_name_from_first_experiment = my_experiments[0].data["name"]
  }
}
```
</summary>
<p>
Example input:

```json
{
  "nested_access.my_experiments": [
    {
      "id": "mouse_size",
      "variables": ["name", "height"],
      "data": {
        "name": "Pinky",
        "height": 7
      }
    },
    {
      "id": "pig_weight",
      "variables": ["name", "weight"],
      "data": {
        "name": "Porky",
        "weight": 1000
      }
    }
  ]
}
```

Example output:

```json
{
  "nested_access.first_var": "name",
  "nested_access.first_var_from_first_experiment": "name",
  "nested_access.subject_name": "Pinky",
  "nested_access.subject_name_from_first_experiment": "Pinky"
}
```
</p>
</details>

#### Ternary operator (if-then-else)

This operator takes three arguments: a condition expression, an if-true expression, and an if-false expression. The condition is always evaluated. If the condition is `true` then the if-true value is evaluated and returned. If the condition is `false`, the if-false expression is evaluated and returned. The if-true and if-false expressions must return values of the same type, such that the value of the if-then-else is the same regardless of which side is evaluated.

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

  call mem { input: array = ["x", "y", "z"] }

  output {
    # Choose whether to say "good morning" or "good afternoon"
    String greeting = "good ~{if morning then "morning" else "afternoon"}"
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
    String instr
  }

  output {
    String s = "~{1 + i}"
    String cmd = "grep '~{start}...~{end}' ~{instr}"
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
  "placeholders.cmd": "grep 'h...o' hello"
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
  "placeholder_coercion.is_true7": true
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
    String salutation = "hello"
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
    File infile
    String pattern
    Int? max_matches
  }

  command <<<
    # If `max_matches` is `None`, the command
    # grep -m ~{max_matches} ~{pattern} ~{infile}
    # would evaluate to
    # 'grep -m <pattern> <infile>', which would be an error.

    # Instead, make both the flag and the value conditional on `max_matches`
    # being defined.
    grep ~{"-m " + max_matches} ~{pattern} ~{infile} | wc -l
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
  "flags.infile": "greetings.txt",
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
  "sep_option_to_function.is_true2": true
}
```

Test config:

```json
{
  "tags": ["deprecated"]
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
Example: true_false_ternary_task.wdl

```wdl
version 1.1

task true_false_ternary {
  input {
    String message
    Boolean newline
  }

  command <<<
    # these two commands have the same result
    printf "~{message}~{true="\n" false="" newline}" > result1
    printf "~{message}~{if newline then "\n" else ""}" > result2
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

Test config:

```json
{
  "tags": ["deprecated"]
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
    printf ~{default="foobar" s} > result1
    printf ~{if defined(s) then "~{select_first([s])}" else "foobar"} > result2
    printf ~{select_first([s, "foobar"])} > result3
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
  printf "~{sep(","), read_lines(f)}"
  >>>
}
```

## WDL Documents

A WDL document is a file that contains valid WDL definitions.

A WDL document must contain:

* A [`version` statement](#versioning) on the first non-comment line of the file.
* At least one [`struct` definition](#struct-definition), [`task` definition](#task-definition), [`workflow` definition](#workflow-definition).

A WDL document may contain any combination of the following:

* Any number of [`import` statements](#import-statements).
* Any number of `struct` definitions.
* Any number of `task` definitions.
* A maximum of one `workflow` definition.

To execute a WDL workflow, the user must provide the execution engine with the location of a "primary" WDL file (which may import additional files as needed) and any input values needed to satisfy all required task and workflow input parameters, using a [standard input JSON file](#json-input-format) or some other execution engine-specific mechanism.

If a workflow appears in the primary WDL file, it is called the "top-level" workflow, and any workflows it calls via imports are "subworkflows". Typically, it is an error for the primary WDL file to not contain a workflow; however, an execution engine may choose to support executing individual tasks.

## Versioning

There are multiple versions of the WDL specification. Every WDL document must include a version statement to specify which version (major and minor) of the specification it adheres to. From `draft-3` forward, the first non-comment statement of all WDL files must be a `version` statement. For example:

```wdl
version 1.1
```

or

```wdl
#Licence header

version 1.1
```

A WDL file that does not have a `version` statement must be treated as [`draft-2`](https://github.com/openwdl/wdl/blob/main/versions/draft-2/SPEC.md).

Because patches to the WDL specification do not change any functionality, all revisions that carry the same major and minor version numbers are considered equivalent. For example, `version 1.1` is used for a WDL document that adheres to the `1.1.x` specification, regardless of the value of `x`.

## Struct Definition

A `Struct` type is a user-defined data type. Structs enable the creation of compound data types that bundle together related attributes in a more natural way than is possible using the general-purpose compound types like `Pair` or `Map`. Once defined, a `Struct` type can be used as the type of a declaration like any other data type.

`Struct` definitions are top-level WDL elements, meaning they exist at the same level as `import`, `task`, and `workflow` definitions. A struct cannot be defined within a task or workflow body.

A struct is defined using the `struct` keyword, followed by a name that is unique within the WDL document, and a body containing the member declarations. A struct member may be of any type, including compound types and even other `Struct` types. A struct member may be optional. Declarations in a struct body differ from those in a task or workflow in that struct members cannot have default initializers.

<details>
<summary>
Example: person_struct_task.wdl

```wdl
version 1.1

struct Name {
  String first
  String last
}

struct Income {
  Float amount
  String period
  String? currency
}

struct Person {
  Name name
  Int age
  Income? income
  Map[String, File] assay_data
}

task greet_person {
  input {
    Person person
  }

  Array[Pair[String, File]] assay_array = as_pairs(person.assay_data)

  command <<<
  printf "Hello ~{person.name.first}! You have ~{length(assay_array)} test result(s) available.\n"

  if ~{defined(person.income)}; then
    if [ "~{select_first([person.income]).amount}" -gt 1000 ]; then
      currency="~{select_first([select_first([person.income]).currency, "USD"])}"
      printf "Please transfer $currency 500 to continue"
    fi
  fi
  >>>

  output {
    String message = read_string(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{
  "person_struct.person": {
    "name": {
      "first": "Richard",
      "last": "Rich"
    },
    "age": 14,
    "income": {
      "amount": 1000000,
      "period": "annually"
    },
    "assay_data": {
      "wealthitis": "hello.txt"
    }
  }
}
```

Example output:

```json
{
  "person_struct.message": "Hello Richard! You have 1 test result(s) available.\nPlease transfer USD 500 to continue"
}
```

Test config:

```json
{
  "target": "greet_person"
}
```
</p>
</details>

An invalid struct:

```wdl
struct Invalid {
  String myString = "Cannot do this"
  Int myInt
}
```

## Import Statements

Although a WDL workflow and the task(s) it calls may be defined completely within a single WDL document, splitting it into multiple documents can be beneficial in terms of modularity and code resuse. Furthermore, complex workflows that consist of multiple subworkflows must be defined in multiple documents because each document is only allowed to contain at most one workflow.

The `import` statement is the basis for modularity in WDL. A WDL document may have any number of `import` statements, each of which references another WDL document and allows access to that document's top-level members (`task`s, `workflow`s, and `struct`s).

The `import` statement specifies a WDL document source as a string literal, which is interpreted as a URI. The execution engine is responsible for resolving each import URI and retrieving the contents of the WDL document. The contents of the document in each URI must be WDL source code **of the same version as the importing document**.

Each imported WDL document must be assigned a unique namespace that is used to refer to its members. By default, the namespace of an imported WDL document is the filename of the imported WDL, minus the `.wdl` extension. A namespace can be assigned explicitly using the `as <identifier>` syntax. The tasks and workflows imported from a WDL file are only accessible through the assigned [namespace](#namespaces) - see [Fully Qualified Names & Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers) for details.

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

### Import URIs

A document is imported using it's [URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier), which uniquely describes its local or network-accessible location. The execution engine must at least support the following protocols for import URIs:

* `http://`
* `https://`
* 🗑 `file://` - Using the `file://` protocol for local imports can be problematic. Its use is deprecated and will be removed in WDL 2.0.

In the event that there is no protocol specified, the import is resolved **relative to the location of the current document**. In the primary WDL document, a protocol-less import is relative to the host file system. If a protocol-less import starts with `/` it is interpreted as relative to the root of the host in the resolved URI.

Some examples of correct import resolution:

| Root Workflow Location                                | Imported Path                      | Resolved Path                                           |
| ----------------------------------------------------- | ---------------------------------- | ------------------------------------------------------- |
| /foo/bar/baz/qux.wdl                                  | some/task.wdl                      | /foo/bar/baz/some/task.wdl                              |
| http://www.github.com/openwdl/coolwdls/myWorkflow.wdl | subworkflow.wdl                    | http://www.github.com/openwdl/coolwdls/subworkflow.wdl  |
| http://www.github.com/openwdl/coolwdls/myWorkflow.wdl | /openwdl/otherwdls/subworkflow.wdl | http://www.github.com/openwdl/otherwdls/subworkflow.wdl |
| /some/path/hello.wdl                                  | /another/path/world.wdl            | /another/path/world.wdl                                 |

### Importing and Aliasing Structs

When importing a WDL document, any struct definitions in that document are "copied" into the importing document. This enables structs to be used by their name alone, without the need for any `namespace.` prefix.

A document may import two or more struct definitions with the same name so long as they are all identical. To be identical, two struct definitions must have members with exactly the same names and types and defined in exactly the same order.

A struct may be imported with a different name using an `alias` clause of the form `alias <source name> as <new name>`. If two structs have the same name but are not identical, at least one of them must be imported with a unique alias. To alias multiple structs, simply add more alias clauses to the `import` statement. If aliases are used for some structs in an imported WDL but not others, the unaliased structs are still imported under their original names.

<details>
<summary>
Example: import_structs.wdl

```wdl
version 1.1

import "person_struct_task.wdl"
  alias Person as Patient
  alias Income as PatientIncome

# This struct has the same name as a struct in 'structs.wdl',
# but they have identical definitions so an alias is not required.
struct Name {
  String first
  String last
}

# This struct also has the same name as a struct in 'structs.wdl',
# but their definitions are different, so it was necessary to
# import the struct under a different name.
struct Income {
  Float dollars
  Boolean annual
}

struct Person {
  Int age
  Name name
  Float? height
  Income income
}

task calculate_bill {
  input {
    Person doctor
    Patient patient
    PatientIncome average_income = PatientIncome {
      amount: 50000,
      currency: "USD",
      period: "annually"
    }
  }
  
  PatientIncome income = select_first([patient.income, average_income])
  String currency = select_first([income.currency, "USD"])
  Float hourly_income = if income.period == "hourly" then income.amount else income.amount / 2000
  Float hourly_income_usd = if currency == "USD" then hourly_income else hourly_income * 100

  command <<<
  printf "The patient makes $~{hourly_income_usd} per hour\n"
  >>>
  
  output {
    Float amount = hourly_income_usd * 5
  }
}

workflow import_structs {
  input {
    Person doctor = Person {
      age: 10,
      name: Name {
        first: "Joe",
        last: "Josephs"
      },
      income: Income {
        dollars: 140000,
        annual: true
      }
    }

    Patient patient = Patient {
      name: Name {
        first: "Bill",
        last: "Williamson"
      },
      age: 42,
      income: PatientIncome {
        amount: 350,
        currency: "Yen",
        period: "hourly"
      },
      assay_data: {
        "glucose": "hello.txt"
      }
    }
  }

  call person_struct.greet_person {
    input: person = patient
  }

  call calculate_bill {
    input: doctor = doctor, patient = patient
  }

  output {
    Float bill = calculate_bill.amount
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
  "import_structs.bill": 175000
}
```
</p>
</details>

When a struct `A` in document `X` is imported with alias `B` in document `Y`, any other structs imported from `X` into `Y` with members of type `A` are updated to replace `A` with `B` when copying them into `Y`'s namespace. The execution engine is responsible for maintaining mappings between structs in different namespaces, such that when a task or workflow in `X` with an input of type `A` is called from `Y` with a value of type `B` it is coerced appropriately.

To put this in concrete terms of the preceding example, when `Person` is imported from `structs.wdl` as `Patient` in `import_structs.wdl`, its `income` member is updated to have type `PatientIncome`. When the `person_struct.greet_person` task is called, the input of type `Patient` is coerced to the `Person` type that is defined in the `person_struct` namespace.

```wdl
struct Patient {
  Name name
  Int age
  PatientIncome? income
  Map[String, Array[File]] assay_data
}
```

## Task Definition

A WDL task can be thought of as a template for running a set of commands - specifically, a Bash script - in a manner that is (ideally) independent of the execution engine and the runtime environment.

A task is defined using the `task` keyword, followed by a task name that is unique within its WDL document.

Tasks are comprised of the following elements:

* A single, optional [`input`](#task-inputs) section, which defines the inputs for the task.
* A single, required [`command`](#command-section), which defines the Bash script to be executed.
* A single, optional [`output`](#task-outputs) section, which defines the outputs for the task.
* A single, optional [`requirements`](#✨-requirements-section) section, which defines the minimum, required runtime environment conditions.
* A single, optional [`hints`](#✨-hints-section) section, which provides hints to the execution engine.
* 🗑️ A single, optional [`runtime`](#-runtime-section) section, which defines the runtime environment conditions. This is mutually exclusive with the `requirements` and `hints` sections.
* A single, optional [`meta`](#metadata-sections) section, which defines task-level metadata.
* A single, optional [`parameter_meta`](#parameter-metadata-section) section, which defines parameter-level metadata.
* Any number of [private declarations](#private-declarations).

There is no enforced order for task elements.

The execution engine is responsible for "instantiating" the shell script (i.e., replacing all references with actual values) in an environment that meets all specified runtime requirements, localizing any input files into that environment, executing the script, and generating any requested outputs.

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

A task's `input` section declares its input parameters. The values for declarations within the `input` section may be specified by the caller of the task. An input declaration may be initialized to a default expression that will be used when the caller does not specify a value. Input declarations may also be optional, in which case a value may be specified but is not required. If an input declaration is not optional and does not have an initialization, then it is a required input, meaning the caller must specify a value.

<details>
<summary>
Example: task_inputs_task.wdl

```wdl
version 1.1

task task_inputs {
  input {
    Int i               # a required input parameter
    String s = "hello"  # an input parameter with a default value
    File? f             # an optional input parameter
  }

  command <<<
  for i in 1..~{i}; do
    printf "~{s}\n"
  done
  if ~{defined(f)}; then
    cat ~{f}
  fi
  >>>
}
```
</summary>
<p>
Example input:

```json
{
  "task_inputs.i": 1
}
```

Example output:

```json
{}
```
</p>
</details>

#### Task Input Localization

`File` inputs may require localization to the execution environment. For example, a file located on a remote web server that is provided to the execution engine as an `https://` URL must first be downloaded to the machine where the task is being executed.

- Files are localized into the execution environment prior to the task execution commencing.
- When localizing a `File`, the engine may choose to place the file wherever it likes so long as it adheres to these rules:
  - The original file name must be preserved even if the path to it has changed.
  - Two input files with the same name must be located separately, to avoid name collision.
  - Two input files that have the same parent location must be localized into the same directory for task execution. For example, `http://foo.com/bar/a.txt` and `http://foo.com/bar/b.txt` have the same parent (`http://foo.com/bar/`), so they must be localized into the same directory. See below for special-case handling for Versioning Filesystems.
- When a WDL author uses a `File` input in their [Command Section](#command-section), the fully qualified, localized path to the file is substituted when the command is instantiated.

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

<details>
<summary>
Example: input_type_quantifiers_task.wdl

```wdl
version 1.1

task input_type_quantifiers {
  input {
    Array[String]  a
    Array[String]+ b
    Array[String]? c
    # If the next line were uncommented it would cause an error
    # + only applies to Array, not File
    #File+ d
    # An optional array that, if defined, must contain at least one element
    Array[String]+? e
  }

  command <<<
    cat ~{write_lines(a)} >> result
    cat ~{write_lines(b)} >> result
    ~{if defined(c) then 
    "cat ~{write_lines(select_first([c]))} >> result"
    else ""}
    ~{if defined(e) then 
    "cat ~{write_lines(select_first([e]))} >> result"
    else ""}
  >>>

  output {
    Array[String] lines = read_lines("result")
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
  "input_type_quantifiers.a": [],
  "input_type_quantifiers.b": ["A", "B"],
  "input_type_quantifiers.e": ["C"]
}
```

Example output:

```json
{
  "input_type_quantifiers.lines": ["A", "B", "C"]
}
```
</p>
</details>

If these input values are provided:

| input | value           |
| ----- | --------------- |
| `a`   | ["1", "2", "3"] |
| `b`   | []              |

the task will fail with an error, because `test.b` is required to have at least one element.

On the other hand, if these input values are provided:

| var | value           |
| --- | --------------- |
| `a` | ["1", "2", "3"] |
| `b` | ["x"]           |

the task will run successfully (`c` and `d` are not required). Given these values, the command would be instantiated as:

```txt
cat /tmp/file1 >> result
cat /tmp/file2 >> result
```

If the inputs were:

| var | value                |
| --- | -------------------- |
| `a` | ["1", "2", "3"]      |
| `b` | ["x", "y"]           |
| `c` | ["a", "b", "c", "d"] |

then the command would be instantiated as:

```txt
cat /tmp/file1 >> result
cat /tmp/file2 >> result
cat /tmp/file3 >> result
```

##### Optional inputs with defaults

It *is* possible to provide a default to an optional input type. This may be desirable in the case where you want to have a defined value by default, but you want the caller to be able to override the default and set the value to undefined (`None`).

<details>
<summary>
Example: optional_with_default.wdl

```wdl
version 1.1

task say_hello {
  input {
    String name
    String? salutation = "hello"
  }

  command <<< >>>

  output {
    String greeting = if defined(salutation) then "~{salutation} ~{name}" else name
  }
}

workflow optional_with_default {
  input {
    String name
    Boolean use_salutation
  }
  
  if (use_salutation) {
    call say_hello as hello1 { 
      input: name = name 
    }
  }

  if (!use_salutation) {
    call say_hello as hello2 { 
      input: 
        name = name,
        salutation = None 
    }
  }

  output {
    String greeting = select_first([hello1.greeting, hello2.greeting])
  }
}
```
</summary>
<p>
Example input:

```json
{
  "optional_with_default.name": "John",
  "optional_with_default.use_salutation": false
}
```

Example output:

```json
{
  "optional_with_default.greeting": "John"
}
```
</p>
</details>

### Private Declarations

A task can have declarations that are intended as intermediate values rather than inputs. These private declarations may appear anywhere in the body of the task, and they must be initialized. Just like input declarations, private declarations may be initialized with literal values, or with expressions that may reference other declarations.

For example, this task takes an input and then performs a calculation, using a private declaration, that can then be referenced in the command template:

<details>
<summary>
Example: private_declaration_task.wdl

```wdl
version 1.1

task private_declaration {
  input {
    Array[String] lines
  }

  Int num_lines = length(lines)
  Int num_lines_clamped = if num_lines > 3 then 3 else num_lines

  command <<<
  head -~{num_lines_clamped} ~{write_lines(lines)}
  >>>

  output {
    Array[String] out_lines = read_lines(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{
  "private_declaration.lines": ["A", "B", "C", "D"]
}
```

Example output:

```json
{
  "private_declaration.out_lines": ["A", "B", "C"]
}
```
</p>
</details>

The value of a private declaration may *not* be specified by the task caller, nor is it accessible outside of the task [scope](#task-scope).

<details>
<summary>
Example: private_declaration_fail.wdl

```wdl
version 1.1

task test {
  input {
    Int i
  }
  String s = "hello"
  command <<< ... >>>
  output {
    String out = "goodbye"
  }
}

workflow private_declaration_fail {
  call test {
    input:
      i = 1,         # this is fine - "i" is in the input section
      s = "goodbye"  # error! "s" is private
  }

  output {
    String out = test.out # this is fine - "out" is in the output section
    String s = test.s # error! "s" is private
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

Test config:

```json
{
  "fail": true
}
```
</p>
</details>

### Command Section

The `command` section is the only required task section. It defines the command template that is evaluated to produce a Bash script that is executed within the task's container. Specifically, the commands are executed after all of the inputs are staged and before the outputs are evaluated.

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

The characters that must be escaped within a command section are different from those that must be escaped in regular strings:

* Unescaped newlines (`\n`) are allowed.
* An unescaped backslash (`\`) may appear as the last character on a line - this is treated as a line continuation.
* In a HEREDOC-style command section, if there are exactly three consecutive right-angle brackets (`>>>`), then at least one of them must be escaped, e.g. `\>>>`.
* In the older-style command section, any right brace (`}`) that is not part of an expression placeholder must be escaped.

#### Expression Placeholders

The body of the command section (the command "template") can be though of as a single string expression, which (like all string expressions) may contain placeholders.

There are two different syntaxes that can be used to define command expression placeholders, depending on which style of command section definition is used:

| Command Definition Style | Placeholder Style          |
| ------------------------ | -------------------------- |
| `command <<< >>>`        | `~{}` only                 |
| `command { ... }`        | `~{}` (preferred) or `${}` |

Note that the `~{}` and `${}` styles may be used interchangeably in other string expressions.

Any valid WDL expression may be used within a placeholder. For example, a command might reference an input to the task. The expression can also be more complex, such as a function call.

<details>
<summary>
Example: test_placeholders_task.wdl

```wdl
version 1.1

task test_placeholders {
  input {
    File infile
  }

  command <<<
    # The `read_lines` function reads the lines from a file into an
    # array. The `sep` function concatenates the lines with a space
    # (" ") delimiter. The resulting string is then printed to stdout.
    printf ~{sep(" ", read_lines(infile))}
  >>>
  
  output {
    # The `stdout` function returns a file with the contents of stdout.
    # The `read_string` function reads the entire file into a String.
    String result = read_string(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{
  "test_placeholders.infile": "greetings.txt"
}
```

Example output:

```json
{
  "test_placeholders.result": "hello world hi_world hello nurse"
}
```
</p>
</details>

In this case, `infile` within the `~{...}` placeholder is an identifier expression referencing the value of the `infile` input parameter that was specified at runtime. Since `infile` is a `File` declaration, the execution engine will have staged whatever file was referenced by the caller such that it is available on the local file system, and will have replaced the original value of the `infile` parameter with the path to the file on the local filesystem.

In most cases, the `~{}` style of placeholder is preferred, to avoid ambiguity between WDL placeholders and Bash variables, which are of the form `$name` or `${name}`. If the `command { ... }` style is used, then `${name}` is always interpreted as a WDL placeholder, so care must be taken to only use `$name` style Bash variables. If the `command <<< ... >>>` style is used, then only `~{name}` is interpreted as a WDL placeholder, so either style of Bash variable may be used.

<details>
<summary>
Example: bash_variables_fail_task.wdl

```wdl
version 1.1

task bash_variables {
  input {
    String str
  }
  
  command {
    # store value of WDL declaration "str" to Bash variable "s"
    s=${str}
    # echo the string referenced by Bash variable "s"
    printf $s
    # this causes an error since "s" is not a WDL declaration
    printf ${s}
  }
}
```
</summary>
<p>
Example input:

```json
{
  "bash_variables.str": "hello"
}
```

Example output:

```json
{}
```
</p>
</details>

Like any other WDL string, the command section is subject to the rules of [string interpolation](#expression-placeholders-and-string-interpolation): all placeholders must contain expressions that are valid when analyzed statically, and that can be converted to a `String` value when evaluated dynamically. However, the evaluation of placeholder expressions during command instantiation is more lenient than typical dynamic evaluation as described in [Expression Placeholder Coercion](#expression-placeholder-coercion).

The implementation is *not* responsible for interpreting the contents of the command section to check that it is a valid Bash script, ignore comment lines, etc. For example, in the following task the `greeting` declaration is commented out, so `greeting` is not a valid identifier in the task's scope. However, the placeholder in the command section refers to `greeting`, so the implementation will raise an error during static analysis. The fact that the placeholder occurs in a commented line of the Bash script doesn't matter.

<details>
<summary>
Example: bash_comment_fail_task.wdl

```wdl
version 1.1

task bash_comment {
  # String greeting = "hello"

  command <<<
  # printf "~{greeting} John!"
  >>>
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

#### Stripping Leading Whitespace

When a command template is evaluated, the execution engine first strips out all *common leading whitespace*.

For example, consider a task that calls the `python` interpreter with an in-line Python script:

<details>
<summary>
Example: python_strip_task.wdl

```wdl
version 1.1

task python_strip {
  input {
    File infile
  }

  command<<<
  python <<CODE
    with open("~{infile}") as fp:
      for line in fp:
        if not line.startswith('#'):
          print(line.strip())
  CODE
  >>>

  output {
    Array[String] lines = read_lines(stdout())
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
{
  "python_strip.infile": "comment.txt"
}
```

Example output:

```json
{
  "python_strip": ["A", "B", "C"]
}
```
</p>
</details>

Given an `infile` value of `/path/to/file`, the execution engine will produce the following Bash script, which has removed the two spaces that were common to the beginning of each line:

```sh
python <<CODE
  with open("/path/to/file") as fp:
    for line in fp:
      if not line.startswith('#'):
        print(line.strip())
CODE
```

When leading whitespace is a mix of tabs and spaces, the execution engine should issue a warning and leave the whitespace unmodified.

### Task Outputs

The `output` section contains declarations that are exposed as outputs of the task after the successful execution of the instantiated command. An output declaration must be initialized, and its value is evaluated only after the task's command completes successfully, enabling any files generated by the command to be used to determine its value.

<details>
<summary>
Example: outputs_task.wdl

```wdl
version 1.1

task outputs {
  input {
    Int t
  }

  command <<<
  printf ~{t} > threshold.txt
  touch a.csv b.csv
  >>>
  
  output {
    Int threshold = read_int("threshold.txt")
    Array[File]+ csvs = glob("*.csv")
    Boolean two_csvs = length(csvs) == 2
  }
}
```
</summary>
<p>
Example input:

```json
{
  "outputs.t": 5,
  "outputs.write_outstr": false
}
```

Example output:

```json
{
  "outputs.threshold": 5,
  "outputs.two_csvs": true
}
```

Test config:

```json
{
  "exclude_output": "csvs"
}
```
</p>
</details>

After the command is executed, the following outputs are expected to be found in the task execution directory:

- A file called "threshold.txt", which contains one line that consists of only an integer and whitespace.
- One or more files (as indicated by the `+` postfix quantifier) with the `.csv` extension in the working directory that are collected into an array by the [`glob`](#glob) function.

See the [WDL Value Serialization](#appendix-a-wdl-value-serialization-and-deserialization) section for more details.

#### Files and Optional Outputs

File outputs are represented as string paths.

A common pattern is to use a placeholder in a string expression to construct a file name as a function of the task input. For example:

<details>
<summary>
Example: file_output_task.wdl

```wdl
version 1.1

task file_output {
  input {
    String prefix
  }

  command <<<
    printf "hello" > ~{prefix}.hello
    printf "goodbye" > ~{prefix}.goodbye
  >>>

  output {
    Array[String] basenames = [basename("~{prefix}.hello"), basename("~{prefix}.goodbye")]
  }
}
```
</summary>
<p>
Example input:

```json
{
  "file_output.prefix": "foo"
}
```

Example output:

```json
{
  "file_output.basenames": ["foo.hello", "foo.goodbye"]
}
```
</p>
</details>

Another common pattern is to use the [`glob`](#glob) function to define outputs that might contain zero, one, or many files.

<details>
<summary>
Example: glob_task.wdl

```wdl
version 1.1

task glob {
  input {
    Int num_files
  }

  command <<<
  for i in 1..~{num_files}; do
    printf ${i} > file_${i}.txt
  done
  >>>

  output {
    Array[File] outfiles = glob("*.txt")
    Int last_file_contents = read_int(outfiles[num_files-1])
  }
}
```
</summary>
<p>
Example input:

```json
{
  "glob.num_files": 3
}
```

Example output:

```json
{
  "glob.last_file_contents": 3
}
```

Test config:

```json
{
  "exclude_output": "outfiles"
}
```
</p>
</details>

Relative paths are interpreted relative to the execution directory, whereas absolute paths are interpreted in a container-dependent way.

<details>
<summary>
Example: relative_and_absolute_task.wdl

```wdl
version 1.1

task relative_and_absolute {
  command <<<
  mkdir -p my/path/to
  printf "something" > my/path/to/something.txt
  >>>

  output {
    File something = read_string("my/path/to/something.txt")
    File bashrc = "/root/.bashrc"
  }

  runtime {
    container: "ubuntu:focal"
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
  "relative_and_absolute.something": "something"
}
```

Test config:

```json
{
  "exclude_output": "bashrc"
}
```
</p>
</details>

All file outputs are required to exist, otherwise the task will fail. However, an output may be declared as optional (e.g., `File?` or `Array[File?]`), in which case the value will be undefined if the file does not exist.

<details>
<summary>
Example: optional_output_task.wdl

```wdl
version 1.1

task optional_output {
  input {
    Boolean make_example2
  }
  command <<<
    printf "1" > example1.txt
    if ~{make_example2}; do
      printf "2" > example2.txt
    fi
  >>>
  output {
    File example1 = "example1.txt"
    File? example2 = "example2.txt"
    Array[File?] file_array = ["example1.txt", "example2.txt"]
    Int file_array_len = length(select_all(file_array))
  }
}
```
</summary>
<p>
Example input:

```json
{
  "optional_output.make_example2": false
}
```

Example output:

```json
{
  "optional_output.example2": null,
  "optional_output.file_array_len": 1
}
```

Test config:

```json
{
  "exclude_output": ["example1", "file_array"]
}
```
</p>
</details>

Executing the above task with `make_example2 = true` will result in the following outputs:

* `optional_output.example1` will resolve to a`File`
* `optional_output.example2` will resolve to `None`
* `optional_output.file_array` will resolve to `[<File>, None]`

### Evaluation of Task Declarations

All non-output declarations (i.e., input and private declarations) must be evaluated prior to evaluating the command section.

Input and private declarations may appear in any order within their respective sections and they may reference each other so long as there are no circular references. Input and private declarations may *not* reference declarations in the output section.

Declarations in the output section may reference any input and private declarations, and may also reference other output declarations.

### Runtime Section

The `runtime` section defines a set of key/value pairs that represent the minimum requirements needed to run a task and the conditions under which a task should be interpreted as a failure or success. 

During execution of a task, resource requirements within the `runtime` section must be enforced by the engine. If the engine is not able to provision the requested resources, then the task immediately fails. 

There are a set of reserved attributes (described below) that must be supported by the execution engine, and which have well-defined meanings and default values. Default values for all optional standard attributes are directly defined by the WDL specification in order to encourage portability of workflows and tasks; execution engines should NOT provide additional mechanisms to set default values for when no runtime attributes are defined.

🗑 Additional arbitrary attributes may be specified in the `runtime` section, but these may be ignored by the execution engine. These non-standard attributes are called "hints". The use of hint attributes in the `runtime` section is deprecated; a later version of WDL will introduce a new `hints` section for arbitrary attributes and disallow non-standard attributes in the `runtime` section.

The value of a `runtime` attribute can be any expression that evaluates to the expected type - and in some cases matches the accepted format - for that attribute. Expressions in the `runtime` section may reference (non-output) declarations in the task:

<details>
<summary>
Example: runtime_container_task.wdl

```wdl
version 1.1

task runtime_container {
  input {
    String ubuntu_version
  }

  command <<<
    cat /etc/*-release | grep DISTRIB_CODENAME | cut -f 2 -d '='
  >>>
  
  output {
    String is_true = ubuntu_version == read_string(stdout())
  }

  runtime {
    container: "ubuntu:~{ubuntu_version}"
  }
}
```
</summary>
<p>
Example input:

```json
{
  "runtime_container.ubuntu_version": "focal"
}
```

Example output:

```json
{
  "runtime_container.is_true": true
}
```
</p>
</details>

#### Units of Storage

Several of the `runtime` attributes (and some [Standard Library](#standard-library) functions) can accept a string value with an optional unit suffix, using one of the valid [SI or IEC abbreviations](https://en.wikipedia.org/wiki/Binary_prefix). At a minimum, execution engines must support the following suffices in a case-insensitive manner:

* B (bytes)
* Decimal: KB, MB, GB, TB
* Binary: KiB, MiB, GiB, TiB

Optional whitespace is allowed between the number/expression and the suffix. For example: `6.2 GB`, `5MB`, `"~{ram}GiB"`.

The decimal and binary units may be shortened by omitting the trailing "B". For example, "K" and "KB" are both interpreted as "kilobytes".

#### Mandatory `runtime` attributes

The following attributes must be supported by the execution engine. The value for each of these attributes must be defined - if it is not specified by the user, then it must be set to the specified default value. 

##### `container`

* Accepted types:
    * `String`: A single container URI.
    * `Array[String]`: An array of container URIs.
* Alias: `docker`

The `container` key accepts a URI string that describes a location where the execution engine can attempt to retrieve a container image to execute the task.

The user is strongly suggested to specify a `container` for every task. There is no default value for `container`. If `container` is not specified, the execution behavior is determined by the execution engine. Typically, the task is simply executed in the host environment. 

🗑 The ability to omit `container` is deprecated. In WDL 2.0, `container` will be required.

The format of a container URI string is `protocol://location`, where protocol is one of the protocols supported by the execution engine. Execution engines must, at a minimum, support the `docker://` protocol, and if no protocol is specified, it is assumed to be `docker://`. An execution engine should ignore any URI with a protocol it does not support.

Container source locations should use the syntax defined by the individual container repository. For example an image defined as `ubuntu:latest` would conventionally refer a docker image living on `DockerHub`, while an image defined as `quay.io/bitnami/python` would refer to a `quay.io` repository.

The `container` key also accepts an array of URI strings. All of the locations must point to images that are equivalent, i.e. they must always produce the same final results when the task is run with the same inputs. It is the responsibility of the execution engine to define the specific image sources it supports, and to determine which image is the "best" one to use at runtime. The ordering of the array does not imply any implicit preference or ordering of the containers. All images are expected to be the same, and therefore any choice would be equally valid. Defining multiple images enables greater portability across a broad range of execution environments.

<details>
<summary>
Example: test_containers.wdl

```wdl
version 1.1

task single_image_task {
  command <<< printf "hello" >>>

  output {
    String greeting = read_string(stdout())
  }

  runtime {
    container: "ubuntu:latest"
  }
}

task multi_image_task {
  command <<< printf "hello" >>>

  output {
    String greeting = read_string(stdout())
  }

  runtime {
    container: ["ubuntu:latest", "https://gcr.io/standard-images/ubuntu:latest"]
  }
}

workflow test_containers {
  call single_image_task
  call multi_image_task
  output {
    String single_greeting = single_image_task.greeting
    String multi_greeting = multi_image_task.greeting
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
  "test_containers.single_greeting": "hello",
  "test_containers.multi_greeting": "hello"
}
```
</p>
</details>

The execution engine must cause the task to fail immediately if none of the container URIs can be successfully resolved to a runnable image.

🗑 `docker` is supported as an alias for `container` with the exact same semantics. Exactly one of the `container` or `docker` is required. The `docker` alias will be dropped in WDL 2.0.

##### `cpu`

* Accepted types:
    * `Int`
    * `Float`
* Default value: `1`

The `cpu` attribute defines the _minimum_ number of CPU cores required for this task, which must be available prior to instantiating the command. The execution engine must provision at least the requested number of CPU cores, but it may provision more. For example, if the request is `cpu: 0.5` but only discrete values are supported, then the execution engine might choose to provision `1.0` CPU instead.

<details>
<summary>
Example: test_cpu_task.wdl

```wdl
version 1.1

task test_cpu {
  command <<<
  cat /proc/cpuinfo | grep processor | wc -l
  >>>

  output {
    Boolean at_least_two_cpu = read_int(stdout()) >= 2
  }

  runtime {
    container: "ubuntu:latest"
    cpu: 2
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
  "test_cpu.at_least_two_cpu": true
}
```

Test config:

```json
{
  "dependencies": "cpu"
}
```
</p>
</details>

##### `memory`

* Accepted types:
    * `Int`: Bytes of RAM.
    * `String`: A decimal value with, optionally with a unit suffix.
* Default value: `2 GiB`

The `memory` attribute defines the _minimum_ memory (RAM) required for this task, which must be available prior to instantiating the command. The execution engine must provision at least the requested amount of memory, but it may provision more. For example, if the request is `1 GB` but only blocks of `4 GB` are available, then the execution engine might choose to provision `4.0 GB` instead.

<details>
<summary>
Example: test_memory_task.wdl

```wdl
version 1.1

task test_memory {
  command <<<
  free --bytes -t | tail -1 | sed -E 's/\s+/\t/g' | cut -f 2
  >>>

  output {
    Boolean at_least_two_gb = read_int(stdout()) >= (2 * 1024 * 1024 * 1024)
  }

  runtime {
    memory: "2 GiB"
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
  "test_memory.at_least_two_gb": true
}
```

Test config:

```json
{
  "dependencies": "memory"
}
```
</p>
</details>

##### `gpu`

* Accepted type: `Boolean`
* Default value: `false`

The `gpu` attribute provides a way to accommodate modern workflows that are increasingly becoming reliant on GPU computations. This attribute simply indicates to the execution engine that a task requires a GPU to run to completion. A task with this flag set to `true` is guaranteed to only run if a GPU is a available within the runtime environment. It is the responsibility of the execution engine to check prior to execution whether a GPU is provisionable, and if not, preemptively fail the task.

This attribute *cannot* request any specific quantity or types of GPUs to make available to the task. Any such information should be provided using an execution engine-specific attribute.

<details>
<summary>
Example: test_gpu_task.wdl

```wdl
version 1.1

task test_gpu {
  command <<<
  lspci -nn | grep ' \[03..\]: ' | wc -l
  >>>

  output {
    Boolean at_least_one_gpu = read_int(stdout()) >= 1
  }
  
  runtime {
    gpu: true
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
  "test_gpu.at_least_one_gpu": true
}
```

Test config:

```json
{
  "dependencies": "gpu"
}
```
</p>
</details>

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

This property does not specify exactly what type of persistent volume is being requested (e.g. SSD, HDD), but leaves this up to the engine to decide, based on what hardware is available or on another execution engine-specific attribute.

If a disk specification string is used to specify a mount point, then the mount point must be an absolute path to a location on the host machine. If the mount point is omitted, it is assumed to be a persistent volume mounted at the root of the execution directory within a task.

details>
<summary>
Example: one_mount_point_task.wdl

```wdl
version 1.1

task one_mount_point {
  command <<<
    findmnt -bno size /mnt/outputs
  >>>
  
  output {
    Boolean at_least_ten_gb = read_int(stdout()) >= (10 * 1024 * 1024 * 1024)
  }

  runtime {
    disks: "/mnt/outputs 10 GiB"
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
  "one_mount_point.at_least_ten_gb": true
}
```

Test config:

```json
{
  "dependencies": "disks"
}
```
</p>
</details>

If an array of disk specifications is used to specify multiple disk mounts, only one of them is allowed to omit the mount point.

<details>
<summary>
Example: multi_mount_points_task.wdl

```wdl
version 1.1

task multi_mount_points {
  command <<<
    findmnt -bno size /
  >>>
  
  output {
    Boolean at_least_two_gb = read_int(stdout()) >= (2 * 1024 * 1024 * 1024)
  }

  runtime {
  	# The first value will be mounted at the execution root
    disks: ["2", "/mnt/outputs 4 GiB", "/mnt/tmp 1 GiB"]
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
  "multi_mount_points.at_least_two_gb": true
}
```

Test config:

```json
{
  "dependencies": "disks"
}
```
</p>
</details>

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

The `returnCodes` attribute provides a mechanism to specify the return code, or set of return codes, that indicates a successful execution of a task. The engine must honor the return codes specified within the `runtime` section and set the tasks status appropriately. 

<details>
<summary>
Example: single_return_code_task.wdl

```wdl
version 1.1

task single_return_code {
  command <<<
  exit 1
  >>>

  runtime {
    return_codes: 1
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

Test config:

```json
{
  "return_code": 1
}
```
</p>
</details>

<details>
<summary>
Example: multi_return_code_fail_task.wdl

```wdl
version 1.1

task multi_return_code {
  command <<<
  exit 42
  >>>

  runtime {
    return_codes: [1, 2, 5, 10]
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

Test config:

```json
{
  "fail": true,
  "return_code": 42
}
```
</p>
</details>

<details>
<summary>
Example: all_return_codes_task.wdl

```wdl
version 1.1

task multi_return_code_task {
  command <<<
  exit 42
  >>>

  runtime {
    return_codes: "*"
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

Test config:

```json
{
  "return_code": 42
}
```
</p>
</details>

#### Reserved `runtime` hints

The following attributes are considered "hints" rather than requirements. They are optional for execution engines to support. The purpose of reserving these attributes is to encourage interoperability of tasks and workflows between different execution engines.

Note: in a future version of WDL, these attributes will move to a new `hints` section.

<details>
<summary>
Example: test_hints_task.wdl

```wdl
version 1.1

task test_hints {
  input {
    File foo
  }

  command <<<
  wc -l ~{foo}
  >>>

  output {
    Int num_lines = read_int(stdout())
  }

  runtime {
    container: "ubuntu:latest"
    maxMemory: "36 GB"
    maxCpu: 24
    shortTask: true
    localizationOptional: false
    inputs: object {
      foo: object { 
        localizationOptional: true
      }
    }
  }
}
```
</summary>
<p>
Example input:

```json
{
  "test_hints.foo": "greetings.txt"
}
```

Example output:

```json
{
  "test_hints.num_lines": 3
}
```
</p>
</details>

##### `maxCpu`

Specifies the maximum CPU to be provisioned for a task. The value of this hint has the same specification as [`requirements.cpu`](#cpu).

##### `maxMemory`

Specifies the maximum memory provisioned for a task. The value of this hint has the same specification as [`requirements.memory`](#memory).

##### `shortTask`

* Allowed type: `Boolean`

A `Boolean` value for which `true` indicates that that this task is not expected to take long to execute. The execution engine can interpret this as permission to attempt to optimize the execution of the task - e.g., by batching together multiple `shortTask`s, or by using the cost-optimized instance types that many cloud vendors provide, e.g., `preemptible` instances on `GCP` and `spot` instances on `AWS`. "Short" is a bit ambiguous, but should generally be interpreted as << 24h.

##### `localizationOptional`

* Allowed type: `Boolean`

A `Boolean` value, for which `true` indicates that, if possible, any `File` inputs for this task should not be (immediately) localized. For example, a task that processes its input file once in linear fashion could have that input streamed (e.g., using a `fifo`) rather than requiring the input file to be fully localized prior to execution. This directive must not have any impact on the success or failure of a task (i.e., a task must run the same with or without localization).

##### `inputs`

* Allowed type: `object`

Provides input-specific hints in the form of an object. Each key within this hint should refer to an actual input defined for the current task. A key may also refer to a specific member of a struct/object input.

<details>
<summary>
Example: input_hint_task.wdl

```wdl
version 1.1

struct Person {
  String name
  File? cv
}

task input_hint {
  input {
    Person person
  }

  command <<<
  if ~{defined(person.cv)}; then
    grep "WDL" ~{person.cv}
  fi
  >>>
  
  output {
    Array[String] experience = read_lines(stdout())
  }

  runtime {
    inputs: object {
      person: object {
        cv: object {
          localizationOptional: true
        }
      }
    }
  }
}
```
</summary>
<p>
Example input:

```json
{
  "input_hint.person": {
    "name": "Joe"
  }
}
```

Example output:

```json
{}
```
</p>
</details>

Reserved input-specific attributes:

* `inputs.<key>.localizationOptional`: Tells the execution engine that a specific `File` input does not need to be localized for this task.

##### `outputs`

* Allowed type: `object`

Provides outputs specific hints in the form of a hints object. Each key within this hint should refer to an actual output defined for the current task. A key may also refer to a specific member of a struct/object input.

#### Conventions and Best Practices

In order to encourage interoperable workflows, WDL authors and execution engine implementors should view hints strictly as an optimization that can be made for a specific task at runtime; hints should not be interpreted as requirements for that task. By following this principle, we can guarantee that a workflow is runnable on all platforms assuming the `runtime` section has the required parameters, regardless of whether it contains any additional hints.

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

There are two optional sections that can be used to store metadata with the task: `meta` and `parameter_meta`. These sections are designed to contain metadata that is only of interest to human readers. The engine can ignore these sections with no loss of correctness. The extra information can be used, for example, to generate a user interface. Any attributes that may influence execution behavior should go in the `runtime` section.

Both of these sections can contain key/value pairs. Metadata values are different than in `runtime` and other sections:

* Only string, numeric, and boolean primitives are allowed.
* Only array and "meta object" compound values are allowed.
* The special value `null` is allowed for undefined attributes.
* Expressions are not allowed.

A meta object is similar to a struct literal, except:

* A type name is not required.
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

This section contains task-level metadata. For example: author and contact email.

#### Parameter Metadata Section

This section contains metadata specific to input and output parameters. Any key in this section *must* correspond to a task input or output.

<details>
<summary>
Example: ex_paramter_meta_task.wdl

```wdl
version 1.1

task ex_paramter_meta {
  input {
    File infile
    Boolean lines_only = false
    String? region
  }

  meta {
    description: "A task that counts the number of words/lines in a file"
  }

  parameter_meta {
    infile: {
      help: "Count the number of words/lines in this file"
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
    wc ~{if lines_only then '-l' else ''} ~{infile}
  >>>

  output {
     String result = stdout()
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
  "ex_paramter_meta.infile": "greetings.txt",
  "ex_paramter_meta.lines_only": true
}
```

Example output:

```json
{
  "ex_paramter_meta.result": "3"
}
```
</p>
</details>

### Advanced Task Examples

#### Example 1: HISAT2

<details>
<summary>
Example: hisat2_task.wdl

```wdl
version 1.1

task hisat2 {
  input {
    File index
    String sra_acc
    Int? max_reads
    Int threads = 8
    Float memory_gb = 16
    Float disk_size_gb = 100
  }

  String index_id = basename(index, ".tar.gz")

  command <<<
    mkdir index
    tar -C index -xzf ~{index}
    hisat2 \
      -p ~{threads} \
      ~{if defined(max_reads) then "-u ~{select_first([max_reads])}" else ""} \
      -x index/~{index_id} \
      --sra-acc ~{sra_acc} > ~{sra_acc}.sam
  >>>
  
  output {
    File sam = "output.sam"
  }
  
  runtime {
    container: "quay.io/biocontainers/hisat2:2.2.1--h1b792b2_3"
    cpu: threads
    memory: "~{memory_gb} GB"
    disks: "~{disk_size_gb} GB"
  }

  meta {
    description: "Align single-end reads with BWA MEM"
  }

  parameter_meta {
    index: "Gzipped tar file with HISAT2 index files"
    sra_acc: "SRA accession number or reads to align"
  }
}
```
</summary>
<p>
Example input:

```json
{
  "hisat2.index_tar_gz": "https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz",
  "hisat2.sra_acc": "SRR3440404",
  "hisat2.max_reads": 10
}
```

Example output:

```json
{
  "hisat2.sam": "SRR3440404.sam"
}
```

Test config:

```json
{
  "dependencies": ["cpu", "memory", "disks"]
}
```
</p>
</details>

#### Example 2: GATK Haplotype Caller

<details>
<summary>
Example: gatk_haplotype_caller_task.wdl

```wdl
version 1.1

struct Reference {
  String id
  File fasta
  File index
  File dict
}

task gatk_haplotype_caller {
  input {
    File bam
    Reference reference
    String? interval
    Int memory_gb = 4
    Float? disks_gb
    String? sample_id
  }
  
  String prefix = select_first([sample_id, basename(bam, ".bam")])
  Float disk_size_gb = select_first([
    disks_gb, 10 + size([bam, reference.fasta], "GB")
  ])

  command <<<
    # ensure all reference files are in the same directory
    mkdir ref
    ln -s ~{reference.fasta} ref/~{reference.id}.fasta
    ln -s ~{reference.index} ref/~{reference.id}.fasta.fai
    ln -s ~{reference.dict} ref/~{reference.id}.dict
    gatk --java-options "-Xmx~{memory_gb}g" HaplotypeCaller \
      ~{if defined(interval) then "-L ~{select_first([interval])}" else ""} \
      -R ref/~{reference.id}.fasta \
      -I ~{bam} \
      -O ~{prefix}.vcf
  >>>

  output {
    File vcf = "~{prefix}.vcf"
  }

  parameter_meta {
    bam: "BAM file to call"
    reference_fasta: "Reference genome in FASTA format"
    memory_gb: "Amount of memory to allocate to the JVM in GB"
    disks_gb: "Amount of disk space to reserve"
    sample_id: "The ID of the sample to call"
  }

  meta {
    author: "Joe Somebody"
    email: "joe@company.org"
  }
  
  runtime {
    container: "broadinstitute/gatk"
    memory: "~{memory_gb + 1} GB"
    disks: "~{disk_size_gb} GB"
  }
}
```
</summary>
<p>
Example input:

```json
{
  "gatk_haplotype_caller.bam": "ftp://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/RMNISTHS_30xdownsample.bam",
  "gatk_haplotype_caller.reference": {
    "id":"Homo_sapiens_assembly38",
    "fasta": "https://storage.googleapis.com/genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.fasta",
    "index": "https://storage.googleapis.com/genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.fasta.fai",
    "dict": "https://storage.googleapis.com/genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.dict"
  },
  "gatk_haplotype_caller.interval": "chr1:1000000-1010000"
}
```

Example output:

```json
{
  "gatk_haplotype_caller.vcf": "HG002.vcf"
}
```

Test config:

```json
{
  "dependencies": ["memory", "disks"]
}
```
</p>
</details>

## Workflow Definition

A workflow can be thought of as a directed acyclic graph (DAG) of transformations that convert the input data to the desired outputs. Rather than explicitly specifying the sequence of operations, a WDL workflow instead describes the connections between the steps in the workflow (i.e., between the nodes in the graph). It is the responsibility of the execution engine to determine the proper ordering of the workflow steps, and to orchestrate the execution of the different steps.

A workflow is defined using the `workflow` keyword, followed by a workflow name that is unique within its WDL document, followed by any number of workflow elements within braces.

```wdl
workflow name {
  input {
    # workflow inputs are declared here
  }

  # other "private" declarations can be made here
 
  # there may be any number of (potentially nested) 
  # calls, scatters, or conditionals
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

### Workflow Elements

Tasks and workflows have several elements in common. When applicable, the task definition for these sections is linked to rather than duplicated.

A workflow is comprised of the following elements:

* A single, optional [`input`](#task-inputs) section (_identical to the `input` section within tasks_).
* Any number of workflow execution elements, which include the following:
* A [private declaration](#private-declarations) (_identical to private declarations within tasks_).
  * A [`call`](#call-statement) statement, which invokes tasks or subworkflows.
  * A [`scatter`](#scatter-statement) statement, which enables parallelized of workflow execution elements across collections.
  * A [conditional (`if`)](#conditional-statement) statement, which enables conditional execution of workflow execution elements.
* A single, optional [`output`](#task-outputs) section (_identical to the `output` section within tasks_).
* A single, optional [`meta`](#metadata-sections) section (_identical to the `meta` section within tasks_).
* A single, optional [`parameter_meta`](#parameter-metadata-section) section (_identical to the `parameter_meta` section within tasks_).

There is no enforced order for workflow elements.

### Workflow Inputs

The workflow and [task `input` sections](#task-inputs) have identical semantics.

### Workflow Outputs

The workflow and [task `output` sections](#task-outputs) have identical semantics.

By default, if the `output {...}` section is omitted from a top-level workflow, then the workflow has no outputs. However, the execution engine may choose allow the user to specify that when the top-level output section is omitted, all outputs from all calls (including nested calls) should be returned.

If the `output {...}` section is omitted from a workflow that is called as a subworkflow, then that call must not have outputs. Formally defined outputs of subworkflows are required for the following reasons:

- To present the same interface when calling subworkflows as when calling tasks.
- To make it easy for callers of subworkflows to find out exactly what outputs the call is creating.
- In the case of nested subworkflows, to give the outputs at the top level a simple fixed name rather than a long qualified name like `a.b.c.d.out` (which is liable to change if the underlying implementation of `c` changes, for example).

### Evaluation of Workflow Elements

As with tasks, declarations can appear in the body of a workflow in any order. Expressions in workflows can reference the outputs of calls, including in input declarations. For example:

<details>
<summary>
Example: input_ref_call.wdl

```wdl
version 1.1

task double {
  input {
    Int int_in
  }

  command <<< >>>

  output {
    Int out = int_in * 2
  }
}

workflow input_ref_call {
  input {
    Int x
    Int y = d1.out
  }

  call double as d1 { input: int_in = x }
  call double as d2 { input: int_in = y }

  output {
    Int result = d2.out
  }
}
```
</summary>
<p>
Example input:

```json
{
  "input_ref_call.x": 5
}
```

Example output:

```json
{
  "input_ref_call.result": 20
}
```
</p>
</details>

The control flow of this workflow changes depending on whether the value of `y` is provided as an input or it's initializer expression is evaluated:

* If an input value is provided for `y` then it receives that value immediately and `d2` may start running as soon as the workflow starts.
* In no input value is provided for `y` then it will need to wait for `d1` to complete before it is assigned.

### Fully Qualified Names & Namespaced Identifiers

A fully qualified name is the unique identifier of any particular call, input, or output, and has the following structure:

* For `call`s: `<parent namespace>.<call alias>`
* For inputs and outputs: `<parent namespace>.<input or output name>`
* For `Struct`s and `Object`s: `<parent namespace>.<member name>`

A [namespace](#namespaces) is a set of names, such that every name is unique within the namespace (but the same name could be used in two different namespaces). The `parent namespace` is the fully qualified name of the workflow containing the call, the workflow or task containing the input or output declaration, or the `Struct` or `Object` declaration containing the member. For the top-level workflow this is equal to the workflow name.

For example: `ns.ns2.mytask` is a fully-qualified name - `ns.ns2` is the parent namespace, and `mytask` is the task name being referred to within that namespace. Fully-qualified names are left-associative, meaning `ns.ns2.mytask` is interpreted as `((ns.ns2).mytask)`, meaning `ns.ns2` has to resolve to a namespace so that `.mytask` can be applied.

When a [call statement](#call-statement) needs to refer to a task or workflow in another namespace, then it must use the fully-qualified name of that task or workflow. When an [expression](#expressions) needs to refer to a declaration in another namespace, it must use a *namespaced identifier*, which is an identifier consisting of a fully-qualified name.

<details>
<summary>
Example: call_imported_task.wdl

```wdl
version 1.1

import "input_ref_call.wdl" as ns1

workflow call_imported_task {
  input {
    Int x
    Int y = d1.out
  }

  call ns1.double as d1 { input: int_in = x }
  call ns1.double as d2 { input: int_in = y }

  output {
    Int result = d2.out
  }
}
```
</summary>
<p>
Example input:

```json
{
  "call_imported_task.x": 5
}
```

Example output:

```json
{
  "call_imported_task.result": 20
}
```
</p>
</details>

The workflow in the above example imports the WDL file from the previous section using an alias. The import creates the namespace `ns1`, and the workflow calls a task in the imported namespace using its fully qualified name, `ns1.double`. Each call is aliased, and the alias is used to refer to the output of the task, e.g., `d1.out` (see the [Call Statement](#call-statement) section for details on call aliasing).

In the following more extensive example, all of the fully-qualified names that exist within the top-level workflow are listed exhaustively.

<details>
<summary>
Example: main.wdl

```wdl
version 1.1

import "other.wdl" as other_wf

task echo {
  input {
    String msg = "hello"
  }
  
  command <<<
  printf ~{msg}
  >>>
  
  output {
    File results = stdout()
  }
  
  runtime {
    container: "ubuntu:latest"
  }
}

workflow main {
  Array[String] arr = ["a", "b", "c"]

  call echo
  call echo as echo2
  call other_wf.foobar { input: infile = echo2.results }
  call other_wf.other { input: b = true, f = echo2.results }
  call other_wf.other as other2 { input: b = false }
  
  scatter(x in arr) {
    call echo as scattered_echo {
      input: msg = x
    }
    String scattered_echo_results = read_string(scattered_echo.results)
  }

  output {
    String echo_results = read_string(echo.results)
    Int foobar_results = foobar.results
    Array[String] echo_array = scattered_echo_results
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
  "main.echo_results": "hello",
  "main.foobar_results": 1,
  "main.echo_array": ["a", "b", "c"]
}
```
</p>
</details>

<details>
<summary>
Example: other.wdl

```wdl
version 1.1

task foobar {
  input {
    File infile
  }

  command <<<
  wc -l ~{infile}
  >>>

  output {
    Int results = read_int(stdout())
  }

  runtime {
    container: "ubuntu:latest"
  }
}

workflow other {
  input {
    Boolean b = false
    File? f
  }

  if (b && defined(f)) {
    call foobar { input: infile = select_first([f]) }
  }

  output {
    Int? results = foobar.results
  }
}
```
</summary>
<p>
Example input:

```json
{
  "other.b": true,
  "other.f": "greetings.txt"
}
```

Example output:

```json
{
  "other.results": 3
}
```
</p>
</details>

The following fully-qualified names exist when calling `workflow main` in `main.wdl`:

| Fully-qualified Name          | References                                                                                  | Accessible                                                      |
| ----------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `other_wf`                    | Namespace created by importing `other.wdl` and aliasing it                                  | Anywhere in `main.wdl`                                          |
| `main`                        | Top-level workflow                                                                          | By the caller of `main`                                         |
| `main.arr`                    | `Array[String]` declaration on the workflow                                                 | Anywhere within `main`                                          |
| `main.echo`                   | First call to task `echo`                                                                   | Anywhere within `main`                                          |
| `main.echo2`                  | Second call to task `echo` (aliased as `echo2`)                                             | Anywhere within `main`                                          |
| `main.echo.msg`               | `String` input of first call to task `echo`                                                 | No*                                                             |
| `main.echo.results`           | `File` output of first call to task `echo`                                                  | Anywhere within `main`                                          |
| `main.echo2.msg`              | `String` input of second call to task `echo`                                                | No*                                                             |
| `main.echo2.results`          | `File` output of second call to task `echo`                                                 | Anywhere within `main`                                          |
| `main.foobar.infile`          | `File` input of the call to `other_wf.foobar`                                               | No*                                                             |
| `main.foobar.results`         | `Int` output of the call to `other_wf.foobar`                                               | Anywhere within `main`                                          |
| `main.other`                  | First call to subworkflow `other_wf.other`                                                  | Anywhere within `main`                                          |
| `main.other.b`                | `Boolean` input of the first call to subworkflow `other_wf.other`                           | No*                                                             |
| `main.other.f`                | `File` input of the first call to subworkflow `other_wf.other`                              | No*                                                             |
| `main.other.foobar.infile`    | `File` input of the call to `foobar` inside the first call to subworkflow `other_wf.other`  | No*                                                             |
| `main.other.foobar.results`   | `Int` output of the call to `foobar` inside the first call to subworkflow `other_wf.other`  | No                                                              |
| `main.other.results`          | `Int?` output of the first call to subworkflow `other_wf.other`                             | Anywhere within `main`                                          |
| `main.other2`                 | Second call to subworkflow `other_wf.other` (aliased as other2)                             | Anywhere within `main`                                          |
| `main.other2.b`               | `Boolean` input of the second call to subworkflow `other_wf.other`                          | No*                                                             |
| `main.other2.f`               | `File input of the second call to subworkflow `other_wf.other`                              | No*                                                             |
| `main.other2.foobar.infile`   | `File` input of the call to `foobar` inside the second call to subworkflow `other_wf.other` | No*                                                             |
| `main.other2.foobar.results`  | `Int` output of the call to `foobar` inside the second call to subworkflow `other_wf.other` | No                                                              |
| `scattered_echo`              | Call to `echo` within scatter of `main`                                                     | Within the scatter                                              |
| `scattered_echo.results`      | `File` results of call to scattered_echo`                                                   | Within the scatter                                              |
| `main.scattered_echo.msg`     | Array of `String` inputs to calls to `scattered_echo`                                       | No*                                                             |
| `main.scattered_echo.results` | Array of `File` results of calls to `echo` within the scatter                               | Anywhere within `main`                                          |
| `scattered_echo_results`      | `String` contents of `File` created by call to `scattered_echo`                             | Within the scatter                                              |
| `main.scattered_echo_results` | Array of `String` contents of `File` results of calls to `echo` within the scatter          | Anywhere within `main`                                          |
| `main.echo_results`           | `String` contents of `File` result from call to `echo`                                      | Anywhere in `main`'s output section and by the caller of `main` |
| `main.foobar_results`         | `Int` result from call to `foobar`                                                          | Anywhere in `main`'s output section and by the caller of `main` |
| `main.echo_array`             | Array of `String` contents of `File` results from calls to `echo` in the scatter            | Anywhere in `main`'s output section and by the caller of `main` |

\* Task inputs are accessible to be set by the caller of `main` if the workflow is called with [`allowNestedInputs: true`](#computing-call-inputs) in its `meta` section.

### Call Statement

A workflow calls other tasks/workflows via the `call` keyword. A `call` is followed by the name of the task or subworkflow to run. If a task is defined in the same WDL document as the calling workflow, it may be called using just the task name. A task or workflow in an imported WDL must be called using its [fully-qualified name](#fully-qualified-names--namespaced-identifiers).

Each `call` must be uniquely identifiable. By default, the `call`'s unique identifier is the task or subworkflow name (e.g., `call foo` would be referenced by name `foo`). However, to `call foo` multiple times in the same workflow, it is necessary to give all except one of the `call` statements a unique alias using the `as` clause, e.g., `call foo as bar`.

A `call` has an optional body in braces (`{}`). The only element that may appear in the call body is the `input:` keyword, followed by an optional, comma-delimited list of inputs to the call. A `call` must, at a minimum, provide values for all of the task/subworkflow's required inputs, and each input value/expression must match the type of the task/subworkflow's corresponding input parameter. An input value may be any valid expression, not just a reference to another call output. If a task has no required parameters, then the `call` body may be empty or omitted.

If a call input has the same name as a declaration from the current scope, the name of the input may appear alone (without an expression) to implicitly bind the value of that declaration. For example, if a workflow and task both have inputs `x` and `z` of the same types, then `call mytask {input: x, y=b, z}` is equivalent to `call mytask {input: x=x, y=b, z=z}`.

<details>
<summary>
Example: call_example.wdl

```wdl
version 1.1

import "other.wdl" as lib

task repeat {
  input {
    Int i
    String? opt_string
  }
  
  command <<<
  for i in 1..~{i}; do
    printf ~{select_first([opt_string, "default"])}
  done
  >>>

  output {
    Array[String] lines = read_lines(stdout())
  }
}

workflow call_example {
  input {
    String s
    Int i
  }

  # Calls repeat with one required input - it is okay to not
  # specify a value for repeat.opt_string since it is optional.
  call repeat { input: i = 3 }

  # Calls repeat a second time, this time with both inputs.
  # We need to give this one an alias to avoid name-collision.
  call repeat as repeat2 {
    input:
      i = i * 2,
      opt_string = s
  }

  # Calls repeat with one required input using the abbreviated 
  # syntax for `i`.
  call repeat as repeat3 { input: i, opt_string = s }

  # Calls a workflow imported from lib with no inputs.
  call lib.other
  # This call is also valid
  call lib.other as other_workflow2 {}

  output {
    Array[String] lines1 = repeat.lines
    Array[String] lines2 = repeat2.lines
    Array[String] lines3 = repeat3.lines
    Int? results1 = other.results
    Int? results2 = other_workflow2.results  
  }
}
```
</summary>
<p>
Example input:

```json
{
  "call_example.s": "hello",
  "call_example.i": 2
}
```

Example output:

```json
{
  "call_example.lines1": ["default", "default", "default"],
  "call_example.lines2": ["hello", "hello", "hello", "hello"],
  "call_example.lines3": ["hello", "hello"],
  "call_example.results1": null,
  "call_example.results2": null
}
```
</p>
</details>

The execution engine may execute a `call` as soon as all its inputs are available. If `call x`'s inputs are based on `call y`'s outputs (i.e., `x` depends on `y`), `x` can be run as soon as - but not before - `y` has completed. 

An `after` clause can be used to create an explicit dependency between `x` and `y` (i.e., one that isn't based on the availability of `y`'s outputs). For example, `call x after y after z`. An explicit dependency is only required if `x` must not execute until after `y` and `x` doesn't already depend on output from `y`.

<details>
<summary>
Example: test_after.wdl

```wdl
version 1.1

import "call_example.wdl" as lib

workflow test_after {
  # Call repeat
  call lib.repeat { input: i = 2, opt_string = "hello" }

  # Call `repeat` again with the output from the first call.
  # This call will wait until `repeat` is finished.
  call lib.repeat as repeat2 {
    input:
      i = 1,
      opt_string = sep(" ", repeat.lines)
  }

  # Call `repeat` again. This call does not depend on the output 
  # from an earlier call, but we specify explicitly that this 
  # task must wait until `repeat` is complete before executing.
  call lib.repeat as repeat3 after repeat { input: i = 3 }

  output {
    Array[String] lines1 = repeat.lines
    Array[String] lines2 = repeat2.lines
    Array[String] lines3 = repeat3.lines
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
  "test_after.lines1": ["hello", "hello"],
  "test_after.lines2": ["hello hello"],
  "test_after.lines3": ["default", "default", "default"]
}
```
</p>
</details>

A `call`'s outputs are available to be used as inputs to other calls in the workflow or as workflow outputs immediately after the execution of the call has completed. The only task declarations that are accessible outside of the task are its output declarations; call inputs and private declarations cannot be referenced by the calling workflow. To expose a call input, add an output to the task that simply copies the input. Note that the output must use a different name since every declaration in a task or workflow must have a unique name.

<details>
<summary>
Example: copy_input.wdl

```wdl
version 1.1

task greet {
  input {
    String greeting
  }

  command <<< printf "~{greeting}, nice to meet you!" >>>

  output {
    # expose the input to s as an output
    String greeting_out = greeting
    String msg = read_string(stdout())
  }
}

workflow copy_input {
  input {
    String name
  }

  call greet { input: greeting = "Hello ~{name}" }
  
  output {
    String greeting = greet.greeting_out
    String msg = greet.msg
  }
}
```
</summary>
<p>
Example input:

```json
{
  "copy_input.name": "Billy"
}
```

Example output:

```json
{
  "copy_input.greeting": "Hello Billy",
  "copy_input.msg": "Hello Billy, nice to meet you!"
}
```
</p>
</details>

#### Computing Call Inputs

Any required workflow inputs (i.e., those that are not initialized with a default expression) must have their values provided when invoking the workflow. Inputs may be specified for a workflow invocation using any mechanism supported by the execution engine, including the [standard JSON format](#json-input-format). 

By default, all calls to subworkflows and tasks must have values provided for all required inputs by the caller. However, the execution engine may allow the workflow to leave some subworkflow/task inputs undefined - to be specified by the user at runtime - by setting the `allowNestedInputs` flag to `true` in the `meta` section of the top-level workflow.

<details>
<summary>
Example: allow_nested.wdl

```wdl
version 1.1

import "call_example.wdl" as lib

task inc {
  input {
    Int y
    File ref_file # Do nothing with this
  }

  command <<<
  printf ~{y + 1}
  >>>

  output {
    Int incr = read_int(stdout())
  }
  
  runtime {
    container: "ubuntu:latest"
  }
}

workflow allow_nested {
  input {
    Int int_val
    String msg1
    String msg2
    Array[Int] my_ints
    File ref_file
  }

  meta {
    allowNestedInputs: true
  }

  call lib.repeat {
    input:
      i = int_val,
      opt_string = msg1
  }

  call lib.repeat as repeat2 {
    input:
      opt_string = msg2
  }

  scatter (i in my_ints) {
    call inc {
      input: y=i, ref_file=ref_file
    }
  }

  output {
    Array[String] lines1 = repeat.lines
    Array[String] lines2 = repeat2.lines
    Array[Int] incrs = inc.incr
  }
}
```
</summary>
<p>
Example input:

```json
{
  "allow_nested.int_val": 3,
  "allow_nested.msg1": "hello",
  "allow_nested.msg2": "goodbye",
  "allow_nested.my_ints": [1, 2, 3],
  "allow_nested.ref_file": "hello.txt"
}
```

Example output:

```json
{
  "allow_nested.lines1": ["hello", "hello", "hello"],
  "allow_nested.lines2": ["goodbye", "goodbye"],
  "allow_nested.repeat2.i": 2,
  "allow_nested.incrs": [2, 3, 4]
}
```
</p>
</details>

In the preceding example, the required input `i` to call `repeat2` is missing. Normally this would result in an error. However, if the execution engine supports `allowNestedInputs`, then the fact that `allowNestedInputs: true` appears in the workflow's `meta` section means that `repeat2.i` may be set by the caller of the workflow, e.g., by including `"allow_nested.repeat2.i": 2,` in the input JSON.

It is not allowed to *override* a call input at runtime, even if nested inputs are allowed. For example, if the user tried to specify `"allow_nested.repeat.opt_string": "hola"` in the input JSON, an error would be raised because the workflow already specifies a value for that input.

The `allowNestedInputs` directive only applies to user-supplied inputs. There is no mechanism for the workflow itself to set a value for a nested input when calling a subworkflow. For example, the following workflow is invalid:

<details>
<summary>
Example: call_subworkflow_fail.wdl

```wdl
version 1.1

import "copy_input.wdl" as copy

workflow call_subworkflow {
  meta {
    allowNestedInputs: true
  }

  # error! A workflow can't specify a nested input for a subworkflow's call.
  call copy.copy_input { input: greet.greeting = "hola" }
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

### Scatter Statement

Scatter/gather is a common parallelization pattern in computer science. Given a collection of inputs (such as an array), the "scatter" step executes a set of operations on each input in parallel. In the "gather" step, the outputs of all the individual scatter-tasks are collected into the final output.

WDL provides a mechanism for scatter/gather using the `scatter` statement. A `scatter` statement begins with the `scatter` keyword and has three essential pieces:

* An expression that evaluates to an `Array[X]` - the array to be scattered over.
* The scatter variable - an identifier that will hold the input value in each iteration of the scatter. The scatter variable is always of type `X`, where `X` is the item type of the `Array`. The scatter variable may only be referenced in the body of the scatter.
* A body that contains any number of nested statements - declarations, calls, scatters, conditionals - that are executed for each value in the collection.

After evaluation has completed for all iterations of a `scatter`, each declaration or call output in the scatter body (except for the scatter variable) is collected into an array, and those array declarations are exposed in the enclosing context. In other words, for a declaration or call output `T <name>` within a scatter body, a declaration `Array[T] <name>` is implicitly available outside of the scatter body. The ordering of an exported array is guaranteed to match the ordering of the input array. In the example below, `String greeting` is accessible anywhere in the `scatter` body, and `Array[String] greeting` is a collection of all the values of `greeting` - in the same order as `name_array` - that is accessible outside of the `scatter` anywhere in `workflow test_scatter`.

<details>
<summary>
Example: test_scatter.wdl

```wdl
version 1.1

task say_hello {
  input {
    String greeting
  }

  command <<<
  printf "~{greeting}, how are you?"
  >>>

  output {
    String msg = read_string(stdout())
  }
}

workflow test_scatter {
  input {
    Array[String] name_array = ["Joe", "Bob", "Fred"]
    String salutation = "Hello"
  }
  
  # `name_array` is an identifier expression that evaluates to an Array 
  # of Strings.
  # `name` is a `String` declaration that is assigned a different value
  # - one of the elements of `name_array` - during each iteration.
  scatter (name in name_array) {
    # these statements are evaluated for each different value of `name`,s
    String greeting = "~{salutation} ~{name}"
    call say_hello { input: greeting = greeting }
  }

  output {
    Array[String] messages = say_hello.msg
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
  "test_scatter.messages": [
    "Hello Joe, how are you?",
    "Hello Bob, how are you?",
    "Hello Fred, how are you?"
  ]
}
```
</p>
</details>

In this example, the scatter body is evaluated three times - once for each value in `name_array`. On a multi-core computer, these evaluations might happen in parallel, with each evaluation running in a separate thread or subprocess; on a cloud platform, each of these evaluations might take place in a different virtual machine.

The scatter body is a nested scope in which the scatter variable is accessible, along with all of the declarations and call outputs that are accessible in the enclosing scope. The scatter variable is *not* accessible outside the scatter body. In the preceding example, it would be an error to reference `name` in the workflow's output section. However, if the `scatter` contained a nested `scatter`, `name` would be accessible in that nested `scatter`'s body. Similarly, calls within the scatter body are able to depend on each other and reference each others' outputs.
 
If scatters are nested to multiple levels, the output types are also nested to the same number of levels.

<details>
<summary>
Example: nested_scatter.wdl

```wdl
version 1.1

import "test_scatter.wdl" as scat

task make_name {
  input {
    String first
    String last
  }

  command <<<
  printf "~{first} ~{last}"
  >>>

  output {
    String name = read_string(stdout())
  }
}

workflow nested_scatter {
  input {
    Array[String] first_names = ["Bilbo", "Gandalf", "Merry"]
    Array[String] last_names = ["Baggins", "the Grey", "Brandybuck"]
    Array[String] salutations = ["Hello", "Goodbye"]
  }

  Array[String] honorifics = ["Wizard", "Mr."]

  # the zip() function creates an array of pairs
  Array[Pair[String, String]] name_pairs = zip(first_names, last_names)
  # the range() function creates an array of increasing integers
  Array[Int] counter = range(length(name_pairs))

  scatter (name_and_index in zip(name_pairs, counter) ) {
    Pair[String, String] names = name_and_index.left

    # Use a different honorific for even and odd items in the array
    # `honorifics` is accessible here
    String honorific = honorifics[name_and_index.right % 2]
    
    call make_name {
      input:
        first = names.left,
        last = names.right
    }

    scatter (salutation in salutations) {
      # `names`, and `salutation` are all accessible here
      String short_greeting = "~{salutation} ~{honorific} ~{names.left}"
      call scat.say_hello { input: greeting = short_greeting }

      # the output of `make_name` is also accessible
      String long_greeting = "~{salutation} ~{honorific} ~{make_name.name}"
      call scat.say_hello as say_hello_long { input: greeting = long_greeting }

      # within the scatter body, when we access the output of the
      # say_hello call, we get a String
      Array[String] messages = [say_hello.msg, say_hello_long.msg]
    }

    # this would be an error - `salutation` is not accessible here
    # String scatter_saluation = salutation
  }

  # Outside of the scatter body, we can access all of the names that
  # are inside the scatter body, but the types are now all Arrays.
  # Each of these outputs will be an array of length 3 (the same
  # length as `name_and_index`).
  output {
    # Here we are one level of nesting away from `honorific`, so
    # the implicitly created array is one level deep
    Array[String] used_honorifics = honorific

    # Here we are two levels of nesting away from `messages`, so
    # the array is two levels deep
    Array[Array[Array[String]]] out_messages = messages

    # This would be an error - 'names' is not accessible here
    # String scatter_names = names  
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
  "nested_scatter.out_messages": [
    [
      ["Hello Mr. Bilbo, how are you?", "Hello Mr. Bilbo Baggins, how are you?"],
      ["Goodbye Mr. Bilbo, how are you?", "Goodbye Mr. Bilbo Baggins, how are you?"]
    ],
    [
      ["Hello Wizard Gandalf, how are you?", "Hello Wizard Gandalf the Grey, how are you?"],
      ["Goodbye Wizard Gandalf, how are you?", "Goodbye Wizard Gandalf the Grey, how are you?"]
    ],
    [
      ["Hello Mr. Merry, how are you?", "Hello Mr. Merry Brandybuck, how are you?"],
      ["Goodbye Mr. Merry, how are you?", "Goodbye Mr. Merry Brandybuck, how are you?"]
    ]
  ]
}
```
</p>
</details>

### Conditional Statement

A conditional statement consists of the `if` keyword, followed by a `Boolean` expression and a body of (potentially nested) statements. The conditional body is only evaluated if the conditional expression evaluates to `true`.

After evaluation of the conditional has completed, each declaration or call output in the conditional body is exposed in the enclosing context as an optional declaration. In other words, for a declaration or call output `T <name>` within a conditional body, a declaration `T? <name>` is implicitly available outside of the conditional body. If the expression evaluated to `true`, and thus the body of the conditional was evaluated, then the value of each exposed declaration is the same as its original value inside the conditional body. If the expression evaluated to `false` and thus the body of the conditional was not evaluated, then the value of each exposed declaration is `None`.

The scoping rules for conditionals are similar to those for scatters - declarations or call outputs inside a conditional body are accessible within that conditional and any nested statements.

In the example below, `Int j` is accessible anywhere in the conditional body, and `Int? j` is an optional that is accessible outside of the conditional anywhere in `workflow test_conditional`.

<details>
<summary>
Example: test_conditional.wdl

```wdl
version 1.1

task gt_three {
  input {
    Int i
  }

  command <<< >>>

  output {
    Boolean valid = i > 3
  }
}

workflow test_conditional {
  input {
    Boolean do_scatter = true
    Array[Int] scatter_range = [1, 2, 3, 4, 5]
  }

  if (do_scatter) {
    Int j = 2

    scatter (i in scatter_range) {
      call gt_three { input: i = i + j }
      
      if (gt_three.valid) {
        Int result = i * j
      }

      # `result` is accessible here as an optional
      Int result2 = if defined(result) then select_first([result]) else 0
    }
  }
  
  # Here there is an implicit `Array[Int?]? result` declaration, since
  # `result` is inside a conditional inside a scatter inside a conditional.
  # We can "unwrap" the other optional using select_first.
  Array[Int?] maybe_results = select_first([result, []])

  output {
    Int? j_out = j
    # We can unwrap the inner optional using select_all to get rid of all
    # the `None` values in the array.
    Array[Int] result_array = select_all(maybe_results)

    # Here we reference the implicit declaration of result2, which is
    # created from an `Int` declaration inside a scatter inside a
    # conditional, and so becomes an optional array.
    Array[Int]? maybe_result2 = result2
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
  "test_conditional.result_array": [4, 6, 8, 10],
  "test_conditional.maybe_result2": [0, 4, 6, 8, 10]
}
```
</p>
</details>

WDL has no `else` keyword. To mimic an `if-else` statement, you would simply use two conditionals with inverted boolean expressions. A common idiom is to use `select_first` to select a value from either the `if` or the `if not` body, whichever one is defined.

<details>
<summary>
Example: if_else.wdl

```wdl
version 1.1

task greet {
  input {
    String time
  }

  command <<<
  printf "Good ~{time} buddy!"
  >>>

  output {
    String greeting = read_string(stdout())
  }
}

workflow if_else {
  input {
    Boolean is_morning = false
  }
  
  # the body *is not* evaluated since 'b' is false
  if (is_morning) {
    call greet as morning { time = "morning" }
  }

  # the body *is* evaluated since !b is true
  if (!is_morning) {
    call greet as afternoon { time = "afternoon" }
  }

  output {
    String greeting = select_first([morning.greeting, afternoon.greeting])
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
  "if_else.greeting": "Good afternoon buddy!"
}
```
</p>
</details>

It is impossible to have a multi-level optional type, e.g., `Int??`. The outputs of a conditional are only ever single-level optionals, even when there are nested conditionals.

<details>
<summary>
Example: nested_if.wdl

```wdl
version 1.1

import "if_else.wdl"

workflow nested_if {
  input {
    Boolean morning
    Boolean friendly
  }

  if (morning) {
    if (friendly) {
      call if_else.greet { time = "morning" }
    }
  }

  output {
    # Even though it's within a nested conditional, greeting
    # has a type of `String?` rather than `String??`
    String? greeting_maybe = greet.greeting

    # Similarly, `select_first` produces a `String`, not a `String?`
    String greeting = select_first([greet.greeting, "hi"])
  }
}
```
</summary>
<p>
Example input:

```json
{
  "nested_if.morning": true,
  "nested_if.friendly": false
}
```

Example output:

```json
{
  "nested_if.greeting_maybe": null,
  "nested_if.greeting": "hi"
}
```
</p>
</details>

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
version 1.1

workflow test_floor {
  input {
    Int i1
  }

  Int i2 = i1 - 1
  Float f1 = i1
  Float f2 = i1 - 0.1
  
  output {
    Array[Boolean] all_true = [floor(f1) == i1, floor(f2) == i2]
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
version 1.1

workflow test_ceil {
  input {
    Int i1
  }

  Int i2 = i1 + 1
  Float f1 = i1
  Float f2 = i1 + 0.1
  
  output {
    Array[Boolean] all_true = [ceil(f1) == i1, ceil(f2) == i2]
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
version 1.1

workflow test_round {
  input {
    Int i1
  }

  Int i2 = i1 + 1
  Float f1 = i1 + 0.49
  Float f2 = i1 + 0.50
  
  output {
    Array[Boolean] all_true = [round(f1) == i1, round(f2) == i2]
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
version 1.1

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
version 1.1

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
version 1.1

workflow test_sub {
  String chocolike = "I like chocolate when\nit's late"

  output {
    String chocolove = sub(chocolike, "like", "love") # I love chocolate when\nit's late
    String chocoearly = sub(chocolike, "late", "early") # I like chocoearly when\nit's early
    String chocolate = sub(chocolike, "late$", "early") # I like chocolate when\nit's early
    String chocoearlylate = sub(chocolike, "[^ ]late", "early") # I like chocearly when\nit's late
    String choco4 = sub(chocolike, " [:alpha:]{4} ", " 4444 ") # I 4444 chocolate 4444\nit's late
    String no_newline = sub(chocolike, "\\n", " ") # "I like chocolate when it's late"
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
  "test_sub.choco4": "I 4444 chocolate 4444\nit's late",
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
version 1.1

task change_extension {
  input {
    String prefix
  }

  command <<<
    printf "data" > ~{prefix}.data
    printf "index" > ~{prefix}.index
  >>>

  output {
    File data_file = "~{prefix}.data"
    String data = read_string(data_file)
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

Test config:

```json
{
  "exclude_output": ["data_file"]
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
version 1.1

workflow test_basename {
  output {
    Boolean is_true1 = basename("/path/to/file.txt") == "file.txt"
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
version 1.1

task gen_files {
  input {
    Int num_files
  }

  command <<<
    for i in 1..~{num_files}; do
      printf ${i} > a_file_${i}.txt
    done
    mkdir a_dir
    touch a_dir/a_inner.txt
  >>>

  output {  
    Array[File] files = glob("a_*")
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

Test config:

```json
{
  "exclude_output": ["files"]
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
version 1.1

task file_sizes {
  command <<<
    printf "this file is 22 bytes\n" > created_file
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
version 1.1

task echo_stdout {
  command <<< printf "hello world" >>>

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
version 1.1

task echo_stderr {
  command <<< >&2 printf "hello world" >>>

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
version 1.1

task read_string {
  # this file will contain "this\nfile\nhas\nfive\nlines\n"
  File f = write_lines(["this", "file", "has", "five", "lines"])
  
  command <<<
  cat ~{f}
  >>>
  
  output {
    # s will contain "this\nfile\nhas\nfive\nlines"
    String s = read_string(stdout())
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

Reads a file that contains a single line containing only an integer and (optional) whitespace. If the line contains a valid integer, that value is returned as an `Int`. If the file is empty or does not contain a single integer, an error is raised.

**Parameters**

1. `File`: Path of the file to read.

**Returns**: An `Int`.

<details>
<summary>
Example: read_int_task.wdl

```wdl
version 1.1

task read_int {
  command <<<
  printf "  1  \n" > int_file
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

Reads a file that contains only a numeric value and (optional) whitespace. If the line contains a valid floating point number, that value is returned as a `Float`. If the file is empty or does not contain a single float, an error is raised.

**Parameters**

1. `File`: Path of the file to read.

**Returns**: A `Float`.

<details>
<summary>
Example: read_float_task.wdl

```wdl
version 1.1

task read_float {
  command <<<
  printf "  1  \n" > int_file
  printf "  2.0  \n" > float_file
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

Reads a file that contains a single line containing only a boolean value and (optional) whitespace. If the non-whitespace content of the line is "true" or "false", that value is returned as a `Boolean`. If the file is empty or does not contain a single boolean, an error is raised. The comparison is case- and whitespace-insensitive.

**Parameters**

1. `File`: Path of the file to read.

**Returns**: A `Boolean`.

<details>
<summary>
Example: read_bool_task.wdl

```wdl
version 1.1

task read_bool {
  command <<<
  printf "  true  \n" > true_file
  printf "  FALSE  \n" > false_file
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

If the file is empty, an empty array is returned.

**Parameters**

1. `File`: Path of the file to read.

**Returns**: An `Array[String]` representation of the lines in the file.

<details>
<summary>
Example: grep_task.wdl

```wdl
version 1.1

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
version 1.1

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

If the file is empty, an empty array is returned.

**Parameters**

1. `File`: Path of the TSV file to read.

**Returns**: An `Array` of rows in the TSV file, where each row is an `Array[String]` of fields.

<details>
<summary>
Example: read_tsv_task.wdl

```wdl
version 1.1

task read_tsv {
  command <<<
    {
      printf "row1\tvalue1\n"
      printf "row2\tvalue2\n"
      printf "row3\tvalue3\n"
    } >> data.tsv
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
version 1.1

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

If the file is empty, an empty map is returned.

**Parameters**

1. `File`: Path of the two-column TSV file to read.

**Returns**: A `Map[String, String]`, with one element for each row in the TSV file.

<details>
<summary>
Example: read_map_task.wdl

```wdl
version 1.1

task read_map {
  command <<<
    printf "key1\tvalue1\n" >> map_file
    printf "key2\tvalue2\n" >> map_file
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
version 1.1

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

Note that an empty file is not valid according to the JSON specification, and so calling `read_json` on an empty file raises an error.

**Parameters**

1. `File`: Path of the JSON file to read.

**Returns**: A value whose type is dependent on the contents of the JSON file.

<details>
<summary>
Example: read_person.wdl

```wdl
version 1.1

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
version 1.1

workflow write_json_fail {
  Pair[Int, Map[Int, String]] x = (1, {2: "hello"})
  # this fails with an error - Map with Int keys is not serializable
  File f = write_json(x)
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

Test config:

```json
{
  "fail": true
}
```
</p>
</details>

<details>
<summary>
Example: write_json_task.wdl

```wdl
version 1.1

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

Reads a tab-separated value (TSV) file representing the names and values of the members of an `Object`. There must be exactly two rows, and each row must have the same number of elements, otherwise an error is raised. Trailing end-of-line characters (`\r` and `\n`) are removed from each line.

The first row specifies the object member names. The names in the first row must be unique; if there are any duplicate names, an error is raised.

The second row specifies the object member values corresponding to the names in the first row. All of the `Object`'s values are of type `String`.

**Parameters**

1. `File`: Path of the two-row TSV file to read.

**Returns**: An `Object`, with as many members as there are unique names in the TSV.

<details>
<summary>
Example: read_object_task.wdl

```wdl
version 1.1

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
    "key_2": "value_2"
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

The first line of the file must be a header row with the names of the object members. The names in the first row must be unique; if there are any duplicate names, an error is raised.

There are any number of additional rows, where each additional row contains the values of an object corresponding to the member names. Each row in the file must have the same number of fields as the header row. All of the `Object`'s values are of type `String`.

If the file is empty or contains only a header line, an empty array is returned.

**Parameters**

1. `File`: Path of the TSV file to read.

**Returns**: An `Array[Object]`, with `N-1` elements, where `N` is the number of rows in the file.

<details>
<summary>
Example: read_objects_task.wdl

```wdl
version 1.1

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
      "key_2": "value_A2"
    },
    {
      "key_0": "value_B0",
      "key_1": "value_B1",
      "key_2": "value_B2"
    },
    {
      "key_0": "value_C0",
      "key_1": "value_C1",
      "key_2": "value_C2"
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
version 1.1

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
  "write_object.obj": {
    "key_1": "value_1",
    "key_2": "value_2",
    "key_3": "value_3"
  }
}
```

Example output:

```json
{
  "write_object.results": ["key_1", "value_1"]
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
version 1.1

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
      "key_3": "value_3"
    },
    {
      "key_1": "value_4",
      "key_2": "value_5",
      "key_3": "value_6"
    },
    {
      "key_1": "value_7",
      "key_2": "value_8",
      "key_3": "value_9"
    }
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
version 1.1

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
version 1.1

workflow test_prefix_fail {
  Array[Array[String]] env3 = [["a", "b], ["c", "d"]]
  # this fails with an error - env3 element type is not primitive
  Array[String] bad = prefix("-x ", env3)
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

Test config:

```json
{
  "fail": true
}
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
version 1.1

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
version 1.1

workflow test_suffix_fail {
  Array[Array[String]] env3 = [["a", "b], ["c", "d"]]
  # this fails with an error - env3 element type is not primitive
  Array[String] bad = suffix("-z", env3)
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

Test config:

```json
{
  "fail": true
}
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
version 1.1

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
version 1.1

workflow test_squote {
  Array[String] env1 = ["key1=value1", "key2=value2", "key3=value3"]
  Array[Int] env2 = [1, 2, 3]
  
  output {
    Array[String] env1_quoted =  squote(env1)
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
version 1.1

workflow test_sep {
  Array[String] a = ["file_1", "file_2"]

  output {
    # these all evaluate to true
    Array[Boolean] all_true = [
      sep(' ', prefix('-i ', a)) == "-i file_1 -i file_2",
      sep("", ["a", "b", "c"]) == "abc",
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
  "test_sep.all_true": [true, true, true, true]
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
version 1.1

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
version 1.1

task double {
  input {
    Int n
  }

  command <<< >>>

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
version 1.1

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
version 1.1

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
version 1.1

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
version 1.1

workflow test_zip_fail {
  Array[Int] xs = [1, 2, 3]
  Array[String] zs = ["d", "e"]
  # this fails with an error - xs and zs are not the same length
  Array[Pair[Int, String]] bad = zip(xs, zs)
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

Test config:

```json
{
  "fail": true
}
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
version 1.1

workflow test_unzip {
  Array[Pair[Int, String]] int_str_arr = [(0, "hello"), (42, "goodbye")]
  Map[String, Int] m = {"a": 0, "b": 1, "c": 2}
  Pair[Array[String], Array[Int]] keys_and_values = unzip(as_pairs(m))
  Pair[Array[Int], Array[String]] expected1 = ([0, 42], ["hello", "goodbye"])
  
  output {
    Boolean is_true1 = unzip(int_str_arr) == expected1
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
version 1.1

workflow test_flatten {
  input {
    Array[Array[Int]] ai2D = [[1, 2, 3], [1], [21, 22]]
    Array[Array[File]] af2D = [["/tmp/X.txt"], ["/tmp/Y.txt", "/tmp/Z.txt"], []]
    Array[Array[Pair[Float, String]]] aap2D = [[(0.1, "mouse")], [(3, "cat"), (15, "dog")]]
    Map[Float, String] f2s = as_map(flatten(aap2D))
    Array[Array[Array[Int]]] ai3D = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    Array[File] expected2D = ["/tmp/X.txt", "/tmp/Y.txt", "/tmp/Z.txt"]
    Array[Array[Int]] expected3D = [[1, 2], [3, 4], [5, 6], [7, 8]]
  }

  output {
    Boolean is_true1 = flatten(ai2D) == [1, 2, 3, 1, 21, 22]
    Boolean is_true2 = flatten(af2D) == expected2D
    Boolean is_true3 = flatten(aap2D) == [(0.1, "mouse"), (3, "cat"), (15, "dog")]
    Boolean is_true4 = flatten(ai3D) == expected3D
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
version 1.1

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
  "test_select_first.five2": 5
}
```
</p>
</details>

<details>
<summary>
Example: select_first_only_none_fail.wdl

```wdl
version 1.1

workflow select_first_only_none_fail {
  Int? maybe_four_but_is_not = None
  select_first([maybe_four_but_is_not])  # error! array contains only None values
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

Test config:

```json
{
  "fail": true
}
```
</p>
</details>

<details>
<summary>
Example: select_first_empty_fail.wdl

```wdl
version 1.1

workflow select_first_empty_fail {
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
{}
```

Test config:

```json
{
  "fail": true
}
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
version 1.1

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
version 1.1

workflow test_as_pairs {
  Map[String, Int] x = {"a": 1, "c": 3, "b": 2}
  Map[String, Pair[File, File]] y = {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}
  Array[Pair[String, Int]] expected1 = [("a", 1), ("c", 3), ("b", 2)]
  Array[Pair[File, String]] expected2 = [("a.bam", "a"), ("b.bam", "b")]
  Map[File, String] expected3 = {"a.bam": "a", "b.bam": "b"}

  scatter (item in as_pairs(y)) {
    String s = item.left
    Pair[File, File] files = item.right
    Pair[File, String] bams = (files.left, s)
  }
  
  Map[File, String] bam_to_name = as_map(bams)

  output {
    Boolean is_true1 = as_pairs(x) == expected1
    Boolean is_true2 = bams == expected2
    Boolean is_true3 = bam_to_name == expected3
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
version 1.1

workflow test_as_map {
  input {
    Array[Pair[String, Int]] x = [("a", 1), ("c", 3), ("b", 2)]
    Array[Pair[String, Pair[File,File]]] y = [("a", ("a.bam", "a.bai")), ("b", ("b.bam", "b.bai"))]
    Map[String, Int] expected1 = {"a": 1, "c": 3, "b": 2}
    Map[String, Pair[File, File]] expected2 = {"a": ("a.bam", "a.bai"), "b": ("b.bam", "b.bai")}
  }

  output {
    Boolean is_true1 = as_map(x) == expected1
    Boolean is_true2 = as_map(y) == expected2
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
version 1.1

workflow test_as_map_fail {
  # this fails with an error - the "a" key is duplicated
  Boolean bad = as_map([("a", 1), ("a", 2)])
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

Test config:

```json
{
  "fail": true
}
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
version 1.1

workflow test_keys {
  input {
    Map[String,Int] x = {"a": 1, "b": 2, "c": 3}
    Map[String, Pair[File, File]] str_to_files = {
      "a": ("a.bam", "a.bai"), 
      "b": ("b.bam", "b.bai")
    }
  }

  scatter (item in as_pairs(str_to_files)) {
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
version 1.1

workflow test_collect_by_key {
  input {
    Array[Pair[String, Int]] x = [("a", 1), ("b", 2), ("a", 3)]
    Array[Pair[String, Pair[File, File]]] y = [
      ("a", ("a_1.bam", "a_1.bai")), 
      ("b", ("b.bam", "b.bai")), 
      ("a", ("a_2.bam", "a_2.bai"))
    ]
    Map[String, Array[Int]] expected1 = {"a": [1, 3], "b": [2]}
    Map[String, Array[Pair[File, File]]] expected2 = {
      "a": [("a_1.bam", "a_1.bai"), ("a_2.bam", "a_2.bai")], 
      "b": [("b.bam", "b.bai")]
    }
  }

  output {
    Boolean is_true1 = collect_by_key(x) == expected1
    Boolean is_true2 = collect_by_key(y) == expected2
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
version 1.1

workflow is_defined {
  input {
    String? name
  }

  if (defined(name)) {
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

  command <<< printf "Hello ~{name}" >>>

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

All WDL implementations are required to support the standard JSON input and output formats. WDL compliance testing is performed using test cases whose inputs and expected outputs are given in these formats. A WDL implementation may choose to provide additional input and output mechanisms so long as they are documented, and/or tools are provided to interconvert between engine-specific input and the standard JSON format, to foster interoperability between tools in the WDL ecosystem.

## JSON Input Format

The inputs for a workflow invocation may be specified as a single JSON object that contains one member for each top-level workflow input. The name of the object member is the [fully-qualified name](#fully-qualified-names--namespaced-identifiers) of the input parameter, and the value is the [serialized form](#appendix-a-wdl-value-serialization-and-deserialization) of the WDL value.

If the WDL implementation supports the [`allowNestedInputs`](#computing-call-inputs) hint, then task/subworkflow inputs can also be specified in the input JSON.

Here is an example JSON input file for a workflow `wf`:

```json
{
  "wf.int_val": 3,
  "wf.my_ints": [5, 6, 7, 8],
  "wf.ref_file": "/path/to/file.txt",
  "wf.some_struct": {
    "fieldA": "some_string",
    "fieldB": 42,
    "fieldC": "/path/to/file.txt"
  },
  "wf.task1.s": "task 1 input",
  "wf.task2.s": "task 2 input"
}
```

WDL implementations are only required to support workflow execution, and not necessarily task execution, so a JSON input format for tasks is not specified. However, it is strongly suggested that if an implementation does support task execution, that it also supports this JSON input format for tasks. It is left to the discretion of the WDL implementation whether it is required to prefix the task input with the task name, i.e., `mytask.infile` vs. `infile`.

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

### Specifying / Overriding Runtime Attributes

The value for any runtime attribute of any task called by a workflow can be overridden in the JSON input file. Unlike inputs, a WDL implementation must support overriding runtime attributes regardless of whether it supports the [`allowNestedInputs](#computing-call-inputs) hint.

Values for runtime attributes provided in the input JSON always supersede values supplied directly in the WDL. Overriding an attribute for a task nested within a `scatter` applies to all invocations of that task.

Values for standardized runtime attributes must adhere to the [supported types and formats](#runtime-section). Any non-standard runtime attributes that are not supported by the implementation are ignored.

To differentiate runtime attributes from task inputs, the `runtime` namespace is added after the task name.

```json
{
  "wf.task1.runtime.memory": "16 GB",
  "wf.task2.runtime.cpu": 2,
  "wf.task2.runtime.disks": "100",
  "wf.subwf.task3.runtime.container": "mycontainer:latest"
}
```

## JSON Output Format

The outputs from a workflow invocation may be serialized as a JSON object that contains one member for each top-level workflow output; subworkflow and task outputs are not provided. The name of the object member is the [fully-qualified name](#fully-qualified-names--namespaced-identifiers) of the output parameter, and the value is the [serialized form](#appendix-a-wdl-value-serialization-and-deserialization) of the WDL value.

Every WDL implementation must provide the ability to serialize workflow outputs in this standard format. It is suggested that WDL implementations make the standard format be the default output format.

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

## JSON Serialization of WDL Types

### Primitive Types

All primitive WDL types serialize naturally to JSON values:

| WDL Type  | JSON Type |
| --------- | --------- |
| `Int`     | `number`  |
| `Float`   | `number`  |
| `Boolean` | `boolean` |
| `String`  | `string`  |
| `File`    | `string`  |
| `None`    | `null`    |

JSON has a single numeric type - it does not differentiate between integral and floating point values. A JSON `number` is always deserialized to a WDL `Float`, which may then be [coerced](#type-coercion) to an `Int` if necessary.

JSON does not have a specific type for filesystem paths, but a WDL `String` may be coerced to a `File` if necessary.

### Array

Arrays are represented naturally in JSON using the `array` type. Each array element is serialized recursively into its JSON format.

When a JSON `array` is deserialized to WDL, each element of the array must be coercible to a common type.

### Struct and Object

`Struct`s and `Object`s are represented naturally in JSON using the `object` type. Each WDL `Struct` or `Object` member value is serialized recursively into its JSON format.

A JSON `object` is deserialized to a WDL `Object` value, and each member value is deserialized to its most likely WDL type. The WDL `Object` may then be coerced to a `Struct` or `Map` type if necessary.

### Pair

There is no natural or unambiguous serialization of a `Pair` to JSON. Attempting to serialize a `Pair` results in an error. A `Pair` must first be converted to a serializable type, e.g., using one of the following suggested methods.

#### Pair to Array

A `Pair[X, X]` may be converted to a two-element array.

<details>
<summary>
Example: pair_to_array.wdl

```wdl
version 1.1

workflow pair_to_array {
  Pair[Int, Int] p = (1, 2)
  Array[Int] a = [p.left, p.right]
  # We can convert back to Pair as needed
  Pair[Int, Int] p2 = (a[0], a[1])

  output {
    Array[Int] aout = a
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
  "pair_to_array.aout": [1, 2]
}
```
</p>
</details>

#### Pair to Struct

A `Pair[X, Y]` may be converted to a struct with two members `X left` and `Y right`.

<details>
<summary>
Example: pair_to_struct.wdl

```wdl
version 1.1

struct StringIntPair {
  String l
  Int r
}

workflow pair_to_struct {
  Pair[String, Int] p = ("hello", 42)
  StringIntPair s = StringIntPair {
    l: p.left,
    r: p.right
  }
  # We can convert back to Pair as needed
  Pair[String, Int] p2 = (s.l, s.r)

  output {
    StringIntPair sout = s
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
  "pair_to_struct.sout": {
    "l": "hello",
    "r": 42
  }
}
```
</p>
</details>

### Map

A `Map[String, X]` may be serialized to a JSON `object` by the same mechanism as a WDL `Struct` or `Object`. This value will be deserialized to a WDL `Object`, after which it may be coerced to a `Map`.

There is no natural or unambiguous serialization of a `Map` with a non-`String` key type. Attempting to serialize a `Map` with a non-`String` key type results in an error. A `Map` with non-`String` keys must first be converted to a serializable type, e.g., using one of the following suggested methods.

#### Map to Struct

A `Map[X, Y]` can be converted to a `Struct` with two array members: `Array[X] keys` and `Array[Y] values`. This is the suggested approach.

<details>
<summary>
Example: map_to_struct2.wdl

```wdl
version 1.1

struct IntStringMap {
  Array[Int] keys
  Array[String] values
}

workflow map_to_struct2 {
  Map[Int, String] m = {0: "a", 1: "b"}
  Array[Pair[Int, String]] int_string_pairs = as_pairs(m)
  Pair[Array[Int], Array[String]] int_string_arrays = unzip(int_string_pairs)

  IntStringMap s = IntStringMap {
    keys: int_string_arrays.left,
    values: int_string_arrays.right
  }

  # We can convert back to Map
  Map[Int, String] m2 = as_map(zip(s.keys, s.values))
  
  output {
    IntStringMap sout = s
    Boolean is_equal = m == m2
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
  "map_to_struct2.sout": {
    "keys": [0, 1],
    "values": ["a", "b"]
  },
  "map_to_struct2.is_equal": true
}
```
</p>
</details>

#### Map to Array

A `Map[X, X]` can be converted to an array of `Pair`s. Each pair can then be converted to a serializable format using one of the methods described in the previous section. This approach is less desirable as it requires the use of a `scatter`.

<details>
<summary>
Example: map_to_array.wdl

```wdl
version 1.1

workflow map_to_array {
  Map[Int, Int] m = {0: 7, 1: 42}
  Array[Pair[Int, Int]] int_int_pairs = as_pairs(m)

  scatter (p in int_int_pairs) {
    Array[Int] a = [p.left, p.right]
  }

  output {
    Array[Array[Int]] aout = a
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
  "map_to_array.aout": [[0, 7], [1, 42]]
}
```
</p>
</details>

# Appendix A: WDL Value Serialization and Deserialization

This section provides suggestions for ways to deal with primitive and compound values in the task [command section](#command-section). When a WDL execution engine instantiates a command specified in the `command` section of a task, it must evaluate all expression placeholders (`~{...}` and `${...}`) in the command and coerce their values to strings. There are multiple different ways that WDL values can be communicated to the command(s) being called in the `command` section, and the best method will vary by command.

For example, a task that wraps a tool that operates on an `Array` of FASTQ files has several ways that it can specify the list of files to the tool:

* A file containing one file path per line, e.g. `Rscript analysis.R --files=fastq_list.txt`
* A file containing a JSON list, e.g. `Rscript analysis.R --files=fastq_list.json`
* Enumerated on the command line, e.g. `Rscript analysis.R 1.fastq 2.fastq 3.fastq`

On the other end, command line tools will output results in files or to standard output, and these outputs need to be converted to WDL values to be used as task outputs. For example, the FASTQ processor task mentioned above outputs a mapping of the input files to the number of reads in each file. This output might be represented as a two-column TSV or as a JSON object, both of which would need to be deserialized to a WDL `Map[File, Int]` value.

The various methods for serializing and deserializing primitive and compound values are enumerated below.

## Primitive Values

WDL primitive values are naturally converted to string values. This is described in detail in the [string interpolation](#expression-placeholders-and-string-interpolation) section.

Deserialization of primitive values is done via one of the `read_*` functions, each of which deserializes a different type of primitive value from a file. The file must contain a single value of the expected type, with optional whitespace. The value is read as a string and then converted to the appropriate type, or raises an error if the value cannot be converted.

<details>
<summary>
Example: read_write_primitives_task.wdl

```wdl
version 1.1

task read_write_primitives {
  input {
    String s
    Int i
  }

  command <<<
  printf ~{s} > str_file
  printf ~{i} > int_file
  >>>

  output {
    String sout = read_string("str_file")
    String istr = read_string("int_file")
    Int iout = read_int("int_file")
    # This would cause an error since "hello" cannot be converted to an Int:
    #Int sint = read_int("str_file")
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
  "read_write_primitives.s": "hello",
  "read_write_primitives.i": 42
}
```

Example output:

```json
{
  "read_write_primitives.sout": "hello",
  "read_write_primitives.istr": "42",
  "read_write_primitives.iout": 42
}
```
</p>
</details>

## Compound Values

A compound value such as `Array` or `Map` must be serialized to a string before it can be used in the command. There are a two general strategies for converting a compound value to a string:

* JSON: most compound values can be written to JSON format using [`write_json`](#write_json).
* Delimitation: convert each element of the compound value to a string, then join them together into a single string using a delimiter. Some common approaches are:
    * Separate values by a tool-specific delimiter (e.g., whitespace or comma) and pass the string as a single command line argument. This can be accomplished with the [`sep`](#sep) function.
    * Prefix each value with a command line option. This can be accomplished with the [`prefix`](#prefix) function.
    * Separate values by newlines (`\n`) and write them to a file. This can be accomplished with the [`write_lines`](function).
    * For nested types such as `Struct`s and `Object`, separate the fields of each value with a tab (`\t`), and write each tab-delimited line to a file. This is commonly called tab_separated value (TSV) format. This can be accomplished using [`write_tsv`](#write_tsv), [`write_map`](#write_map), [`write_object`](#write_object), or [`write_objects`](#write_objects).

Similarly, data output by a command must be deserialized to be used in WDL. Commands generally either write output to `stdout` (or sometimes `stderr`) or to a regular file. The contents of `stdout` and `stderr` can be read a files using the [`stdout`](#stdout) and [`stderr`](#stderr) functions. The two general strategies for deserializing data from a file are:

* If the output is in JSON format, it can be read into a WDL value using [`read_json`](#read_json).
* If the output is line-oriented (i.e., one value per line), it can be read into a WDL `Array` using [`read_lines`](#read_lines).
* If the output is tab-delimited (TSV), it can be read into a structured value using [`read_tsv`](#read_tsv), [`read_map`](#read_map), [`read_object`](#read_object), or [`read_objects`](#read_objects).

Specific examples of serializing and deserializing each type of compound value are given below.

### Array

#### Array serialization by delimitation

This method applies to an array of a primitive type. Each element of the array is coerced to a string, and the strings are then joined into a single string separated by a delimiter. This is done using the [`sep`](#sep) function.

<details>
<summary>
Example: serialize_array_delim_task.wdl

```wdl
version 1.1

task serialize_array_delim {
  input {
    File infile
    Array[Int] counts
  }

  Array[String] args = squote(prefix("-n", counts))

  command <<<
  for arg in ~{sep(" ", args)}; do
    head $arg ~{infile}
  done
  >>>
  
  output {
    Array[String] heads = read_lines(stdout())
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
  "serialize_array_delim.infile": "greetings.txt",
  "serialize_array_delim.counts": [1, 2]
}
```

Example output:

```json
{
  "serialize_array_delim.strings": [
    "hello world",
    "hello world",
    "hi_world"
  ]
}
```
</p>
</details>

Given an array `[1, 2]`, the instantiated command would be:

```sh
for arg in '-n1' '-n2'; do
  head $arg greetings.txt
done
```

#### Array serialization/deserialization using `write_lines()`/`read_lines()`

This method applies to an array of a primitive type. Using `write_lines`, Each element of the array is coerced to a string, and the strings are written to a file, one element per line. Using `read_lines`, each line of the file is read as a `String` and coerced to the target type.

<details>
<summary>
Example: serde_array_lines_task.wdl

```wdl
version 1.1

task serde_array_lines {
  input {
    File infile
    Array[String] patterns
  }

  command <<<
  while read -r pattern; do
    grep -c "$pattern" ~{infile}
  done < ~{write_lines(patterns)}
  >>>

  output {
    Array[Int] matches = read_lines(stdout())
  }
}
```
</summary>
<p>
Example input:

```json
{
  "serde_array_lines.infile": "greetings.txt",
  "serde_array_lines.patterns": ["hello", "world"]
}
```

Example output:

```json
{
  "serde_array_lines.matches": [2, 2]
}
```
</p>
</details>

Given an array of patterns `["hello", "world"]`, the instantiated command would be:

```sh
while read pattern; do
  grep "$pattern" greetings.txt | wc -l
done < /jobs/564758/patterns
```

Where `/jobs/564758/patterns` contains:

```txt
hello
world
```

#### Array serialization/deserialization using `write_json()`/`read_json()`

This method applies to an array of any type that can be serialized to JSON. Calling [`write_json`](#write_json) with an `Array` parameter results in the creation of a file containing a JSON array.

<details>
<summary>
Example: serde_array_json_task.wdl

```wdl
version 1.1

task serde_array_json {
  input {
    Map[String, Int] string_to_int
  }

  command <<<
    python <<CODE
    import json
    import sys
    with open("~{write_json(string_to_int)}") as j:
      d = json.load(j)
      json.dump(list(d.keys()), sys.stdout)
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
{
  "serde_array_json.string_to_int": {
    "a": 1,
    "b": 2
  }
}
```

Example output:

```json
{
  "serde_array_json.keys": ["a", "b"]
}
```
</p>
</details>

Given the `Map` `{"a": 1, "b": 2}`, the instantiated command would be:

```python
import json
import sys
with open("/jobs/564758/string_to_int.json") as j:
  d = json.load(j)
  json.dump(list(d.keys()), sys.stdout)
```

Where `/jobs/564758/string_to_int.json` would contain:

```json
{
  "a": 1,
  "b": 2
}
```

### Pair

A `Pair` cannot be directly serialized to a `String`, nor can it be deserialized from a string or a file.

The most common approach to `Pair` serialization is to serialize the `left` and `right` values separately, e.g., by converting each to a `String` or writing each to a separate file using one of the `write_*` functions. Similarly, two values can be deserialized independently and then used to create a `Pair`.

<details>
<summary>
Example: serde_pair.wdl

```wdl
version 1.1

task tail {
  input {
    Pair[File, Int] to_tail
  }

  command <<<
  tail -n ~{to_tail.right} ~{to_tail.left}
  >>>

  output {
    Array[String] lines = read_lines(stdout())
  }
}

workflow serde_pair {
  input {
    Map[File, Int] to_tail
  }

  scatter (item in as_pairs(to_tail)) {
    call tail {
      input: to_tail = item
    }
    Pair[String, String]? two_lines = 
      if item.right >= 2 then (tail.lines[0], tail.lines[1]) else None
  }

  output {
    Map[String, String] tails_of_two = as_map(select_all(two_lines))
  }
}
```
</summary>
<p>
Example input:

```json
{
  "serde_pair.to_tail": {
    "cities.txt": 2,
    "hello.txt": 1
  }
}
```

Example output:

```json
{
  "serde_pair.tails_of_two": {
    "Houston": "Chicago"
  }
}
```
</p>
</details>

#### Homogeneous Pair serialization/deserialization as Array

A homogeneous `Pair[X, X]` can be converted to/from an `Array` and then serialized/deserialized by any of the methods in the previous section.

<details>
<summary>
Example: serde_homogeneous_pair.wdl

```wdl
version 1.1

task serde_int_strings {
  input {
    Pair[String, String] int_strings
  }

  Array[String] pair_array = [int_strings.left, int_strings.right]

  command <<<
  cat ~{write_lines(pair_array)}
  >>>

  output {
    Array[Int] ints = read_lines(stdout())
  }
}

workflow serde_homogeneous_pair {
  input {
    Map[String, String] int_strings
  }

  scatter (pair in as_pairs(int_strings)) {
    call serde_int_strings { input: int_strings = pair }
  }

  output {
    Array[Int] ints = flatten(serde_int_strings.ints)
  }
}
```
</summary>
<p>
Example input:

```json
{
  "serde_homogeneous_pair.int_strings": {
    "1": "2",
    "3": "4"
  }
}
```

Example output:

```json
{
  "serde_homogeneous_pair.ints": [1, 2, 3, 4]
}
```
</p>
</details>

#### Pair serialization/deserialization using `read_json`/`write_json`

A `Pair[X, Y]` can be [converted to JSON](#pair) and then serialized using [`write_json`](#write_json) and deserialized using [`read_json`](#read_json).

### Map

#### Map serialization by delimitation

A `Map` is a common way to represent a set of arguments that need to be passed to a command. Each key/value pair can be converted to a `String` using a `scatter`, or the keys and value can be independently converted to Bash arrays and referenced by index.

<details>
<summary>
Example: serialize_map.wdl

```wdl
version 1.1

task grep1 {
  input {
    File infile
    String pattern
    Array[String] args
  }

  command <<<
  grep ~{sep(" ", args)} ~{pattern} ~{infile}
  >>>
  
  output {
    Array[String] results = read_lines(stdout())
  }
}

task grep2 {
  input {
    File infile
    String pattern
    Map[String, String] args
  }

  Pair[Array[String], Array[String]] opts_and_values = unzip(as_pairs(args))
  Int n = length(opts_and_values.left)

  command <<<
  opts=( ~{sep(" ", quote(opts_and_values.left))} )
  values=( ~{sep(" ", quote(opts_and_values.right))} )
  command="grep"
  for i in 1..~{n}; do
    command="$command ${opts[i]}"="${values[i]}"
  done
  $command ~{pattern} ~{infile}
  >>>

  output {
    Array[String] results = read_lines(stdout())
  }
}

workflow serialize_map {
  input {
    File infile
    String pattern
    Map[String, String] args
  }

  scatter (arg in as_pairs(args)) {
    String arg_str = "~{arg.left}=~{arg.right}"
  }

  call grep1 { input: infile, pattern, args = arg_str }

  call grep2 { input: infile, pattern, args }

  output {
    Array[String] results1 = grep1.results
    Array[String] results2 = grep2.results
  }
}
```
</summary>
<p>
Example input:

```json
{
  "serialize_map.infile": "greetings.txt",
  "serialize_map.pattern": "hello",
  "serialize_map.args": {
    "--after-context": "1",
    "--max-count": "1"
  }
}
```

Example output:

```json
{
  "serialize_map.results1": ["hello world", "hi_world"],
  "serialize_map.results2": ["hello world", "hi_world"]
}
```
</p>
</details>

#### Map serialization/deserialization using `write_map()`/`read_map()`

A `Map[String, String]` value can be serialized as a two-column TSV file using [`write_map`](#write_map), and deserialized from a two-column TSV file using [`read_map`](#read_map).

<details>
<summary>
Example: serde_map_tsv_task.wdl

```wdl
version 1.1

task serde_map_tsv {
  input {
    Map[String, String] items
  }

  File item_file = write_map(items)

  command <<<
  cut -f 1 ~{item_file} >> lines
  cut -f 2 ~{item_file} >> lines
  paste -s -d '\t\n' lines
  >>>

  output {
    Map[String, String] new_items = read_map("lines")
  }
}
```
</summary>
<p>
Example input:

```json
{
  "serde_map_tsv.items": {
    "a": "b",
    "c": "d",
    "e": "f"
  }
}
```

Example output:

```json
{
  "serde_map_tsv.new_items": {
    "a": "c",
    "e": "b",
    "d": "f"
  }
}
```
</p>
</details>

Given a `Map` `{ "a": "b", "c": "d", "e": "f" }`, the instantiated command would be:

```sh
cut -f 1 /jobs/564757/item_file >> lines
cut -f 2 /jobs/564757/item_file >> lines
paste -s -d '\t\n' lines
```

Where `/jobs/564757/item_file` would contain:

```txt
a\tb
c\td
e\tf
```

And the created `lines` file would contain:

```txt
a\tc,
e\tb,
d\tf
```

Which is deserialized to the `Map` `{"a": "c", "e": "b", "d": "f"}`.

#### Map serialization/deserialization using `write_json()`/`read_json()`

A `Map[String, Y]` value can be serialized as a JSON `object` using [`write_json`](#write_json), and a JSON object can be read into a `Map[String, Y]` using [`read_json`](#read_json) so long as all the values of the JSON object are coercible to `Y`.

<details>
<summary>
Example: serde_map_json_task.wdl

```wdl
version 1.1

task serde_map_json {
  input {
    Map[String, Float] read_quality_scores
  }

  command <<<
    python <<CODE
    import json
    import sys
    with open("~{write_json(read_quality_scores)}") as j:
      d = json.load(j)
      for key in d.keys():
        d[key] += 33
      json.dump(d, sys.stdout)
    CODE
  >>>

  output {
    Map[String, Float] ascii_values = read_json(stdout())
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
{
  "serde_map_json.read_quality_scores": {
    "read1": 32,
    "read2": 41,
    "read3": 55
  }
}
```

Example output:

```json
{
  "serde_map_json.ascii_values": {
    "read1": 65,
    "read2": 74,
    "read3": 88
  }
}
```
</p>
</details>

Given a `Map` `{ "read1": 32, "read2": 41, "read3": 55 }`, the instantiated command would be:

```python
import json
import sys
with open("/jobs/564757/sample_quality_scores.json") as j:
  d = json.load(j)
  for key in d.keys():
    d[key] += 33
  json.dump(d, sys.stdout)
```

Where `/jobs/564757/sample_quality_scores.json` would contain:

```json
{
  "read1": 32,
  "read2": 41,
  "read3": 55,
}
```

### Struct and Object serialization/deserialization

There are two alternative serialization formats for `Struct`s and `Objects:

* JSON: `Struct`s and `Object`s are serialized identically using [`write_json`](#write_json). A JSON object is deserialized to a WDL `Object` using [`read_json`](#read_json), which can then be coerced to a `Struct` type if necessary.
* TSV: `Struct`s and `Object`s can be serialized to TSV format using [`write_object`](#write_object). The generated file has two lines tab-delimited: a header with the member names and the values, which must be coercible to `String`s. An array of `Struct`s or `Object`s can be written using [`write_objects`](#write_objects), in which case the generated file has one line of values for each struct/object. `Struct`s and `Object`s can be deserialized from the same TSV format using [`read_object`](#read_object)/[`read_objects`](#read_objects). Object member values are always of type `String` whereas struct member types must be coercible from `String`.

# Appendix B: WDL Namespaces and Scopes

Namespaces and scoping in WDL are somewhat complex topics, and some aspects are counter-intuitive for users coming from backgrounds in other programming languages. This section goes into deeper details on these topics.

## Namespaces

The following WDL namespaces exist:

* [WDL document](#wdl-documents)
    * The namespace of an [imported](#import-statements) document equals that of the basename of the imported file by default, but may be aliased using the `as <identifier>` syntax.
    * A WDL document may contain a `workflow` and/or `task`s, which are names within the document's namespace.
    * A WDL document may contain `struct`s, which are also names within the document's namespace and usable as types in any declarations. Structs from any imported documents are [copied into the document's namespace](#importing-and-aliasing-structs) and may be aliased using the `alias <source name> as <new name>` syntax.
* A [WDL `task`](#task-definition) is a namespace consisting of:
    * `input`, `output`, and private declarations
    * A [`runtime`](#runtime-section) namespace that contains all the runtime attributes
* A [WDL `workflow`](#workflow-definition) is a namespace consisting of:
    * `input`, `output`, and private declarations
    * The [`call`s](#call-statement) made to tasks and subworkflows within the body of the workflow.
        * A call is itself a namespace that equals the name of the called task or subworkflow by default, but may be aliased using the `as <identifier>` syntax.
        * A call namespace contains the output declarations of the called task or workflow.
    * The body of each nested element (`struct` or `if` statement).
* A [`Struct` instance](#struct-definition): is a namespace consisting of the members defined in the struct. This also applies to `Object` instances.

All members of a namespace must be unique within that namespace. For example:

* Two documents cannot be imported while they have the same namespace identifier - at least one of them would need to be aliased.
* A workflow and a namespace both named `foo` cannot exist inside a common namespace.
* There cannot be a call `foo` in a workflow also named `foo`.
 
However, two sub-namespaces imported into the same parent namespace are allowed to contain the same names. For example, two documents with different namespace identifiers `foo` and `bar` can both have a task named `baz`, because the [fully-qualified names](#fully-qualified-names--namespaced-identifiers) of the two tasks would be different: `foo.baz` and `bar.baz`.

## Scopes

A "scope" is associated with a level of nesting within a namespace. The visibility of WDL document elements is governed by their scope, and by WDL's scoping rules, which are explained in this section.

### Global Scope

A WDL document is the top-level (or "outermost") scope. All elements defined within a document that are not nested inside other elements are in the global scope and accessible from anywhere in the document. The elements that may be in a global scope are:

* A `workflow`
* Any number of `task`s
* Imported namespaces
* All `struct`s defined in the document and in any imported documents

### Task Scope

A task scope consists of all the declarations in the task `input` section and in the body of the task. The `input` section is used only to delineate which declarations are visible outside the task (i.e., they are part of the task's namespace) and which are private to the task. Input declarations may reference private declarations, and vice-versa. Declarations in the task scope may be referenced in expressions anywhere in the task (i.e., `command`, `runtime`, and `output` sections).

The `output` section can be considered a nested scope within the task. Expressions in the output scope may reference declarations in the task scope, but the reverse is not true. This is because declarations in the task scope are evaluated when a task is invoked (i.e., before it's command is evaluated and executed), while declarations in the output scope are only evaluated after execution of the command is completed.

For example, in this task:

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

  runtime {
    memory: "~{y} GB"
  }
}
```

* `x` and `f` are `input` values that are evaluated when the task is invoked.
* `y` is an private declaration with a dependency on the input `x`.
* The `command` references both `input` and private declarations. However, it would be an error for  the `command` to reference `z`.
* `z` is an `output` declaration.
* `z_plus_one` is also an `output` declaration - it references another output declaration `z`.
* In the `runtime` section, attribute values may be expressions that reference declarations in the task body. The value of `memory` is determined using the value of `y`.

### Workflow Scope

A workflow scope consists of:

* Declarations in the workflow `input` section.
* Private declarations in the body of the workflow.
* Calls in the workflow.
* Declarations and call outputs that are exported from nested scopes within the workflow (i.e., scatters and conditionals).
 
Just like in the task scope, all declarations in the workflow scope can reference each other, and the `output` section is a nested scope that has access to - but cannot be accessed from - the workflow scope.

For example, in this workflow (which calls the `my_task` task from the previous example):

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

* `file` and `x` are `input` declarations that are evaluated when the workflow is invoked.
* The call body provides inputs for the task values `x` and `f`. Note that `x` is used twice in the line `x = x`:
    * First: to name the value in the task being provided. This must reference an input declaration in the namespace of the called task.
    * Second: as part of the input expression. This expression may reference any values in the current workflow scope.
* `z` is an output declaration that depends on the output from the `call` to `my_task`. It is not accessible from elsewhere outside the `output` section.

Workflows can have (potentially nested) scatters and conditionals, each of which has a body that defines a nested scope. A nested scope can have declarations, calls, scatters, and conditionals (which create another level of nested scope). The declarations and calls in a nested scope are visible within that scope and within any sub-scopes, recursively.

Every nested scope implicitly "exports" all of its declarations and call outputs in the following manner:

* A scatter scope exports its declarations and calls with the same names they have inside the scope, but with their types modified, such that the exported types are all `Array[X]`, where `X` is the type of the declaration within the scope.
    * A scatter scope *does not* export its scatter variable. For example, the `x` variable in `scatter (x in array)` is only accessible from within the scatter scope and any nested scopes; it is not accessible outside of the scatter scope.
* A conditional scope exports its declarations and calls with the same names they have inside the scope, but with their types modified, such that the exported types are all `X?`, where `X` is the type of the declaration within the scope.

For example: in this workflow (which scatters over the `my_task` task from the previous examples):

```wdl
workflow my_workflow {
  input {
    File file
    Array[Int] xs = [1, 2, 3]
  }

  scatter (x in xs) {
    call my_task {
      input:
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
* The output `zs` references `z` even though it was declared in a sub-section. However, because `z` is declared within a `scatter` body, the type of `zs` is `Array[Int]` outside of that scatter.

The concept of a single name within a workflow having different types depending on where it appears can be confusing at first, and it helps to think of these as two different variables. When the user makes a declaration within a nested scope, they are essentially reserving that name in all of the higher-level scopes so that it cannot be reused.

For example, the following workflow is invalid:

```wdl
workflow invalid {
  Boolean b = true
  
  scatter {
    String x = "hello"
  }
  
  # The scatter exports x to the top-level scope - there is an implicit 
  # declaration `Array[String] x` here that is reserved to hold the 
  # exported value and cannot be used by any other declaration in this scope.
  
  if (b) {
    # error! `x` is already reserved in the top-level scope to hold the exported 
    # value of `x` from the scatter, so we cannot reserve it here
    Float x = 1.0
  }

  # error! `x` is already reserved
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

Cycles can be tricky to detect, for example when they occur between declarations in different scopes within a workflow. For example, here is a workflow with one block that references a declaration that originates in another block:

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

* The declaration for `x_b` is able to access the value for `x_a` even though the declaration is in another sub-section of the workflow.
* Because the declaration for `x_b` is outside the `scatter` in which `x_a` was declared, the type is `Array[Int]`

The following change introduces a cyclic dependency between the scatters:

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

The dependency graph now has cyclic dependencies between elements in the `scatter (a in as)` and `scatter (b in bs)` bodies, which is not allowed. One way to avoid such cyclic dependencies would be to create two separate `scatter`s over the same input array:

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

Elements such as structs and task `runtime` sections are namespaces, but they lack scope because their members cannot reference each other. For example, one member of a struct cannot reference another member in that struct, nor can a runtime attribute reference another attribute.

## Evaluation Order

A key concept in WDL is: **the order in which statements are evaluated depends on the availability of their dependencies, not on the linear orderering of the statements in the document.**

All values in tasks and workflows *can* be evaluated as soon as - but not before - their expression inputs are available; beyond this, it is up to the execution engine to determine when to evaluate each value.

Remember that, in tasks, the `command` section implicitly depends on all the input and private declarations in the task, and the `output` section implicitly depends on the `command` section. In other words, the `command` section cannot be instantiated until all input and private declarations are evaluated, and the `output` section cannot be evaluated until the command successfully completes execution. This is true even for private declarations that follow the `command` positionally in the file.

A "forward reference" occurs when an expression refers to a declaration that occurs at a later position in the WDL file. Given the above cardinal rule of evaluation order, forward references are allowed, so long as all declarations can ultimately be processed as an acyclic graph.

For example, this is a valid workflow:

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
