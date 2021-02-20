# WDL Specification v1.1 Errata

## Coercion of `read_lines` return value

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
