composite_task foo {
  
  step short_task[version=0] {
    output: File("foo.txt") as alpha;
  }
  
  step long_task[version=0] {
    output: File("bar.txt") as beta;
  }

  for ( item in items ) {
    step atask[version=0] {
      input: p0=alpha;
      output: File("baz.txt") as gamma;
    }
  }

  for ( item in items ) {
    step btask[version=0] {
      input: p0=beta;
      output: File("quux.txt") as epsilon;
    }
  }

  step generate_report[version=0] {
    input: p0=gamma, p1=epsilon;
    output: File("report.txt") as report;
  }

}
