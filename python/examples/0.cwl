task inline {
  command<<<
    python3 <<CODE
    with open('${file path}') as fp:
      for line in fp:
        if line.startswith('zoologic'):
          print(line.strip())
    CODE
  >>>
  runtime {
    docker: docker
  }
}

task task1 {
  command {
    grep '^aberran' ${quote=false file infile}
  }
  output {
    array[string] words_a = tsv("stdout")
    int blah = 1+1
  }
  runtime {
    docker: docker
  }
}

task task2 {
  command {
    grep '^backbone' ${file infile}
  }
  output {
    array[string] words_b = tsv("stdout")
  }
  runtime {
    docker: docker
  }
}

task task3 {
  command {
    grep '^xantha' ${file infile} || exit 0
  }
  output {
    array[string] words_x = tsv("stdout")
  }
  runtime {
    docker: docker
  }
}

workflow simple {
  array[string] array_of_str
  array[array[array[file]]] scatter_files
  string docker
  string words = "w"+"o"+"r"+"d"+"s"
  file dict_file = "/usr/share/dict/" + words
  boolean b = false

  call task1 {
    int x = (1 + 2) * (10 - 4) * 7
    int y = strlen("hello world") + 10 + x
    input: docker=docker, infile=dict_file
  }
  call task2 {
    input: infile=dict_file, docker=docker
  }
  call task3 as alias {
    input: infile="/usr/share/dict/" + words, docker=docker
    output: array_of_str=words_x
  }
  call inline {
    input: path=dict_file, docker=docker
  }
  while(b) {
    call task3 as alias1 {
      input: docker=docker, infile=dict_file
    }
  }
  scatter(x in scatter_files) {
    scatter(y in x) {
      scatter(z in y) {
        call task2 as alias2 {
          input: infile=z, docker=docker
        }
      }
    }
  }
}
