import pytest
from wdl_parser.WdlV1Parser import WdlV1Parser

from .helpers import *


@pytest.mark.parametrize("file_stream, file_name", get_example_files(False))
def test_should_parse_successfully(file_stream, file_name):
    print("Testing file {} should pass".format(file_name))
    lexer = WdlV1Lexer(file_stream)
    parser = WdlV1Parser(input=CommonTokenStream(lexer))
    parser.removeErrorListeners()
    error_listener = WdlParserTestErrorListener()
    parser.addErrorListener(error_listener)
    parser.document()
    assert not error_listener.hasError(), error_listener.errorStrings()


@pytest.mark.parametrize("file_stream, file_name", get_example_files(True))
def test_should_fail_parsing(file_stream, file_name):
    print("Testing file {} should fail".format(file_name))
    lexer = CommentAggregatingTokenSource(file_stream)
    parser = WdlV1Parser(input=CommonTokenStream(lexer))
    parser.removeErrorListeners()
    error_listener = WdlParserTestErrorListener()
    parser.addErrorListener(error_listener)
    parser.document()
    assert error_listener.hasError(), error_listener.errorStrings()
