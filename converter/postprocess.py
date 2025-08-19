import os
import re

MATH_PATTERN = re.compile(r'(\$[^$]*?\$|\$\$.*?\$\$)', flags=re.DOTALL)

def remove_stray_character_from_md(md_file, char_to_remove="Ł", logger=None):
    """
    Opens the final .md file, removes the given character everywhere, and overwrites the file.
    """
    if not os.path.exists(md_file):
        return

    if logger:
        logger.info(f"Removing stray character '{char_to_remove}' from {md_file}")

    with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    new_content = content.replace(char_to_remove, "")

    if content != new_content and logger:
        logger.info("Stray characters found and removed.")

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

def flip_parentheses_outside_math(md_file, logger=None):
    """
    Reads the final Markdown file, splits it into math vs. non-math segments,
    flips parentheses only in the non-math segments, and overwrites the file.
    """
    if not os.path.exists(md_file):
        return
    
    if logger:
        logger.info(f"Flipping parentheses in {md_file}")

    with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    segments = MATH_PATTERN.split(content)

    def flip_parens(s):
        return s.replace('(', '§').replace(')', '(').replace('§', ')')

    new_segments = [flip_parens(seg) if not MATH_PATTERN.fullmatch(seg) else seg for seg in segments]
    new_content = ''.join(new_segments)

    if content != new_content and logger:
        logger.info("Parentheses flipped successfully.")

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
