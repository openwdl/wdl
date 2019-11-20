from antlr4 import *
from ..WdlLexerPython import WdlLexerPython
from ..WdlParser import WdlParser
from .helpers import WdlParserTestErrorListener, CommentAggregatingTokenSource

import re
import os
import unittest

DEFAULT_EXAMPLE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../examples")
PATTERN = re.compile(r"#EXPECTED_ERROR\s+line:(?P<linenum>[0-9]+)\s(msg:(?P<msg>\s(\"[^\n\r]+\"|'[^\n\r]+')))?.*?")


def get_example_files(error):
    example_dir = os.environ.get("WDL_TEXT_EXAMPLES", DEFAULT_EXAMPLE_DIR)
    files = [f for f in os.listdir(example_dir) if
             os.path.isfile(os.path.join(example_dir, f))]
    parameters = []
    for file in files:
        if error:
            if file.endswith(".error"):
                parameters.append((FileStream(os.path.join(example_dir, file), "utf-8"), file))
        else:
            if not file.endswith(".error"):
                parameters.append((FileStream(os.path.join(example_dir, file), "utf-8"), file))

    return parameters


class WdlParserTest(unittest.TestCase):
    pass


def successful_test_generator(fileStream, fileName):
    def test(self):
        print "Testing file %s" % fileName
        lexer = WdlLexerPython(fileStream)
        parser = WdlParser(input=CommonTokenStream(lexer))
        parser.removeErrorListeners()
        errorListener = WdlParserTestErrorListener()
        parser.addErrorListener(errorListener)
        parser.document()
        self.assertFalse(expr=errorListener.hasError(), msg=errorListener.errorStrings())

    return test


def failure_test_generator(fileStream, fileName):
    def test(self):
        print "Testing file %s" % fileName
        lexer = CommentAggregatingTokenSource(fileStream)
        parser = WdlParser(input=CommonTokenStream(lexer))
        parser.removeErrorListeners()
        errorListener = WdlParserTestErrorListener()
        parser.addErrorListener(errorListener)
        parser.document()
        self.assertTrue(expr=errorListener.hasError(), msg="Expecting parser to have error")

    return test


if __name__ == "__main__":

    for fileStream, fileName in get_example_files(False):
        test_name = "test_%s_should_parse_successfully" % fileName
        test = successful_test_generator(fileStream, fileName)
        setattr(WdlParserTest, test_name, test)
    for fileStream, fileName in get_example_files(True):
        test_name = "test_%s_should_fail_parsing" % fileName
        test = failure_test_generator(fileStream, fileName)
        setattr(WdlParserTest, test_name, test)

    unittest.main()
