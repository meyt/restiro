import re

docstring_block_regex = re.compile(r'\"\"\"([\s\S]*?)\"\"\"')
within_parentheses_regex = re.compile(r'\(([\s\S]*?)\)')
within_brackets_regex = re.compile(r'{([\s\S]*?)}')
single_word_regex = re.compile(r'\s(\[?\w+\]?)(?=\s?)')
path_regex = re.compile(r'\s/([/\w:]+)(?=\s?)')


ansi_orange_fg = '\033[33m'
ansi_reset = '\033[0m'
