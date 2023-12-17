# Workflow Description Language (WDL)

The **Workflow Description Language (WDL)** is an open standard for describing data processing workflows with a human-readable and writeable syntax.
WDL makes it straightforward to define analysis tasks, connect them together in workflows, and parallelize their execution.
The language strives to be accessible and understantable to all manner of users, including programmers, analysts, and operators of a production system.
The language enables common patterns, such as scatter-gather and conditional execution, to be expressed simply.
WDL is designed for portability, and there are several [implementations](#execution-engines-and-platforms) to choose from that run in a variety of environments, including HPC systems and cloud platforms.

## Versioning

WDL versioning follows [semantic versioning](https://semver.org) conventions.

The WDL *language* has a two-number version (e.g., `1.1`).
An increase in the minor (second) version number (e.g., `1.0` to `1.1`) indicates the addition of, or non-breaking changes to, the language or standard library functions.
An increase in the major (first) version number (e.g., `1.0` to `2.0`) indicates that breaking changes have been made.

The WDL *specification* has a three-number version (e.g., `1.1.2`).
The specification version tracks the language version, but there may also be patch releases (indicated by a change to the patch, or third, version number) that include fixes for typos, additional examples, or non-breaking clarifications of ambiguous language.

## Language Specifications

The WDL specification contains all relevant information for users and developers, including those wanting to implement an execution engine.
This GitHub project uses the branch for the current version of the specification as its primary branch, so you will always see the current version of the specification so long as you visit this project's [root URL](https://github.com/openwdl/wdl).
Users are strongly encouraged to use the current version of the specification unless absolutely necessary.

This branch is for version **1.1** of the [WDL language specification](https://github.com/openwdl/wdl/blob/wdl-1.1/SPEC.md).

Previous versions of the spec can be found here:

- [1.0](https://github.com/openwdl/wdl/blob/main/versions/1.0/SPEC.md)

There are a number of draft versions that correspond to initial efforts at creating WDL.
While these are functional specifications, they should not be considered feature complete, and they contain many bugs and irregularities.

- [draft-3](https://github.com/openwdl/wdl/blob/main/versions/draft-3/SPEC.md)
- [draft-2](https://github.com/openwdl/wdl/blob/main/versions/draft-2/SPEC.md)
- [draft-1](https://github.com/openwdl/wdl/blob/main/versions/draft-1/SPEC.md)

The next *minor* version of the specification is [1.2](https://github.com/openwdl/wdl/blob/wdl-1.2/SPEC.md).
All development of new *non-breaking* features should be done against that branch.

The next *major* version of the specification is [2.0](https://github.com/openwdl/wdl/blob/wdl-2.0/SPEC.md).
All development of new *breaking* features should be done against that branch.

## Community and Support

The WDL community depends on your involvement to thrive.
You are encouraged to ask questions, help other users, and make contributions where you can.
Interactions occur primarily on [GitHub](https://github.com/openwdl/wdl) and [Slack](https://join.slack.com/t/openwdl/shared_invite/zt-ctmj4mhf-cFBNxIiZYs6SY9HgM9UAVw).
The WDL community also has an official [blog](https://dev.to/openwdl) where announcements are made.

### Asking a Question

- Search in the [discussions](https://github.com/openwdl/wdl/discussions) to see if the question has been asked already; if not, start a new discussion.
- Join our [Slack](https://join.slack.com/t/openwdl/shared_invite/zt-ctmj4mhf-cFBNxIiZYs6SY9HgM9UAVw) and ask in the `#support` channel.
- Search the [Bioinformatics Stack Exchange](https://bioinformatics.stackexchange.com/search?q=wdl) for previously answered questions, or ask a new question. 
- Search the [Google Group](https://groups.google.com/a/openwdl.org/forum/#!forum/community) for previously answered questions. This group is largely inactive, so you're encoraged to ask new questions in one of the above places instead.

### Bugs and New Features

- Search for an existing [issue](https://github.com/openwdl/wdl/issues). If your issue has not already been reported, create a new one.
- For feature reqeusts, you are encoraged to first start a discussion at one of the places listed above to get feedback from the community.
- If you'd like to provide a fix/implementation for an issue, please read about [contributing](#contributing) before submitting a [pull request](https://github.com/openwdl/wdl/pulls).

### Documentation

- [wdl-docs](https://docs.openwdl.org/en/stable/)
- [learn-wdl](https://github.com/openwdl/learn-wdl)
- [WDL Resources](https://support.terra.bio/hc/en-us/sections/360007274612-WDL-Documentation) provided by Terra (a product of the Broad Institute)

## Published Workflows 

The following are collections of open-source WDL workflows.
The WDL task or workflow you need may already be available in one of these repositories, or you may find a similar workflow and customize it to your needs.

- [Dockstore](https://dockstore.org/search?entryType=workflows&descriptorType=WDL&searchMode=files)
- [BioWDL](https://github.com/biowdl)
- [Broad Institute WARP](https://broadinstitute.github.io/warp/docs/get-started/)
- [GATK Workflows](https://github.com/gatk-workflows/)
- [ENCODE](https://www.encodeproject.org/pipelines/)
- [Terra](https://app.terra.bio) (requires registration)

## Software and Tools

### Execution Engines and Platforms

WDL does not have an official implementation.
Third parties are relied upon to provide installable software or hosted platforms that interpret and execute WDL workflows and tasks.
Although WDL does not yet have an official compliance program or certification process, implementers are expected to design their tools according to the specification so as to maximize the portability of workflows across implementations.
Nonetheless, implementers may provide additional optional features specific.
Please see the documentation associated with each tool/platform for information on available execution options and support.

| Implementation                                                                 | Requires Installation | Local Execution | HPC   | Cloud                 |
| ------------------------------------------------------------------------------ | --------------------- | --------------- | ----- | --------------------- |
| [AWS HealthOmics](https://docs.aws.amazon.com/omics/latest/dev/workflows.html) | Yes                   | No              | No    | AWS                   |
| [Cromwell](https://github.com/broadinstitute/cromwell) *                       | Yes                   | Yes             | Many  | AWS Batch, Azure, GCP |
| [dxCompiler](https://github.com/dnanexus/dxCompiler)                           | Yes                   | No              | No    | DNAnexus              |
| [MiniWDL](https://github.com/chanzuckerberg/miniwdl)                           | Yes                   | Yes             | SLURM | AWS Batch             |
| [Terra](https://terra.bio/)                                                    | No                    | No              | No    | Azure, GCP            |

\* Also see [WDL Runner](https://github.com/broadinstitute/wdl-runner), a script for launch WDL workflows on GCP using Cromwell

### Grammars, Parsers, and Language Support

- The WDL [parsers repository](https://github.com/openwdl/wdl-parsers/) provides grammar definitions in various formats and generated parsers for various languages.
- [MiniWDL](https://github.com/chanzuckerberg/miniwdl) provides python bindings for WDL as well as commandline tools for validation, linting, and generating workflow input templates.
- [WOMTool](https://cromwell.readthedocs.io/en/stable/WOMtool/) is a standalone Java tool for WDL parsing, validating, linting, and diagramming.
- [wdlTools](https://github.com/dnanexus/wdlTools) - provides 1) a parser Java/Scala library, based on the  [ANTLR4 grammars](https://github.com/openwdl/wdl-parsers) grammars, for WDL draft-2, 1.0, 1.1, and 2.0; and 2) command-line tools for sytanx checking, type-checking, linting, code formatting (including upgrading from older to newer WDL versions), generating documentation, and executing WDL tasks locally.

### IDE Support

| IDE                | Tool                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| Emacs              | [poly-wdl](https://github.com/jmonlong/poly-wdl)                                                 |
| Emacs              | [wdl-mode](https://github.com/zhanxw/wdl-mode)                                                   |
| JetBrains          | [Winstanly](https://plugins.jetbrains.com/plugin/8154-winstanley-wdl)                            |
| Sublime            | [WDL Syntax Highlighter](https://github.com/broadinstitute/wdl-sublime-syntax-highlighter)       |
| Vim                | [vim-wdl](https://github.com/broadinstitute/vim-wdl)                                             |
| Visual Studio Code | [WDL Syntax Highlighter](https://marketplace.visualstudio.com/items?itemName=broadinstitute.wdl) |

### Documentation

- [wdl-aid](https://github.com/biowdl/wdl-aid) generates documentation for the inputs of WDL workflows, based on the parameter_meta information defined in the WDL file.	
- [wdldoc](https://github.com/stjudecloud/wdldoc)

### Testing

- [wdl-tests](https://github.com/openwdl/wdl-tests) is a collection of test cases for WDL implementations. A specification is provided for writing new tests that are compatible with automated testing frameworks.
- [Pytest-workflow](https://github.com/LUMC/pytest-workflow) is a implementation-agnostic workflow tester. It can be used with both Cromwell and MiniWDL. Uses pytest as the underlying test framework. Tests can be specified in either YAML format or python code.
- [Pytest-wdl](https://github.com/EliLillyCo/pytest-wdl) is a plugin for the pytest unit testing framework that enables testing of WDL tasks and workflows. Tests can be specified in either YAML format or python code.

### Packaging

- [miniwdl zip](https://miniwdl.readthedocs.io/en/latest/zip.html) generates a ZIP file including a given WDL source code file and any other WDL files it imports. The ZIP file can be supplied directly to miniwdl run, which can extract it automatically.
- [wdl-packager](https://github.com/biowdl/wdl-packager) packages a workflow and all of its imports into a zip file. The zip can be used as an imports zip package for cromwell. The utility can add non-WDL files (such as the license) to the zip package and provides options to package the zip in a binary reproducible way.

## Contributing

WDL only advances through community contributions.
While participating in discussions and submitting issues are great ways to be involved, help is also needed to implement changes to the specification.
For more information on how you can contribute, please read the [Contributing](CONTRIBUTING.md) guide.

### RFC Process

Submitted [pull requests](https://github.com/openwdl/wdl/pulls) are subject to the [RFC Process](RFC.md).
Please review and familiarize yourself with the process if you would like to see changes submitted to the specification.

## Governance

The WDL specification is entirely community driven; however, it is overseen by a [Governance committee](GOVERNANCE.md).
If you are interested in being involved in WDL governance, please join the [Slack](https://join.slack.com/t/openwdl/shared_invite/zt-ctmj4mhf-cFBNxIiZYs6SY9HgM9UAVw) and post a message in the `#general` channel.
