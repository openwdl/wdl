version 1.0

task sometask {
  input {
    File inf
  }

  command {
    echo "this is a command"
    cat ~{inf}
  }

  output {
    File outf = glob("/***")
  }
}