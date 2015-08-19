import subprocess
import re
import os
import tempfile
import toc

def run(command, cwd=None):
    proc = subprocess.Popen(
        command,
        shell=True,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
        cwd=cwd
    )
    stdout, stderr = proc.communicate()
    return (proc.returncode, stdout.strip(' \n'), stderr.strip(' \n'))

def write_and_close(contents):
    (fd, path) = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as fp:
        fp.write(wdl_source)
    return path

with open('SPEC.md') as fp:
    contents = fp.read()

toc.modify_and_write("SPEC.md")

source_regex = re.compile(r'```wdl(.*?)```', re.DOTALL)
count = 0
wdl_lines = 0

def lines(string, index=None):
  string = string[:index] if index else string
  return sum([1 for c in string if c == '\n']) + 1

for match in source_regex.finditer(contents):
    count += 1
    wdl_source = match.group(1)
    wdl_lines += lines(wdl_source)
    line = lines(contents, match.start(1))
    wdl_file = write_and_close(wdl_source)
    cmd = 'java -jar ../cromwell/target/scala-2.11/cromwell-0.9.jar parse ' + wdl_file
    (rc, stdout, stderr) = run(cmd)
    if rc != 0:
        print("Line {}: Failure".format(line))
        print("  rc: " + str(rc))
        print("  stdout: " + write_and_close(stdout))
        print("  stderr: " + write_and_close(stderr))
        print("  WDL: " + wdl_file)
        print("  Command: " + cmd)
    else:
        print("Line {}: Success".format(line))
        os.unlink(wdl_file)
print('Total: {}'.format(wdl_lines))
