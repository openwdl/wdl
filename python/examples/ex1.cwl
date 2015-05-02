task grep_words {
  command {
    grep '^${start}' ${file infile}
  }
  output {
    array[string] words = tsv("stdout")
  }
}
workflow wf {
  file dictionary
  call grep_words as grep_pythonic_words {
    input: start="pythonic", infile=dictionary
  }
  call grep_words as grep_workf_words {
    input: start="workf", infile=dictionary
  }
}
