import re
import sys

as_link = lambda x: re.sub(r'[^a-zA-Z0-9-_]', '', x.lower().replace(' ', '-'))
escape = lambda x: x.replace('[', '\\[').replace(']', '\\]')

def modify_and_write(path):
    toc = []
    with open(path) as fp:
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
    with open(path, 'w') as fp:
        fp.write(contents)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Replaces contents between delimiters:\n")
        print("<\!---toc start--->")
        print("<\!---toc end--->\n")
        print("With the table of contents for the file\n")
        print("Usage: toc.py [markdown file]")
        sys.exit(-1)
    modify_and_write(sys.argv[1])
