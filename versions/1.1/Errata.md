# WDL Specification v1.1 Errata

## Type coercions

The following coercions are missing from the [table](https://github.com/openwdl/wdl/blob/main/versions/1.1/SPEC.md#type-coercion):

|Target Type |Source Type     |Notes/Constraints |
|------------|----------------|------------------|
|`Array[Y]`  |`Array[X]+`     |`X` must be coercible to `Y`|

### Coercion of `read_lines` return value

In the [Type Coercion](https://github.com/openwdl/wdl/blob/main/versions/1.1/SPEC.md#type-coercion) section, coercion from `String` to any other type (except `File`) is not allowed. However, in [Appendix A](https://github.com/openwdl/wdl/blob/main/versions/1.1/SPEC.md#array-deserialization-using-read_lines) it is stated that

> `read_lines()` will return an `Array[String]` where each element in the array is a line in the
> file. This return value can be auto converted to other `Array` values.

Because there is currently no alternative method to convert `String` to non-`String` values, the coercion of `read_lines` return value is allowed as a *special case*.

However, in this situation, it is strongly recommended to instead use a JSON file containing an array. For example, if you want to read an array of integers into an `Array[Int]`, the file would look like:

`ints.json`
```json
[1, 2, 3]
```

And the WDL would be:

```wdl
Array[Int] ints = read_json("ints.json")
```

### Missing sections

The following sub-sections are missing from the Type Coercions section of the spec.

#### Order of precedence

During string interpolation, there are some operators for which it is possible to coerce the same arguments in multiple different ways. For such operators, it is necessary to define the order of preference so that a single function prototype can be selected from among the available options for any given set of arguments.

The `+` operator is overloaded for both numeric addition and String concatenation. This can lead to the following kinds of situations:

```
String s = "1.0"
Float f = 2.0
String x = "${s + f}"
```

There are two possible ways to evaluate the `s + f` expression:

1. Coerce `s` to `Float` and perform floating point addition, then coerce to `String` with the result being `x = "3.0"`.
2. Coerce `f` to `String` and perform string concatenation with result being `x = "1.02.0"`.

Similarly, the equality/inequality operators can be applied to any primitive type.

The order of preference is:

1. `Int`, `Float`: `Int` coerces to `Float`
2. `X`, `Y`: For any primitive types `X` != `Y`, both are coerced to `String`
3. If applying `+` to two values of the same type that cannot otherwise be summed/concatenated (i.e. `Boolean`, `File`, `Directory`), both values are first coerced to `String`

#### Limited exceptions

Implementers may choose to allow limited exceptions to the above rules, with the understanding that workflows depending on these exceptions may not be portable. These exceptions are provided for backward-compatibility, are considered deprecated, and will be removed in a future version of WDL.

* `Float` to `Int`, when the coercion can be performed with no loss of precision, e.g. `1.0 -> 1`.
* `String` to `Int`/`Float`, when the coercion can be performed with no loss of precision.
* `X?` may be coerced to `X`, and an error is raised if the value is undefined.
* `Array[X]` to `Array[X]+`, when the array is non-empty (an error is raised otherwise).
* `Map[W, X]` to `Array[Pair[Y, Z]]`, in the case where `W` is coercible to `Y` and `X` is coercible to `Z`.
* `Array[Pair[W, X]]` to `Map[Y, Z]`, in the case where `W` is coercible to `Y` and `X` is coercible to `Z`.
* `Map` to `Object`, in the case of `Map[String, X]`.
* `Map` to struct, in the case of `Map[String, X]` where all members of the struct have type `X`.
* `Object` to `Map[String, X]`, in the case where all object values are of the same type.