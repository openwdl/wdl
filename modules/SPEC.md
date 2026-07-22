# WDL Module Specification

This is version 1.0.0 of the WDL Module Specification. It defines the structure of a WDL module, the manifest format (`module.json`), the lockfile format (`module-lock.json`), dependency resolution, content hashing, module signing, credential management, and expectations placed on compliant execution engines.

This document is a peer specification to [`SPEC.md`](../SPEC.md), the WDL language specification. The language specification defines the `from` import syntax and the scoping rules that apply to symbolic imports; this specification defines how symbolic module paths resolve to WDL documents.

## Table of Contents

- [Introduction](#introduction)
- [Module Directory Layout](#module-directory-layout)
- [Module File Tree Constraints](#module-file-tree-constraints)
- [Manifest File (`module.json`)](#manifest-file-modulejson)
  - [Core Fields](#core-fields)
  - [Tools](#tools)
  - [Dependencies](#dependencies)
  - [Full Example](#full-example)
  - [Notes on the Manifest Format](#notes-on-the-manifest-format)
- [Module Entrypoint](#module-entrypoint)
- [Symbolic Module Paths](#symbolic-module-paths)
- [Resolution](#resolution)
  - [Version Discovery](#version-discovery)
  - [Transitive Dependencies](#transitive-dependencies)
  - [Cycle Detection](#cycle-detection)
  - [Version Precedence](#version-precedence)
  - [Version Resolution and Conflicts](#version-resolution-and-conflicts)
  - [Resource Limits](#resource-limits)
- [Lockfile (`module-lock.json`)](#lockfile-module-lockjson)
- [Content Hashing](#content-hashing)
- [Module Signing](#module-signing)
- [Credential Management](#credential-management)
- [API Stability Guidance](#api-stability-guidance)
- [Engine Tooling Expectations](#engine-tooling-expectations)
- [Appendix: Rationale](#appendix-rationale)

## Introduction

A WDL **module** is a directory containing a `module.json` manifest and one or more `.wdl` files. A module declares its dependencies, license, and the upstream tools it wraps; a module's own version is defined by its Git tags (see [Version Discovery](#version-discovery)). Modules are resolved and composed by compliant execution engines through the mechanisms defined in this specification.

Modules are independent of WDL version. The `.wdl` files within a module may use any WDL version, including versions earlier than 1.4, and consumers of those files are subject to the version-compatibility rule in [`SPEC.md`](../SPEC.md#import-statements) at each import site. Symbolic import syntax is available only in documents with `version` 1.4 or later, so a module composed entirely of pre-1.4 documents cannot reference its declared dependencies and can participate in a dependency tree only as a leaf.

This specification describes:

- The required directory layout for a module.
- The structure and fields of the `module.json` manifest.
- The entrypoint convention by which consumers reach a module's public surface.
- The resolution algorithm for symbolic module paths, including version discovery from Git tags.
- The `module-lock.json` format that pins a fully resolved dependency tree.
- The deterministic content-hashing algorithm used by both the lockfile and module signatures.
- The Ed25519 signing scheme for module provenance.
- Credential management for private repositories.
- The minimum functionality compliant engines must provide.

The language-level grammar for symbolic imports, and the scoping rules that govern the names brought into scope by those imports, are defined in [`SPEC.md`](../SPEC.md).

## Module Directory Layout

A module is a directory containing a `module.json` manifest at its root and one or more `.wdl` files. There is no additional organizational construct—no workspace type, no grouping file, no hierarchy requirement. This specification defines the logical module tree that engines consume; archive formats for distributing that tree, such as zipped module bundles, are intentionally left to future tooling as long as they materialize the same files and metadata.

Each dependency declared by a consumer points to exactly one module folder: the directory containing that module's `module.json`. A repository may host a single module at its root or several modules in distinct subdirectories, but a single dependency entry never resolves to more than one module. To consume multiple modules from the same repository, declare each as its own dependency, distinguished by the `path` field (see [Path within a Repository](#path-within-a-repository)).

A single-module repository:

```
csvcut-wdl/
  module.json
  index.wdl
  csvcut.wdl
```

A multi-module repository:

```
openwdl-tasks/
  csvkit/
    module.json
    index.wdl
    cut.wdl
    grep.wdl
    sort.wdl
    stats.wdl
  duckdb/
    module.json
    index.wdl
    duckdb.wdl
  jq/
    module.json
    index.wdl
    jq.wdl
```

Both layouts are valid. The resolution logic is identical for both. Authors who require fine-grained independent versioning may split modules further; authors who prefer fewer manifests may group related tasks under a single `module.json`.

## Module File Tree Constraints

The structural rules below are normative.

1. Each file's relative path (computed per [Content Hashing](#content-hashing)) is treated as a sequence of `/`-separated components. The path must contain no `.` or `..` components, must not be absolute (no leading `/`, no Windows-style drive letter), and must not contain a null byte.
2. Symbolic links are not permitted anywhere in a module tree. A module containing a symbolic link is invalid.
3. The names `module.json`, `module-lock.json`, and `module.sig` are reserved for files at the module root. A file with any of these names appearing at any other path within the module tree is a validation error.
4. A quoted import inside a module must resolve to a file inside the same module root. An import such as `import "../shared.wdl"` that escapes the module root makes the module invalid, even if the target file exists on disk.
5. A module that, when materialized on disk, would produce any path failing these rules is invalid; engines must refuse to load it and surface a clear error identifying the offending entry.

## Manifest File (`module.json`)

The manifest file for a module is always located at the module's root directory with the name `module.json`. It is a JSON document containing the fields described in the subsections below. A companion JSON Schema is available at [`schemas/module.schema.json`](schemas/module.schema.json).

### Core Fields

- **`name`** (string, required). A human-readable display name for the module (e.g., `"csvcut"`, `"csvkit-sort"`). Used by tooling for display. Not used for dependency resolution.
- **`license`** (string, required). An [SPDX license expression](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/) (e.g., `"MIT"`, `"Apache-2.0"`, `"MIT OR Apache-2.0"`, `"MIT AND (Apache-2.0 WITH LLVM-exception)"`).
- **`authors`** (array of strings, optional). Author descriptions. The convention for individual authors is `"First Last <first.last@example.com>"`, but this is not enforced.
- **`description`** (string, optional). A brief description of what the module does.
- **`repository`** (string, optional). The canonical Git URL for the module's source repository.
- **`homepage`** (string, optional). A URL for the module's documentation or landing page, if distinct from the repository. Use this for external documentation; `readme` is only for documentation files that ship inside the module tree.
- **`entrypoint`** (string, optional). Path to the module's entrypoint WDL file. The path must be relative and, after resolving any `.` or `..` components, must point to a location under the module root; absolute paths (leading `/` or a Windows-style drive letter) and paths that resolve outside the module root are not permitted. The path separator is `/`. Defaults to `index.wdl` if omitted.
- **`readme`** (string or `false`, optional). Path to a markdown file. The path must be relative and, after resolving any `.` or `..` components, must point to a location under the module root; absolute paths (leading `/` or a Windows-style drive letter) and paths that resolve outside the module root are not permitted. The path separator is `/`. If omitted, engines and tooling look for `README.md` in the module directory. If set to `false`, no readme is associated with the module.
- **`exclude`** (array of strings, optional). A list of gitignore-style glob patterns identifying files within the module that consumers may not reach via symbolic import. Each pattern must be a relative path that, after resolving any `.` or `..` components, points to a location under the module root. Absolute paths (leading `/` or a Windows-style drive letter) and patterns that resolve outside the module root are not permitted. The path separator is `/`. Plain directory names exclude the directory and everything beneath it; `*` matches any sequence of non-separator characters; `**` matches any sequence including separators. The patterns govern the public import surface only and have no effect on content hashing, signing, validation, packaging, or quoted imports within the module itself. See [Symbolic Module Paths](#symbolic-module-paths) for the resolution behavior. Defaults to the empty list.

### Tools

The `tools` field is an array of objects that tracks the upstream software wrapped by the module. Each entry records:

- **`name`** (string, required). The tool name.
- **`version`** (string, required). The tool version.
- **`license`** (string, required). The tool's SPDX license identifier.
- **`url`** (string, optional). URL for the tool's homepage, documentation, repository, or canonical project page.
- **`ids`** (array of strings, optional). External identifiers for the tool. Each entry is a [CURIE](https://www.w3.org/TR/curie/) of the form `prefix:reference`, using a prefix registered with [identifiers.org](https://identifiers.org/) or the [Bioregistry](https://bioregistry.io/) (e.g., `"doi:10.21105/joss.04704"`, `"biotools:csvkit"`).

The `tools` array is metadata: it describes which version of the upstream software the module wraps, for provenance and license tracking. It does not substitute for the module's own semver version. If the wrapped tool changes in a way that alters expected output, the module version must also change, independent of the `tools` entry.

### Dependencies

The `dependencies` field is a JSON object with one key per dependency. Each key must match `[A-Za-z][A-Za-z0-9_-]*` and, after replacing every `-` with `_`, must be a valid WDL identifier (i.e., not a reserved keyword). Hyphens and underscores are interchangeable for the purpose of identity: `spell-book` and `spell_book` name the same dependency and must not both appear in a single `dependencies` object. The key is the **consumer-chosen name** and need not match the dependency's own `name` field; two consumers may refer to the same module by different local names without ambiguity.

Each dependency must specify a source and a version selector. A dependency with a `git` URL and no `version`, `tag`, `branch`, or `commit` is invalid.

#### Version Requirements (Default)

The recommended form declares a **`version`** field containing a semver requirement, written without a `v` prefix (e.g. `"^1.2.0"`, not `"v1.2.0"`). The resolver lists the repository's Git tags, keeps those of the form `v<semver>`—the `v` prefix is required on the tag, not on this requirement (see [Version Discovery](#version-discovery))—and selects the highest tagged version that satisfies the requirement.

The version requirement syntax:

- **`^1.2.0`** — compatible updates. Versions are compatible when they differ only to the right of the leftmost non-zero component: `^1.2.0` is `>=1.2.0, <2.0.0`, `^0.2.3` is `>=0.2.3, <0.3.0`, and `^0.0.3` is `>=0.0.3, <0.0.4`. This is the default behavior when no operator is specified, i.e., `"1.2.0"` is equivalent to `"^1.2.0"`.
- **`~1.2.0`** — patch-level updates only: `>=1.2.0, <1.3.0`.
- **`=1.2.0`** — exactly this version.
- **`>=1.0.0, <2.0.0`** — an explicit range using comparison operators (`>=`, `>`, `<=`, `<`), combined with commas.
- **`*`** — any version. Permitted but discouraged.

A requirement may omit trailing version components. Missing components are treated as `0` in the lower bound, while the upper bound follows from the components given: `^1` is `>=1.0.0, <2.0.0`, `~1.2` is `>=1.2.0, <1.3.0`, `~1` is `>=1.0.0, <2.0.0`, and `=1.2` is `>=1.2.0, <1.3.0`.

Example:

```json
{
  "dependencies": {
    "csvkit": { "git": "https://git.openwdl.org/someone/csvkit-wdl", "version": "^1.2.0" },
    "openwdl": { "git": "https://git.openwdl.org/openwdl/tasks", "version": ">=2.0.0, <3.0.0" }
  }
}
```

#### Alternative Version Selectors

For cases where semver requirements do not suffice (pre-release testing, pinning to a specific commit, tracking a development branch), the following alternative selectors are available:

- **`tag`** — a specific Git tag name (e.g., `"v1.2.0-rc1"`). Not subject to semver resolution.
- **`branch`** — a Git branch name. The resolved commit varies over time; the lockfile pins the exact commit SHA at resolution time.
- **`commit`** — a Git commit SHA selector. Any prefix that uniquely identifies a commit in the source repository is accepted; the resolver expands the prefix to the full 40-character SHA at lock time and records that value in `module-lock.json`. The most precise and immutable selector.

The four selectors—`version`, `tag`, `branch`, and `commit`—are mutually exclusive. Specifying more than one on a single dependency is invalid.

```json
{
  "dependencies": {
    "bleeding_edge": { "git": "https://git.openwdl.org/org/tool", "branch": "main" },
    "pinned": { "git": "https://git.openwdl.org/org/tool", "commit": "abc123d" },
    "prerelease": { "git": "https://git.openwdl.org/org/tool", "tag": "v2.0.0-rc1" }
  }
}
```

#### Local Path Dependencies

A dependency with a **`path`** key points to a local filesystem directory. Local path dependencies take no version selector; the module is used as-is from the local path. The target directory must be a module root: it must contain its own `module.json` and satisfies all module validation rules independently. A `path` dependency does not extend the consuming module's boundary; it names a separate module, exactly as a `git` dependency does.

```json
{
  "dependencies": {
    "local_utils": { "path": "../../shared/utils" }
  }
}
```

#### Path within a Repository

For Git dependencies, an optional **`path`** key names the directory within the repository that contains the module's `module.json`. The dependency resolves to that directory and only that directory. The path must be relative and, after resolving any `.` or `..` components, must point to a location under the repository root; absolute paths (leading `/` or a Windows-style drive letter) and paths that resolve outside the repository root are not permitted. The path separator is `/`. To consume multiple modules from the same repository, declare each as its own dependency, each with a different `path` value.

```json
{
  "dependencies": {
    "mytool": { "git": "https://git.openwdl.org/org/mytool", "version": "^1.0.0", "path": "wdl" }
  }
}
```

A complete `dependencies` object may mix selector styles and source types:

```json
{
  "dependencies": {
    "csvkit": { "git": "https://git.openwdl.org/openwdl/tasks", "version": "^1.2.0", "path": "csvkit" },
    "duckdb": { "git": "https://git.openwdl.org/openwdl/tasks", "tag": "duckdb/v3.0.1", "path": "duckdb" },
    "local_utils": { "path": "../local-utils" }
  }
}
```

### Full Example

```json
{
  "name": "csvcut",
  "license": "MIT OR Apache-2.0",
  "authors": ["Jane Doe <jane.doe@example.com>"],
  "description": "WDL wrapper for csvcut column selection",
  "repository": "https://git.openwdl.org/someone/csvcut-wdl",
  "homepage": "https://csvcut-wdl.someone.example.com",
  "tools": [
    {
      "name": "csvcut",
      "version": "2.0.1",
      "license": "MIT",
      "url": "https://csvkit.readthedocs.io/",
      "ids": ["doi:10.21105/joss.04704", "biotools:csvkit"]
    }
  ],
  "dependencies": {}
}
```

### Notes on the Manifest Format

- JSON was chosen for consistency with other WDL-associated configuration (e.g., input files) and because it is broadly supported.
- The `name` field is for display only. It plays no role in dependency resolution; consumers name each dependency locally in their own `module.json`. This eliminates global namespace management and the associated squatting problem.
- The `readme` field defaults to `README.md` if omitted.
- Engines **must ignore unrecognized fields** anywhere in `module.json`—at the top level, within `tools` entries, within `dependencies` entries, and in any nested object—rather than treating them as errors. This allows the format to evolve; new optional fields can be added without breaking older engines.
- Engines must parse `module.json` strictly, per [RFC 8259](https://datatracker.ietf.org/doc/html/rfc8259). Duplicate keys within any object, trailing commas, comments, leading byte-order marks, and any other non-JSON extension are validation errors and must be rejected. The same parsing requirements apply to `module-lock.json`. Strict parsing eliminates ambiguity—different parsers must produce identical document trees—and prevents attacks that hide overrides behind tolerated parser quirks.

## Module Entrypoint

Every module designates an **entrypoint** WDL file. By default, the entrypoint is `index.wdl` at the module root. Authors may override this by setting the `entrypoint` field in `module.json` to a different path relative to the module root. The override is intended for cases where the default name conflicts with domain terminology (e.g., a module wrapping a database indexing tool may prefer `db_index.wdl` to avoid confusion with the module entrypoint).

The default name `index.wdl` mirrors package index conventions: it names the file that represents the directory as a whole. A module that prefers `main.wdl` or another project-specific name can use the `entrypoint` field without changing resolution semantics.

The entrypoint provides the module's **default surface**: when a consumer writes a **root module import** of the dependency (`import samtools`, with no sub-path), the engine resolves the import to the entrypoint file. The entrypoint file uses ordinary quoted imports to pull in its sibling files, exactly as defined in [`SPEC.md`](../SPEC.md#-import-forms), and the names brought into its scope become the surface that root module consumers see. Tasks and workflows enter that scope only through the scope-merging forms (`import * from`, `import { ... } from`); a form 1 (namespaced) import contributes the user-defined types it copies into scope, while its tasks and workflows remain referenceable only by namespace within the entrypoint and are not part of the module's surface.

The entrypoint is the default surface, not a privacy boundary. Consumers may also import individual files within the module folder by sub-path (see [Symbolic Module Paths](#symbolic-module-paths)); such imports do not pass through the entrypoint, and any `.wdl` file in the module folder is reachable in this way. Authors who wish to mark certain files as internal should list them in the manifest's `exclude` field, which removes the matched paths from the public import surface (see [Core Fields](#core-fields)).

If a consumer writes a root module import and the entrypoint file does not exist at the resolved path, the engine must refuse to proceed and surface an error; the wording and presentation of that error are engine-specific. This error is raised at import time, not at manifest validation time; a manifest with no `entrypoint` field and no `index.wdl` on disk is valid until something tries to resolve a root module import against it.

A minimal module places its tasks, workflows, and user-defined types directly in the entrypoint:

```
csvcut/
  module.json
  index.wdl
```

A consumer with a dependency named `csvcut` then chooses how to bring those names into scope using the import forms defined in [`SPEC.md`](../SPEC.md#-import-forms):

```wdl
version 1.4

import csvcut              # tasks/workflows reachable as `csvcut.*`; UDTs in scope unqualified
import * from csvcut       # tasks, workflows, and UDTs all in scope unqualified, no namespace
```

A module with multiple files curates its default surface by importing them from the entrypoint with the scope-merging forms:

```wdl
version 1.4

import * from "sort.wdl"
import * from "grep.wdl"
import { cut_columns } from "cut.wdl"
```

Names brought into the entrypoint's scope this way become members of the entrypoint's namespace, so they are exactly what an `import csvcut` consumer reaches as `csvcut.*` (or unqualified, via `import * from csvcut`). A namespaced (form 1) import in the entrypoint contributes only the user-defined types it copies into scope; the namespace it creates is local to the entrypoint, and tasks and workflows behind it do not propagate to consumers. Files the entrypoint does not import are still reachable via sub-path imports; the entrypoint's import list controls only what `import csvcut` (without a sub-path) brings into scope.

A module may also omit the entrypoint entirely and rely solely on sub-path imports:

```
csvcut/
  module.json
  sort.wdl
  grep.wdl
  cut.wdl
```

With this layout, `import csvcut` raises the missing-entrypoint error described above, but each individual file remains reachable by sub-path:

```wdl
version 1.4

import csvcut/sort
import csvcut/grep as search
import csvcut/cut
```

This shape suits modules whose surface is a flat collection of independent units that consumers always pick from explicitly.

## Symbolic Module Paths

A **symbolic module path** is the unquoted path used in a symbolic import (see [`SPEC.md`](../SPEC.md#-import-forms) for grammar). It has the general form:

```
<dep-name>[/<sub-path>]
```

- **`<dep-name>`** is the key under which the consumer declared the dependency in their `module.json`, with any hyphens normalized to underscores. It must not contain `/`.
- **`<sub-path>`** (optional) is a `/`-separated file path within the dependency's module folder. The resolver appends `.wdl` to the joined path and reads that file directly, without consulting the entrypoint.

If `<sub-path>` is omitted, the import resolves to the module's entrypoint (see [Module Entrypoint](#module-entrypoint)).

The `<dep-name>` component must satisfy the dependency-name grammar described in [Dependencies](#dependencies); engines normalize it (replacing `-` with `_`) before looking up the dependency. Each component of `<sub-path>` must be a valid WDL identifier, per the symbolic module path grammar in [`SPEC.md`](../SPEC.md). Empty components, leading or trailing `/`, `.`, `..`, whitespace, null bytes, and any other character not permitted in a WDL identifier are themselves not permitted in a symbolic module path.

Sub-path components are matched against file and directory names with the same normalization applied to `<dep-name>`: a component matches a directory entry whose name, after replacing every `-` with `_`, equals the component (with `.wdl` appended for the final component). The component `my_task` therefore matches either `my_task.wdl` or `my-task.wdl`. If more than one entry in the same directory matches a component, resolution fails with an ambiguity error naming the matching entries.

A sub-path may not escape the dependency's module folder. The identifier-only component rule already forbids `..`, so a path such as `samtools/../another_file` is rejected at parse time rather than being resolved against the surrounding repository. This guarantee is normative: engines may rely on it to fetch only the module folder—via sparse Git checkout, partial clone, or any other mechanism that omits the rest of the repository—without risk that a symbolic import will later require content outside that folder.

Sub-path resolution is a direct file lookup. Intermediate directories along the sub-path do not need to contain `module.json` files, and any nested `module.json` files that happen to be present along the way are ignored.

If the manifest's `exclude` field matches the path that resolution would otherwise read—either the entrypoint file for a root module import or `<sub-path>.wdl` for a sub-path import—the engine must treat the import as unresolvable and surface a missing-file error that names the path. An excluded path is not part of the module's public import surface. `exclude` is an import-surface policy, not a filesystem security boundary: it controls resolution through symbolic module paths, but it does not hide bytes from a user who already has direct access to the module source. Excluding the entrypoint therefore makes root module imports of that dependency fail while leaving non-excluded files reachable by sub-path. Quoted imports inside the module (e.g., the entrypoint's own `import "helper.wdl"`) are file-relative and are unaffected by `exclude`.

Path components are case-sensitive. A symbolic path whose resolved file does not exist on disk is a resolution error; the engine must surface an appropriate error.

## Resolution

When a parser encounters a symbolic import, resolution proceeds as follows:

1. Split the module path on the first `/`. The left side is the dependency name; the right side (if any) is the sub-path within the dependency.
2. Look up the dependency name in the consuming module's `module.json` under `dependencies`.
3. Resolve the source: clone the Git repository at the selected version, or read the directory referenced by a local `path`. The dependency's **module folder** is the source root, narrowed to the directory named by the dependency's optional `path` field if present. The module folder must contain a `module.json`.
4. If no sub-path was given, locate the module's entrypoint file: the path named by the manifest's `entrypoint` field, or `<module-folder>/index.wdl` if the field is absent. If the manifest's `exclude` field matches that path, treat the file as unresolvable and raise a missing-file error per [Symbolic Module Paths](#symbolic-module-paths). Otherwise, if the file does not exist on disk, raise the dedicated missing-entrypoint error described in [Module Entrypoint](#module-entrypoint).
5. If a sub-path was given, append `.wdl` to the sub-path and locate `<module-folder>/<sub-path>.wdl`, matching each component with the hyphen normalization described in [Symbolic Module Paths](#symbolic-module-paths). If the manifest's `exclude` field matches the resolved path, or no entry matches, raise a missing-file resolution error that names the path. The entrypoint is not consulted in this branch.
6. Parse the resolved file and resolve the requested name against its scope according to the symbolic import rules in [`SPEC.md`](../SPEC.md#-import-forms). The resolved file is subject to the language specification's version-compatibility rule for imports: it must have the same major version and a minor version less than or equal to that of the importing document. A dependency authored against a newer minor version therefore fails at import time, regardless of how it was resolved.

These steps describe the logical behavior that compliant engines must produce. Implementation mechanics—caching strategies, scan ordering, eager vs. lazy fetching—are left to the engine.

### Version Discovery

How versions are discovered depends on the source type.

For **Git-based dependencies**, the resolver lists the repository's Git tags and considers those of the form `v<semver>` (e.g., tag `v1.2.0` → version `1.2.0`). The `v` prefix is required: a tag without it, or whose remainder does not parse as valid semver, is not a version tag and is ignored. The resulting set is matched against the `version` requirement. Publishing a new version therefore consists of tagging a commit; there is no separate publication step, no upload, no registry submission.

Git tags are the sole source of module versions. The versioning contract is that unchanged versions must produce unchanged expected output: a change to the WDL interface (inputs, outputs, behavior) or to the wrapped tool's output behavior requires tagging a new version.

**Multi-module repositories.** A repository containing multiple independently versioned modules must use path-prefixed tags, following the convention established by [Go modules](https://go.dev/doc/modules/managing-source). For a module at path `foo/` relative to the repository root, version tags take the form `foo/v1.2.0`. For modules at the repository root, tags use the unprefixed form `v1.2.0`. When discovering versions for a module at path `P`, the resolver filters to tags matching `P/v*` (or `v*` if `P` is the root) and ignores all others.

A repository containing `csvkit/` at version `1.2.0` and `duckdb/` at version `3.0.1` would therefore have tags `csvkit/v1.2.0` and `duckdb/v3.0.1`.

**Tag mutability.** Git tags are mutable and may be force-pushed to a different commit. The lockfile (see [Lockfile](#lockfile-module-lockjson)) guards against this by pinning the full commit SHA and a content checksum for every resolved module. After a lockfile exists, engines verify against the SHA and checksum rather than the tag. Tag movement can only affect initial resolution; the content hash ensures that what was fetched is what is evaluated. Engines should warn when a tag's commit differs from the `sha` recorded in the lockfile.

**Local path dependencies** have no version discovery; the module at the specified path is used as-is.

### Transitive Dependencies

Dependencies are fully transitive. If module A depends on module B and B depends on C, the resolver walks the full tree.

### Cycle Detection

A dependency cycle exists when, during resolution, the resolver re-enters a module it is already in the process of resolving along the current path through the dependency tree. For cycle detection, module identity is the module's source coordinates—the Git repository URL and `path` for Git sources, or the resolved directory for local path sources—irrespective of version or selector. Cycles are not permitted: a module may not transitively depend on itself, even at a different version. Engines must detect cycles during resolution and refuse to proceed.

### Version Precedence

Version precedence follows [SemVer v2.0.0, section 11](https://semver.org/#spec-item-11). When multiple tags satisfy a version requirement, the resolver selects the highest version according to semver precedence rules. Build metadata (anything following `+`) is ignored for precedence purposes.

### Version Resolution and Conflicts

When multiple modules in the dependency tree require the same dependency with compatible version constraints (e.g., `^1.2.0` and `^1.5.0`), the resolver should attempt to find a single version satisfying all constraints. This avoids unnecessary duplication.

When the constraints are incompatible (e.g., `^1.0.0` and `^2.0.0`), both versions are fetched and used independently. No deduplication is attempted and no warning is emitted. WDL modules are text files, and the tasks they define execute in isolated containers with no shared runtime state; no conflict can arise from duplicate versions coexisting. The cost of duplication is a few kilobytes of WDL source per duplicate.

### Resource Limits

Resolution consumes network and disk resources whose size is controlled by upstream repositories rather than the consumer. Engines may impose upper bounds on resolution-time resource use—tag count, repository size, file count, dependency depth, or any other dimension that proves problematic in practice—and report a clear error identifying the offending dependency when a bound is exceeded. The specific limits, and whether any are enforced at all, are an engine concern.

## Lockfile (`module-lock.json`)

A `module-lock.json` file, if present at a module's root, pins the fully resolved dependency tree—every module in the tree, the exact commit each was resolved to, and a content checksum that detects tampering. Modules whose consumers need reproducible builds should maintain a lockfile; modules intended as libraries, where version resolution is deliberately left to the consumer, may omit it. When a lockfile exists, it must be committed to version control.

Engines are responsible for upholding lockfile invariants. Before executing a workflow that imports a module with a lockfile, the engine must verify that each cached Git-sourced module's content matches the recorded checksum and refuse to proceed on mismatch. Local path sources carry no checksum; their content is read as-is at execution time.

The engine must also verify that the lockfile matches its manifest: every dependency declared in `module.json` must have a lockfile entry whose source and selector match the declaration, and every top-level lockfile entry must correspond to a declared dependency. A lockfile that does not match its manifest is stale; the engine must regenerate it, or surface an error, before executing. Engines that perform dependency resolution are also responsible for generating and updating the lockfile so its content remains consistent with the resolved tree.

Lockfiles apply only to the module they sit in. When resolving dependencies, the engine consults the consuming module's `module.json` constraints and, if present, the consumer's own `module-lock.json`; lockfiles shipped by upstream dependencies are not consulted. There is therefore no lockfile conflict between a consumer and a dependency: the consumer's resolver owns the full tree it records, and an upstream lockfile is ignored during downstream resolution. This keeps consumers in control of their transitive version choices and prevents upstream version decisions from silently propagating through the dependency tree.

Cached module sources (the local directories where resolved modules are downloaded or cloned) must **not** be committed. These are ephemeral and can be reconstructed from the lockfile. This specification does not prescribe where engines store the cache. An engine may keep it inside the project directory (e.g., under a `modules/` subdirectory by default, covered by `.gitignore`) or outside it (e.g., under a user-level global cache); the choice is an engine concern.

A companion JSON Schema is available at [`schemas/module-lock.schema.json`](schemas/module-lock.schema.json).

### Lockfile Format

The `module-lock.json` file is a JSON object with the following structure:

```json
{
  "version": 1,
  "dependencies": {
    "openwdl": {
      "source": {
        "git": "https://git.openwdl.org/openwdl/tasks",
        "sha": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
        "selector": {"version": "^1"},
        "path": "csvcut"
      },
      "checksum": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "signer": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIN3kJh1mYpQ9...",
      "dependencies": {
        "common": {
          "source": {
            "git": "https://git.openwdl.org/openwdl/common",
            "sha": "d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5",
            "selector": {"version": "^0.3"}
          },
          "checksum": "sha256:4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865",
          "dependencies": {}
        }
      }
    },
    "duckdb": {
      "source": {
        "git": "https://git.openwdl.org/someone/duckdb-wdl",
        "sha": "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3",
        "selector": {"tag": "v3.0.1"}
      },
      "checksum": "sha256:d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
      "dependencies": {}
    },
    "local_utils": {
      "source": {
        "path": "../../shared/utils"
      },
      "dependencies": {}
    }
  }
}
```

The structure is recursive: each dependency's `dependencies` field has the same shape as the top-level `dependencies` object, mirroring the full dependency tree. A dependency resolves to exactly one module, so the module's checksum and transitive dependencies sit directly on the dependency entry rather than behind an intermediate map.

The fields:

- **`version`** (integer, required). The lockfile format version. Currently `1`. Engines must reject lockfiles with an unrecognized version.
- **`dependencies`** (object, required). A map from consumer-chosen dependency name (matching the key in the consuming `module.json`) to its resolved state.

Each dependency entry contains:

- **`source`** (object, required). The resolved source. For Git sources, this contains `git` (the repository URL), `sha` (the full 40-character commit SHA that the `tag`, `branch`, or `commit` selector resolved to at lock time), `selector` (the selector from the consuming `module.json` that produced this entry, encoded as an object with a single key of `version`, `tag`, `branch`, or `commit`), and optionally `path` (the sub-path within the repository, matching the `path` key in the consuming `module.json` dependency declaration; omitted when the module sits at the repository root). For local path sources, this contains only `path`.
- **`checksum`** (string, required for Git sources). The module's content hash in the format `sha256:<hex_digest>`, computed using the content hashing algorithm defined in [Content Hashing](#content-hashing). Absent for local path sources.
- **`signer`** (string, optional; Git sources only). The signer's Ed25519 public key in OpenSSH public key format (see [Signature File Format](#signature-file-format)), if the module was signed at lock time. See [Module Signing](#module-signing).
- **`dependencies`** (object, required). The module's own transitive dependencies, in the same format as the top-level `dependencies` object. Empty if the module has no dependencies.

When two modules in the dependency tree require different versions of the same source, both resolved versions appear in the tree at whatever point in the nesting they were required. See [Version Resolution and Conflicts](#version-resolution-and-conflicts) for the resolver's behavior that produces this shape.

## Content Hashing

Both the lockfile checksum and module signatures depend on the same deterministic content hash. All compliant engines must produce the same digest for the same module contents.

The algorithm:

1. Enumerate all files in the module directory, recursively. Exclude `module.sig`, `module-lock.json`, any entry named `.git` (and, when it is a directory, everything beneath it), and any engine-managed cache or scratch directory the engine writes inside the module tree (and everything beneath it). An engine that materializes its dependency cache inside the module tree (see [Lockfile](#lockfile-module-lockjson)) must exclude that directory from hashing and must keep it out of version control, so that a distributed module never contains it and the digest of the distributed content remains identical across engines.
2. Compute each file's relative path from the module root using `/` as the path separator, regardless of the host operating system. Normalize each relative path to Unicode Normalization Form C (NFC) before any further use. If two distinct entries normalize to the same NFC form, the module is invalid.
3. Sort the file list lexicographically by relative path, comparing UTF-8 byte values of the NFC-normalized paths.
4. Initialize a SHA-256 hasher.
5. Hash the magic sequence: the literal ASCII bytes `wdl-module-content`, a single `\0` byte, the literal ASCII bytes `v1`, and a single `\0` byte (22 bytes total). The first field is the protocol identifier; the second is the algorithm version.
6. For each file in sorted order:
   a. Hash the byte length of the relative path as a little-endian 64-bit unsigned integer.
   b. Hash the relative path (UTF-8 bytes).
   c. Hash the byte length of the file contents as a little-endian 64-bit unsigned integer.
   d. Hash the file contents (raw bytes).
7. Hash the total file count as a little-endian 64-bit unsigned integer.
8. Finalize. The resulting hex-encoded digest is the module's content hash.

The magic sequence in step 5 prevents cross-protocol confusion: a digest produced by this algorithm cannot collide with a digest produced by a different algorithm that uses SHA-256 over different framing. The length prefixes in step 6 and the file count in step 7 together make the rest of the input an injective encoding of the module's contents: no two distinct modules can produce the same byte stream. Without length framing, a file `foo.wdl` containing `bar` and a file `foo.wdlbar` containing nothing would feed identical bytes into the hasher; with length framing, the two encodings differ on their first eight bytes.

The lockfile records the digest in the format `sha256:<hex_digest>`.

### Integrity: Lockfile Checksums

The `module-lock.json` checksum field provides tamper detection. Once a module is resolved and its checksum recorded, any modification to the cached content—whether by a compromised cache, a man-in-the-middle, or a corrupted download—is detectable. Engines must verify checksums against the lockfile before using cached modules. If the checksum does not match, the engine must refuse to proceed.

## Module Signing

Module ecosystems are targets for supply chain attacks: compromised repositories, force-pushed tags, impersonated maintainers. The signing model defined here addresses content tampering and maintainer impersonation without requiring centralized infrastructure. Signing is optional but encouraged.

### Signature File Format

Module authors sign a module by producing a `module.sig` file at the module root. It is a JSON file containing an Ed25519 signature computed over the domain-separated payload defined in [Signature Payload Encoding](#signature-payload-encoding), which encodes the module's content hash and optional identity metadata.

```json
{
  "public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIN3kJh1mYpQ9...",
  "identity": {
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "signature": "base64-encoded-64-byte-signature"
}
```

The fields:

- **`public_key`** (string, required). The signer's Ed25519 public key in OpenSSH public key format—the single-line `ssh-ed25519 <base64-blob> [comment]` representation produced by `ssh-keygen -t ed25519` (i.e., the contents of the corresponding `.pub` file). Engines must parse the OpenSSH wire format inside the base64 blob to recover the underlying 32-byte Ed25519 public key for verification. Trailing whitespace and the optional comment field are not significant.
- **`identity`** (object, optional). Human-readable metadata associated with the signing key. The object contains either the required string fields `name` and `email`, or the single required string field `comment`. Engines may parse an OpenSSH public key comment that exactly matches `Name <email>` into `name` and `email`; otherwise, they may preserve the complete public key comment in `comment`. Engines may display this metadata in trust prompts, lockfile verification reports, and trust-store listings. The identity is authenticated by the module signature, so changing its representation or any value invalidates verification. Identity metadata remains informational and must not replace public-key matching or determine trust; the signing key asserts the identity, but the protocol does not independently validate the assertion. Each string must be non-empty, contain at most 256 Unicode scalar values, and contain no Unicode control characters.
- **`signature`** (string, required). The Ed25519 signature over the payload defined in [Signature Payload Encoding](#signature-payload-encoding), base64-encoded.

A signed module looks like:

```
csvcut/
  module.json
  module.sig
  index.wdl
  csvcut.wdl
```

Ed25519 was chosen because it is fast, produces small signatures (64 bytes) and small keys (32 bytes), and has mature implementations in every major language. Engines can verify signatures in-process without shelling out to external tools or depending on a system keychain. Keys are stored in OpenSSH public key format so authors generate signing keys with the standard `ssh-keygen -t ed25519` tool and reuse the resulting `.pub` file directly; the OpenSSH wire format inside the base64 blob is short, well-specified, and supported by mainstream cryptography libraries.

### Signature Payload Encoding

The Ed25519 signature covers this exact byte sequence, without separators other than the field framing defined below:

1. The 27 ASCII bytes `openwdl.module-signature.v1`.
2. The raw 32-byte SHA-256 module content digest.
3. One identity discriminant byte followed by the fields selected by that discriminant.

The identity discriminant and its fields encode as follows:

- `0x00` represents an absent `identity` and has no following fields.
- `0x01` represents a signer identity and is followed by the encoded `name` and then the encoded `email`.
- `0x02` represents an unstructured identity and is followed by the encoded `comment`.

Each string encodes as its UTF-8 byte length as an unsigned 64-bit little-endian integer, followed by exactly that many UTF-8 bytes. The `openwdl.module-signature.v1` domain prefix prevents cross-protocol confusion, while the discriminant and length framing prevent both representation ambiguity and field-boundary ambiguity.

#### Test Vector

```text
digest: 32 bytes, each 0x42
identity.name: Jane Doe
identity.email: jane@example.com
payload length: 100 bytes
payload hex:
6f70656e77646c2e6d6f64756c652d7369676e61747572652e763142424242424242424242424242424242424242424242424242424242424242420108000000000000004a616e6520446f6510000000000000006a616e65406578616d706c652e636f6d
```

```text
digest: 32 bytes, each 0x42
identity.comment: release signer
payload length: 82 bytes
payload hex:
6f70656e77646c2e6d6f64756c652d7369676e61747572652e76324242424242424242424242424242424242424242424242424242424242424242020e0000000000000072656c65617365207369676e6572
```

### Trust on First Use (TOFU)

The trust model follows trust on first use:

1. On first resolution, if `module.sig` is present, the engine reconstructs the payload from the module's content digest and the `identity` fields (if present), verifies the signature against that payload, and records the signer's public key in `module-lock.json` under the module entry's `signer` field. If the signature file also contains `identity`, the engine may copy it into a user-level trust store when the signer key is accepted.
2. On subsequent resolutions, the engine verifies the signature matches the previously recorded key.
3. If the signing key has changed, the engine must **refuse to proceed** and surface a clear warning explaining what happened. The engine may proceed only after the user explicitly accepts the new key through an engine-defined trust mechanism. This protects against compromised repositories where an attacker replaces both content and signature.
4. If a module was unsigned on first resolution and later becomes signed, the engine records the key going forward without disruption.
5. If a previously signed module is later resolved without a `module.sig`, the engine must treat that result as a trust-relevant downgrade and refuse to proceed, exactly as if the signing key had changed. The engine may proceed only after the user explicitly accepts the downgrade. Accepting the downgrade authorizes the engine to update `module-lock.json` to record the module as unsigned; it must not revoke or remove the signer key from any user-level or global trust store, because that key may still sign other modules.

The lockfile `signer` field is absent for unsigned modules and for local path dependencies, which are not subject to signature verification.

When one resolution or lockfile update observes multiple signer transitions, the engine must evaluate them as one atomic batch. If policy refuses any transition, the engine must reject the entire batch, must not update either user trust state or `module-lock.json`, and must not prompt for acceptances that could not make the batch succeed. If the user declines the batch, the engine must accept none of the transitions and must not update either user trust state or `module-lock.json`.

A legitimate key rotation is indistinguishable from a compromise at the protocol level; the engine cannot tell them apart, so the user must. Authors rotating a signing key should announce the new key through a channel consumers already trust, such as the repository's README or a release note, so that users have something to verify against before accepting the new key.

### Engine Policy

Engines are encouraged to:

- Surface a notice when resolving unsigned modules, nudging authors toward signing.
- Provide a configuration option (e.g., `require_signed = true`) that rejects unsigned modules entirely. Whether this defaults to on or off is left to the engine implementor.

## Credential Management

Engines must rely on the user's configured Git credential helpers for authentication to private repositories. If the user's `git` command can clone a repository, module resolution from that repository must succeed without additional configuration. Engines must not introduce a new credential store or configuration format specifically for module resolution.

This approach works with SSH keys, personal access tokens, and platform-specific credential managers (macOS Keychain, Windows Credential Manager, etc.) without modification. Most developers and CI systems already have Git credentials configured, and any such configuration applies to module resolution automatically.

## API Stability Guidance

This section is non-normative.

A common cause of avoidable major version bumps in WDL modules is the addition of required task inputs. Under semver, adding a required input is a breaking change, and every downstream consumer that calls the task must update.

The remedy is to prefer **optional inputs** with sensible defaults wherever possible. WDL supports this well. A task wrapping `csvcut`, for example, might initially expose only the required flags. When `csvcut` adds a new `--no-header-row` option, the WDL wrapper should add an optional input with a default value rather than a required input. Existing consumers continue to work unchanged, and the module version bump is minor rather than major.

Module authors are encouraged to default to optional inputs for any parameter that has a reasonable default, reserving required inputs for genuinely mandatory parameters (e.g., input files).

## Engine Tooling Expectations

Compliant engines must provide, at minimum, the following:

1. **Dependency resolution.** Given a module and its `module.json`, resolve all dependencies according to this specification and generate or update `module-lock.json` as required.
2. **Lockfile verification.** Before executing any workflow that imports a module, verify the content checksum of each cached module against the lockfile. Refuse to proceed on mismatch.
3. **Signature verification.** When a `module.sig` is present, reconstruct the payload from the module's content digest and `identity` fields per [Signature Payload Encoding](#signature-payload-encoding), verify the signature against that payload, compare the signer's public key against the lockfile entry, and enforce the trust-on-first-use contract.
4. **Structural validation.** Report clear errors for malformed `module.json` files, missing required fields, invalid SPDX license expressions, invalid semver version requirements, and unrecognized selectors.

Engines may additionally provide higher-level commands for authoring convenience (e.g., scaffolding, validation, upgrade). This specification does not prescribe the command surface; engine authors are free to design their own CLI.

## Appendix: Rationale

This appendix is non-normative. It preserves the design rationale behind decisions made during the RFC process so that future readers have context for the specification's shape.

**Distributed hosting over a centralized registry.** Git-based resolution was chosen over a central package server. The cost is discoverability—distributed systems are harder to search—which the ecosystem may address through community-maintained indexes outside the scope of this specification. The benefit is that no single organization can become a bottleneck or point of failure for the ecosystem. Environments that cannot depend on third-party SaaS can use this system unmodified.

**Versions from Git tags.** Following Go modules, a module's version is defined by its Git tags rather than a manifest field. A manifest version would duplicate the tag and require engines to detect and reject mismatches between the two; deriving the version from the tag alone leaves nothing to fall out of sync.

**Separate tool versioning.** The module version (defined by Git tags) and the upstream tool version (tracked in the `tools` field) are recorded in different places, but they are not independent. The module version contract is that unchanged versions must produce unchanged expected output; a tool update that alters output requires a module version bump. The `tools` array exists for provenance and license tracking, not as a substitute for proper semver on the module itself.

**Display name, not resolution name.** The `name` field exists for human consumption. It is not used for dependency resolution; the importer names each dependency locally. This eliminates global namespace management, the squatting problem, and the need for a naming authority.

**Out-of-band signing over Git-native signing.** Git tag signing would be simpler today, but it couples security to the transport mechanism. A `module.sig` file travels with the module regardless of distribution mechanism—Git clone, tarball, or any future format. The cost is a separate signing step; engines can reduce this to a single command.

**Trust on first use over a certificate authority.** TOFU has known downsides: the first resolution is unverified, key rotation requires manual acceptance, and there is no revocation mechanism. A PKI would address these but would require infrastructure and governance that a small open-source community cannot realistically sustain. TOFU protects against the most common attack—a repository compromised after adoption—and accepts the tradeoff that it cannot protect against pre-existing compromise.

**Optional signing with encouraged adoption.** Requiring signatures would be more secure but would raise the authoring barrier. Making it optional, with an engine-level policy that enforces it for security-conscious environments, preserves adoption while enabling strong policy where needed.

**Soft deprecation of remote URL imports.** A hard removal would strand existing workflows. Warnings give the ecosystem time to migrate while making the direction clear.
