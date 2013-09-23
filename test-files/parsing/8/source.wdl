composite_task test {
  step s0[version=0] {
    output: File("abc") as foo;
  }

  for (I in L) {
    for (J in M) {
      step s1[version=0] {
        input: p0=I, p1=J, p2=foo;
        output: File("def") as bar;
      }
    }
  }

  step s2[version=0] {
    input: p0=bar;
  }
}
