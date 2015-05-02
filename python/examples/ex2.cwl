task scatter_task {
  command <<<
    egrep ^.{${count}}$ ${file in} || exit 0
  >>>
  output {
    array[string] words = tsv("stdout")
  }
}

task gather_task {
  command {
    python3 <<CODE
    import json
    with open('count', 'w') as fp:
      fp.write(str(int(${int count}) - 1))
    with open('wc', 'w') as fp:
      fp.write(str(sum([len(x) for x in json.loads(open("${array[array[string]] word_lists}").read())])))
    CODE
  }
  output {
    int count = read_int("count")
  }
}

workflow wf {
  array[file] files
  int count

  while(count > 3) {
    scatter(filename in files) {
      call scatter_task {
        input: in=filename, count=count
      }
    }
    call gather_task {
      input: count=count, word_lists=scatter_task.words
      output: count=count
    }
  }
}
