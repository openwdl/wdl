import re
import sys
if len(sys.argv) < 2:
    println("Usage: toc.py [markdown file]")
    sys.exit(-1)
filename = sys.argv[1]
as_link = lambda x: re.sub(r'[^a-zA-Z0-9-_]', '', x.lower().replace(' ', '-'))
escape = lambda x: x.replace('[', '\\[').replace(']', '\\]')
toc = []
with open(filename) as fp:
  contents = fp.read()
for line in contents.split('\n'):
  header = re.match(r'^(#+)(.*)', line)
  if header:
    level = len(header.group(1))
    header = header.group(2).strip()
    toc.append('{spaces}* [{header}](#{link})'.format(
      spaces='  ' * (level-1),
      header=escape(header),
      link=as_link(header)
    ))
toc_re = re.compile(r'<\!---toc start-->(.*?)<\!---toc end-->', flags=re.DOTALL)
(contents, replacements) = toc_re.subn('<!---toc start-->\n\n{}\n\n<!---toc end-->'.format('\n'.join(toc)), contents)
with open(filename, 'w') as fp:
  fp.write(contents)
