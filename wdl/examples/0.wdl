composite_task foo {
  
  step atask[version=0] {
    output: File("foo.txt") as x;
  }

  for ( item in foo ) {
    step btask[version=0] {
      input: p0=x, p1=s;
      output: File("bar.txt") as y;
    }

    step ctask[version=0] {
      input: p0=x, p1=y;
      output: File("quux.txt") as z;
    }
  }

  step dtask[version=0] {
    input: p0=x, p1=y, p2=z;
    output: File("report.txt") as r;
  }

}
