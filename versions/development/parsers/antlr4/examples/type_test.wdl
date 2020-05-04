version development


struct LiteralStruct {
  String foo
  Int bar
}


workflow string_interpolation {

  input {
    String s1
    String? s1o

    Int i1
    Int? i1o

    Float f1
    Float? f1o

    Boolean b1
    Boolean b1o

    File f1
    File? f1o

    Array[File] a1
    Array[File]+ a1p
    Array[File]? a1o
    Array[File]+? a1po

    Pair[String,String] p1
    Pair[String,String]? p1o

    Map[String,String] m1
    Map[String,String]? m1o
    Map[String,Map[String,Array[Int]]] m2

    LiteralStruct st1
    LiteralStruct? st1o


  }

}