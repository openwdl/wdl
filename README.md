Workflow Description Language (WDL)
========================================

The **Workflow Description Language (WDL)** is a way to specify data processing workflows with a human-readable and writeable syntax. WDL makes it straightforward to define complex analysis tasks, chain them together in workflows, and parallelize their execution. The language makes common patterns simple to express, while also admitting uncommon or complicated behavior; and strives to achieve portability not only across execution platforms, but also different types of users. Whether one is an analyst, a programmer, an operator of a production system, or any other sort of user, WDL should be accessible and understandable.

# Versioning

WDL versioning follows [semantic versioning](https://semver.org) conventions.

The WDL *language* has a two-number version (e.g., 1.1). An increase in the minor (second) version number (e.g., 1.0 to 1.1) indicates the addition of, or non-breaking changes to, the language or the standard library functions. An increase in the major (first) version number (e.g., 1.0 to 2.0) indicates that breaking changes have been made.

The WDL *specification* has a three-number version (e.g., 1.1.1). The specification version tracks the language version, but there may also be patch releases (indicated by a change to the patch, or third, version number) that include fixes for typos, additional examples, or non-breaking clarifications of ambiguous language.

# Language Specifications

The WDL specification contains all relevant information for users, developers, and engine developers. This GitHub project uses the branch for the current version of the specification as its primary branch, so you will always see the current version of the specification so long as you visit this project's [root URL](https://github.com/openwdl/wdl).

This branch is for version **1.1** of the [WDL language specification](https://github.com/openwdl/wdl/blob/wdl-1.1/SPEC.md).

Previous versions of the spec can be found here:

* [1.0](https://github.com/openwdl/wdl/blob/main/versions/1.0/SPEC.md)

There are a number of draft versions (draft 1 - 3) which correspond to our initial efforts at creating WDL. While these are functional specifications, they should not be considered feature complete and contain many bugs and irregularities. Unless absolutely necessary, we would recommend that users should start with the current version of the language.

* [draft-3](https://github.com/openwdl/wdl/blob/main/versions/draft-3/SPEC.md)
* [draft-2](https://github.com/openwdl/wdl/blob/main/versions/draft-2/SPEC.md)
* [draft-1](https://github.com/openwdl/wdl/blob/main/versions/draft-1/SPEC.md)

The next *minor* version of the specification is [1.2](https://github.com/openwdl/wdl/blob/wdl-1.2/SPEC.md). All development of new *non-breaking* features should be done against that branch.

The next *major* version of the specification is [2.0](https://github.com/openwdl/wdl/blob/wdl-2.0/SPEC.md). All development of new *breaking* features should be done against that branch.

# Community and Support

There are a number of places to ask questions and get involved within the WDL community. Our community thrives the more you get involved and we encourage you to ask questions, provide answers, and make contributions.

- [Mailing list](https://groups.google.com/a/openwdl.org/forum/#!forum/community) - Joining our google group allows you to stay up to date with recent developments, be informed when new PRs are ready for voting, and participate in broader discussions about the language.
- [GitHub](https://github.com/openwdl/wdl)
    - [Discussions](https://github.com/openwdl/wdl/discussions) - For discussing the specification, proposing syntax changes or additions to the standard library, and general Q&A.
    - [Issues](https://github.com/openwdl/wdl/issues) - Any bugs, ambiguity, or problems with the specification you encounter should be reported here. You can also create issues which are feature requests, however the most likely way to get a feature into the spec is by [creating a PR yourself](#contributing).
- [Slack Channel](https://join.slack.com/t/openwdl/shared_invite/zt-ctmj4mhf-cFBNxIiZYs6SY9HgM9UAVw) - Live chat with WDL users
- [Support Forum](https://bioinformatics.stackexchange.com/search?q=wdl) - View Previously answered questions about WDL or pose new questions. 
- [User Guide](https://wdl-docs.readthedocs.io/en/latest/) - View WDL tutorials, guides, cookbook-style how-to articles, and links to community resources (previously [hosted by the Broad](https://support.terra.bio/hc/en-us/sections/360007274612))

# Published Workflows 

There are many WDLs that have previously been published which provide a good starting point to extend or use as is to fit your workflow needs. While many of these workflows are scattered across the web and in many different repositories, you can find a great selection of high quality, published WDLs available at [Dockstore](https://dockstore.org/search?entryType=workflows&descriptorType=WDL&searchMode=files) as well as a large number of workflows and tasks at [BioWDL](https://github.com/biowdl).

Additionally, you can view and test out a number of different workflows using [Terra](https://app.terra.bio). Please note, that you have to register with Terra in order to view the workflows.

# Software and Tools

### Execution Engines

WDL is not executable in and of itself, but requires an execution engine to run. Compliant executions engines should support the features of a specific version of the WDL specification. Please see the corresponding engine documentation for information on available execution options and support. 

- [Cromwell](https://github.com/broadinstitute/cromwell)
- [MiniWDL](https://github.com/chanzuckerberg/miniwdl)
- [dxCompiler](https://github.com/dnanexus/dxCompiler)

### Parsers and Language Support

- Grammar definitions in various formats can be found in the `[grammars repository](https://github.com/openwdl/grammars/)`.
- [MiniWDL](https://github.com/chanzuckerberg/miniwdl) - MiniWDL provides python bindings for WDL as well as command line validation. It is light weight and easy to use.
- [WOMTool](https://cromwell.readthedocs.io/en/stable/WOMtool/) - a standalone tool for parsing, validating, linting, and generating a graph of a WDL.
- [wdl-aid](https://github.com/biowdl/wdl-aid) - generate documentation for the inputs of WDL workflows, based on the parameter_meta information defined in the WDL file.	
- [wdlTools](https://github.com/dnanexus/wdlTools) - provides 1) a parser library, based on the new [ANTLR4](https://github.com/openwdl/grammars/tree/main/antlr4) grammars, for WDL draft-2, 1.0, 1.1, and 2.0, and 2) command-line tools for sytanx checking, type-checking, linting, code formatting (including upgrading from older to newer WDL versions), generating documentation, and executing WDL tasks locally.

### IDE Support

- Visual Studio Code: [WDL Syntax Highlighter](https://marketplace.visualstudio.com/items?itemName=broadinstitute.wdl)
- JetBrains IDEs: [Winstanly](https://plugins.jetbrains.com/plugin/8154-winstanley-wdl)
- Atom: [Language-WDL](https://atom.io/packages/language-wdl)
- Vim: [vim-wdl](https://github.com/broadinstitute/vim-wdl)

### Documentation

- [wdldoc](https://github.com/stjudecloud/wdldoc)

### Test tools

- [Pytest-workflow](https://github.com/LUMC/pytest-workflow) - workflow-engine agnostic workflow tester. Can be used with both Cromwell and MiniWDL. Tests are specified in YAML format. Uses pytest as underlying test framework. Allows for using python 
code tests in case the standard simple YAML tests are not sufficient.
- [Pytest-wdl](https://github.com/EliLillyCo/pytest-wdl) This package is a plugin for the pytest unit testing framework that enables testing of workflows written in Workflow Description Language.

### Packaging

- [wdl-packager](https://github.com/biowdl/wdl-packager). WDL packaging utility that uses miniwdl to find which paths are imported and packages these into a zip 
  together with the calling workflow. The zip can be used as an imports zip package for cromwell. The utility can add non-WDL files (such as the license) to the
  zip package and provides options to package the zip in a binary reproducible way.

# Contributing

WDL only advances through community contributions. While submitting an issue is a great way to report a bug in the spec, or create discussion around current or new features, it will ultimately not translate into an actual change in the spec. The best way to make changes is by submitting a PR. For more information on how you can contribute, please see the [Contributing](CONTRIBUTING.md) readme. 

Additionally, once a PR has been submitted, it will be subjected to our [RFC Process](RFC.md).

# Governance

The WDL specification is entirely community driven, however it is overseen by a governance committee. For more information please see the [Governance](GOVERNANCE.md) documentation.

# RFC Process

Any changes submitted to the WDL Specification are subject to the [RFC Process](RFC.md). Please review and familiarize yourself with the process if you would like to see changes submitted to the specification.
