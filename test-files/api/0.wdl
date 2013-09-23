composite_task foo {
  
  step atask[version=0] {
    output: File("foo.txt") as x,
            FirstLine("bar.txt") as y;
  }

  for ( item in foobar ) {
    step btask[version=0] {
      input: p0=x, p1=item, p2=GLOBAL;
      output: File("baz.txt") as z;
    }
  }

}
