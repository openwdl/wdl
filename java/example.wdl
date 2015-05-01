task wc {
  command {
    echo "${str}" | wc -c
  }
  output {
    int count = read_int("stdout") - 1
  }
}

workflow wf {
  array[string] str_array
  scatter(s in str_array) {
    call wc{input: str=s}
  }
}
