# Workflow Description Language Specification 

The WDL specification contains all relevant information for users, developers, and engine developers. It is versioned, meaning that when a certain amount of new features are added, a new version is released. WDL versioning follows semantic versioning conventions; non-breaking changes are added in "minor version" increments (eg 1.0 to 1.1), while breaking changes are added in "major version" increments (eg 1.0 to 2.0). 

The current released version is [WDL 1.1](https://github.com/openwdl/wdl/blob/main/versions/1.1/SPEC.md).

Upcoming features which have previously been accepted but are not yet part of the latest release can be viewed as part of the [development spec](https://github.com/openwdl/wdl/blob/main/versions/development/SPEC.md).

Since the release of WDL 1.0, execution engines require that every WDL file include a version statement as its first line of code, like this:

    version 1.0

Note that the version statement CAN be preceded by comments.

To propose changes to the WDL specification, please read the [contributions guide](https://github.com/openwdl/wdl/blob/main/CONTRIBUTING.md).
