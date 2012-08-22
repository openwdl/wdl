composite_task foo {
  
  step atask[version=0] {
    output: File("foo.txt") as x;
  }

  for ( item in foo ) {
    step btask[version=0] {
      input: p0=x, p1=global;
      output: File("bar.txt") appendto list;
    }
  }

  for ( item in list ) {
    step ctask[version=0] {
      input: p0=x, p1=item, p2=list, p3=blah;
      output: File("quux.txt") as z;
    }
  }

  step dtask[version=0] {
    input: p0=x, p1=y, p2=z;
    output: File("report.txt") as r;
  }

  step etask[version=0] {
    output: File("blah.txt") as blah;
  }

}
