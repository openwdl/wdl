import wdl.binding
import wdl.parser
import glob
import pytest
import os

@pytest.mark.parametrize(("test_case_dir",), [[x] for x in glob.glob("wdl/test/cases/*")] )
def test_parse(test_case_dir):
    wdl_file = os.path.join(test_case_dir, "wdl")
    parsetree_file = os.path.join(test_case_dir, "parsetree")
    parsetree = wdl.parser.parse(open(wdl_file).read(), os.path.basename(wdl_file))

    if not os.path.exists(parsetree_file):
        with open(parsetree_file, 'w') as fp:
            fp.write(parsetree.dumps(indent=2))

    with open(parsetree_file) as fp:
        assert fp.read() == parsetree.dumps(indent=2)

@pytest.mark.parametrize(("test_case_dir",), [[x] for x in glob.glob("wdl/test/cases/*")] )
def test_ast(test_case_dir):
    wdl_file = os.path.join(test_case_dir, "wdl")
    ast_file = os.path.join(test_case_dir, "ast")
    parsetree = wdl.parser.parse(open(wdl_file).read(), os.path.basename(wdl_file))

    if not os.path.exists(ast_file):
        with open(ast_file, 'w') as fp:
            fp.write(parsetree.ast().dumps(indent=2))

    with open(ast_file) as fp:
        assert fp.read() == parsetree.ast().dumps(indent=2)
