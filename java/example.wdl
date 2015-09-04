task wc {
  String str
  command {
    echo "${str}" | wc -c
  }
  output {
    Int count = read_int("stdout") - 1
  }
}

workflow wf {
  String esc = "a\n\"b\t\""
  Array[String] str_array
  scatter(s in str_array) {
    call wc{input: str=s}
  }
}
