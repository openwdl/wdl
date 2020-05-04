version 1.0


struct FooStruct {
  File f
  String s
  Int p
  Array[Map[String,Pair[String,String]]] deeply_nested_property
}


struct BizStruct {
  String f
  Array[FooStruct] foo
}