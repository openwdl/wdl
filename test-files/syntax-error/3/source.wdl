composite_task foo {
  
  step atask[version=0] {
    output: File("foo.txt") as abc;
  }

  step atask[version=0] {
    input: p0=x, p1=y, p2=z;
    output: File("bar.txt") as xyz;
  }

}
