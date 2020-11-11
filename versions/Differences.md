# Differences Between WDL Versions 

⚙️denotes a change that affects the parser

## 1.0 to development (2.0)

The next version of WDL will be 2.0 - the major version change indicates that there are breaking changes from 1.0.

Note that WDL 2.0 is currently called `development` to indicate that it is under active development. New features are still being added to the specification, and existing features are being deprecated/removed. Runtime engines are not required to maintain backward compatibility, so please use the `development` version with caution and at your own risk.

Adding further to the confusion is that some changes have been ratified (by vote of the [OpenWDL core team](../../GOVERNANCE.md) but not merged into the specification in the `main` branch, because they are waiting for implementation in at least one runtime engine. The list of changes below includes some of these ratified-but-unimplemented changes.

Specification changes under active consideration are tracked [here](https://github.com/openwdl/wdl/discussions/411))

* [Added the `Directory` type](https://github.com/openwdl/wdl/pull/241)
* [Relative imports](https://github.com/openwdl/wdl/pull/220)
* [Changes to the `runtime` section, and new `hints` section](https://github.com/openwdl/wdl/pull/315)
    * The `runtime` section no longer accepts arbitrary keys. Instead, only a specific set of keys are allowed. Any keys not supported by the `runtime` section must go in the `hints` section instead.
    * The `docker` key that was previously used by convention in the `runtime` section is changed to `container`.
    * The `hints` section is created to allow non-binding hints to the execution engine, including engine-specific keys.
    * `hint` values follow the same syntax as `meta` and `parameter_meta` - i.e. no expressions are allowed, only literal values.
* [Options (sep, true/false, default) are no longer allowed in placeholders](https://github.com/openwdl/wdl/pull/366)
    * The `sep` function was added to replace the behavior of the sep option
    * The behavior of true/false and default can be replicated with the ternary operator
        * `~{if flag then "hello" else "goodbye"}`)
        * `~{if defined(opt) then "-foo" else ""}`)
* `object`s should be considered deprecated. Both the `object` data type and the object literal syntax (`object {...}`) should no longer be used, and may be removed entirely from WDL 2.0 or a subsequent version.
    * The `read_object`, `read_objects`, `write_object`, and `write_objects` functions are removed
* [New `min` and `max` functions](https://github.com/openwdl/wdl/pull/304)
* [New `suffix`, `quote`, and `squote` functions](https://github.com/openwdl/wdl/pull/362/files)
* [New `keys` function](https://github.com/openwdl/wdl/pull/244)
* [New `as_map`, `as_pairs`, and `collect-by_key` functions](https://github.com/openwdl/wdl/pull/219)
* [Engines must minimally support a standard JSON syntax for inputs and outputs](https://github.com/openwdl/wdl/pull/357)
* [`runtime` attributes may be overridden in task/workflow inputs](https://github.com/openwdl/wdl/pull/313)
* [`file://` protocol no longer allowed for imports](https://github.com/openwdl/wdl/pull/349)
* [Optional variables can be defined with `None` value](https://github.com/openwdl/wdl/pull/263)
* Clarifications: many issues were identified as under-specified in `WDL 1.0`, and have been clarified in `development`.
    * [The `sub` function supports POSIX Extended Regular Expressions](https://github.com/openwdl/wdl/pull/243)
    * [New notation for struct literals](https://github.com/openwdl/wdl/pull/297)
    * [Optional vs required file outputs](https://github.com/openwdl/wdl/pull/310)
    * [Unsatisfied task inputs](https://github.com/openwdl/wdl/pull/359)
        * Execution engines are not requred to allow required task inputs to go unsatisfied by the calling workflow.
        * Execution engines may choose to recognize `allowNestedInputs` in the workflow meta section to enable overriding of unsatisfied task inputs.
    
## Draft-2 to 1.0

*   ⚙️Version statement required (as of draft-3)
*   ⚙️Structs
*   ⚙️For both tasks and workflows, unbound inputs must be within the `input {}` block
    *   Declarations outside input block cannot be overridden
    *   As a consequence of this, the way workflow inputs are calculated differs between the two specs - refer to the “Computing Inputs” sections for details
*   The workflow `output` section is optional in both specs, but the 1.0 spec clarifies that the output section is required in a workflow called as a sub-workflow.
*   Task command section
    *   ⚙️Placeholders can begin with `~` rather than `$`
    *   ⚙️Placeholders in heredoc-style command (`command <<< >>>`) may only use the `~{}` style placeholder
    *   `command <<< >>>` with `~{}` placeholders is strongly preferred to avoid any mis-parsing of bash variables
    *   In Draft-2 it was allowed to specify only one of the `true/false` options in a placeholder - the other option evaluated to empty string. In 1.0, both options are required.
*   `meta` and `parameter_meta` are allowed to contain number, boolean, object, or array values in addition to strings
*   Standard library
    *   `size` can be computed for certain compound types


## Non-features

These are features that appear in either or both of the Draft-2 and 1.0 specs that are here explicitly specified as non-features _i.e._ consider these sections of the spec(s) as redlined.

*   Both Draft-2 and 1.0 mention a `loop` (or `while`) construct. It appears in both the Draft-2 and 1.0 Hermes grammars. However, I don’t think it was ever supported in Cromwell, and it is dropped in 2.0.
*   ⚙️Wildcard syntax in the output section in Draft-2 is deprecated, and is dropped in 1.0. Parsers are not required to support this syntax in order to be considered compliant.

## Open Questions

These items are ambiguous in either or both of the Draft-2 and 1.0 specs - whether or not they should be considered part of the spec will probably be determined by whether they are implemented in Cromwell.

*   Coercion of Map to Object - 1.0 does support this, but I _think_ Draft-2 does not support this.
*   The Draft-2 spec mentions a `quote` placeholder option once, but it is never referred to again. The Hermes grammar does not enumerate the allowed options. It is definitely not supported in 1.0.
*   The 1.0 spec says that optional inputs with defaults are allowed, whereas the Draft-2 spec does not say one way or the other.
*   The Draft-2 spec says that an optional variable whose value is unspecified will evaluate to the empty string. The 1.0 spec does not say how a variable with an unspecified value is evaluated - I am guessing it is an error?

## References

*   Draft-2
    *   [Specification](https://github.com/openwdl/wdl/blob/main/versions/draft-2/SPEC.md#alternative-heredoc-syntax)
    *   [Hermes grammar](https://github.com/openwdl/wdl/blob/main/versions/draft-2/parsers/grammar.hgr)
*   1.0
    *   [Specification](https://github.com/openwdl/wdl/blob/main/versions/1.0/SPEC.md#command-section)
    *   [Hermes grammar](https://github.com/openwdl/wdl/blob/main/versions/1.0/parsers/hermes/grammar.hgr)
*   [The diff between Draft-2 and 1.0 specs](https://github.com/jdidion/wdl/commit/35b49a815858d45e6111899296ae4beb729fe13a?short_path=22feea2#diff-22feea2e46776b17b2da5ddc2717b767)
