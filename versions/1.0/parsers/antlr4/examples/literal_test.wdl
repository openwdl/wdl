version 1.0


struct LiteralStruct {
  String foo
  Int bar
}


workflow string_interpolation {

  input {
    String inp
  }


  String none = None
  Int int = 1
  Float float = 1.0
  Boolean bool = true
  File file = "/path/to/some/file"

  Array[String] strings = ["foo","bar","biz","baz"]
  Pair[String,Int] pair = ("foo",10)
  Map[String,String] map = {"foo":"bar"}
  Map[String,String] map_with_expression = {strings[0]:"bar"}
  Object literal_strict = object {foo: "bar", bar: 1 }


}