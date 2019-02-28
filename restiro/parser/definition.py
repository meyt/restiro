
class DocstringApiDefinition:
    name = None
    title = None
    description = ''
    content = ''

    def __init__(self, docstring):
        for line in docstring.split('\n'):
            exploded_line = line.split(' ')
            if line.startswith('@apiDefine '):
                self.name = exploded_line[1]
                self.title = exploded_line[2] \
                    if len(exploded_line) > 2 else None
                self.description = ' '.join(exploded_line[3:]) \
                    if len(exploded_line) > 3 else ''

            elif line.startswith(' '):
                self.description += ' %s' % line.lstrip()

            else:
                self.content += line + '\n'
