from antlr4 import *
from WdlParser.WdlLexerPython import WdlLexerPython
from WdlParser.WdlParser import WdlParser
from WdlParser.tests.helpers import WdlParserTestErrorListener, CommentAggregatingTokenSource

import re
import os
import unittest

DEFAULT_EXAMPLE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../examples")

PATTERN = re.compile(r"#EXPECTED_ERROR\s+line:(?P<linenum>[0-9]+)\s(msg:(?P<msg>\s(\"[^\n\r]+\"|'[^\n\r]+')))?.*?")


def get_example_files(error: bool):
    example_dir = os.environ.get("WDL_TEXT_EXAMPLES", DEFAULT_EXAMPLE_DIR)
    print(example_dir)
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


def successful_generator(fileStream, fileName):
    def test(self):
        print("Testing file {}".format(fileName))
        lexer = WdlLexerPython(fileStream)
        parser = WdlParser(input=CommonTokenStream(lexer))
        parser.removeErrorListeners()
        errorListener = WdlParserTestErrorListener()
        parser.addErrorListener(errorListener)
        parser.document()
        self.assertFalse(expr=errorListener.hasError(), msg=errorListener.errorStrings())

    return test


def failure_generator(fileStream, fileName):
    def test(self):
        print("Testing file {}".format(fileName))
        lexer = CommentAggregatingTokenSource(fileStream)
        parser = WdlParser(input=CommonTokenStream(lexer))
        parser.removeErrorListeners()
        errorListener = WdlParserTestErrorListener()
        parser.addErrorListener(errorListener)
        parser.document()
        self.assertTrue(expr=errorListener.hasError(), msg="Expecting parser to have error")

    return test


print (__name__)
if __name__ == "__main__":

    print("here")
    for fileStream, fileName in get_example_files(False):
        test_name = "test_{}_should_parse_successfully".format(fileName)
        test = successful_generator(fileStream, fileName)
        setattr(WdlParserTest, test_name, test)
    for fileStream, fileName in get_example_files(True):
        test_name = "test_{}_should_fail_parsing".format(fileName)
        test = failure_generator(fileStream, fileName)
        setattr(WdlParserTest, test_name, test)

    unittest.main()
