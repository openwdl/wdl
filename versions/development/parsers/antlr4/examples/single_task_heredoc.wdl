version development

task sometask {
  input {
    File inf
  }

  command <<<
    echo "this is a command"
    cat ~{inf} ~{basename(inf)}
  >>>

  output {
    File outf = "somefile.txt"
  }
}