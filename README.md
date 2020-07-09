Workflow Description Language (WDL)
========================================

The **Workflow Description Language (WDL)** is a way to specify data processing workflows with a human-readable and writeable syntax. WDL makes it straightforward to define complex analysis tasks, chain them together in workflows, and parallelize their execution. The language makes common patterns simple to express, while also admitting uncommon or complicated behavior; and strives to achieve portability not only across execution platforms, but also different types of users. Whether one is an analyst, a programmer, an operator of a production system, or any other sort of user, WDL should be accessible and understandable.

# Language Specifications:

The current version of the WDL language is **1.0**. The [1.0 specification](https://github.com/openwdl/wdl/blob/main/versions/1.0/SPEC.md) contains all relevant information for users, developers, and engine developers. Upcoming features which have previously been accepted can be viewed as part of the [development spec](https://github.com/openwdl/wdl/blob/main/versions/development/SPEC.md). 

There are a number of draft versions (draft 1 - 3) which correspond to our initial efforts at creating WDL. While these are functional specifications, they should not be considered feature complete and contain many bugs and irregularities. Unless absolutely necessary, we would recommend that users should start with the current version of the language.


# Community and Support

There are a number of places to ask questions and get involved within the WDL community. Our community thrives the more you get involved and we encourage you to ask questions, provide answers, and make contributions.


- [Mailing list](https://groups.google.com/a/openwdl.org/forum/#!forum/community) - Joining our google group allows you to stay up to date with recent developments, be informed when new PR's are ready for voting, and participate in broader discussions about the language.
- [Issues](https://github.com/OpenWDL/wdl/issues) - Any bugs, ambiguity, or problems with the specification you encounter should be reported here. You can also create issues which are feature requests, however the most likely way to get a feature into the spec is by creating a PR yourself.
- [Slack Channel](https://join.slack.com/t/openwdl/shared_invite/zt-ctmj4mhf-cFBNxIiZYs6SY9HgM9UAVw) - Live chat with WDL users
- [Support Forum](https://bioinformatics.stackexchange.com/search?q=wdl) - View Previously answered questions about WDL or pose new questions. 
- [User Guide](https://support.terra.bio/hc/en-us/sections/360007274612-WDL-Documentation) (hosted by the Broad) View a general user guide and simple how-to for WDL

# Published Workflows 

There are many WDL's that have previously been published which provide a good starting point to extend or use as is to fit your workflow needs. While many of these workflows are scattered across the web and in many different repositories, you can find a great selection of high quality, published WDL's available at [Dockstore](https://dockstore.org/search?_type=workflow&descriptorType=wdl&searchMode=files) as well as a large number of workflows and tasks at [BioWDL](https://github.com/biowdl).

Additionally, you can view and test out a number of different workflow's using [Terra](https://app.terra.bio). Please note, that you have to register with Terra in order to view the workflows.


# Software and Tools

### Execution Engines

WDL is not executable in and of itself, but requires an execution engine to run. Compliant executions engines should support the features of a specific version of the WDL specification. Please see the corresponding engine documentation for information on available execution options and support. 

- [Cromwell](https://github.com/broadinstitute/cromwell)
- [MiniWDL](https://github.com/chanzuckerberg/miniwdl)
- [dxWDL](https://github.com/dnanexus/dxWDL)


### Parsers and Language Support

- Basic parsers and their grammar definitions (based on hermes) can be found in the `parsers/` directory for each respective version. Currently there is support for java, python and javascript. We believe these parsers work, however have not validated these claims.
- [MiniWDL](https://github.com/chanzuckerberg/miniwdl) - MiniWDL provides python bindings for WDL as well as command line validation. It is light weight and easy to use.
- [WOMTool](https://cromwell.readthedocs.io/en/stable/WOMtool/) - a standalone tool for parsing, validating, linting, and generating a graph of a WDL.
- [wdl-aid](https://github.com/biowdl/wdl-aid) - generate documentation for the inputs of WDL workflows, based on the parameter_meta information defined in the WDL file.	

### IDE Support

- Visual Studio Code: [WDL Syntax Highlighter](https://marketplace.visualstudio.com/items?itemName=broadinstitute.wdl)
- JetBrains IDE's: [Winstanly](https://plugins.jetbrains.com/plugin/8154-winstanley-wdl)
- Atom: [Language-WDL](https://atom.io/packages/language-wdl)
- Vim: [vim-wdl](https://github.com/broadinstitute/vim-wdl)

### Test tools

- [Pytest-workflow](https://github.com/LUMC/pytest-workflow) - workflow-engine agnostic workflow tester. Can be used with both Cromwell and MiniWDL. Tests are specified in YAML format. Uses pytest as underlying test framework. Allows for using python 
code tests in case the standard simple YAML tests are not sufficient.
- [Pytest-wdl](https://github.com/EliLillyCo/pytest-wdl) This package is a plugin for the pytest unit testing framework that enables testing of workflows written in Workflow Description Language.

# Contributing

WDL only advances through community contributions. While submitting an issue is a great way to report a bug in the spec, or create disscussion around current or new features, it will ultimately not translate into an actual change in the spec. The best way to make changes is by submitting a PR. For more information on how you can contribute, please see the [Contributing](CONTRIBUTING.md) readme. 

Additionally, once a PR has been submitted, it will be subjected to our [RFC Process](RFC.md).

# Governance

The WDL specification is entirely community driven, however it is overseen by a governance committee. For more information please see the [Governance](GOVERNANCE.md) documentation.

# RFC Process

Any changes submitted to the WDL Specification are subject to the [RFC Process](RFC.md). Please review and familiarize yourself with the process if you would like to see changes submitted to the specification.
