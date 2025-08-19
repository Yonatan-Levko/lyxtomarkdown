import os
import re

MATH_PATTERN = re.compile(r'(\$[^$]*?\$|\$\$.*?\$\$)', flags=re.DOTALL)

def remove_stray_character_from_md(md_file, char_to_remove="Ł"):
    """
    Opens the final .md file, removes the given character everywhere, and overwrites the file.
    """
    if not os.path.exists(md_file):
        return

    with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    content = content.replace(char_to_remove, "")

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)

def flip_parentheses_outside_math(md_file):
    """
    Reads the final Markdown file, splits it into math vs. non-math segments,
    flips parentheses only in the non-math segments, and overwrites the file.
    """
    if not os.path.exists(md_file):
        return

    with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    segments = MATH_PATTERN.split(content)

    def flip_parens(s):
        return s.replace('(', '§').replace(')', '(').replace('§', ')')

    new_segments = [flip_parens(seg) if not MATH_PATTERN.fullmatch(seg) else seg for seg in segments]

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(''.join(new_segments))
