task scatter_task {
  command <<<
    egrep ^[a-f]{${count}}$ ${file in}
  >>>
  output {
    array[string] words = tsv("stdout")
  }
  runtime {
    docker: docker
  }
}

task gather_task {
  command {
    python3 <<CODE
    import sys
    count = int(${count}) - 1
    with open('count', 'w') as fp:
      fp.write(str(count))
    with open('reiterate', 'w') as fp:
      fp.write('false' if count == 0 else 'true')
    CODE
  }
  output {
    boolean re_iterate = read_boolean("reiterate")
    int count = read_int("count")
  }
  runtime {
    docker: docker
  }
}

workflow loop_wf {
  boolean iterate = true
  array[file] files
  int count
  string docker

  while(iterate) {
    scatter(filename in files) {
      call scatter_task {
        input: in=filename, count=count, docker=docker
      }
    }
    call gather_task {
      input: count=count, docker=docker
      output: iterate=re_iterate, count=count
    }
  }
}
