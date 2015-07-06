task scatter_task {
  command <<<
    egrep ^.{${count}}$ ${File in} || exit 0
  >>>
  output {
    Array[String] words = tsv(stdout())
  }
}

task gather_task {
  command {
    python3 <<CODE
    import json
    with open('count', 'w') as fp:
      fp.write(str(int(${Int count}) - 1))
    with open('wc', 'w') as fp:
      fp.write(str(sum([len(x) for x in json.loads(open("${Array[Array[String]] word_lists}").read())])))
    CODE
  }
  output {
    Int count = read_int("count")
  }
}

workflow wf {
  Array[File] files
  Int count

  scatter(filename in files) {
    call scatter_task {
      input: in=filename, count=count
    }
  }
  call gather_task {
    input: count=count, word_lists=scatter_task.words
  }
}
