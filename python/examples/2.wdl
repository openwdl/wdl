task grep_words {
  command {
    grep '^${start}' ${File infile}
  }
  output {
    Array[String] words = tsv("stdout")
  }
}
workflow wf {
  File dictionary
  call grep_words as grep_pythonic_words {
    input: start="pythonic", infile=dictionary
  }
  call grep_words as grep_workf_words {
    input: start="workf", infile=dictionary
  }
}
