task scatter_task {
  command <<<
    egrep ^[a-f]{${Int count}}$ ${File in}
  >>>
  output {
    Array[String] words = tsv("stdout")
  }
  runtime {
    docker: docker
  }
}

task gather_task {
  command {
    python3 <<CODE
    import sys
    count = int(${Int count}) - 1
    with open('count', 'w') as fp:
      fp.write(str(count))
    with open('reiterate', 'w') as fp:
      fp.write('false' if count == 0 else 'true')
    CODE
  }
  output {
    Boolean re_iterate = read_boolean("reiterate")
    Int count = read_int("count")
  }
  runtime {
    docker: docker
  }
}

workflow loop_wf {
  Boolean iterate = true
  Array[File] files
  Int count
  String docker

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
