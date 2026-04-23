# WDL Module Specification

This is version 1.0.0 of the WDL Module Specification. It defines the structure of a WDL module, the manifest format (`module.json`), the lockfile format (`module-lock.json`), dependency resolution, content hashing, module signing, credential management, and expectations placed on compliant execution engines.

This document is a peer specification to [`SPEC.md`](../SPEC.md), the WDL language specification. The language specification defines the `from` import syntax and the scoping rules that apply to symbolic imports; this specification defines how symbolic module paths resolve to WDL documents.

## Table of Contents

- [Introduction](#introduction)
- [Module Directory Layout](#module-directory-layout)
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
  - [Version Precedence](#version-precedence)
  - [Version Resolution and Conflicts](#version-resolution-and-conflicts)
- [Lockfile (`module-lock.json`)](#lockfile-module-lockjson)
- [Content Hashing](#content-hashing)
- [Module Signing](#module-signing)
- [Credential Management](#credential-management)
- [API Stability Guidance](#api-stability-guidance)
- [Engine Tooling Expectations](#engine-tooling-expectations)
- [Known Open Questions](#known-open-questions)
- [Appendix: Rationale](#appendix-rationale)

## Introduction

A WDL **module** is a directory containing a `module.json` manifest and one or more `.wdl` files. A module declares its own version, dependencies, license, and the upstream tools it wraps. Modules are resolved and composed by compliant execution engines through the mechanisms defined in this specification.

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

A module is a directory containing a `module.json` manifest at its root and one or more `.wdl` files. There is no additional organizational construct—no workspace type, no grouping file, no hierarchy requirement.

When the resolver encounters a dependency source (a Git repository or a local path), it scans the source tree for `module.json` files. Each such file identifies a module, registered at the path where it sits relative to the source root. A repository may therefore contain one module at the root, many modules in subdirectories, or any combination.

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

## Manifest File (`module.json`)

The manifest file for a module is always located at the module's root directory with the name `module.json`. It is a JSON document containing the fields described in the subsections below. A companion JSON Schema is available at [`schemas/module.schema.json`](schemas/module.schema.json).

### Core Fields

- **`name`** (string, required). A human-readable display name for the module (e.g., `"csvcut"`, `"csvkit-sort"`). Used by tooling for display. Not used for dependency resolution.
- **`version`** (string, required). The module version, conforming to [SemVer v2.0.0](https://semver.org/). The versioning contract is that unchanged versions must produce unchanged expected output. A change to the WDL interface (inputs, outputs, behavior) or to the wrapped tool's output behavior requires a version bump.
- **`license`** (string, required). An [SPDX license expression](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/) (e.g., `"MIT"`, `"Apache-2.0"`, `"MIT OR Apache-2.0"`, `"MIT AND (Apache-2.0 WITH LLVM-exception)"`).
- **`authors`** (array of strings, optional). Author descriptions. The convention for individual authors is `"First Last <first.last@example.com>"`, but this is not enforced.
- **`description`** (string, optional). A brief description of what the module does.
- **`repository`** (string, optional). The canonical Git URL for the module's source repository.
- **`homepage`** (string, optional). A URL for the module's documentation or landing page, if distinct from the repository.
- **`index`** (string, optional). Path to the module's entrypoint WDL file, relative to the module root. Defaults to `index.wdl` if omitted.
- **`readme`** (string, optional). Path to a markdown file relative to the module root. If omitted, engines and tooling look for `README.md` in the module directory. If set to `false`, no readme is associated with the module.

### Tools

The `tools` field is an array of objects that tracks the upstream software wrapped by the module. Each entry records:

- **`name`** (string, required). The tool name.
- **`version`** (string, required). The tool version.
- **`license`** (string, required). The tool's SPDX license identifier.
- **`homepage`** (string, optional). URL for the tool's homepage or repository.
- **`doi`** (string, optional). DOI for the tool's publication.
- **`biotools`** (string, optional). [bio.tools](https://bio.tools/) registry identifier.

The `tools` array is metadata: it describes which version of the upstream software the module wraps, for provenance and license tracking. It does not substitute for the module's own semver version. If the wrapped tool changes in a way that alters expected output, the module version must also change, independent of the `tools` entry.

### Dependencies

The `dependencies` field is a JSON object with one key per dependency. Each key must be a valid WDL identifier. The key is the **consumer-chosen name** and need not match the dependency's own `name` field; two consumers may refer to the same module by different local names without ambiguity.

Each dependency must specify a source and a version selector. A dependency with a `git` URL and no `version`, `tag`, `branch`, or `commit` is invalid.

#### Version Requirements (Default)

The recommended form declares a **`version`** field containing a semver requirement. The resolver lists Git tags from the repository, parses each as semver (stripping a leading `v` if present, e.g., `v1.2.0` → `1.2.0`), and selects the highest matching version.

The version requirement syntax:

- **`^1.2.0`** — compatible updates: `>=1.2.0, <2.0.0`. This is the default behavior when no operator is specified, i.e., `"1.2.0"` is equivalent to `"^1.2.0"`.
- **`~1.2.0`** — patch-level updates only: `>=1.2.0, <1.3.0`.
- **`=1.2.0`** — exactly this version.
- **`>=1.0.0, <2.0.0`** — an explicit range using comparison operators (`>=`, `>`, `<=`, `<`), combined with commas.
- **`*`** — any version. Permitted but discouraged.

Example:

```json
{
  "dependencies": {
    "csvkit": { "git": "https://github.com/someone/csvkit-wdl", "version": "^1.2.0" },
    "openwdl": { "git": "https://github.com/openwdl/tasks", "version": ">=2.0.0, <3.0.0" }
  }
}
```

#### Alternative Version Selectors

For cases where semver requirements do not suffice (pre-release testing, pinning to a specific commit, tracking a development branch), the following alternative selectors are available:

- **`tag`** — a specific Git tag name (e.g., `"v1.2.0-rc1"`). Not subject to semver resolution.
- **`branch`** — a Git branch name. The resolved commit varies over time; the lockfile pins the exact commit at resolution time.
- **`commit`** — a full Git commit SHA. The most precise and immutable selector.

The four selectors—`version`, `tag`, `branch`, and `commit`—are mutually exclusive. Specifying more than one on a single dependency is invalid.

```json
{
  "dependencies": {
    "bleeding_edge": { "git": "https://github.com/org/tool", "branch": "main" },
    "pinned": { "git": "https://github.com/org/tool", "commit": "abc123d" },
    "prerelease": { "git": "https://github.com/org/tool", "tag": "v2.0.0-rc1" }
  }
}
```

#### Local Path Dependencies

A dependency with a **`path`** key points to a local filesystem directory. No version selector is required; the module is used as-is from the local path.

```json
{
  "dependencies": {
    "local_utils": { "path": "../../shared/utils" }
  }
}
```

#### Path within a Repository

For Git dependencies, an optional **`path`** key sets the root directory for module scanning within the repository. This is useful when WDL modules live in a subdirectory alongside other files.

```json
{
  "dependencies": {
    "mytool": { "git": "https://github.com/org/mytool", "version": "^1.0.0", "path": "wdl" }
  }
}
```

### Full Example

```json
{
  "name": "csvcut",
  "version": "1.2.0",
  "license": "MIT OR Apache-2.0",
  "authors": ["Jane Doe <jane.doe@example.com>"],
  "description": "WDL wrapper for csvcut column selection",
  "repository": "https://github.com/someone/csvcut-wdl",
  "homepage": "https://someone.github.io/csvcut-wdl",
  "tools": [
    {
      "name": "csvcut",
      "version": "2.0.1",
      "license": "MIT",
      "homepage": "https://csvkit.readthedocs.io/"
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

## Module Entrypoint

Every module must contain an **entrypoint** WDL file at its root. By default, the entrypoint is `index.wdl`. Authors may override this by setting the `index` field in `module.json` to a different path relative to the module root. The override is intended for cases where the default name conflicts with domain terminology (e.g., a module wrapping a database indexing tool may wish to use `db_index.wdl` to avoid confusion with the module entrypoint).

The entrypoint defines the module's public surface. Its imports—and how those imports are written—determine what is visible to consumers. A file that the entrypoint does not import is private to the module and is not reachable from outside it. This provides visibility control without introducing a new access-control keyword.

The entrypoint itself uses ordinary quoted imports to pull in its sibling files, exactly as defined in [`SPEC.md`](../SPEC.md). Consumers of the module reach the resulting surface through symbolic imports (see [Symbolic Module Paths](#symbolic-module-paths) and the symbolic import forms in [`SPEC.md`](../SPEC.md)).

A minimal module:

```
csvcut/
  module.json
  index.wdl
  csvcut.wdl
```

Where `index.wdl` contains:

```wdl
version 1.4

import "csvcut.wdl"
```

The contents of `csvcut.wdl`—its tasks, workflows, and user-defined types—become available under the `csvcut` namespace to consumers using the associated rules outlined in [`SPEC.md`](../SPEC.md). A consumer imports the module symbolically:

```wdl
version 1.4

import openwdl/csvcut              # namespace: csvcut
# or: import openwdl/csvcut as csv  # namespace: csv
```

A module with multiple files controls its surface the same way:

```wdl
version 1.4

import "sort.wdl"
import "grep.wdl" as search
import "cut.wdl"
```

Here, `sort`, `search`, and `cut` are the three namespaces the module exposes. Internal helper files that `index.wdl` does not import remain private.

## Symbolic Module Paths

A **symbolic module path** is the unquoted path used in a symbolic import (see [`SPEC.md`](../SPEC.md#-symbolic-import-forms) for grammar). It has the general form:

```
<dep-name>[/<sub-path>]
```

- **`<dep-name>`** is the key under which the consumer declared the dependency in their `module.json`.
- **`<sub-path>`** (optional) is a `/`-separated path that addresses a specific module within a multi-module dependency source. It is the directory path, relative to the source root, that contains the target module's `module.json`.

If `<sub-path>` is omitted, the target module is the one whose `module.json` sits at the root of the dependency source.

Examples, given a consumer `module.json` with `"openwdl": { "git": "https://github.com/openwdl/tasks", "version": "^1.0.0" }`:

- `openwdl` refers to a module whose `module.json` lives at the root of `openwdl/tasks`.
- `openwdl/csvkit` refers to the module at `csvkit/module.json` within the same repository.
- `openwdl/csvkit/subtools` refers to a nested module at `csvkit/subtools/module.json` if one exists.

Path components are case-sensitive. A path that does not resolve to a discovered module is a resolution error.

## Resolution

When a parser encounters a symbolic import, resolution proceeds as follows:

1. Split the module path on the first `/`. The left side is the dependency name; the right side (if any) is the sub-path within the dependency.
2. Look up the dependency name in the consuming module's `module.json` under `dependencies`.
3. Resolve the source: clone the Git repository at the selected version, or read the directory referenced by a local `path`.
4. Scan the source recursively for `module.json` files, registering each as a module at its relative path.
5. Look up the sub-path (or the root module if no sub-path was given) in the registered modules.
6. Parse the target module's entrypoint (see [Module Entrypoint](#module-entrypoint)) and resolve the requested name against its scope according to the symbolic import rules in [`SPEC.md`](../SPEC.md#-symbolic-import-forms).

These steps describe the logical behavior that compliant engines must produce. Implementation mechanics—caching strategies, scan ordering, eager vs. lazy fetching—are left to the engine.

### Version Discovery

How versions are discovered depends on the source type.

For **Git-based dependencies**, the resolver lists the repository's Git tags and parses each as a semver version, stripping a leading `v` if present (e.g., tag `v1.2.0` → version `1.2.0`). Tags that do not parse as valid semver are ignored. The resulting set is matched against the `version` requirement. Publishing a new version therefore consists of tagging a commit; there is no separate publication step, no upload, no registry submission.

**Tag-to-manifest consistency.** The `version` field in `module.json` at the tagged commit must match the version encoded in the tag (after stripping `v` and any path prefix). A tag `v1.2.0` pointing to a commit whose `module.json` declares `"version": "1.3.0"` is a validation error. Engines must reject such mismatches during resolution and surface a clear error message that suggests either downgrading to a known-good version or filing an issue on the upstream repository.

**Multi-module repositories.** A repository containing multiple independently versioned modules must use path-prefixed tags, following the convention established by [Go modules](https://go.dev/doc/modules/managing-source). For a module at path `foo/` relative to the repository root, version tags take the form `foo/v1.2.0`. For modules at the repository root, tags use the bare form `v1.2.0`. When discovering versions for a module at path `P`, the resolver filters to tags matching `P/v*` (or `v*` if `P` is the root) and ignores all others.

A repository containing `csvkit/` at version `1.2.0` and `duckdb/` at version `3.0.1` would therefore have tags `csvkit/v1.2.0` and `duckdb/v3.0.1`.

**Tag mutability.** Git tags are mutable and may be force-pushed to a different commit. The lockfile (see [Lockfile](#lockfile-module-lockjson)) guards against this by pinning the full commit SHA and a content checksum for every resolved module. After a lockfile exists, engines verify against the SHA and checksum rather than the tag. Tag movement can only affect initial resolution; the content hash ensures that what was fetched is what is evaluated. Engines should warn when a tag's commit differs from the SHA recorded in the lockfile.

For **local path dependencies**, the resolver reads the `version` field from the `module.json` at the specified path. If the dependency declaration includes a `version` requirement, the local module's version must satisfy it; otherwise resolution fails.

### Transitive Dependencies

Dependencies are fully transitive. If module A depends on module B and B depends on C, the resolver walks the full tree.

### Version Precedence

Version precedence follows [SemVer v2.0.0, section 11](https://semver.org/#spec-item-11). When multiple tags satisfy a version requirement, the resolver selects the highest version according to semver precedence rules. Build metadata (anything following `+`) is ignored for precedence purposes.

### Version Resolution and Conflicts

When multiple modules in the dependency tree require the same dependency with compatible version constraints (e.g., `^1.2.0` and `^1.5.0`), the resolver should attempt to find a single version satisfying all constraints. This avoids unnecessary duplication.

When the constraints are incompatible (e.g., `^1.0.0` and `^2.0.0`), both versions are fetched and used independently. No deduplication is attempted and no warning is emitted. WDL modules are text files, and the tasks they define execute in isolated containers with no shared runtime state; no conflict can arise from duplicate versions coexisting. The cost of duplication is a few kilobytes of WDL source per duplicate.

## Lockfile (`module-lock.json`)

A `module-lock.json` file, if present at a module's root, pins the fully resolved dependency tree—every module in the tree, the exact commit each was resolved to, and a content checksum that detects tampering. Modules whose consumers need reproducible builds should maintain a lockfile; modules intended as libraries, where version resolution is deliberately left to the consumer, may omit it. When a lockfile exists, it must be committed to version control.

Engines are responsible for upholding lockfile invariants. Before executing a workflow that imports a module with a lockfile, the engine must verify that each cached module's content matches the recorded checksum and refuse to proceed on mismatch. Engines that perform dependency resolution are also responsible for generating and updating the lockfile so its content remains consistent with the resolved tree.

Lockfiles apply only to the module they sit in. When resolving dependencies, the engine consults the consuming module's `module.json` constraints and, if present, the consumer's own `module-lock.json`; lockfiles shipped by upstream dependencies are not consulted. This keeps consumers in control of their transitive version choices and prevents upstream version decisions from silently propagating through the dependency tree.

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
        "git": "https://github.com/openwdl/tasks",
        "commit": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
      },
      "modules": {
        "csvcut": {
          "version": "1.2.0",
          "checksum": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "dependencies": {
            "common": {
              "source": {
                "git": "https://github.com/openwdl/common",
                "commit": "d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5"
              },
              "modules": {
                ".": {
                  "version": "0.3.0",
                  "checksum": "sha256:4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865",
                  "dependencies": {}
                }
              }
            }
          }
        }
      }
    },
    "duckdb": {
      "source": {
        "git": "https://github.com/someone/duckdb-wdl",
        "commit": "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3"
      },
      "modules": {
        ".": {
          "version": "3.0.1",
          "checksum": "sha256:d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
          "dependencies": {}
        }
      }
    },
    "local_utils": {
      "source": {
        "path": "../../shared/utils"
      },
      "modules": {
        ".": {
          "version": "0.5.0",
          "checksum": "sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
          "dependencies": {}
        }
      }
    }
  }
}
```

The structure is recursive: each module's `dependencies` field has the same shape as the top-level `dependencies` object, mirroring the full dependency tree.

The fields:

- **`version`** (integer, required). The lockfile format version. Currently `1`. Engines must reject lockfiles with an unrecognized version.
- **`dependencies`** (object, required). A map from consumer-chosen dependency name (matching the key in the consuming `module.json`) to its resolved state.

Each dependency entry contains:

- **`source`** (object, required). The resolved source. For Git sources, this contains `git` (the repository URL) and `commit` (the full 40-character SHA that the `tag`, `branch`, or `commit` reference resolved to at lock time). For local path sources, this contains only `path`.
- **`modules`** (object, required). A map from module path within the dependency source to that module's locked state. The key is the relative path from the source root to the directory containing `module.json`. For modules at the source root, the key is `"."`.

Each module entry contains:

- **`version`** (string, required). The version from the module's `module.json` at lock time.
- **`checksum`** (string, required). The module's content hash in the format `sha256:<hex_digest>`, computed using the content hashing algorithm defined in [Content Hashing](#content-hashing).
- **`signer`** (string, optional). The signer's Ed25519 public key, base64-encoded, if the module was signed at lock time. See [Module Signing](#module-signing).
- **`dependencies`** (object, required). The module's own transitive dependencies, in the same format as the top-level `dependencies` object. Empty if the module has no dependencies.

When two modules in the dependency tree require different versions of the same source, both resolved versions appear in the tree at whatever point in the nesting they were required. See [Version Resolution and Conflicts](#version-resolution-and-conflicts) for the resolver's behavior that produces this shape.

## Content Hashing

Both the lockfile checksum and module signatures depend on the same deterministic content hash. All compliant engines must produce the same digest for the same module contents.

The algorithm:

1. Enumerate all files in the module directory, recursively. Exclude `module.sig` and `module-lock.json`.
2. Compute each file's relative path from the module root using `/` as the path separator, regardless of the host operating system.
3. Sort the file list lexicographically by relative path, comparing UTF-8 byte values.
4. Initialize a SHA-256 hasher.
5. For each file in sorted order:
   a. Hash the relative path (UTF-8 bytes).
   b. Hash the file contents (raw bytes).
6. Hash the total file count as a little-endian 64-bit unsigned integer.
7. Finalize. The resulting hex-encoded digest is the module's content hash.

The entry count in step 6 ensures that a module with files `a` and `bc` produces a different digest than a module with files `ab` and `c`, even if the concatenation of paths and contents happens to collide.

The lockfile records the digest in the format `sha256:<hex_digest>`.

### Integrity: Lockfile Checksums

The `module-lock.json` checksum field provides tamper detection. Once a module is resolved and its checksum recorded, any modification to the cached content—whether by a compromised cache, a man-in-the-middle, or a corrupted download—is detectable. Engines must verify checksums against the lockfile before using cached modules. If the checksum does not match, the engine must refuse to proceed.

## Module Signing

Module ecosystems are targets for supply chain attacks: compromised repositories, force-pushed tags, impersonated maintainers. The signing model defined here addresses content tampering and maintainer impersonation without requiring centralized infrastructure. Signing is optional but encouraged.

### Signature File Format

Module authors sign a module by producing a `module.sig` file at the module root. It is a JSON file containing an Ed25519 signature computed over the module's content hash (the raw 32-byte SHA-256 digest produced by the algorithm in [Content Hashing](#content-hashing), not the hex-encoded string).

```json
{
  "algorithm": "ed25519",
  "public_key": "base64-encoded-32-byte-public-key",
  "signature": "base64-encoded-64-byte-signature"
}
```

The fields:

- **`algorithm`** (string, required). The signing algorithm. The only value currently permitted is `"ed25519"`. Future specification versions may add additional algorithms; engines must reject unrecognized values.
- **`public_key`** (string, required). The signer's Ed25519 public key, base64-encoded.
- **`signature`** (string, required). The Ed25519 signature over the module's raw 32-byte content hash, base64-encoded.

A signed module looks like:

```
csvcut/
  module.json
  module.sig
  index.wdl
  csvcut.wdl
```

Ed25519 was chosen because it is fast, produces small signatures (64 bytes) and small keys (32 bytes), and has mature implementations in every major language. Engines can verify signatures in-process without shelling out to external tools or depending on a system keychain.

### Why Out-of-Band Rather than Git-Native Signing

Git tag and commit signing would be simpler today: authors already sign tags, and engines could verify them directly. Git signatures, however, couple the security model to the transport mechanism. If modules are ever distributed as tarballs, through a package server, or through any non-Git mechanism, Git signatures do not travel with the content. A `module.sig` file does. The cost is a separate signing step; the benefit is a security model that survives changes to distribution infrastructure.

### Trust on First Use (TOFU)

The trust model follows trust on first use:

1. On first resolution, if `module.sig` is present, the engine verifies the signature and records the signer's public key in `module-lock.json` under the module entry's `signer` field.
2. On subsequent resolutions, the engine verifies the signature matches the previously recorded key.
3. If the signing key has changed, the engine must **refuse to proceed** and surface a clear warning explaining what happened. The user must explicitly accept the new key through an engine-specific command (e.g., `sprocket module trust openwdl/csvcut`). This protects against compromised repositories where an attacker replaces both content and signature.
4. If a module was unsigned on first resolution and later becomes signed, the engine records the key going forward without disruption.

The lockfile `signer` field is absent for unsigned modules.

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
3. **Signature verification.** When a `module.sig` is present, verify the signature against the module's content hash, compare the signer's public key against the lockfile entry, and enforce the trust-on-first-use contract.
4. **Structural validation.** Report clear errors for malformed `module.json` files, missing required fields, invalid SPDX license expressions, invalid semver versions, tag-to-manifest version mismatches, and unrecognized selectors.

Engines may additionally provide higher-level commands for authoring convenience (e.g., scaffolding, validation, upgrade). This specification does not prescribe the command surface; engine authors are free to design their own CLI.

Semantic annotation of task inputs and outputs (e.g., file format, ontology terms from EDAM) is a complementary concern and out of scope for this specification. Standardized `parameter_meta` conventions for declaring input/output formats would help tooling match compatible tasks and are worth pursuing as a separate effort.

## Known Open Questions

The following concerns are acknowledged but not resolved in this version of the specification. They are listed here so future revisions can track and address them.

- **Cascaded importing of WDL documents through the dependency tree, while decoupling version requirements from source code.** The current specification requires consumers to explicitly declare every module they import directly. An open question is whether, and how, a module should be able to re-export or surface its dependencies' entrypoints so that consumers can reach them without redeclaring the transitive dependency. The challenge is to do so without reintroducing the version-coupling problem that the module system was designed to eliminate.

## Appendix: Rationale

This appendix is non-normative. It preserves the design rationale behind decisions made during the RFC process so that future readers have context for the specification's shape.

**Distributed hosting over a centralized registry.** Git-based resolution was chosen over a central package server. The cost is discoverability—distributed systems are harder to search—which the ecosystem may address through community-maintained indexes outside the scope of this specification. The benefit is that no single organization can become a bottleneck or point of failure for the ecosystem. Environments that cannot depend on third-party SaaS can use this system unmodified.

**Separate tool versioning.** The module version and the upstream tool version are tracked in distinct fields, but they are not independent. The module version contract is that unchanged versions must produce unchanged expected output; a tool update that alters output requires a module version bump. The `tools` array exists for provenance and license tracking, not as a substitute for proper semver on the module itself.

**Display name, not resolution name.** The `name` field exists for human consumption. It is not used for dependency resolution; the importer names each dependency locally. This eliminates global namespace management, the squatting problem, and the need for a naming authority.

**Out-of-band signing over Git-native signing.** Git tag signing would be simpler today, but it couples security to the transport mechanism. A `module.sig` file travels with the module regardless of distribution mechanism—Git clone, tarball, or any future format. The cost is a separate signing step; engines can reduce this to a single command.

**Trust on first use over a certificate authority.** TOFU has known downsides: the first resolution is unverified, key rotation requires manual acceptance, and there is no revocation mechanism. A PKI would address these but would require infrastructure and governance that a small open-source community cannot realistically sustain. TOFU protects against the most common attack—a repository compromised after adoption—and accepts the tradeoff that it cannot protect against pre-existing compromise.

**Optional signing with encouraged adoption.** Requiring signatures would be more secure but would raise the authoring barrier. Making it optional, with an engine-level policy that enforces it for security-conscious environments, preserves adoption while enabling strong policy where needed.

**Soft deprecation of remote URL imports.** A hard removal would strand existing workflows. Warnings give the ecosystem time to migrate while making the direction clear.

**Auto-discovery over workspace configuration.** A separate workspace manifest (e.g., `wdl-workspace.json` listing member modules) was considered and rejected. One concept (the module) with one file format (`module.json`) is simpler to explain, implement, and support across all repository layouts.
