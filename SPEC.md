# Workflow Description Language (WDL)

This is version 1.2.1 of the Workflow Description Language (WDL) specification. It describes WDL `version 1.2`. It introduces a number of new features (denoted by the ✨ symbol) and clarifications to the [1.1.*](https://github.com/openwdl/wdl/blob/wdl-1.1/SPEC.md) version of the specification. It also deprecates several aspects of the 1.0 and 1.1 specifications that will be removed in the [next major WDL version](https://github.com/openwdl/wdl/blob/wdl-2.0/SPEC.md) (denoted by the 🗑 symbol).

## Revisions

Revisions to this specification are made periodically in order to correct errors, clarify language, or add additional examples. Revisions are released as "patches" to the specification, i.e., the third number in the specification version is incremented. No functionality is added or removed after the initial revision of the specification is ratified.

* [1.2.1]():
* [1.2.0](https://github.com/openwdl/wdl/tree/release-1.2.0/SPEC.md): 2024-05-24
 
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
          - [Multi-line Strings](#multi-line-strings)
        - [Files and Directories](#files-and-directories)
      - [Optional Types and None](#optional-types-and-none)
      - [Compound Types](#compound-types)
        - [Array\[X\]](#arrayx)
        - [Pair\[X, Y\]](#pairx-y)
        - [Map\[P, Y\]](#mapp-y)
        - [🗑 Object](#-object)
        - [Custom Types (Structs)](#custom-types-structs)
      - [Hidden and Scoped Types](#hidden-and-scoped-types)
        - [`Union` (Hidden Type)](#union-hidden-type)
        - [`hints`, `input`, and `output` (Scoped Types)](#hints-input-and-output-scoped-types)
        - [`task` (Hidden Scoped Type)](#task-hidden-scoped-type)
      - [Type Conversion](#type-conversion)
        - [Primitive Conversion to String](#primitive-conversion-to-string)
        - [Type Coercion](#type-coercion)
          - [Order of Precedence](#order-of-precedence)
          - [Coercion of Optional Types](#coercion-of-optional-types)
          - [Struct/Object Coercion from Map](#structobject-coercion-from-map)
          - [Struct-to-Struct Coercion](#struct-to-struct-coercion)
          - [🗑 Limited Exceptions](#-limited-exceptions)
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
    - [Environment Variables](#environment-variables)
      - [String Escaping and Injection Prevention](#string-escaping-and-injection-prevention)
    - [Command Section](#command-section)
      - [Expression Placeholders](#expression-placeholders)
      - [Stripping Leading Whitespace](#stripping-leading-whitespace)
    - [Task Outputs](#task-outputs)
      - [File, Directory, and Optional Outputs](#file-directory-and-optional-outputs)
    - [Evaluation of Task Declarations](#evaluation-of-task-declarations)
    - [✨ Requirements Section](#-requirements-section)
      - [Units of Storage](#units-of-storage)
      - [Requirements attributes](#requirements-attributes)
        - [`container`](#container)
        - [`cpu`](#cpu)
        - [`memory`](#memory)
        - [Hardware Accelerators (`gpu` and ✨ `fpga`)](#hardware-accelerators-gpu-and--fpga)
        - [`disks`](#disks)
        - [`max_retries`](#max_retries)
        - [`return_codes`](#return_codes)
    - [✨ Hints Section](#-hints-section)
      - [Hints-scoped types](#hints-scoped-types)
      - [Reserved Task Hints](#reserved-task-hints)
        - [`max_cpu`](#max_cpu)
        - [`max_memory`](#max_memory)
        - [✨ `disks`](#-disks)
        - [✨ `gpu` and ✨ `fpga`](#-gpu-and--fpga)
        - [`short_task`](#short_task)
        - [`localization_optional`](#localization_optional)
        - [`inputs`](#inputs)
        - [`outputs`](#outputs)
      - [Compute Environments](#compute-environments)
      - [Conventions and Best Practices](#conventions-and-best-practices)
    - [🗑 Runtime Section](#-runtime-section)
    - [Metadata Sections](#metadata-sections)
      - [Meta Values](#meta-values)
      - [Task Metadata Section](#task-metadata-section)
      - [Parameter Metadata Section](#parameter-metadata-section)
    - [Runtime Access to Requirements, Hints, and Metadata](#runtime-access-to-requirements-hints-and-metadata)
    - [Advanced Task Examples](#advanced-task-examples)
      - [Example 1: HISAT2](#example-1-hisat2)
      - [Example 2: GATK Haplotype Caller](#example-2-gatk-haplotype-caller)
  - [Workflow Definition](#workflow-definition)
    - [Workflow Elements](#workflow-elements)
    - [Evaluation of Workflow Elements](#evaluation-of-workflow-elements)
    - [Fully Qualified Names \& Namespaced Identifiers](#fully-qualified-names--namespaced-identifiers)
    - [Workflow Inputs](#workflow-inputs)
    - [Workflow Outputs](#workflow-outputs)
    - [Workflow Hints](#workflow-hints)
      - [Reserved Workflow Hints](#reserved-workflow-hints)
        - [`allow_nested_inputs`](#allow_nested_inputs)
    - [Call Statement](#call-statement)
      - [Computing Call Inputs](#computing-call-inputs)
    - [Scatter Statement](#scatter-statement)
    - [Conditional Statement](#conditional-statement)
- [Standard Library](#standard-library)
  - [Numeric Functions](#numeric-functions)
    - [`floor`](#floor)
    - [`ceil`](#ceil)
    - [`round`](#round)
    - [`min`](#min)
    - [`max`](#max)
  - [String Functions](#string-functions)
    - [✨ `find`](#-find)
    - [✨ `matches`](#-matches)
    - [`sub`](#sub)
  - [File Functions](#file-functions)
    - [`basename`](#basename)
    - [✨ `join_paths`](#-join_paths)
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
    - [`suffix`](#suffix)
    - [`quote`](#quote)
    - [`squote`](#squote)
    - [`sep`](#sep-1)
  - [Generic Array Functions](#generic-array-functions)
    - [`range`](#range)
    - [`transpose`](#transpose)
    - [`cross`](#cross)
    - [`zip`](#zip)
    - [`unzip`](#unzip)
    - [✨ `contains`](#-contains)
    - [✨ `chunk`](#-chunk)
    - [`flatten`](#flatten)
    - [`select_first`](#select_first)
    - [`select_all`](#select_all)
  - [Map Functions](#map-functions)
    - [`as_pairs`](#as_pairs)
    - [`as_map`](#as_map)
    - [`keys`](#keys)
    - [✨ `contains_key`](#-contains_key)
    - [✨ `values`](#-values)
    - [`collect_by_key`](#collect_by_key)
  - [Other Functions](#other-functions)
    - [`defined`](#defined)
    - [`length`](#length)
- [Input and Output Formats](#input-and-output-formats)
  - [JSON Input Format](#json-input-format)
    - [Optional Inputs](#optional-inputs)
    - [Specifying / Overriding Requirements and Hints](#specifying--overriding-requirements-and-hints)
  - [JSON Output Format](#json-output-format)
  - [Extended File/Directory Input/Output Format](#extended-filedirectory-inputoutput-format)
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
  version 1.2

  task hello_task {
    input {
      File infile
      String pattern
    }

    command <<<
      grep -E '~{pattern}' '~{infile}'
    >>>

    requirements {
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
      infile, pattern
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
  version 1.2
  
  import "hello.wdl"

  workflow hello_parallel {
    input {
      Array[File] files
      String pattern
    }
    
    scatter (path in files) {
      call hello.hello_task {
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
    "hello_parallel.files": ["greetings.txt", "hello.txt"]
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
  version 1.2

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
      echo ~{number * 2}
    >>>

    output {
      Int result = read_int(stdout())
    }
      
    requirements {
      container: "ubuntu:latest"
    }
  }

  workflow workflow_with_comments {
    input {
      Int number
    }

    # You can have comments anywhere in the workflow
    call task_with_comments { number }
    
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
Directory
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
hints
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
requirements
runtime 
scatter
struct
task
then
true
version
workflow
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
* ✨ A `Directory` represents a (possibly nested) directory of files.

<details>
  <summary>
  Example: primitive_literals.wdl
  
  ```wdl
  version 1.2

  task write_file_task {
    command <<<
    mkdir -p testdir
    printf "hello" > testdir/hello.txt
    >>>

    output {
      File x = "testdir/hello.txt"
      Directory d = "testdir"
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
      Directory d = write_file_task.d
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
    "primitive_literals.x": "hello.txt",
    "primitive_literals.d": "testdir/hello.txt"
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

###### Multi-line Strings

Strings that begin with `<<<` and end with `>>>` may span multiple lines.

<details>
  <summary>
  Example: multiline_strings1.wdl
  
  ```wdl
  version 1.2

  workflow multiline_strings1 {
    output {
      String s = <<<
        This is a
        multi-line string!
      >>>
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
    "multiline_strings1.s": "This is a\nmulti-line string!"
  }
  ```
  </p>
</details>

In multi-line strings, leading *whitespace* is removed according to the following rules. In the context of multi-line strings, whitespace refers to space (`\x20`) and tab characters only and is treated differently from newline characters.

1. Remove all line continuations and subsequent white space.
   * A line continuation is a backslash (`\`) immediately preceding the newline. A line continuation indicates that two consecutive lines are actually the same line (e.g. when breaking a long line for better readability).
   * If a line ends in multiple `\` then standard character escaping applies. Each pair of consecutive backslashes (`\\`) is an escaped backslash. So a line is continued only if it ends in an odd number of backslashes.
   * Removing a line continuation means removing the last `\` character, the immediately following newline, and all the whitespace preceeding the next non-whitespace character or end of line (whichever comes first).
2. Remove all whitespace following the opening `<<<`, up to and including a newline (if any).
3. Remove all whitespace preceeding the closing `>>>`, up to and including a newline (if any).
4. Use all remaining non-*blank* lines to determine the *common leading whitespace*.
   * A blank line contains zero or more whitespace characters followed by a newline.
   * Common leading whitespace is the minimum number of whitespace characters occuring before the first non-whitespace character in a non-blank line.
   * Each whitespace character is counted once regardless of whether it is a space or tab (so care should be taken when mixing whitespace characters).
5. Remove common leading whitespace from each line.

<details>
  <summary>
  Example: multiline_strings2.wdl
  
  ```wdl
  version 1.2

  workflow multiline_strings2 {
    output {
      # all of these strings evaluate to "hello  world"
      String hw0 = "hello  world"
      String hw1 = <<<hello  world>>>
      String hw2 = <<<   hello  world   >>>
      String hw3 = <<<   
          hello world>>>
      String hw4 = <<<   
          hello  world
          >>>
      String hw5 = <<<   
          hello  world
      >>>
      # The line continuation causes the newline and all whitespace preceding 'world' to be 
      # removed - to put two spaces between 'hello' and world' we need to put them before 
      # the line continuation.
      String hw6 = <<<
          hello  \
              world
      >>>

      # This string is not equivalent - the first line ends in two backslashes, which is an 
      # escaped backslash, not a line continuation. So this string evaluates to 
      # "hello \\\n  world".
      String not_equivalent = <<<
      hello \\
        world
      >>>
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
    "multiline_strings2.hw0": "hello  world"
    "multiline_strings2.hw1": "hello  world"
    "multiline_strings2.hw2": "hello  world"
    "multiline_strings2.hw3": "hello  world"
    "multiline_strings2.hw4": "hello  world"
    "multiline_strings2.hw5": "hello  world"
    "multiline_strings2.hw6": "hello  world"
    "multiline_strings2.not_equivalent": "hello \\\n  world"
  }
  ```
  </p>
</details>

Common leading whitespace is also removed from blank lines that contain whitespace characters; newlines are *not* removed from blank lines. This means blank lines may be used to ensure that a multi-line string begins/ends with a newline.

<details>
  <summary>
  Example: multiline_strings3.wdl
  
  ```wdl
  version 1.2

  workflow multiline_strings3 {
    output {
      # These strings are all equivalent. In strings B, C, and D, the middle lines are blank and 
      # so do not count towards the common leading whitespace determination.

      String multi_line_A = "\nthis is a\n\n  multi-line string\n"
      
      # This string's common leading whitespace is 0.
      String multi_line_B = <<<

      this is a
      
        multi-line string
      
      >>>

      # This string's common leading whitespace is 2. The middle blank line contains two spaces
      # that are also removed.
      String multi_line_C = <<<
      
        this is a
        
          multi-line string
      >>>
      
      # This string's common leading whitespace is 8.
      String multi_line_D = <<<

              this is a
      
                multi-line string
      >>>
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
    "multiline_strings3.multi_line_A": "\nthis is a\n\n  multi-line string\n"
    "multiline_strings3.multi_line_B": "\nthis is a\n\n  multi-line string\n"
    "multiline_strings3.multi_line_C": "\nthis is a\n\n  multi-line string\n"
    "multiline_strings3.multi_line_D": "\nthis is a\n\n  multi-line string\n"
  }
  ```
  </p>
</details>

Single- and double-quotes do not need to be escaped within a multi-line string.

<details>
  <summary>
  Example: multiline_strings4.wdl
  
  ```wdl
  version 1.2

  workflow multiline_strings4 {
    output {
      String multi_line_with_quotes = <<<
        multi-line string \
        with 'single' and "double" quotes
      >>>
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
    "multiline_strings4.multi_line_with_quotes": "multi-line string with 'single' and \"double\" quotes"
  }
  ```
  </p>
</details>

##### Files and Directories

A `File` or `Directory` declaration may have have a string value indicating a relative or absolute path on the local file system.

Within a WDL file, literal values for files may only be (relative or absolute) paths that are local to the execution environment. If the specified path does not exist, it is an error unless the declaration is optional.

```wdl
task literals_paths {
  input {
    # If the user does not overide the value of `f1`, and /foo/bar.txt
    # does not exist, it is an error.
    File f1 = "/foo/bar.txt"

    # If the user does not override the value of `f2` and /foo/bar.txt
    # does not exist, then `f2` is set to `None`.
    File? f2 = "/foo/bar.txt"
  }
}
```

An execution engine may support [other ways](#input-and-output-formats) to specify `File` and `Directory` inputs (e.g., as URIs), but prior to task execution it must [localize inputs](#task-input-localization) so that the runtime value of a `File`/`Directory` variable is a local path.

#### Optional Types and None

A type may have a `?` postfix quantifier, which means that its value is allowed to be undefined without causing an error. A declaration with an optional type can only be used in calls or functions that accept optional values.

WDL has a special value `None` whose meaning is "an undefined value". The `None` value has the (hidden) type [`Union`](#union-hidden-type), meaning `None` can be assigned to an optional declaration of any type.

An optional declaration has a default initialization of `None`, which indicates that it is undefined. An optional declaration may be initialized to any literal or expression of the correct type, including the special `None` value.

<details>
  <summary>
  Example: optionals.wdl
  
  ```wdl
  version 1.2

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
  version 1.2

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
  version 1.2
  
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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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

A `Map` is insertion-ordered, meaning the order in which elements are added to the `Map` is preserved, for example when [converting a `Map` to an array of `Pair`s](#as_pairs).

<details>
<summary>
Example: test_map_ordering.wdl

```wdl
version 1.2

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
version 1.2

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

Due to the lack of explicitness in the typing of `Object` being at odds with the goal of being able to know the type information of all WDL declarations, the use of the `Object` type and the `object` literal syntax have been deprecated. In WDL 2.0, `Object` will become a [hidden type](#hidden-and-scoped-types) that may only be instantiated by the execution engine. `Object` declarations can be replaced with use of [structs](#struct-definition).

##### Custom Types (Structs)

WDL provides the ability to define custom compound types called [structs](#struct-definition). `Struct` types are defined directly in the WDL document and are usable like any other type. A struct is defined using the `struct` keyword, followed by a unique name, followed by member declarations within braces. A struct definition contains any number of declarations of any types, including other `Struct`s.

A declaration with a custom type can be initialized with a struct literal, which begins with the `Struct` type name followed by a comma-separated list of name-value pairs in braces (`{}`), where name-value pairs are delimited by `:`. The member names in a struct literal are not quoted. A struct literal must provide values for all of the struct's non-optional members, and may provide values for any of the optional members. The members of a struct literal are validated against the struct's definition at the time of creation. Members do not need to be in any specific order. Once a struct literal is created, it is immutable like any other WDL value.

The value of a specific member of a struct value can be [accessed](#member-access) by placing a `.` followed by the member name after the identifier.

<details>
<summary>
Example: test_struct.wdl

```wdl
version 1.2

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
  "test_struct.john": {
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
version 1.2

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

* The value of each `Object`/`Map` member must be coercible to the declared type of the struct member.
* The `Object`/`Map` must at least contain values for all of the struct's non-optional members.
* Any `Object`/`Map` member that does not correspond to a member of the struct is ignored.

Note that the ability to assign values to `Struct` declarations other than struct literals is deprecated and will be removed in WDL 2.0.

#### Hidden and Scoped Types

A hidden type is one that may only be instantiated by the execution engine, and cannot be used in a declaration within a WDL file.

A scoped type is one that can only be defined by the execution engine within a specific scope. A scoped type may also be hidden.

The following sections enumerate the hidden and scoped types that are available in the current version of WDL. In WDL 2.0, `Object` will also become a hidden type.

##### `Union` (Hidden Type)

`Union` is a hidden type that is used for a value that may have any one of several concrete types. A `Union` value must always be coerced to a concrete type. The `Union` type is used in the following contexts:

* It is the type of the special [`None`](#optional-types-and-none) value.
* It is the return type of some standard library functions, such as [`read_json`](#read_json).
* It is the type of some [`requirements`](#-requirements-section) and reserved [`hints`](#-hints-section) attributes.

##### `hints`, `input`, and `output` (Scoped Types)

The [`hints`](#-hints-section) section has [three scoped types](#hints-scoped-types) that may be instantiated by the user within that scope.

##### `task` (Hidden Scoped Type)

The [`task` type](#runtime-access-to-requirements-hints-and-metadata) is a hidden type that is scoped to the `command` and `output` sections.

#### Type Conversion

WDL has some limited facilities for converting a value of one type to another type. Some of these are explicitly provided by [standard library](#standard-library) functions, while others are [implicit](#type-coercion). When converting between types, it is best to be explicit whenever possible, even if an implicit conversion is allowed.

The execution engine is also responsible for converting (or "serializing") input values when constructing commands, as well as "deserializing" command outputs. For more information, see the [Command Section](#command-section) and the more extensive Appendix on [WDL Value Serialization and Deserialization](#appendix-a-wdl-value-serialization-and-deserialization).

Note that type conversion is non-destructive - the converted value can be considered to be a new value that copies whatever properties of the original value are supported by the target type. If the original value was assigned to a variable, then that variable remains unchanged after the type conversion. For example:

```
String path = "/path/to/file"
File file = path
String new_path = "~{path}_2"  # can still use `path` here
```

##### Primitive Conversion to String 

Primitive types can always be converted to `String` using [string interpolation](#expression-placeholders-and-string-interpolation). See [Expression Placeholder Coercion](#expression-placeholder-coercion) for details.

<details>
<summary>
Example: primitive_to_string.wdl

```wdl
version 1.2

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
version 1.2

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

Attempting to use a declaration that is both of the wrong type and for which there is no coercion to the correct type results in an error.

<details>
<summary>
Example: coercion_fail.wdl

```wdl
version 1.2

workflow coercion_fail {
  Array[String] strings = ["/foo/bar"]
  Boolean is_true1 = contains(strings, "/foo/bar")
  
  File foobar = "/foo/bar"
  # returns `true` - string interpolation creates a string from `foobar`
  Boolean is_true2 = contains(strings, "~{foobar}")
  # error - `foobar` is not of type `String` and is not coercible to `String`
  contains(strings, foobar)
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

The table below lists all globally valid coercions. The "target" type is the type being coerced to (this is often called the "left-hand side" or "LHS" of the coercion) and the "source" type is the type being coerced from (the "right-hand side" or "RHS").

| Target Type      | Source Type      | Notes/Constraints                                                                                                                                |
| ---------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `File`           | `String`         |                                                                                                                                                  |
| `Directory`      | `String`         |
| `Float`          | `Int`            | May cause overflow error                                                                                                                         |
| `Y?`             | `X`              | `X` must be coercible to `Y`                                                                                                                     |
| `Array[Y]`       | `Array[X]`       | `X` must be coercible to `Y`                                                                                                                     |
| `Array[Y]`       | `Array[X]+`      | `X` must be coercible to `Y`                                                                                                                     |
| `Map[X, Z]`      | `Map[W, Y]`      | `W` must be coercible to `X` and `Y` must be coercible to `Z`                                                                                    |
| `Pair[X, Z]`     | `Pair[W, Y]`     | `W` must be coercible to `X` and `Y` must be coercible to `Z`                                                                                    |
| `Struct`         | `Map[String, Y]` | `Map` keys must match `Struct` member names, and all `Struct` members types must be coercible from `Y`                                           |
| `Map[String, Y]` | `Struct`         | All `Struct` members must be coercible to `Y`                                                                                                    |
| `Object`         | `Map[String, Y]` |                                                                                                                                                  |
| `Map[String, Y]` | `Object`         | All object values must be coercible to `Y`                                                                                                       |
| `Object`         | `Struct`         |                                                                                                                                                  |
| `Struct`         | `Object`         | `Object` keys must match `Struct` member names, and `Object` values must be coercible to `Struct` member types                                   |
| `Struct`         | `Struct`         | The two `Struct` types must have members with identical names and compatible types (see [Struct-to-Struct Coercion](#struct-to-struct-coercion)) |

The [`read_lines`](#read_lines) function presents a special case in which the `Array[String]` value it returns may be immediately coerced into other `Array[P]` values, where `P` is a primitive type. See [Appendix A](#array-serializationdeserialization-using-write_linesread_lines) for details and best practices.

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

This constraint propagates into compound types. For example, an `Array[T?]` can contain both optional and non-optional elements. This facilitates the common idiom [`select_first([expr, default])`](#select_first), where `expr` is of type `T?` and `default` is of type `T`, for converting an optional type to a non-optional type. However, an `Array[T?]` could not be passed to the [`sep`](#sep) function, which requires an `Array[T]`.

There are two exceptions where coercion from `T?` to `T` is allowed:

* [String concatenation in expression placeholders](#concatenation-of-optional-values)
* [Equality and inequality comparisons](#equality-and-inequality-comparison-of-optional-types)

###### Struct/Object Coercion from Map

`Struct`s and `Object`s can be coerced from map literals, but beware the difference between `Map` keys (expressions) and `Struct`/`Object` member names.

<details>
<summary>
Example: map_to_struct.wdl

```wdl
version 1.2

struct Words {
  Int a
  Int b
  Int c
}

workflow map_to_struct {
  String a = "beware"
  String b = "key"
  String c = "lookup"

  output {
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

###### Struct-to-Struct Coercion

Two `Struct` types are considered compatible when the following are true:

1. They have the same number of members.
2. Their members' names are identical.
3. The type of each member in the source struct is coercible to the type of the member with the same name in the target struct.

<details>
<summary>
Example: struct_to_struct.wdl

```wdl
version 1.2

struct A {
  String s
}

Struct B {
  A a_struct
  Int i
}

struct C {
  String s
}

struct D {
  C a_struct
  Int i
}

workflow struct_to_struct {
  B my_b = B {
    a_struct: A { s: 'hello' },
    i: 10
  }
  # We can coerce `my_b` from type `B` to type `D` because `B` and `D`
  # have members with the same names and compatible types. Type `A` can
  # be coerced to type `C` because they also have members with the same
  # names and compatible types.
  
  output {
    D my_d = my_b
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
  "struct_to_struct.my_d": {
    "a_struct": { 
      "s": "hello"
    },
    "i": 10
  }
}
```
</p>
</details>

###### 🗑 Limited Exceptions

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
version 1.2

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
version 1.2

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
    name="John"
  }
  
  call greet as y {
    name="Sarah"
  }

  Array[String] greetings = [x.greeting, y.greeting]
  call count_lines {
    array=greetings
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
version 1.2

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
version 1.2

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

In operations on mismatched numeric types (e.g., `Int` + `Float`), the `Int` is first is coerced to `Float`, and the result type is `Float`. This may result in loss of precision, for example if the `Int` is too large to be represented exactly by a `Float`. A `Float` can be converted to `Int` with the [`ceil`](#ceil), [`round`](#round), or [`floor`](#floor) functions.

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
| `Int`       | `**`     | `Int`     | `Int`     | Integer exponentiation                                   |
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
| `Int`       | `**`     | `Float`   | `Float`   |                                                          |
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
| `Float`     | `**`     | `Float`   | `Float`   |                                                          |
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
| `Float`     | `**`     | `Int`     | `Float`   |                                                          |
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
version 1.2

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
version 1.2

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
version 1.2

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
| 12         | Grouping              | n/a           | `(x)`        |
| 11         | Member Access         | left-to-right | `x.y`        |
| 10         | Index                 | left-to-right | `x[y]`       |
| 9          | Function Call         | left-to-right | `x(y,z,...)` |
| 8          | Logical NOT           | right-to-left | `!x`         |
|            | Unary Negation        | right-to-left | `-x`         |
| 7          | Exponentiation        | left-to-right | `x**y`       |
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
version 1.2

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
version 1.2

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

Attempting to access a non-existent member of an object, struct, or call results in an error.

<details>
<summary>
Example: illegal_access_fail.wdl

```wdl
version 1.2

import "member_access.wdl"

workflow illegal_access {
  input {
    MyStruct my
  }

  Int i = my.x  # error: field 'x' does not exist in MyStruct
  
  call foo

  output {
    String baz = foo.baz  # error: 'baz' is not an output field of task 'foo'    
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

#### Ternary operator (if-then-else)

This operator takes three arguments: a condition expression, an if-true expression, and an if-false expression. The condition is always evaluated. If the condition is `true` then the if-true value is evaluated and returned. If the condition is `false`, the if-false expression is evaluated and returned. The if-true and if-false expressions must return values of the same type, such that the value of the if-then-else is the same regardless of which side is evaluated.

<details>
<summary>
Example: ternary.wdl

```wdl
version 1.2

task mem {
  input {
    Array[String] array
  }

  Int array_length = length(array)
  # choose how much memory to use for a task
  String memory = if array_length > 100 then "2GB" else "1GB"

  command <<<
  >>>

  requirements {
    memory: memory
  }
}

workflow ternary {
  input {
    Boolean morning
  }

  call mem { array = ["x", "y", "z"] }

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
version 1.2

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
version 1.2

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

Placeholders are evaluated in multi-line strings exactly the same as in regular strings. Common leading whitespace is stripped from a multi-line string *before* placeholder expressions are evaluated.

<details>
  <summary>
  Example: multiline_string_placeholders.wdl
  
  ```wdl
  version 1.2

  workflow multiline_strings {
    output {
      String spaces = "  "
      String name = "Henry"
      String company = "Acme"
      # This string evaluates to: "  Hello Henry,\n  Welcome to Acme!"
      # The string still has spaces because the placeholders are evaluated after removing the 
      # common leading whitespace.
      String multi_line = <<<
        ~{spaces}Hello ~{name},
        ~{spaces}Welcome to ~{company}!
      >>>
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
    "multiline_string_placeholders.multi_line": "  Hello Henry,\n  Welcome to Acme!"
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

Compound types cannot be implicitly converted to `String`s. To convert an `Array` to a `String`, use the [`sep`](#sep) function: `~{sep(",", str_array)}`. See the guide on [WDL value serialization](#appendix-a-wdl-value-serialization-and-deserialization) for more details and examples.

If an expression within a placeholder evaluates to `None`, and either causes the entire placeholder to evaluate to `None` or causes an error, then the placeholder is replaced by the empty string.

<details>
<summary>
Example: placeholder_coercion.wdl

```wdl
version 1.2

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

<details>
  <summary>
  Example: placeholder_none.wdl
  
  ```wdl
  version 1.2

  workflow placeholder_none {
    output {
      String? foo = None
      # The expression in this string results in an error (calling `select_first` on an array 
      # containing no non-`None` values) and so the placeholder evaluates to the empty string and 
      # `s` evalutes to: "Foo is "
      String s = "Foo is ~{select_first([foo])}"
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
    "placeholder_none.s": "Foo is "
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
version 1.2

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
version 1.2

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

The `sep` option can be replaced with a call to the [`sep`](#sep) function:

<details>
<summary>
Example: sep_option_to_function.wdl

```wdl
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2
```

or

```wdl
#Licence header

version 1.2
```

A WDL file that does not have a `version` statement must be treated as [`draft-2`](https://github.com/openwdl/wdl/blob/main/versions/draft-2/SPEC.md).

Because patches to the WDL specification do not change any functionality, all revisions that carry the same major and minor version numbers are considered equivalent. For example, `version 1.2` is used for a WDL document that adheres to the `1.2.x` specification, regardless of the value of `x`.

## Struct Definition

A `Struct` type is a user-defined data type. Structs enable the creation of compound data types that bundle together related attributes in a more natural way than is possible using the general-purpose compound types like `Pair` or `Map`. Once defined, a `Struct` type can be used as the type of a declaration like any other data type.

`Struct` definitions are top-level WDL elements, meaning they exist at the same level as `import`, `task`, and `workflow` definitions. A struct cannot be defined within a task or workflow body.

A struct is defined using the `struct` keyword, followed by a name that is unique within the WDL document, and a body containing the member declarations. A struct member may be of any type, including compound types and even other `Struct` types. A struct member may be optional. Declarations in a struct body differ from those in a task or workflow in that struct members cannot have default initializers.

A `struct` definition may include a `meta` section with metadata about the struct, and a `parameter_meta` section with metadata about any of the struct's members. These sections have identical sematics to task and workflow [`meta` and `parameter_meta` sections](#metadata-sections). Any key in the `parameter_meta` section *must* correspond to a member of the `struct`.

<details>
<summary>
Example: person_struct_task.wdl

```wdl
version 1.2

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
  
  meta {
    description: "Encapsulates data about a person"
  }

  paramter_meta {
    name: "The person's name"
    age: "The person's age"
    income: "How much the person makes (optional)"
    assay_data: "Mapping of assay name to the file that contains the assay data"
  }
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
    file=bam_file
  }
  
  call analysis.my_analysis_task {
    size=file_size.bytes, file=bam_file
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
version 1.2

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
    person = patient
  }

  call calculate_bill {
    doctor = doctor, patient = patient
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
* A single, optional [`requirements`](#-requirements-section) section, which defines the minimum, required runtime environment conditions.
* A single, optional [`hints`](#-hints-section) section, which provides hints to the execution engine.
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

  requirements {
    # runtime requirements are specified here
  }

  hints {
    # runtime hints are specified here
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

A task's `input` section declares its input parameters. The values for declarations within the `input` section may be specified by the caller of the task. An input declaration may be initialized to a default expression to use when the caller does not supply a value. Input declarations with the optional type quantifier `?` also may be omitted by the caller even when there is no default initializer. If an input declaration has neither an optional type nor a default initializer, then it is a required input, meaning the caller must specify a value.

<details>
<summary>
Example: task_inputs_task.wdl

```wdl
version 1.2

task task_inputs {
  input {
    Int i               # a required input parameter
    String s = "hello"  # an input parameter with a default value
    File? f             # an optional input parameter
    Directory? d = "/etc"             # an optional input parameter with a default value
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
</p>
</details>

#### Task Input Localization

`File` and `Directory` inputs may require localization to the execution environment. For example, a file located on a remote web server that is provided to the execution engine as an `https://` URL must first be downloaded to the machine where the task is being executed.

- `File`s and `Directory`s are localized into the execution environment prior to evaluating any expressions. This means that references to `File` or `Directory` declarations in input declaration expressions, private declaration expressions, and the command section are always replaced with the local paths to those files/directories.
- When localizing a `File` or `Directory`, the engine may choose to place the local resource wherever it likes so long as it adheres to these rules:
  - The original file/directory name (the "basename") must be preserved even if the path to it has changed.
  - Two inputs with the same basename must be located separately, to avoid name collision.
  - Two input files that originate from the same "parent" must be localized into the same directory for task execution.
    - For local paths, "parent" means the parent directory.
    - For remote paths specified as a URI, "parent" means the entire URI up to the last '/' of the path (i.e., excluding the final component and any parameters). For example, http://foo.com/bar/a.txt and http://foo.com/bar/b.txt have the same parent (http://foo.com/bar/), so they must be localized into the same directory.
    - For remote paths specified by other means, it is up to the execution engine to determine what is meant by "parent".
  - See the [special case handling for Versioning Filesystems](#special-case-versioning-filesystem) below.
- When a WDL author uses a `File` or `Directory` input in their [Command Section](#command-section), the absolute path to the localized file/directory is substituted when that declaration is referenced.

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

Runtime engines **should** treat input `File`s and `Directory`s as read-only, e.g., by setting their permissions appropriately on the local file system, or by localizing them to a directory marked as read-only.

Note starting in WDL 2.0 engines **must** treat input `File`s and `Directory`s as read-only.

A common pattern for tasks that require multiple input files to be in the same directory is to create a new directory in the execution environment and soft-link the files into that directory.

```wdl
task two_files_one_directory {
  input {
    File bam
    File bai
  }
  String prefix = basename(bam, ".bam")
  command <<<
  mkdir inputs
  ln -s ~{bam} inputs/~{prefix}.bam
  ln -s ~{bai} inputs/~{prefix}.bam.bai
  varcall inputs/~{prefix}.bam
  >>>
}
```

##### Special Case: Versioning Filesystem

Two or more versions of a file in a versioning filesystem might have the same name and come from the same directory. In that case, the following special procedure must be used to avoid collision:
  - The first file is always placed according to the rules above.
  - Subsequent files that would otherwise overwrite this file are instead placed in a subdirectory named for the version.

For example, imagine two versions of file `fs://path/to/A.txt` are being localized (labeled version `1.0` and `1.1`). The first might be localized as `/execution_dir/path/to/A.txt`. The second must then be placed in `/execution_dir/path/to/1.1/A.txt`

#### Input Type Constraints

Recall that a type may have a quantifier:

* `?` means that the input is optional and a caller does not need to specify a value for the input.* `+` applies only to `Array` types and it represents a constraint that the `Array` value must contain one-or-more elements.

The following task has several inputs with type quantifiers:

<details>
<summary>
Example: input_type_quantifiers_task.wdl

```wdl
version 1.2

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
  
  requirements {
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

Inputs with default initializers are implicitly optional: callers may omit the input or supply `None` *whether or not* its declared type carries the optional quantifier `?`. Usually, inputs with defaults should omit the `?` from their type, except when callers need the ability to override the default with `None`.

In detail, if a caller omits an input from the call `input:` section, then the default initializer applies whether or not the input type is declared optional. But if the caller explicitly supplies `None` for the input (either literally or by passing an optional value), then the default initializer applies only if the declared type isn't optional. This table illustrates the value taken by an input `x` depending on what the caller supplies:

| input declaration:     | `Int x = 1` | `Int? x = 1` | `Int? x` | `Int x` |
| ---------------------- | ----------- | ------------ | -------- | ------- |
| call input: `x = 42`   | 42          | 42           | 42       | 42      |
| call input: `x = None` | 1           | `None`       | `None`   | *error* |
| call input: *omitted*  | 1           | 1            | `None`   | *error* |

<details>
<summary>
Example: optional_with_default.wdl

```wdl
version 1.2

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
      name = name 
    }
  }

  if (!use_salutation) {
    call say_hello as hello2 {
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
version 1.2

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
version 1.2

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

### Environment Variables

Any input to a task may be converted into an environment variable that will be accessible from within the task's
shell environment during command execution. Unlike inputs, environment variables are not interpolated in the command when
preparing the execution script, but are actually available at runtime directly from the environment. They may be accessed using
normal shell variable access semantics (i.e. `$FOO` or `${FOO}`).

In order to access an input value as an environment variable, you can add the `env` modifier preceding a declaration anywhere
within the task. This applies to declarations within the input section as well as [private declarations](#private-declarations).
An important thing to note is that while the `env` modifier makes the declaration available in the
environment, it does not change its access to normal WDL expressions within a command. That means you can refer to a declaration
annotated with `env` either through the shell semantics (`${FOO}`) or through normal WDL semantics (`~{FOO}`).

When an input is annotated with `env` it is the engine's responsibility to serialize the value appropriately into a string (see section on [Serialization of WDL values](#appendix-a-wdl-value-serialization-and-deserialization))
that will then be set as an environment variable. Engines may impose limits on the total length a single environment variable is allowed to occupy as well as the number of environment variables that are allowed to be passed into a single task.
If such limitations exist, it is the engine's responsibility to provide clear documentation outlining what they are for the user. 

The environment variable should be evaluated by the engine prior to injecting it into the execution environment. if the task is run in a container the env var is "injected" into the container and not applied to the shell on the host that runs the container.


<details>
<summary>

```wdl
version 1.2

task test  {
  input {
    env String greeting
  }
  command <<<
    echo $foo
  >>>
  output {
    String out= read_string(stdout())
  }
}

workflow environment_variable_should_echo {
  input {
    String greeting 
  }
  
  call test {
    input: greeting = greeting
  }
  
  output {
    String out = test.out
  }
```
</summary>
<p>
Example input:

```json
{
  "environment_variable_should_echo.greeting": "hello"
}
```

Example output:

```json
{
  "environment_variable_should_echo.out": "hello"
}
```

Test config:

```json
{
  "fail": false
}
```

</p>
</details>

#### String Escaping and Injection Prevention
Environment variables provide a mechanism to pass a value to a command which would otherwise be considered unsafe.

For example, in some cloud environments, any code run within a task is given the same identity and permissions as the node that the task is running
on, without needing to perform any additional authentication mechanisms. A bad actor could construct a string to pass into a task
which then performs a privileged operation as the node's identity. It's important to note that this can happen **even if**
only validated workflows are allowed by the execution engine (Which is possibly the case when dealing with restricted data).


Imagine the task looks something like the following:

```wdl
task some_task {
  input {
    String thing_to_do
  }
  
  command <<<
   echo ${thing_to_do}
  >>> 
```

You could then construct an input that downloads a file, and attempts to gain access to anything that the said node has access to.

```json
{
  "some_workflow.some_task":"\nwget bad-script.sh && eval bad-script.sh"
}
```
While the example above illustrates how a user of workflow may submit a bad value, there could possibly be many other sources of injection attacks. As workflows become dependent on other community generated workflows and files, it becomes quite easy to generate a source of an attack to perform some nefarious purpose.

Using environment variables mitigates this problem almost entirely. When a value is declared with the `env` modifier, it becomes the execution engine's responsibility to escape the string thus preventing any sort of interpolation. Functionally, using an environment variable is the same as first escaping the string of any special characters and then wrapping it single quotes.

```
single_quote(escape(${variable}))
```



### Command Section

The `command` section is the only required task section. It defines the command template that is evaluated to produce a Bash script that is executed within the task's container. Specifically, the commands are executed after all of the inputs are staged and before the outputs are evaluated. There may be any number of commands within a command section.

There are two different syntaxes that can be used to define the command section:

```wdl
# HEREDOC style - this way is preferred
command <<< ... >>>

# older style - may be preferable in some cases
command { ... }
```

The command template is evaluated *after* all of the inputs are staged and before the outputs are evaluated. The command template is evaluated similarly to [multi-line strings](#multi-line-strings):

1. Remove all whitespace following the opening `<<<`, up to and including a newline (if any).
2. Remove all whitespace preceeding the closing `>>>`, up to and including a newline (if any).
3. Use all remaining non-*blank* lines to determine the *common leading whitespace*.
4. Remove common leading whitespace from each line.
5. Evaluate placeholder expressions.

Notice that there is one major difference between the evaluation of multi-line strings vs the command template: line continuations are removed in the former but left as-is in the latter. This also means that continued lines are considered when determining common leading whitespace, and that common leading whitespace is removed from continued lines as well.

```wdl
String s = <<<
  This string has \
  no newlines
>>>

command <<<
  echo "~{s}"
  echo "This command has line continuations \
    that still appear in the Bash script \
    after evaluation"
>>>
```

When the above command template is evaluated the resulting Bash script is:

```sh
echo "This string has no newlines"
echo "This command has line continuations \
  that still appear in the Bash script \
  after evaluation"
```

For another example, consider a task that calls the `python` interpreter with an in-line Python script:

```wdl
task heredoc {
  input {
    File infile
  }

  command <<<
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

Given an `infile` value of `/path/to/file`, the execution engine produces the following Bash script, which has removed the 4 spaces that were common to the beginning of each line:

```sh
python <<CODE
  with open("/path/to/file") as fp:
    for line in fp:
      if not line.startswith('#'):
        print(line.strip())
CODE
```

Each whitespace character is counted once regardless of whether it is a space or tab, so care should be taken when mixing whitespace characters. For example, if a command block has two lines, and the first line begins with `<space><space><space><space>`, and the second line begins with `<tab>` then only one whitespace character is removed from each line.

The characters that must be escaped within a command section are different from those that must be escaped in regular strings:

* Unescaped newlines (`\n`) are allowed.
* An unescaped backslash (`\`) may appear as the last character on a line - this is treated as a line continuation.
* In a HEREDOC-style command section, if there are exactly three consecutive right-angle brackets (`>>>`), then at least one of them must be escaped, e.g. `\>>>`.
* In the older-style command section, any right brace (`}`) that is not part of an expression placeholder must be escaped.

#### Expression Placeholders

The command "template" can be thought of as a single string expression, which (like all string expressions) may contain placeholders.

There are two different syntaxes that can be used to define command expression placeholders, depending on which style of command section definition is used:

| Command Definition Style | Placeholder Style          |
| ------------------------ | -------------------------- |
| `command <<< >>>`        | `~{}` only                 |
| `command { ... }`        | `~{}` (preferred) or `${}` |

Note that the restriction on using `${}` only applies to the HEREDOC-style command section - it may be used interchangeably with `~{}` in string expressions including multi-line strings.

Any valid WDL expression may be used within a placeholder. For example, a command might reference an input to the task. The expression can also be more complex, such as a function call.

<details>
<summary>
Example: test_placeholders_task.wdl

```wdl
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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

  requirements {
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
  "python_strip.lines": ["A", "B", "C"]
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

If the user mixes tabs and spaces, the behavior is undefined. The execution engine should, at a minimum, issue a warning and leave the whitespace unmodified, though it may choose to raise an exception or to substitute e.g. 4 spaces per tab.

### Task Outputs

The `output` section contains declarations that are exposed as outputs of the task after the successful execution of the instantiated command. An output declaration must be initialized, and its value is evaluated only after the task's command completes successfully, enabling any files generated by the command to be used to determine its value.

<details>
<summary>
Example: outputs_task.wdl

```wdl
version 1.2

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

#### File, Directory, and Optional Outputs

`File` and `Directory` outputs are represented as path strings.

A common pattern is to use a placeholder in a string expression to construct a file name as a function of the task input. For example:

<details>
<summary>
Example: file_output_task.wdl

```wdl
version 1.2

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

In the preceding example, if `prefix` were specified as `"foobar"`, then `"~{prefix}.out"` would be evaluated to `"foobar.out"`.

Another common pattern is to use the [`glob`](#glob) function to define outputs that might contain zero, one, or many files.

<details>
<summary>
Example: glob_task.wdl

```wdl
version 1.2

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
version 1.2

task relative_and_absolute {
  command <<<
  mkdir -p my/path/to
  printf "something" > my/path/to/something.txt
  >>>

  output {
    File something = read_string("my/path/to/something.txt")
    File bashrc = "/root/.bashrc"
  }

  requirements {
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

All `File` and `Directory` outputs are required to exist, otherwise the task will fail. However, an output may be declared as optional (e.g. `File?`, `Directory?`, or `Array[File?]`), in which case the value will be undefined if the file does not exist.

<details>
<summary>
Example: optional_output_task.wdl

```wdl
version 1.2

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

The execution engine may need to "de-localize" `File` and `Directory` outputs. For example, if the WDL is executed on a cloud instance, then the outputs must be copied to cloud storage after execution completes successfully.

When a `File` or `Directory` is de-localized, its name and contents (including subdirectories) are preserved, but not necessarily its local path. Any hard- or soft-links shall be resolved into regular files/directories.

For example, if a task produces the following `Directory` output:

```txt
dir/
 - a           # a file, 10 MB
 - b -> a      # a softlink to 'a'
```

Then, after de-localization, it would be:

```txt
dir/
 - a           # a file, 10 MB
 - b           # another file, 10 MB
```

If this were then passed to the `Directory` input of another task, it would contain two independent files, `dir/a` and `dir/b`, with identical contents.

WDL does not have any built-in way to specify that an output `Directory` should only contain a subset of files in the local directory, so a common pattern is to create an output directory with the desired structure and soft-link the desired output files into that directory.

```wdl
task output_subset {
  command <<<
  for i in 1..10; do
    touch file${i}
  done
  # we only want the first three files in the output directory
  mkdir -p outdir/subdir
  ln -s file1 outdir
  ln -s file2 outdir
  ln -s file3 outdir/subdir
  >>>
  
  output {
    Directory outdir = "outdir"
  }
}
```

### Evaluation of Task Declarations

All non-output declarations (i.e., input and private declarations) must be evaluated prior to evaluating the command section.

Input and private declarations may appear in any order within their respective sections and they may reference each other so long as there are no circular references. Input and private declarations may *not* reference declarations in the output section.

Declarations in the output section may reference any input and private declarations, and may also reference other output declarations.

### ✨ Requirements Section

The `requirements` section defines a set of key/value pairs that represent the minimum requirements needed to run a task and the conditions under which a task should be interpreted as a failure or success. The `requirements` section is limited to the attributes defined in this specification. Arbitrary key/value pairs are not allowed in the `requirements` section, and must instead be placed in the [`hints`](#-hints-section) section.

During execution of a task, all resource requirements within the `requirements` section must be enforced by the engine. If the engine is not able to provision the requested resources, then the task immediately fails. 

All attributes of the `requirements` section have well-defined meanings and default values. Default values for the optional attributes are directly defined by the WDL specification to encourage portability of workflows and tasks; execution engines should not provide additional mechanisms to set default values for when no requirements are defined.

The value of a `requirements` attribute may be any expression that evaluates to the expected type - and, in some cases, matches the accepted format - for that attribute. Expressions in the `requirements` section may reference input and private declarations.

<details>
<summary>
Example: dynamic_container_task.wdl

```wdl
version 1.2

task dynamic_container {
  input {
    String ubuntu_version = "latest"
  }

  command <<<
    cat /etc/*-release | grep DISTRIB_CODENAME | cut -f 2 -d '='
  >>>
  
  output {
    String is_true = ubuntu_version == read_string(stdout())
  }

  requirements {
    container: "ubuntu:~{ubuntu_version}"
  }
}
```
</summary>
<p>
Example input:

```json
{
  "dynamic_container.ubuntu_version": "focal"
}
```

Example output:

```json
{
  "dynamic_container.is_true": true
}
```
</p>
</details>

#### Units of Storage

Several of the `requirements` attributes (and some [Standard Library](#standard-library) functions) accept a string value with an optional unit suffix, using one of the valid [SI or IEC abbreviations](https://en.wikipedia.org/wiki/Binary_prefix). At a minimum, execution engines must support the following suffices in a case-insensitive manner:

* B (bytes)
* Decimal: KB, MB, GB, TB
* Binary: KiB, MiB, GiB, TiB

Optional whitespace is allowed between the number/expression and the suffix. For example: `6.2 GB`, `5MB`, `"~{ram}GiB"`.

The decimal and binary units may be shortened by omitting the trailing "B". For example, "K" and "KB" are both interpreted as "kilobytes".

#### Requirements attributes

The following attributes must be supported by the execution engine. The value for each of these attributes must be defined - if it is not specified by the user, then it must be set to the specified default value.

##### `container`

* Accepted types:
    * `"*"`: This special value indicates that the runtime engine may use any POSIX-compliant operating environment it wishes to execute the task, whether that be a container or directly in the host environment.
    * `String`: A single container URI.
    * `Array[String]`: An array of container URIs.
* Default value: `"*"`
* Alias: `docker`

The `container` attribute accepts a URI string that describes a container resource the execution engine can use when executing the task.

It is strongly suggested to specify a `container` for every task. If `container` is not specified, or is specified with the special `"*"` value, the execution behavior is determined by the execution engine. A task that depends on the engine to determine the execution environment should be careful to only use built-in Bash operations and tools specified as mandatory by the [POSIX standard](https://unix.stackexchange.com/questions/228888/what-are-the-posix-mandatory-utilities).

The format of a container URI is `protocol://location`, where `protocol` is one of the protocols supported by the execution engine. Execution engines must, at a minimum, support the `docker` protocol. If only `location` is specified, the protocol is assumed to be `docker`. An execution engine should ignore any URI with a protocol it does not support.

A container location uses the syntax defined by the container repository. For example, the URI `ubuntu:latest` refers to a Docker image hosted on `DockerHub`, while the URI `quay.io/bitnami/python` refers to an image in a `quay.io` repository. To promote reproducibility, it is recommended to use the most specific possible URI to refer to a container; e.g. for Docker, using the [digest](https://docs.docker.com/engine/reference/commandline/image_ls/#digests) or a specific version tag rather than `latest`.

The `container` attribute also accepts an unordered array of URI strings. All the URIs must resolve to containers that are equivalent. In other words, when given the same inputs the task should produce the same outputs regardless of which of the containers is used to execute the task. It is the responsibility of the execution engine to specify the container protocols and locations it supports, and to determine which container is the "best" one to use at runtime. Defining multiple images enables greater portability across a broad range of execution environments.

If the value is a `String` or `Array[String]` and none of the specified containers can be sucessfully resolved by the exeution engine, the task fails with an error.

<details>
<summary>
Example: test_containers.wdl

```wdl
version 1.2

task single_image_task {
  command <<< printf "hello" >>>

  output {
    String greeting = read_string(stdout())
  }

  requirements {
    container: "ubuntu:latest"
  }
}

task multi_image_task {
  command <<< printf "hello" >>>

  output {
    String greeting = read_string(stdout())
  }

  requirements {
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

The execution engine must cause the task to fail immediately if it is not able to resolve at least one of the URIs to a runnable container.

🗑 `docker` is supported as an alias for `container` with the exact same semantics. Exactly one of the `container` or `docker` attributes is required. The `docker` alias is deprecated and will be removed in WDL 2.0.

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
version 1.2

task test_cpu {
  command <<<
  cat /proc/cpuinfo | grep processor | wc -l
  >>>

  output {
    Boolean at_least_two_cpu = read_int(stdout()) >= 2
  }

  requirements {
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
version 1.2

task test_memory {
  command <<<
  free --bytes -t | tail -1 | sed -E 's/\s+/\t/g' | cut -f 2
  >>>

  output {
    Boolean at_least_two_gb = read_int(stdout()) >= (2 * 1024 * 1024 * 1024)
  }

  requirements {
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

##### Hardware Accelerators (`gpu` and ✨ `fpga`)

* Accepted type: `Boolean`
* Default value: `false`

The `gpu` and `fpga` attributes indicate to the execution engine whether a task requires a GPU and/or FPGA accelerator to run to completion. The execution engine must guarantee that at least one of each of the request types of accelerators is available or immediately fail the task prior to instantiating the command.

The [`gpu` and `fpga` hints](#-gpu-and--fpga) can be used to request specific attributes for the provisioned accelerators (e.g., quantity, model, driver version).

<details>
<summary>
Example: test_gpu_task.wdl

```wdl
version 1.2

task test_gpu {
  command <<<
  lspci -nn | grep ' \[03..\]: ' | wc -l
  >>>

  output {
    Boolean at_least_one_gpu = read_int(stdout()) >= 1
  }
  
  requirements {
    container: "archlinux:latest"
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
        * `"<size>"`: Amount of disk space to request, in `GiB`.
        * `"<size> <units>"`: Amount of disk space to request, in the given units.
        * `"<mount-point> <size>"`: A mount point and the amount of disk space to request, in `GiB`.
        * `"<mount-point> <size> <units>"`: A mount point and the amount of disk space to request, in the given units.
    * `Array[String]` - An array of disk specifications.
* Default value: `1 GiB`

The `disks` attribute provides a way to request one or more persistent volumes, each of which has a minimum size and is mounted at a specific location. When the `disks` attribute is provided, the execution engine must guarantee the requested resources are available or immediately fail the task prior to instantiating the command.

If a mount point is specified, then it must be an absolute path to a location in the host environment. If the mount point is omitted, it is assumed to be a persistent volume mounted at the root of the execution directory within a task.

The execution engine is free to provision any class(es) of persistent volume it has available (e.g., SSD or HDD). The [`disks` hint](#-disks) hint can be used to request specific attributes for the provisioned disks.

<details>
<summary>
Example: one_mount_point_task.wdl

```wdl
version 1.2

task one_mount_point {
  command <<<
    findmnt -bno size /mnt/outputs
  >>>
  
  output {
    Boolean at_least_ten_gb = read_int(stdout()) >= (10 * 1024 * 1024 * 1024)
  }

  requirements {
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
version 1.2

task multi_mount_points {
  command <<<
    findmnt -bno size /
  >>>
  
  output {
    Boolean at_least_two_gb = read_int(stdout()) >= (2 * 1024 * 1024 * 1024)
  }

  requirements {
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

##### `max_retries`

* Accepted type: `Int`
* Default value: `0`
* Alias: `maxRetries`

The `max_retries` attribute specifies the maximum number of times a task should be retried in the event of failure. The execution engine must retry the task at least once and up to (but not exceeding) the specified number of attempts.

The execution engine may choose to define an upper bound (>= 1) on the number of retry attempts that it permits.

A value of `0` means that the task as not retryable, and therefore any failure in the task should never result in a retry by the execution engine, and the final status of the task should remain the same.

```wdl
task max_retries_test {
  #.....
  requirements {
    max_retries: 4
  }
}
```

##### `return_codes`

* Accepted types:
    * `"*"`: This special value indicates that ALL returnCodes should be considered a success.
    * `Int`: Only the specified return code should be considered a success.
    * `Array[Int]`: Any of the return codes specified in the array should be considered a success.
* Default value: `0`
* Alias: `returnCodes`

The `return_codes` attribute specifies the return code, or set of return codes, that indicates a successful execution of a task. If the task exits with one of the specified return codes, it must be considered successful if possible (i.e., assuming all output expressions are evaluated successfully). 

<details>
<summary>
Example: single_return_code_task.wdl

```wdl
version 1.2

task single_return_code {
  command <<<
  exit 1
  >>>

  requirements {
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
version 1.2

task multi_return_code {
  command <<<
  exit 42
  >>>

  requirements {
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
version 1.2

task multi_return_code {
  command <<<
  exit 42
  >>>

  requirements {
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

### ✨ Hints Section

The `hints` section is optional and may contain any number of attributes (key/value pairs) that provide hints to the execution engine. A hint provides additional context that the execution engine can use to optimize the execution of the task. The execution engine may also ignore any hint for any reason. A task execution never fails due to the inability of the execution engine to recognize or satisfy a hint.

#### Hints-scoped types

There are three [scoped types](#hidden-and-scoped-types) that must be declared by the execution engine within the `hints` section. These types are intentionally given names that are already reserved keywords so that they don't conflict with any user-defined types.

The `hints` type is similar to `Object` in that it can contain arbitrary key-value pairs. However, the members of a `hints` object must have the same semantics as the `hints` section itself (i.e., any [reserved hints](#reserved-task-hints) must have the same types and allowed values), and the `hints` type cannot be nested (i.e., a member of a `hints` object may not have a `hints` type value). The `hints` type is primarily intended to be used to define the [`inputs`](#inputs), [`outputs`](#outputs), and [compute environment](#compute-environments) attributes.

The `input` and `output` types are similar to Structs whose member names are identical to the names of the enclosing task's input and output variables, respectively, and whose member values are all of type `hints`. However, unlike Structs, the keys of `input` and `output` literals may use dotted notation to refer to nested members of input and output Structs. See [`inputs`](#inputs) and [`outputs`](#outputs) for examples.

#### Reserved Task Hints

The following hints are reserved. An implementation is not required to support these attributes, but if it does support a reserved attribute it must enforce the semantics and allowed values defined below. The purpose of reserving these hints is to encourage interoperability of tasks and workflows between different execution engines.

<details>
<summary>
Example: test_hints_task.wdl

```wdl
version 1.2

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

  requirements {
    container: "ubuntu:latest"
  }

  hints {
    max_memory: "36 GB"
    max_cpu: 24
    short_task: true
    localization_optional: false
    inputs: input {
      foo: hints { 
        localization_optional: true
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

##### `max_cpu`

* Accepted types:
    * `Int`
    * `Float`
* Alias: `maxCpu`

A hint to the execution engine that the task expects to use no more than the specified number of CPUs. The value of this hint has the same specification as [`requirements.cpu`](#cpu).

##### `max_memory`

* Accepted types:
    * `Int`: Bytes of RAM.
    * `String`: A decimal value with, optionally with a unit suffix.
* Alias: `maxMemory`

A hint to the execution engine that the task expects to use no more than the specified amount of memory. The value of this hint has the same specification as [`requirements.memory`](#memory).

##### ✨ `disks`

* Accepted types:
    * `String`: Disk specification.
    * `Map[String, String]`: Map of mount point to disk specification.

A hint to the execution engine to mount [disks](#disks) with specific attributes. The value of this hint can be a `String` with a specification that applies to all mount points, or a `Map` with the key being the mount point and the value being a `String` with the specification for that mount point.

Volume specifications are left intentionally vague as they are primarily intented to be used in the context of a specific [compute environment](#compute-environments). The values "HDD" and "SSD" should be recognized to indicate that a specific class of hardware is being requested.

##### ✨ `gpu` and ✨ `fpga`

* Accepted types:
    * `Int`: Minimum number of accelerators being requested.
    * `String`: Specification for accelerator(s) being requested, e.g., manufacturer or model name.

A hint to the execution engine to provision [hardware accelerators](#hardware-accelerators-gpu-and--fpga) with specific attributes. Accelerator specifications are left intentionally vague as they are primarily intended to be used in the context of a specific [compute environment](#compute-environments).

##### `short_task`

* Accepted types: `Boolean`
* Default value: `false`

A hint to the execution engine about the expected duration of this task. The value of this hint is a `Boolean` for which `true` indicates that that this task is not expected to take long to execute, which the execution engine can interpret as permission to optimize the execution of the task.

For example, the engine may batch together multiple `short_task`s, or it may use the cost-optimized instance types that many cloud vendors provide, e.g., `preemptible` instances on `GCP` and `spot` instances on `AWS`.

##### `localization_optional`

* Accepted types: `Boolean`
* Default value: `false`
* Alias: `localizationOptional`

A hint to the execution engine about whether the `File` inputs for this task need to be localized prior to executing the task. The value of this hint is a `Boolean` for which `true` indicates that the contents of the `File` inputs may be streamed on demand.

For example, a task that processes its input file once in linear fashion could have that input streamed (e.g., using a `fifo`) rather than requiring the input file to be fully localized prior to execution.

##### `inputs`

* Accepted types: [`input`](#hints-scoped-types)

Provides input-specific hints. Each key must refer to a parameter defined in the task's [`input`](#task-inputs) section. A key may also used dotted notation to refer to a specific member of a struct input.

<details>
<summary>
Example: input_hint_task.wdl

```wdl
version 1.2

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

  hints {
    inputs: input {
      person.name: hints {
        min_length: 3
      },
      person.cv: hints {
        localization_optional: true
      }
    }
    outputs: output {
      experience: hints {
        max_length: 5
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

* `inputs.<key>.localization_optional`: Indicates that a specific `File` input does not need to be localized prior to executing this task. This attribute has the same semantics as the task-level [localization_optional](#localization_optional) hint.

##### `outputs`

* Accepted types: `output`

Provides output-specific hints. Each key must refer to a parameter defined in the task's [`output`](#task-outputs) section. A key may also use dotted notation to refer to a specific member of a struct output.

#### Compute Environments

The `hints` section should be used to provide hints that are specific to different compute environments such as HPC systems or cloud platforms. Attributes for a compute environment should be specified in a `hints` value, in which any of the [reserved hints](#reserved-task-hints) are allowed to override the values specified at the task level (if any), and other attributes are platform-specific.

```wdl
task foo {
  ...

  requirements {
    gpu: true
  }

  hints {
    aws: hints {
      instance_type: "p5.48xlarge"
    }
    gcp: hints {
      gpu: 2
    }
    azure: hints {
      ...
    }
    alibaba: hints {
      ...
    }
  }
}
```

#### Conventions and Best Practices

To encourage interoperable workflows, WDL authors and execution engine implementors should view hints strictly as runtime optimizations. Hints must not be interpreted as requirements. Following this principle will ensure that a workflow is runnable on all platforms (assuming the `requirements` section has the required attributes) regardless of whether it contains any additional hints.

Please observe the following guidelines when using hints:

* A hint must never be required for successful task execution.
* Before adding a new hint, ask yourself "do I really need another hint, or is there a better way to specify the behavior I require?".
* Avoid unnecessary complexity. By allowing any arbitrary keys and compound values, it is possible for the `hints` section to become quite complex. Use the simplest value possible to achieve the desired outcome.
* Sharing is caring. Users tend to look for similar behavior between different execution engines. It is strongly encouraged that implementers of execution engines agree on common names and accepted values for hints that describe common usage patterns. [Compute environments](#compute-environments) are a good example of hints that have conventions attached to them. 

### 🗑 Runtime Section

The `runtime` section is essentially the same as the [`requirements`](#-requirements-section) section, with the only difference being that arbitrary attributes *are* allowed in the `runtime` section. All attributes defined in the `requirements` section have the same semantics when used in the `runtime` section and are considered as reserved.

The `runtime` section is mutually exclusive with `requirements` and `hints`, i.e., if you use `runtime` in a task, you cannot also use `requirements` or `hints` in that task.

The `runtime` section is deprecated and will be removed in WDL 2.0.

### Metadata Sections

There are two optional sections that can be used to store metadata with the task: `meta` and `parameter_meta`. These sections are intended to contain metadata that is only of interest to human readers. The engine can ignore these sections with no loss of correctness. The extra information can be used, for example, to generate a user interface or documentation.

#### Meta Values

The metadata sections can contain arbitrary key/value pairs. However, the values allowed in these sections ("meta values") are different than in other sections:

* Only string, numeric, and boolean primitives are allowed.
* Only array and object compound values are allowed.
* The special value `null` is allowed for undefined attributes.
* Expressions are not allowed.

A meta object is similar to a struct literal, except:

* A `Struct` type name is not required.
* Its values must conform to the same metadata rules defined above.

Note that, unlike the WDL `Object` type, metadata objects are not deprecated and will continue to be supported in future versions.

<details>
<summary>
Example: test_meta_values.wdl

```wdl
version 1.2

workflow test_meta_values {
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

#### Task Metadata Section

This section contains task-level metadata. For example: author and contact email.

#### Parameter Metadata Section

This section contains metadata specific to input and output parameters. Any key in this section *must* correspond to a task input or output.

<details>
<summary>
Example: ex_paramter_meta_task.wdl

```wdl
version 1.2

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

  requirements {
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

### Runtime Access to Requirements, Hints, and Metadata

The `requirements` and `hints` sections comprise resource requests to the execution engine. But these requests can be [specified or overridden at runtime](#specifying--overriding-requirements-and-hints), and the execution engine has some latitude in whether and how it fulfills them. Thus, the workflow developer may wish to know exactly what resources are available at runtime, such as:

* What are the actual resource allocations. For example, a task may request at least `8 GiB` of memory but may be able to use more memory if it is available.
* The task metadata, to avoid duplication. For example, the task may wish to write log messages with the task's name and description without having to duplicate the information in the task's `meta` section.
* The runtime engine may also choose to provide additional information at runtime.

This information is provided by the `task` variable, which is implicitly defined by the execution engine. The type of `task` is a [scoped type](#hidden-and-scoped-types) with the following members:

* `name`: The task name.
* `id`: A `String` with the unique ID of the task. The execution engine may choose the format for this ID, but it is suggested to include at least the following information:
    * The task name
    * The task alias, if it differs from the task name
    * The index of the task instance, if it is within a scatter statement
* `container`: The URI `String` of the container in which the task is executing, or `None` if the task is being executed in the host environment. 
* `cpu`: The allocated number of cpus as a `Float`. Must be greater than `0`.
* `memory`: The allocated memory in bytes as an `Int`. Must be greater than `0`.
* `gpu`: An `Array[String]` with one specification per allocated GPU. The specification is execution engine-specific. If no GPUs were allocated, then the value must be an empty array.
* `fpga`: An `Array[String]` with one specification per allocated FPGA. The specification is execution engine-specific. If no FPGAs were allocated, then the value must be an empty array.
* `disks`: A `Map[String, Int]` with one entry for each disk mount point. The key is the mount point and the value is the initial amount of disk space allocated, in bytes. The execution engine must, at a minimum, provide one entry for each disk mount point requested, but may provide more. The amount of disk space available for a given mount point may increase during the lifetime of the task (e.g., autoscaling volumes provided by some cloud services).
* `attempt`: The current task attempt. The value must be `0` the first time the task is executed, and incremented by `1` each time the task is retried (if any).
* `end_time`: An `Int?` whose value is the time by which the task must be completed, as a [Unix time stamp](https://en.wikipedia.org/wiki/Unix_time). A value of `0` means that the execution engine does not impose a time limit. A value of `None` means that the execution engine cannot determine whether the runtime of the task is limited. A positive value is a guarantee that the task will be preempted at the specified time, but is *not* a guarantee that the task won't be preempted earlier.
* `return_code`: An `Int?` whose value is initially `None` and is set to the value of the `command`'s return code. The value is only guaranteed to be defined in the `output` section.
* `meta`: An `Object` containing a copy of the task's `meta` section, or the empty `Object` if there is no `meta` section or if it is empty.
* `parameter_meta`: An `Object` containing a copy of the task's `parameter_meta` section, or the empty `Object` if there is no `parameter_meta` section or if it is empty.
* `ext`: An `Object` containing execution engine-specific attributes, or the empty `Object` if there aren't any. Members of `ext` should be considered optional. It is recommended to only access a member of `ext` using [string interpolation](#expression-placeholders-and-string-interpolation) to avoid an error if it is not defined.

If the runtime engine is not able to provide the actual value of a requirement, then it must provide the requested value instead, or the default value if no specific value was requested.

<details>
<summary>
Example: test_runtime_info_task.wdl

```wdl
version 1.2

task test_runtime_info_task {
  meta {
    description: "Task that shows how to use the implicit 'task' declaration"
  }

  command <<<
  echo "Task name: ~{task.name}"
  echo "Task description: ~{task.meta.description}"
  echo "Task container: ~{task.container}"
  echo "Available cpus: ~{task.cpu}"
  echo "Available memory: ~{task.memory / (1024 * 1024 * 1024)} GiB"
  exit 1
  >>>
  
  output {
    Boolean at_least_two_gb = task.memory >= (2 * 1024 * 1024 * 1024)
    Int return_code = task.return_code
  }
  
  requirements {
    container: ["ubuntu:latest", "quay.io/ubuntu:focal"]
    memory: "2 GiB"
    return_codes: [0, 1]
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
  "test_runtime_info_task.at_least_two_gb": true,
  "test_runtime_info_task.return_code": 1
}
```

Test config:

```json
{
  "dependencies": ["cpu", "memory"]
}
```
</p>
</details>

If a task is using the deprecated [`runtime`](#-runtime-section) section rather than `requirements` and `hints`, then the runtime values of the reserved `runtime` attributes (i.e., the ones that appear in the `requirements` section) are populated in the `requirements` member.

### Advanced Task Examples

#### Example 1: HISAT2

<details>
<summary>
Example: hisat2_task.wdl

```wdl
version 1.2

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
  
  requirements {
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
version 1.2

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
  
  requirements {
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
  call target { ... }
  scatter (i in collection) { ... }
  if (condition) { ... }

  output {
    # workflow outputs are declared here
  }

  hints {
    # workflow hints are declared here
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

### Evaluation of Workflow Elements

As with tasks, declarations can appear in the body of a workflow in any order. Expressions in workflows can reference the outputs of calls, including in input declarations. For example:

<details>
<summary>
Example: input_ref_call.wdl

```wdl
version 1.2

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

  call double as d1 { int_in = x }
  call double as d2 { int_in = y }

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
version 1.2

import "input_ref_call.wdl" as ns1

workflow call_imported_task {
  input {
    Int x
    Int y = d1.out
  }

  call ns1.double as d1 { int_in = x }
  call ns1.double as d2 { int_in = y }

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
version 1.2

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
  
  requirements {
    container: "ubuntu:latest"
  }
}

workflow main {
  Array[String] arr = ["a", "b", "c"]

  call echo
  call echo as echo2
  call other_wf.foobar { infile = echo2.results }
  call other_wf.other { b = true, f = echo2.results }
  call other_wf.other as other2 { b = false }
  
  scatter(x in arr) {
    call echo as scattered_echo {
      msg = x
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
version 1.2

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

  requirements {
    container: "ubuntu:latest"
  }
}

workflow other {
  input {
    Boolean b = false
    File? f
  }

  if (b && defined(f)) {
    call foobar { infile = select_first([f]) }
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

\* Task inputs are accessible to be set by the caller of `main` if the workflow is called with [`allow_nested_inputs: true`](#allow_nested_inputs) in its `hints` section.

### Workflow Inputs

The workflow and [task `input` sections](#task-inputs) have identical semantics.

### Workflow Outputs

The workflow and [task `output` sections](#task-outputs) have identical semantics.

By default, if the `output {...}` section is omitted from a top-level workflow, then the workflow has no outputs. However, the execution engine may choose allow the user to specify that when the top-level output section is omitted, all outputs from all calls (including nested calls) should be returned.

If the `output {...}` section is omitted from a workflow that is called as a subworkflow, then that call must not have outputs. Formally defined outputs of subworkflows are required for the following reasons:

- To present the same interface when calling subworkflows as when calling tasks.
- To make it easy for callers of subworkflows to find out exactly what outputs the call is creating.
- In the case of nested subworkflows, to give the outputs at the top level a simple fixed name rather than a long qualified name like `a.b.c.d.out` (which is liable to change if the underlying implementation of `c` changes, for example).

### Workflow Hints

The `hints` section is optional and may contain any number of attributes (key/value pairs) that provide hints to the execution engine. Some workflow hint keys are reserved and have well-defined values.

The execution engine may ignore any unsupported hint. A workflow execution never fails due to the inability of the execution engine to recognize or satisfy a hint.

Unlike [task hints](#-hints-section), workflow hints must have literal values; expressions are not allowed.

#### Reserved Workflow Hints

The following hints are reserved. An implementation is not required to support these attributes, but if it does support a reserved attribute it must enforce the semantics and allowed values defined below. The purpose of reserving these hints is to encourage interoperability of tasks and workflows between different execution engines.

##### `allow_nested_inputs`

* Allowed type: `Boolean`
* Alias: `allowNestedInputs`

When running a workflow, the user typically is only allowed to specify values for the inputs defined in the top-level workflow's `input` section. However, setting the `allow_nested_inputs` hint to `true` specifies that the execution engine is allowed to let the user set the value of some call inputs at runtime.

A call input value is eligible to be set at runtime if it corresponds to a subworkflow or task input that has a default value *and* its value is not set explicitly in the call's `input` section. The default value is used for an eligible call input when `allow_nested_inputs` is set to `false`, when the user does not specify a value for the input at runtime, or when the execution engine does not suppport `allow_nested_inputs`. 

The execution engine may refuse to execute a workflow when `allow_nested_inputs` is set to `false` and the user attempts to specify a value for a nested input, but if it does execute the workflow and ignore the user-specified value then it should show a warning.

<details>
<summary>
Example: test_allow_nested_inputs.wdl

```wdl
version 1.2

task nested {
  input {
    String greeting
    String name = "Joe"
  }

  command <<<
  echo "~{greeting} ~{name}"
  >>>

  output {
    String greeting = read_string(stdout())
  }
}

workflow test_allow_nested_inputs {
  call nested {
    greeting = "Hello"
  }

  output {
    String greeting = nested.greeting
  }

  hints {
    allow_nested_inputs: true
  }
}
```
</summary>
<p>
Example input:

```json
{
  "test_allow_nested_inputs.nested.name": "John"
}

```

Example output:

```json
{
  "test_allow_nested_inputs.greeting": "Hello John"
}

```

Test config:

```json
{
  "dependencies": "allow_nested_inputs"
}
```
</p>
</details>

Setting `allow_nested_inputs` to `false` in a workflow has the effect of also setting it to `false` in any nested subworkflows called by that workflow. In the following example, `allow_nested_inputs` is set to `false` in the top-level workflow (`multi_nested_inputs`), which overrides the value of `true` in the subworkflow (`test_allow_nested_inputs`).

<details>
<summary>
Example: multi_nested_inputs.wdl

```wdl
version 1.2

import "test_allow_nested_inputs.wdl"

workflow multi_nested_inputs { 
  call test_allow_nested_inputs

  hints {
    allow_nested_inputs: false
  }

  output {
    String greeting = test_allow_nested_inputs.greeting
  }
}
```
</summary>
<p>
Example input:

```json
{
  "multi_nested_inputs.test_allow_nested_inputs.nested.name": "John"
}
```

Example output:

```json
{
  "multi_nested_inputs.greeting": "Hello Joe"
}
```

Test config:

```json
{
  "dependencies": "allow_nested_inputs"
}
```
</p>
</details>

### Call Statement

A workflow calls other tasks/workflows via the `call` keyword. A `call` is followed by the name of the task or subworkflow to run. If a task is defined in the same WDL document as the calling workflow, it may be called using just the task name. A task or workflow in an imported WDL must be called using its [fully-qualified name](#fully-qualified-names--namespaced-identifiers).

Each `call` must be uniquely identifiable. By default, the `call`'s unique identifier is the task or subworkflow name (e.g., `call foo` would be referenced by name `foo`). However, to `call foo` multiple times in the same workflow, it is necessary to give all except one of the `call` statements a unique alias using the `as` clause, e.g., `call foo as bar`.

A `call` has an optional body in braces (`{}`), which may contain a comma-delimited list of inputs to the call. A `call` must, at a minimum, provide values for all of the task/subworkflow's required inputs, and each input value/expression must match the type of the task/subworkflow's corresponding input parameter. An input value may be any valid expression, not just a reference to another call output. If a task has no required parameters, then the `call` body may be empty or omitted.

If a call input has the same name as a declaration from the current scope, the name of the input may appear alone (without an expression) to implicitly bind the value of that declaration. For example, if a workflow and task both have inputs `x` and `z` of the same types, then `call mytask {x, y=b, z}` is equivalent to `call mytask {x=x, y=b, z=z}`.

<details>
<summary>
Example: call_example.wdl

```wdl
version 1.2

import "other.wdl" as lib

task repeat {
  input {
    Int i = 0  # this will cause the task to fail if not overriden by the caller
    String? opt_string
  }
  
  command <<<
  if [ "~{i}" -lt "1" ]; then
    echo "i must be >= 1"
    exit 1
  fi
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
  call repeat { i = 3 }

  # Calls repeat a second time, this time with both inputs.
  # We need to give this one an alias to avoid name-collision.
  call repeat as repeat2 {
    i = i * 2,
    opt_string = s
  }

  # Calls repeat with one required input using the abbreviated 
  # syntax for `i`.
  call repeat as repeat3 { i, opt_string = s }

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

For historical reasons, the keyword `input:` may optionally precede the list of inputs inside the braces. In the following example, all the `call` statements are equivalent.

<details>
<summary>
Example: test_input_keyword.wdl

```wdl
version 1.2

import "call_example.wdl" as lib

workflow test_input_keyword {
  input {
    Int i
  }

  # These three calls are equivalent
  call lib.repeat as rep1 { i }

  call lib.repeat as rep2 { i = i}

  call lib.repeat as rep3 {
    input:  # optional (for backward compatibility)
      i
  }

  call lib.repeat as rep4 {
    input:  # optional (for backward compatibility)
      i = i
  }

  output {
    Array[String] lines1 = rep1.lines
    Array[String] lines2 = rep2.lines
    Array[String] lines3 = rep3.lines
    Array[String] lines4 = rep4.lines
  }
}
```
</summary>
<p>
Example input:

```json
{
  "test_input_keyword.i": 2
}
```

Example output:

```json
{
  "test_input_keyword.lines1": ["default", "default"],
  "test_input_keyword.lines2": ["default", "default"],
  "test_input_keyword.lines3": ["default", "default"],
  "test_input_keyword.lines4": ["default", "default"]
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
version 1.2

import "call_example.wdl" as lib

workflow test_after {
  # Call repeat
  call lib.repeat { i = 2, opt_string = "hello" }

  # Call `repeat` again with the output from the first call.
  # This call will wait until `repeat` is finished.
  call lib.repeat as repeat2 {
    i = 1,
    opt_string = sep(" ", repeat.lines)
  }

  # Call `repeat` again. This call does not depend on the output 
  # from an earlier call, but we specify explicitly that this 
  # task must wait until `repeat` is complete before executing.
  call lib.repeat as repeat3 after repeat { i = 3 }

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
version 1.2

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

  call greet { greeting = "Hello ~{name}" }
  
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

A call to a subworkflow or task must, at a minimum, provide a value for each required input. The call may also specify values for any optional inputs. Any optional inputs that are not specified in the call may be set by the user at runtime if the execution engine supports the `allow_nested_inputs` hint and it is set to `true` in the workflow's `hints` section.

The following table describes whether a subworkflow or task input's value must be specified in the call inputs and whether it may be set at runtime based on whether it has a default value and the value of the `allow_nested_inputs` hint:

| Has default value? | Value of `allow_nested_inputs` | Must be specified in call inputs? | Can be overriden at runtime? |
| ------------------ | ------------------------------ | --------------------------------- | ---------------------------- |
| No                 | `false`                        | Yes                               | No                           |
| No                 | `true`                         | Yes                               | No                           |
| Yes                | `false`                        | No                                | No                           |
| Yes                | `true`                         | No                                | Yes                          |

🗑 Previously, setting `allow_nested_inputs` to `true` also allowed for required task inputs to be left unsatisfied by the calling workflow and only specified at runtime. This behavior is deprecated and will be removed in WDL 2.0.

🗑 The ability to set `allowNestedInputs` in the workflow's `meta` section is deprecated and will be removed in WDL 2.0.

<details>
<summary>
Example: allow_nested.wdl

```wdl
version 1.2

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
  
  requirements {
    container: "ubuntu:latest"
  }
}

workflow allow_nested {
  input {
    Int int_val
    String msg1
    Array[Int] my_ints
    File ref_file
  }

  hints {
    allow_nested_inputs: true
  }

  call lib.repeat {
    i = int_val,
    opt_string = msg1
  }

  call lib.repeat as repeat2 {
    # Note: the default value of `0` for the `i` input causes the task to fail
    i = 2
  }

  scatter (i in my_ints) {
    call inc {
      y=i, ref_file=ref_file
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
  "allow_nested.my_ints": [1, 2, 3],
  "allow_nested.ref_file": "hello.txt",
  "allow_nested.repeat2.opt_string": "goodbye"
}
```

Example output:

```json
{
  "allow_nested.lines1": ["hello", "hello", "hello"],
  "allow_nested.lines2": ["goodbye", "goodbye"],
  "allow_nested.incrs": [2, 3, 4]
}
```
</p>
</details>

In the preceding example, the workflow calling `repeat2` does not provide a value for the optional input `i`. Normally this would cause the task to fail, since `i` must have a value `>= 1` and its default value is `0`. However, if the execution engine supports `allow_nested_inputs`, then specifying `allow_nested_inputs: true` in the workflow's `hints` section means that `repeat2.i` may be set by the caller of the workflow, e.g., by including `"allow_nested.repeat2.i": 2,` in the input JSON.

It is not allowed to *override* a call input at runtime, even if nested inputs are allowed. For example, if the user tried to specify `"allow_nested.repeat.opt_string": "hola"` in the input JSON, an error would be raised because the workflow already specifies a value for that input.

The `allow_nested_inputs` directive only applies to user-supplied inputs. There is no mechanism for the workflow itself to set a value for a nested input when calling a subworkflow. For example, the following workflow is invalid:

<details>
<summary>
Example: call_subworkflow_fail.wdl

```wdl
version 1.2

import "copy_input.wdl" as copy

workflow call_subworkflow {
  meta {
    allow_nested_inputs: true
  }

  # error! A workflow can't specify a nested input for a subworkflow's call.
  call copy.copy_input { greet.greeting = "hola" }
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
version 1.2

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
    call say_hello { greeting = greeting }
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
version 1.2

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
      first = names.left,
      last = names.right
    }

    scatter (salutation in salutations) {
      # `names`, and `salutation` are all accessible here
      String short_greeting = "~{salutation} ~{honorific} ~{names.left}"
      call scat.say_hello { greeting = short_greeting }

      # the output of `make_name` is also accessible
      String long_greeting = "~{salutation} ~{honorific} ~{make_name.name}"
      call scat.say_hello as say_hello_long { greeting = long_greeting }

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
version 1.2

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
      call gt_three { i = i + j }
      
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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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

### `min`

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
version 1.2

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

### `max`

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
version 1.2

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

### ✨ `find`

Given two `String` parameters `input` and `pattern`, searches for the occurrence of `pattern` within `input` and returns the first match or `None` if there are no matches. `pattern` is a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) and is evaluated as a [POSIX Extended Regular Expression (ERE)](https://en.wikipedia.org/wiki/Regular_expression#POSIX_basic_and_extended).

Note that regular expressions are written using regular WDL strings, so backslash characters need to be double-escaped. For example:

```wdl
String? first_match = find("hello\tBob", "\\t")
```

**Parameters**

1. `String`: the input string to search.
2. `String`: the pattern to search for.

**Returns**: The contents of the first match, or `None` if `pattern` does not match `input`.

<details>
<summary>
Example: test_find_task.wdl

```wdl
version 1.2
workflow find_string {
  input {
    String in = "hello world"
    String pattern1 = "e..o"
    String pattern2 = "goodbye"
  }
  output {
    String? match1 = find(in, pattern1)  # "ello"
    String? match2 = find(in, pattern2)  # None
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
  "test_find.match1": "ello",
  "test_matches.is_read1": null
}
```
</p>
</details>

### ✨ `matches`

Given two `String` parameters `input` and `pattern`, tests whether `pattern` matches `input` at least once. `pattern` is a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) and is evaluated as a [POSIX Extended Regular Expression (ERE)](https://en.wikipedia.org/wiki/Regular_expression#POSIX_basic_and_extended).

To test whether `pattern` matches the entire `input`, make sure to begin and end the pattern with anchors. For example:

```wdl
Boolean full_match = matches("abc123", "^a.+3$")
```

Note that regular expressions are written using regular WDL strings, so backslash characters need to be double-escaped. For example:

```wdl
Boolean has_tab = matches("hello\tBob", "\\t")
```

**Parameters**

1. `String`: the input string to search.
2. `String`: the pattern to search for.

**Returns**: `true` if `pattern` matches `input` at least once, otherwise `false`.

<details>
<summary>
Example: test_matches_task.wdl

```wdl
version 1.2
workflow contains_string {
  input {
    File fastq
  }
  output {
    Boolean is_compressed = matches(basename(fastq), "\\.(gz|zip|zstd)")
    Boolean is_read1 = matches(basename(fastq), "_R1")
  }
}
```
</summary>
<p>
Example input:

```json
{
  "fastq": "sample1234_R1.fastq"
}
```

Example output:

```json
{
  "test_matches.is_compressed": false,
  "test_matches.is_read1": true
}
```
</p>
</details>

### `sub`

```
String sub(String, String, String)
```

Given three String parameters `input`, `pattern`, `replace`, this function replaces all non-overlapping occurrences of `pattern` in `input` by `replace`. `pattern` is a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) and is evaluated as a [POSIX Extended Regular Expression (ERE)](https://en.wikipedia.org/wiki/Regular_expression#POSIX_basic_and_extended).
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
version 1.2

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
version 1.2

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

  requirements {
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

These functions have a `File` or `Directory` as an input and/or output. Due to [type coercion](#type-coercion), `File` or `Directory` arguments may be specified as `String` values.

For functions that read from or write to the file system, if the entire contents of the  cannot be read/written for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having appropriate permissions, resource limitations (e.g., memory) when reading the file, and implementation-imposed file size limits.

For functions that write to the file system, the implementation should generate a random file name in a temporary directory so as not to conflict with any other task output files.

**Restrictions**

1. A function that only manipulates a path (i.e., doesn't require reading any of the file's attributes or contents) may be called anywhere, whether or not the file exists.
2. A function that *reads* a file or its attributes may only be called in a context where the input file exists. If the file is an input to a task or workflow, then it may be read anywhere in that task or worklow. If the file is created by a task, then it may only be read after it is created. For example, if the file is written during the execution of the `command`, then it may only be read in the task's `output` section. This includes functions like `stdout` and `stderr` that read a task's output stream.
3. A function that *writes* a file may be called anywhere. However, writing a file in a workflow is discouraged since it may have the side-effect of creating a permanent output file that is not named in the output section. For example, calling [`write_lines`](#write_lines) in a workflow and then passing the resulting `File` as input to a task may require the engine to persist that file to cloud storage.

### `basename`

```
String basename(File, [String])
String basename(Directory, [String])
```

Returns the "basename" of a file or directory - the name after the last directory separator in the path. 

The optional second parameter specifies a literal suffix to remove from the file name. If the file name does not end with the specified suffix then it is ignored.

**Parameters**

1. `File|Directory`: Path of the file or directory to read. If the argument is a `String`, it is assumed to be a local file path relative to the current working directory of the task.
2. `String`: (Optional) Suffix to remove from the file name.

**Returns**: The file's basename as a `String`.

<details>
<summary>
Example: test_basename.wdl

```wdl
version 1.2

workflow test_basename {
  output {
    Boolean is_true1 = basename("/path/to/file.txt") == "file.txt"
    Boolean is_true2 = basename("/path/to/file.txt", ".txt") == "file"
    Boolean is_true3 = basename("/path/to/dir") == "dir" 
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

### ✨ `join_paths`

```
File join_paths(File, String)
File join_paths(File, Array[String]+)
File join_paths(Array[String]+)
```

Joins together two or more paths into an absolute path in the host filesystem.

There are three variants of this function:

1. `File join_paths(File, String)`: Joins together exactly two paths. The first path may be either absolute or relative and must specify a directory; the second path is relative to the first path and may specify a file or directory.
2. `File join_paths(File, Array[String]+)`: Joins together any number of relative paths with a base path. The first argument may be either an absolute or a relative path and must specify a directory. The paths in the second array argument must all be relative. The *last* element may specify a file or directory; all other elements must specify a directory.
3. `File join_paths(Array[String]+)`: Joins together any number of paths. The array must not be empty. The *first* element of the array may be either absolute or relative; subsequent path(s) must be relative. The *last* element may specify a file or directory; all other elements must specify a directory.

An absolute path starts with `/` and indicates that the path is relative to the root of the environment in which the task is executed. Only the first path may be absolute. If any subsequent paths are absolute, it is an error.

A relative path does not start with `/` and indicates the path is relative to its parent directory. It is up to the execution engine to determine which directory to use as the parent when resolving relative paths; by default it is the working directory in which the task is executed.

**Parameters**

1. `File|Array[String]+`: Either a path or an array of paths.
2. `String|Array[String]+`: A relative path or paths; only allowed if the first argument is a `File`.

**Returns**: A `File` representing an absolute path that results from joining all the paths in order (left-to-right), and resolving the resulting path against the default parent directory if it is relative.

<details>
<summary>
Example: join_paths_task.wdl

```wdl
version 1.2

task resolve_paths_task {
  input {
    File abs_file = "/usr"
    String abs_str = "/usr"
    String rel_dir_str = "bin"
    File rel_file = "echo"
    File rel_dir_file = "mydir"
    String rel_str = "mydata.txt"
  }

  # these are all equivalent to '/usr/bin/echo'
  File bin1 = join_paths(abs_file, [rel_str_dir, rel_file])
  File bin2 = join_paths(abs_str, [rel_str_dir, rel_file])
  File bin3 = join_paths([abs_str, rel_str_dir, rel_file])
  
  # the default behavior is that this resolves to 
  # '<working dir>/mydir/mydata.txt'
  File data = join_paths(rel_dir_file, rel_str)
  
  # this resolves to '<working dir>/bin/echo', which is non-existent
  File doesnt_exist = join_paths([rel_dir_str, rel_file])
  command <<<
    mkdir ~{rel_dir_file}
    ~{bin1} -n "hello" > ~{data}
  >>>

  output {
    Boolean bins_equal = (bin1 == bin2) && (bin1 == bin3)
    String result = read_string(data)
    File? missing_file = doesnt_exist
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
  "join_paths_task.bins_equal": true,
  "join_paths_task.result": "hello"
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
version 1.2

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
Float size(File|File?, [String])
Float size(Directory|Directory?, [String])
Float size(X|X?, [String])
```

Determines the size of a file, directory, or the sum total sizes of the files/directories contained within a compound value. The files may be optional values; `None` values have a size of `0.0`. By default, the size is returned in bytes unless the optional second argument is specified with a [unit](#units-of-storage)

In the second variant of the `size` function, the parameter type `X` represents any compound type that contains `File` or `File?` nested at any depth.

If the size cannot be represented in the specified unit because the resulting value is too large to fit in a `Float`, an error is raised. It is recommended to use a unit that will always be large enough to handle any expected inputs without numerical overflow.

**Parameters**

1. `File|File?|Directory|Directory?|X|X?`: A file, directory, or a compound value containing files/directories, for which to determine the size.
2. `String`: (Optional) The unit of storage; defaults to 'B'.

**Returns**: The size of the files/directories as a `Float`.

<details>
<summary>
Example: file_sizes_task.wdl

```wdl
version 1.2

task file_sizes {
  command <<<
    printf "this file is 22 bytes\n" > created_file
  >>>

  File? missing_file = None

  output {
    File created_file = "created_file"
    Float missing_file_bytes = size(missing_file)
    Float created_file_bytes = size(created_file, "B")
    Float multi_file_kb = size([created_file, missing_file], "K")

    Map[String, Pair[Int, File]] nested = {
      "a": (10, created_file),
      "b": (50, missing_file)
    }
    Float nested_bytes = size(nested)
  }
  
  requirements {
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
  "file_sizes.multi_file_kb": 0.022,
  "file_sizes.nested_bytes": 22.0
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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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
  
  requirements {
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
version 1.2

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
  
  requirements {
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
Array[Object] read_tsv(File, true)
Array[Object] read_tsv(File, Boolean, Array[String])
```

Reads a tab-separated value (TSV) file as an `Array[Array[String]]` representing a table of values. Trailing end-of-line characters (`\r` and `\n`) are removed from each line.

This function has three variants:

1. `Array[Array[String]] read_tsv(File, [false])`: Returns each row of the table as an `Array[String]`. There is no requirement that the rows of the table are all the same length.
2. `Array[Object] read_tsv(File, true)`: The second parameter must be `true` and specifies that the TSV file contains a header line. Each row is returned as an `Object` with its keys determined by the header (the first line in the file) and its values as `String`s. All rows in the file must be the same length and the field names in the header row must be valid `Object` field names, or an error is raised.
3. `Array[Object] read_tsv(File, Boolean, Array[String])`: The second parameter specifies whether the TSV file contains a header line, and the third parameter is an array of field names that is used to specify the field names to use for the returned `Object`s. If the second parameter is `true`, the specified field names override those in the file's header (i.e., the header line is ignored).

If the file is empty, an empty array is returned.

If the entire contents of the file can not be read for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, not having access to the file, resource limitations (e.g. memory) when reading the file, and implementation-imposed file size limits.

**Parameters**

1. `File`: The TSV file to read.
2. `Boolean`: (Optional) Whether to treat the file's first line as a header.
3. `Array[String]`: (Optional) An array of field names. If specified, then the second parameter is also required.

**Returns**: An `Array` of rows in the TSV file, where each row is an `Array[String]` of fields or an `Object` with keys determined by the second and third parameters and `String` values.

<details>
<summary>
Example: read_tsv_task.wdl

```wdl
version 1.2

task read_tsv {
  command <<<
    {
      printf "row1\tvalue1\n"
      printf "row2\tvalue2\n"
      printf "row3\tvalue3\n"
    } >> data.no_headers.tsv

    {
      printf "header1\header2\n"
      printf "row1\tvalue1\n"
      printf "row2\tvalue2\n"
      printf "row3\tvalue3\n"
    } >> data.headers.tsv
  >>>

  output {
    Array[Array[String]] output_table = read_tsv("data.no_headers.tsv")
    Array[Object] output_objs1 = read_tsv("data.no_headers.tsv", false, ["name", "value"])
    Array[Object] output_objs2 = read_tsv("data.headers.tsv", true)
    Array[Object] output_objs3 = read_tsv("data.headers.tsv", true, ["name", "value"])
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
  ],
  "read_tsv.output_objs1": [
    {
      "name": "row1",
      "value": "value1"
    },
    {
      "name": "row2",
      "value": "value2"
    },
    {
      "name": "row3",
      "value": "value3"
    }
  ],
  "read_tsv.output_objs2": [
    {
      "header1": "row1",
      "header2": "value1"
    },
    {
      "header1": "row2",
      "header2": "value2"
    },
    {
      "header1": "row3",
      "header2": "value3"
    }
  ],  
  "read_tsv.output_objs3": [
    {
      "name": "row1",
      "row": "value1"
    },
    {
      "name": "row2",
      "row": "value2"
    },
    {
      "name": "row3",
      "row": "value3"
    }
  ]
}
```
</p>
</details>

### `write_tsv`

```
File write_tsv(Array[Array[String]]|Array[Struct])
File write_tsv(Array[Array[String]], true, Array[String])
File write_tsv(Array[Struct], Boolean, Array[String])
```
Given an `Array` of elements, writes a tab-separated value (TSV) file with one line for each element.

There are three variants of this function:

1. `File write_tsv(Array[Array[String]])`: Each element is concatenated using a tab ('\t') delimiter and written as a row in the file. There is no header row.

2. `File write_tsv(Array[Array[String]], true, Array[String])`: The second argument must be `true` and the third argument provides an `Array` of column names. The column names are concatenated to create a header that is written as the first row of the file. All elements must be the same length as the header array.

3. `File write_tsv(Array[Struct], [Boolean, [Array[String]]])`: Each element is a struct whose field values are concatenated in the order the fields are defined. The optional second argument specifies whether to write a header row. If it is `true`, then the header is created from the struct field names. If the second argument is `true`, then the optional third argument may be used to specify column names to use instead of the struct field names.

Each line is terminated by the newline (`\n`) character. 

The generated file should be given a random name and written in a temporary directory, so as not to conflict with any other task output files.

If the entire contents of the file can not be written for any reason, the calling task or workflow fails with an error. Examples of failure include, but are not limited to, insufficient disk space to write the file.


**Parameters**

1. `Array[Array[String]] | Array[Struct]`: An array of rows, where each row is either an `Array` of column values or a struct whose values are the column values.
2. `Boolean`: (Optional) Whether to write a header row.
3. `Array[String]`: An array of column names. If the first argument is `Array[Array[String]]` and the second argument is `true` then it is required, otherwise it is optional. Ignored if the second argument is `false`.


**Returns**: A `File`.

<details>
<summary>
Example: write_tsv_task.wdl

```wdl
version 1.2

task write_tsv {
  input {
    Array[Array[String]] array = [["one", "two", "three"], ["un", "deux", "trois"]]
    Array[Numbers] structs = [
      Numbers {
        first: "one",
        second: "two",
        third: "three"
      },
      Numbers {
        first: "un",
        second: "deux",
        third: "trois"
      }
    ]
  }

  command <<<
    cut -f 1 ~{write_tsv(array)} >> array_no_header.txt
    cut -f 1 ~{write_tsv(array, true, ["first", "second", "third"])} > array_header.txt
    cut -f 1 ~{write_tsv(structs)} >> structs_default.txt
    cut -f 2 ~{write_tsv(structs, false)} >> structs_no_header.txt
    cut -f 2 ~{write_tsv(structs, true)} >> structs_header.txt
    cut -f 3 ~{write_tsv(structs, true, ["no1", "no2", "no3"])} >> structs_user_header.txt
  >>>

  output {
    Array[String] array_no_header = read_lines("array_no_header.txt")
    Array[String] array_header = read_lines("array_header.txt")
    Array[String] structs_default = read_lines("structs_default.txt")
    Array[String] structs_no_header = read_lines("structs_no_header.txt")
    Array[String] structs_header = read_lines("structs_header.txt")
    Array[String] structs_user_header = read_lines("structs_user_header.txt")

  }
  
  requirements {
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
  "write_tsv.array_no_header": ["one", "un"],
  "write_tsv.array_header": ["first", "one", "un"],
  "write_tsv.structs_default": ["first", "one", "un"], 
  "write_tsv.structs_no_header": ["two", "deux"], 
  "write_tsv.structs_header": ["second", "two", "deux"], 
  "write_tsv.structs_user_header": ["no3", "three", "trois"], 

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
version 1.2

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
version 1.2

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

  requirements {
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

The return value is of type [`Union`](#union-hidden-type) and must be used in a context where it can be coerced to the expected type, or an error is raised. For example, if the JSON file contains `null`, then the return value will be `None`, meaning the value can only be used in a context where an optional type is expected.

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
version 1.2

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
version 1.2

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
version 1.2

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
  
  requirements {
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

Each line is terminated by the newline (`\n`) character. 
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
version 1.2

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

  requirements {
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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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

### `suffix`

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
version 1.2

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
version 1.2

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

### `quote`

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
version 1.2

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

### `squote`

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
version 1.2

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

### `sep`

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
version 1.2

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
version 1.2

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
    call double { n = idx }
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
version 1.2

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
version 1.2

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
version 1.2

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
version 1.2

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

### `unzip`

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
version 1.2

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

### ✨ `contains`

```
Boolean contains(Array[P], P)
Boolean contains(Array[P?], P?)
```

Tests whether the given array contains at least one occurrence of the given value.

**Parameters**

1. `Array[P]` or `Array[P?]`: an array of any primitive type.
2. `P` or `P?`: a primitive value of the same type as the array. If the array's type is optional, then the value may also be optional.

**Returns**: `true` if the array contains at least one occurrence of the value, otherwise `false`.

**Example**

<details>
<summary>
Example: test_contains.wdl

```wdl
version 1.2

task null_sample {
  command <<<
  echo "Sample array contains a null value!"
  >>>
}

task missing_sample {
  input {
    String name
  }

  command <<<
  echo "Sample ~{name} is missing!"
  >>>
}

workflow test_contains {
  input {
    Array[String?] samples
    String name
  }

  Boolean has_null = contains(samples, None)
  if (has_null) {
    call null_sample
  }
  
  Boolean has_missing = !contains(samples, name)
  if (has_missing) {
    call missing_sample { input: name }
  }

  output {
    Boolean samples_are_valid = !(has_null || has_missing)
  }
}
```
</summary>
<p>
Example input:

```json
{
  "test_contains.samples": [null, "foo"],
  "test_contains.name": "bar"
}
```

Example output:

```json
{
  "test_contains.samples_are_valid": false
}
```
</p>
</details>

### ✨ `chunk`

```
Array[Array[X]] chunk(Array[X], Int)
```

Given an array and a length *n*, splits the array into consecutive, non-overlapping arrays of *n* elements. If the length of the array is not a multiple *n* then the final sub-array will have `length(array) % n` elements.

**Parameters**

1. `Array[X]`: The array to split. May be empty.
2. `Int`: The desired length of the sub-arrays. Must be > 0.

**Returns**: An array of sub-arrays, where each sub-array is of length `N` except possibly the last one.

<details>
<summary>
Example: chunk_array.wdl

```wdl
version 1.2
workflow chunk_array {
  Array[String] s1 = ["a", "b", "c", "d", "e", "f"]
  Array[String] s2 = ["a", "b", "c", "d", "e"]
  Array[String] s3 = ["a", "b"]
  Array[String] s4 = []
  
  scatter (a in chunk(s1, 3)) {
    String concat = sep("", a)
  }

  output {
    Boolean is_reversible = s1 == flatten(chunk(s1, 3))
    Array[Array[String]] o1 = chunk(s1, 3)
    Array[Array[String]] o2 = chunk(s2, 3)
    Array[Array[String]] o3 = chunk(s3, 3)
    Array[Array[String]] o4 = chunk(s4, 3)
    Array[String] concats = concat
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
  "chunk_array.is_reversible": true,
  "chunk_array.o1": [["a", "b", "c"], ["d", "e", "f"]],
  "chunk_array.o2": [["a", "b", "c"], ["d", "e"]],
  "chunk_array.o3": [["a", "b"]],
  "chunk_array.o4": [[]],
  "chunk_array.concats": ["abc", "def"]
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
version 1.2

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
X select_first(Array[X?], X)
```

Selects the first - i.e., left-most - non-`None` value from an `Array` of optional values. The optional second parameter provides a default value that is returned if the array is empty or contains only `None` values. If the default value is not provided and the array is empty or contains only `None` values, then an error is raised.

**Parameters**

1. `Array[X?]+`: Non-empty `Array` of optional values.
2. `X`: (Optional) The default value.

**Returns**: The first non-`None` value in the input array, or the default value if it is provided and the array does not contain any non-`None` values.

<details>
<summary>
Example: test_select_first.wdl

```wdl
version 1.2

workflow test_select_first {
  input {
    Int? maybe_five = 5
    Int? maybe_four_but_is_not = None
    Int? maybe_three = 3
  }

  output {
    # all of these statements evaluate to 5
    Int fiveA = select_first([maybe_five, maybe_four_but_is_not, maybe_three])
    Int fiveB = select_first([maybe_four_but_is_not, maybe_five, maybe_three])
    Int fiveC = select_first([], 5)
    Int fiveD = select_first([None], 5)
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
  "test_select_first.fiveA": 5,
  "test_select_first.fiveB": 5,
  "test_select_first.fiveC": 5,
  "test_select_first.fiveD": 5
}
```
</p>
</details>

<details>
<summary>
Example: select_first_only_none_fail.wdl

```wdl
version 1.2

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
version 1.2

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
version 1.2

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

### `as_pairs`

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
version 1.2

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

### `as_map`

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
version 1.2

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
version 1.2

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

### `keys`

```
Array[P] keys(Map[P, Y])
Array[String] keys(Struct|Object)
```

Given a key-value type collection (`Map`, `Struct`, or `Object`), returns an `Array` of the keys from the input collection, in the same order as the elements in the collection.

When the argument is a `Struct`, the returned array will contain the keys in the same order they appear in the struct definition. When the argument is an `Object`, the returned array has no guaranteed order.

When the input `Map` or `Object` is empty, an empty array is returned.

**Parameters**

1. `Map[P, Y]`|`Struct`|`Object`: Collection from which to extract keys.

**Returns**: `Array[P]` of the input collection's keys. If the input is a `Struct` or `Object`, then the returned array will be of type `Array[String]`.

<details>
<summary>
Example: test_keys.wdl

```wdl
version 1.2

struct Name {
  String first
  String last
}

workflow test_keys {
  input {
    Map[String, Int] x = {"a": 1, "b": 2, "c": 3}
    Map[String, Pair[File, File]] str_to_files = {
      "a": ("a.bam", "a.bai"), 
      "b": ("b.bam", "b.bai")
    }
    Name name = Name {
      first: "John",
      last: "Doe"
    }
  }

  scatter (item in as_pairs(str_to_files)) {
    String key = item.left
  }

  Array[String] str_to_files_keys = key

  output {
    Boolean is_true1 = keys(x) == ["a", "b", "c"]
    Boolean is_true2 = str_to_files_keys == keys(str_to_files)
    Boolean is_true3 = keys(name) == ["first", "last"]
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
  "test_keys.is_true2": true,
  "test_keys.is_true3": true
}
```
</p>
</details>

### ✨ `contains_key`

```
* Boolean contains_key(Map[P, Y], P)
* Boolean contains_key(Object, String)
* Boolean contains_key(Map[String, Y]|Struct|Object, Array[String])
```

Given a key-value type collection (`Map`, `Struct`, or `Object`) and a key, tests whether the collection contains an entry with the given key.

This function has thre variants:

1. `Boolean contains_key(Map[P, Y], P)`: Tests whether the `Map` has an entry with the given key. If `P` is an optional type (e.g., `String?`), then the second argument may be `None`.
2. `Boolean contains_key(Object, String)`: Tests whether the `Object` has an entry with the given name.
3. `Boolean contains_key(Map[String, Y]|Struct|Object, Array[String])`: Tests recursively for the presence of a compound key within a nested collection.

For the third variant, the first argument is a collection that may be nested to any level, i.e., contain values that are collections, which themselves may contain collections, and so on. The second argument is an array of keys that are resolved recursively. If the value associated with any except the last key in the array is `None` or not a collection type, this function returns `false`.

For example, if the first argument is a `Map[String, Map[String, Int]]` and the second argument is `["foo", "bar"]`, then the outer `Map` is tested for the presence of key "foo", and if it is present, then its value is tested for the presence of key "bar". This only tests for the presence of the named element, *not* whether or not it is `defined`.

**Parameters**

1. `Map[P, Y]`|`Struct`|`Object`: Collection to search for the key.
2. `P|Array[String]`: The key to search. If the first argument is a `Map`, then the key must be of the same type as the `Map`'s key type. If the `Map`'s key type is optional then the key may also be optional. If the first argument is a `Map[String, Y]`, `Struct`, or `Object`, then the key may be either a `String` or `Array[String]`.

**Returns**: `true` if the collection contains the key, otherwise false.

**Example**

<details>
  <summary>
  Example: test_contains_key.wdl
  
  ```wdl
  version 1.2

  struct Person {
    String name
    Map[String, String]? details
  }

  workflow test_contains_key {
    input {
      Map[String, Int] m
      String key1
      String key2
      Person p1
      Person p2
    }

    output {
      Int? i1 = m[s1] if contains_key(m, key1) else None
      Int? i2 = m[s2] if contains_key(m, key2) else None
      String? phone1 = p1.details["phone"] if contains_key(p1, ["details", "phone"]) else None
      String? phone2 = p2.details["phone"] if contains_key(p2, ["details", "phone"]) else None
    }
  }
  ```
  </summary>
  <p>
  Example input:

  ```json
  {
    "test_contains_key.m": {"a": 1, "b": 2},
    "test_contains_key.key1": "a",
    "test_contains_key.key2": "c",
    "test_contains_key.p1": {
      "name": "John",
      "details": {
        "phone": "123-456-7890"
      }
    },
    "test_contains_key.p2": {
      "name": "Agent X"
    }
  }
  ```
   
  Example output:

  ```json
  {
    "test_contains_key.i1": 1,
    "test_contains_key.i2": null,
    "test_contains_key.phone1": "123-456-7890",
    "test_contains_key.phone2": null,
  }
  ``` 
  </p>
</details>

### ✨ `values`

```
Array[Y] values(Map[P, Y])
```

Returns an `Array` of the values from the input `Map`, in the same order as the elements in the map. If the map is empty, an empty array is returned.

**Parameters**

1. `Map[P, Y]`: `Map` from which to extract values.

**Returns**: `Array[Y]` of the input `Map`s values.

**Example**

<details>
<summary>
Example: test_values.wdl

```wdl
version 1.2

task add {
  input {
    Int x
    Int y
  }

  Int z = x + y

  command <<<
  echo "~{x} + ~{y} = ~{z}"
  >>>

  output {
    Int sum = z
  }
}

workflow test_values {
  input {
    Map[String, Pair[Int, Int]] str_to_ints = {
      "a": (1, 2),
      "b": (3, 4)
    }
  }
  
  scatter (files in values(str_to_files)) {
    call add { x=ints.left, y=ints.right }
  }
  
  output {
    Array[Int] sums = add.sum
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
  "test.values.sums": [3, 7]
}
```
</p>
</details>

### `collect_by_key`

```
Map[P, Array[Y]] collect_by_key(Array[Pair[P, Y]])
```

Given an `Array` of `Pair`s, creates a `Map` in which the right elements of the `Pair`s are grouped by the left elements. In other words, the input `Array` may have multiple `Pair`s with the same key. Rather than causing an error (as would happen with [`as_map`](#as_map)), all the values with the same key are grouped together into an `Array`.

The order of the keys in the output `Map` is the same as the order of their first occurrence in the input `Array`. The order of the elements in the `Map` values is the same as their order of occurrence in the input `Array`.

**Parameters**

1. `Array[Pair[P, Y]]`: `Array` of `Pair`s to group.

**Returns**: `Map` of keys to `Array`s of values.

<details>
<summary>
Example: test_collect_by_key.wdl

```wdl
version 1.2

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
version 1.2

workflow is_defined {
  input {
    String? name
  }

  if (defined(name)) {
    call say_hello { name = select_first([name]) }
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

### `length`

```
Int length(Array[X]|Map[X, Y]|Object|String)
```

Returns the length of the input argument as an `Int`:

* For an `Array[X]` argument: the number of elements in the array.
* For a `Map[X, Y]` argument: the number of items in the map.
* For an `Object` argument: the number of key-value pairs in the object.
* For a `String` argument: the number of characters in the string.

**Parameters**

1. `Array[X]`|`Map[X, Y]`|`Object`|`String`: A collection or string whose elements are to be counted.

**Returns**: The length of the collection/string as an `Int`.

<details>
<summary>
Example: test_length.wdl

```wdl
version 1.2

workflow test_length {
  Array[Int] xs = [1, 2, 3]
  Array[String] ys = ["a", "b", "c"]
  Array[String] zs = []
  Map[String, Int] m = {"a": 1, "b", 2}
  String s = "ABCDE"

  output {
    Int xlen = length(xs)
    Int ylen = length(ys)
    Int zlen = length(zs)
    Int mlen = length(m)
    Int slen = length(s)
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
  "test_length.zlen": 0,
  "test_length.mlen": 2,
  "test_length.slen": 5,
}
```
</p>
</details>

# Input and Output Formats

WDL uses [JSON](https://www.json.org) as its native serialization format for task and workflow inputs and outputs. The specifics of these formats are described below.

All WDL implementations are required to support the standard JSON input and output formats. WDL compliance testing is performed using test cases whose inputs and expected outputs are given in these formats. A WDL implementation may choose to provide additional input and output mechanisms so long as they are documented, and/or tools are provided to interconvert between engine-specific input and the standard JSON format, to foster interoperability between tools in the WDL ecosystem.

## JSON Input Format

The inputs for a workflow invocation may be specified as a single JSON object that contains one member for each top-level workflow input. The name of the object member is the [fully-qualified name](#fully-qualified-names--namespaced-identifiers) of the input parameter, and the value is the [serialized form](#appendix-a-wdl-value-serialization-and-deserialization) of the WDL value.

If the WDL implementation supports the [`allow_nested_inputs`](#computing-call-inputs) hint, then optional inputs for nested calls can also be specified in the input JSON, provided the call does not already specify a value for the input. Nested inputs are referenced using the name of the `call`, which may be different from the name of the task or subworkflow (i.e., if is imported or called with an alias). When a `call` appears within a `scatter`, setting the value of an input applies to every instance of the call.

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
  "wf.call1.s": "call 1 input",
  "wf.call2.s": "call 2 input"
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

### Specifying / Overriding Requirements and Hints

[Requirement](#-requirements-section) and [hint](#-hints-section) attributes can be specified (or overridden) for any task in the JSON input file. To differentiate requirements and hints from task inputs, the `requirements` or `hints` namespace is added after the task name.

```json
{
  "wf.task1.requirements.memory": "16 GB",
  "wf.task2.requirements.cpu": 2,
  "wf.task2.requirements.disks": "100",
  "wf.subwf.task3.requirements.container": "mycontainer:latest",
  "wf.task4.hints.foo": "bar"
}
```

Overriding an attribute for a task nested within a `scatter` applies to all invocations of that task.

Unlike inputs, a WDL implementation must support overriding requirements and hints regardless of whether it supports the [`allow_nested_inputs`](#allow_nested_inputs) workflow hint. Requirements and hints specified in the input JSON always supersede values supplied directly in the WDL. Any hints that are not supported by the execution engine are ignored.

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

## Extended File/Directory Input/Output Format

There is no guarantee that executing a workflow multiple times with the same input file or directory URIs will result in the same outputs. For example the contents of a file may change between one execution and the next, or a file may be added to or removed from a directory.

To help ensure the reproducibility of workflow executions, and to support job output reuse features of the runtime engine (sometimes called "call caching"), it is strongly recommended that runtime engines support the more explicit extended format for `File` and `Directory` inputs and outputs.

In the extended format, `File` and `Directory` inputs and outputs may be specified using either a JSON string or object.

A directory object has the following attributes:

* `type`: Always "Directory"; optional for the top-level inputs/outputs but required within directory listings.
* `location`: The directory URI. This is equivalent to the string value in the simple form. May be absent if the directory is within a listing as long as `basename` is specified. If location is not specified, then `basename` and `listing` are both required, and all files/directories in the listing must have a location that is an absolute path or URI.
* `basename`: The name of the directory relative to the containing directory. If the basename differs from the actual directory name at the given location, the file must be localized with the given basename.
* `listing`: An array of files/subdirectories within the directory. May be nested to any degree.

A file object has the following attributes:

* `type`: Always "File"; optional for top-level inputs/outputs but required within directory listings.
* `location`: The file URI. This is equivalent to the string value in the simple form. May be absent if the file is within a listing so long as `basename` is specified.
* `basename`: The name of the file relative to the containing directory. If the basename differs from the actual file name at the given location, the file must be localized with the given basename.

It is recommended that the runtime engine support additional attributes to promote reproducibility, such as a file checksum.

The following example shows a directory input in extended format. The directory listing makes explicit the structure of the directory. If a file were added to the source directory between one execution and the next, the new file would be ignored since it doesn't appear in the listing. If a file were removed from the source directory between one execution and the next, the workflow execution would fail because the input directory would not match the expected structure.

```json
{
  "wf.indir": {
    "location": "/mnt/data/results/foo",
    "listing": [
      {
        "type": "File",
        "location": "/mnt/data/results/foo/bar.txt",
        "basename": "something_else.txt"
      },
      {
        "type": "Directory",
        "basename": "baz",
        "listing": [
          {
            "type": "File",
            "basename": "qux.fa"
          }
        ]
      }
    ]
  }
}
```

When this directory is localized, it will result in the following local folder structure:

```
<workdir>
|_ foo
   |_ something_else.txt
   |_ baz
      |_ qux.fa
```

A directory listing can also be used to construct an input directory from files that originate from disparate locations. The following input would result in the same local directory structure as above:

```json
{
  "wf.indir": {
    "basename": "foo",
    "listing": [
      {
        "type": "File",
        "location": "/mnt/data/results/foo/bar.txt",
        "basename": "something_else.txt"
      },
      {
        "type": "Directory",
        "basename": "baz",
        "listing": [
          {
            "type": "File",
            "location": "/home/fred/qux.fa"
          }
        ]
      }
    ]
  }
}
```

## JSON Serialization of WDL Types

### Primitive Types

All primitive WDL types serialize naturally to JSON values:

| WDL Type    | JSON Type |
| ----------- | --------- |
| `Int`       | `number`  |
| `Float`     | `number`  |
| `Boolean`   | `boolean` |
| `String`    | `string`  |
| `File`      | `string`  |
| `Directory` | `string`  |
| `None`      | `null`    |

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
version 1.2

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
version 1.2

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

A `Map[P, Y]` can be converted to a `Struct` with two array members: `Array[X] keys` and `Array[Y] values`. This is the suggested approach.

<details>
<summary>
Example: map_to_struct2.wdl

```wdl
version 1.2

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

A `Map[P, P]` can be converted to an array of `Pair`s. Each pair can then be converted to a serializable format using one of the methods described in the previous section. This approach is less desirable as it requires the use of a `scatter`.

<details>
<summary>
Example: map_to_array.wdl

```wdl
version 1.2

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
version 1.2

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
  
  requirements {
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
    * Separate values by newlines (`\n`) and write them to a file. This can be accomplished with the [`write_lines`](#write_lines) function.
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
version 1.2

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

  requirements {
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
version 1.2

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
version 1.2

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
  
  requirements {
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
version 1.2

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
      to_tail = item
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
version 1.2

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
    call serde_int_strings { int_strings = pair }
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
version 1.2

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

  call grep1 { infile, pattern, args = arg_str }

  call grep2 { infile, pattern, args }

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
version 1.2

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
version 1.2

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

  requirements {
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
    * A [`requirements`](#-requirements-section) namespace that contains all the runtime requirements
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

A task scope consists of all the declarations in the task `input` section and in the body of the task. The `input` section is used only to delineate which declarations are visible outside the task (i.e., they are part of the task's namespace) and which are private to the task. Input declarations may reference private declarations, and vice-versa. Declarations in the task scope may be referenced in expressions anywhere in the task (i.e., `command`, `requirements`, and `output` sections).

The `output` section can be considered a nested scope within the task. Expressions in the output scope may reference declarations in the task scope, but the reverse is not true. This is because declarations in the task scope are evaluated when a task is invoked (i.e., before it's command is evaluated and executed), while declarations in the output scope are only evaluated after execution of the command is completed.

For example, in this task:

```wdl
version 1.2

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

  requirements {
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

  call mytask { inp = i }
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

Elements such as structs and task `requirements` sections are namespaces, but they lack scope because their members cannot reference each other. For example, one member of a struct cannot reference another member in that struct, nor can a `requirements` attribute reference another attribute.

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
