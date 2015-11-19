import wdl
import wdl.binding
from wdl.binding import *

with open('wdl/test/cases/0/wdl') as fp:
    wdl_document = wdl.load(fp, '<test>')
    workflow = wdl_document.workflows[0]

def test_document():
    assert len(wdl_document.workflows) == 1
    assert len(wdl_document.tasks) == 4

def test_workflow():
    assert workflow.name == 'simple'
    assert len([c for c in workflow.body if isinstance(c, wdl.binding.Call)]) == 4
    assert len([s for s in workflow.body if isinstance(s, wdl.binding.Scatter)]) == 1

def test_workflow_declarations():
    decls = workflow.declarations
    assert len(decls) == 5
    assert decls[0].wdl_string() == 'Array[Array[Array[File]]] scatter_files'
    assert decls[0].name == 'scatter_files'
    assert decls[0].expression is None
    assert decls[0].type == WdlArrayType(WdlArrayType(WdlArrayType(WdlFileType())))
    assert decls[0].type.wdl_string() == 'Array[Array[Array[File]]]'
    assert decls[1].wdl_string() == 'String docker'
    assert decls[1].name == 'docker'
    assert decls[1].expression is None
    assert decls[1].type == WdlStringType()
    assert decls[1].type.wdl_string() == 'String'
    assert decls[2].wdl_string() == 'String words = "w"+"o"+"r"+"d"+"s"'
    assert decls[2].name == 'words'
    assert decls[2].expression.wdl_string() == '"w"+"o"+"r"+"d"+"s"'
    assert decls[2].type == WdlStringType()
    assert decls[2].type.wdl_string() == 'String'
    assert decls[3].wdl_string() == 'File dict_file = "/usr/share/dict/"+words'
    assert decls[3].name == 'dict_file'
    assert decls[3].expression.wdl_string() == '"/usr/share/dict/"+words'
    assert decls[3].type == WdlFileType()
    assert decls[3].type.wdl_string() == 'File'
    assert decls[4].wdl_string() == 'Boolean b = false'
    assert decls[4].name == 'b'
    assert decls[4].expression.wdl_string() == 'false'
    assert decls[4].type == WdlBooleanType()
    assert decls[4].type.wdl_string() == 'Boolean'

def test_workflow_calls():
    assert len(workflow.body) == 5
    assert workflow.body[0].name == 'task1'
    assert workflow.body[0].task.name == 'task1'
    assert workflow.body[0].alias == None
    assert workflow.body[0].parent == workflow
    assert workflow.body[0].inputs['docker'].wdl_string() == 'docker'
    assert workflow.body[0].inputs['infile'].wdl_string() == 'dict_file'
    assert workflow.body[1].name == 'task2'
    assert workflow.body[1].task.name == 'task2'
    assert workflow.body[1].alias == None
    assert workflow.body[1].parent == workflow
    assert workflow.body[1].inputs['docker'].wdl_string() == 'docker'
    assert workflow.body[1].inputs['infile'].wdl_string() == 'dict_file'
    assert workflow.body[2].name == 'alias'
    assert workflow.body[2].task.name == 'task3'
    assert workflow.body[2].inputs['docker'].wdl_string() == 'docker'
    assert workflow.body[2].inputs['infile'].wdl_string() == '"/usr/share/dict/"+words'
    assert workflow.body[2].alias == 'alias'
    assert workflow.body[2].parent == workflow
    assert workflow.body[3].name == 'inline'
    assert workflow.body[3].task.name == 'inline'
    assert workflow.body[3].alias == None
    assert workflow.body[3].parent == workflow
    assert workflow.body[3].inputs['docker'].wdl_string() == 'docker'
    assert workflow.body[3].inputs['path'].wdl_string() == 'dict_file'

def test_workflow_scatters():
    assert workflow.body[4].name == '_s15'
    assert workflow.body[4].body[0].name == '_s17'
    assert workflow.body[4].body[0].body[0].name == '_s19'

def test_task_inline():
    task = wdl_document.task('inline')
    assert task.name == 'inline'
    assert len(task.declarations) == 2
    assert task.declarations[0].name == 'path'
    assert task.declarations[0].expression is None
    assert task.declarations[0].type == WdlFileType()
    assert task.declarations[0].type.wdl_string() == 'File'
    assert task.declarations[1].name == 'docker'
    assert task.declarations[1].expression is None
    assert task.declarations[1].type == WdlStringType()
    assert task.declarations[1].type.wdl_string() == 'String'
    assert task.command.wdl_string() == """python3 <<CODE
with open('${path}') as fp:
  for line in fp:
    if line.startswith('zoologic'):
      print(line.strip())
CODE"""

    def lookup(name):
        if name == 'path': return WdlString('/x/y/z.txt')

    assert task.command.instantiate(lookup) == """python3 <<CODE
with open('/x/y/z.txt') as fp:
  for line in fp:
    if line.startswith('zoologic'):
      print(line.strip())
CODE"""

    assert task.outputs == []
    assert task.runtime.keys() == ['docker']
    assert task.runtime['docker'].wdl_string() == '"${docker}"'

    def lookup(name):
        if name == 'docker': return WdlString('foo/bar')

    assert task.runtime['docker'].eval(lookup) == WdlString('foo/bar')
    assert task.parameter_meta == {}
    assert task.meta == {}

def test_task_task1():
    task = wdl_document.task('task1')
    assert task.name == 'task1'
    assert len(task.declarations) == 2
    assert task.declarations[0].name == 'infile'
    assert task.declarations[0].expression is None
    assert task.declarations[0].type == WdlFileType()
    assert task.declarations[0].type.wdl_string() == 'File'
    assert task.declarations[1].name == 'docker'
    assert task.declarations[1].expression is None
    assert task.declarations[1].type == WdlStringType()
    assert task.declarations[1].type.wdl_string() == 'String'
    assert task.command.wdl_string() == """grep '^aberran' ${infile}"""

    def lookup(name):
        if name == 'infile': return WdlString('/x/y/z.txt')

    assert task.command.instantiate(lookup) == """grep '^aberran' /x/y/z.txt"""

    assert len(task.outputs) == 2
    assert task.outputs[0].name == 'words_a'
    assert task.outputs[0].expression.wdl_string() == 'read_lines(stdout())'
    assert task.outputs[0].type == WdlArrayType(WdlStringType())
    assert task.outputs[1].name == 'foo'
    assert task.outputs[1].expression.wdl_string() == '1+1'
    assert task.outputs[1].type == WdlIntegerType()
    assert task.runtime.keys() == ['docker']
    assert task.runtime['docker'].wdl_string() == '"${docker}"'

    def lookup(name):
        if name == 'docker': return WdlString('foo/bar')

    assert task.runtime['docker'].eval(lookup) == WdlString('foo/bar')
    assert task.parameter_meta == {}
    assert task.meta == {}
