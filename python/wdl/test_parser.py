import wdl.binding
import wdl.parser
import glob
import pytest
import os

def test_exceess_tokens():
  got_exception = False
  try:
    wdl.binding.parse("{", "str")
  except wdl.parser.SyntaxError as e:
    got_exception = "Finished parsing without consuming all tokens" in str(e)
  assert got_exception  
  
@pytest.mark.parametrize(("filename",), [[x] for x in glob.glob("examples/*.wdl")] )
def test_trivial_parse(filename):
   ast = wdl.binding.parse(open(filename).read(), os.path.basename(filename))
   print(ast.dumps(indent=2))
