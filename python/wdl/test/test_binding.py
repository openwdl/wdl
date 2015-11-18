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

def test_blah():
    task_task1 = wdl_document.task('task1')
    task_task2 = wdl_document.task('task2')
    task_task3 = wdl_document.task('task3')

    assert task_task1.name == 'task1'
    assert task_task2.name == 'task2'
    assert task_task3.name == 'task3'
