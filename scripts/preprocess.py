#!/usr/bin/env python3
"""
Preprocess Verse documentation markdown for Pandoc/LaTeX conversion.

Handles:
- MkDocs admonitions (!!! warning, !!! note, etc.)
- Cross-reference link conversion
- Code block cleanup (remove versetest comments)
- Chapter numbering and ordering
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

# Chapter order and titles
CHAPTERS = [
    ("index.md", "Preface", False),  # Not numbered
    ("00_overview.md", "Overview", True),
    ("01_expressions.md", "Expressions", True),
    ("02_primitives.md", "Primitive Types", True),
    ("03_containers.md", "Container Types", True),
    ("04_operators.md", "Operators", True),
    ("05_mutability.md", "Mutability", True),
    ("06_functions.md", "Functions", True),
    ("07_control.md", "Control Flow", True),
    ("08_failure.md", "Failure", True),
    ("09_structs_enums.md", "Structs and Enums", True),
    ("10_classes_interfaces.md", "Classes and Interfaces", True),
    ("11_types.md", "Type System", True),
    ("12_access.md", "Access Specifiers", True),
    ("13_effects.md", "Effects", True),
    ("14_concurrency.md", "Concurrency", True),
    ("15_live_variables.md", "Live Variables", True),
    ("16_modules.md", "Modules and Paths", True),
    ("17_persistable.md", "Persistable Types", True),
    ("18_evolution.md", "Code Evolution", True),
    ("concept_index.md", "Concept Index", False),  # Appendix
]

# Parts structure for grouping chapters
PARTS = [
    ("Part I: Fundamentals", ["00_overview.md", "01_expressions.md", "02_primitives.md", "03_containers.md", "04_operators.md"]),
    ("Part II: Core Features", ["05_mutability.md", "06_functions.md", "07_control.md", "08_failure.md", "09_structs_enums.md"]),
    ("Part III: Object-Oriented Programming", ["10_classes_interfaces.md", "11_types.md", "12_access.md"]),
    ("Part IV: Advanced Topics", ["13_effects.md", "14_concurrency.md", "15_live_variables.md", "16_modules.md"]),
    ("Part V: Production", ["17_persistable.md", "18_evolution.md"]),
]


def convert_admonitions(content: str) -> str:
    """Convert MkDocs admonitions to LaTeX-friendly format."""

    # Pattern for admonitions: !!! type "title" or !!! type
    admonition_pattern = re.compile(
        r'^(!{3})\s+(warning|note|info|tip|danger|important)(?:\s+"([^"]*)")?\s*\n((?:[ ]{4}.*\n?)*)',
        re.MULTILINE
    )

    def replace_admonition(match):
        admon_type = match.group(2)
        title = match.group(3) or admon_type.capitalize()
        body = match.group(4)

        # Remove the 4-space indent from body lines
        body_lines = []
        for line in body.split('\n'):
            if line.startswith('    '):
                body_lines.append(line[4:])
            elif line.strip() == '':
                body_lines.append('')
            else:
                body_lines.append(line)
        body = '\n'.join(body_lines).strip()

        # Map to LaTeX environment names
        env_map = {
            'warning': 'warningbox',
            'note': 'notebox',
            'info': 'infobox',
            'tip': 'tipbox',
            'danger': 'dangerbox',
            'important': 'warningbox',
        }
        env = env_map.get(admon_type, 'notebox')

        # Use raw LaTeX block for Pandoc
        return f'''
::: {{{env}}}
**{title}**

{body}
:::

'''

    return admonition_pattern.sub(replace_admonition, content)


def build_filename_anchor_map() -> dict:
    """Build a mapping from source filenames to their Pandoc anchor IDs.

    Numbered chapters get explicit anchors like 'chapter-01'.
    Unnumbered chapters get Pandoc auto-generated IDs from their title.
    """
    anchor_map = {}
    chapter_num = 1

    for filename, title, is_numbered in CHAPTERS:
        if is_numbered:
            anchor_map[filename] = f'chapter-{chapter_num:02d}'
            chapter_num += 1
        else:
            # Pandoc auto-generates IDs from heading text: lowercase, spaces→hyphens
            anchor_map[filename] = title.lower().replace(' ', '-')

    return anchor_map


# Corrections for broken section anchors in source docs where headings were
# renamed or removed. Maps old anchor → correct anchor (without '#' prefix).
BROKEN_ANCHOR_FIXES = {
    'semicolons-vs-commas-sequences-and-tuples': 'semicolons-vs-commas',
    'range-operator-restrictions': 'for-expressions',
    'floating-point-keys': 'floats',
    'recursive-targets': 'issues-and-patterns',
}


def convert_cross_references(content: str, current_file: str, anchor_map: dict) -> str:
    """Convert relative markdown links to internal references."""

    # Pattern for markdown links: [text](file.md) or [text](file.md#anchor)
    # Handles numbered files (00_overview.md), unnumbered files (index.md, concept_index.md),
    # and optional trailing slash before anchor (06_functions.md/#anchor)
    link_pattern = re.compile(
        r'\[([^\]]+)\]\(([a-z0-9_]+\.md)/?(#[a-z0-9_-]+)?\)'
    )

    # Also fix same-file broken anchors: [text](#broken-anchor)
    same_file_pattern = re.compile(
        r'\[([^\]]+)\]\((#[a-z0-9_-]+)\)'
    )

    def replace_link(match):
        text = match.group(1)
        target_file = match.group(2)
        anchor = match.group(3) or ''

        if target_file in anchor_map:
            chapter_anchor = anchor_map[target_file]
            if anchor:
                # Fix known broken section anchors
                anchor_id = anchor[1:]  # strip '#'
                if anchor_id in BROKEN_ANCHOR_FIXES:
                    anchor = '#' + BROKEN_ANCHOR_FIXES[anchor_id]
                return f'[{text}]({anchor})'
            else:
                # Link to the chapter itself
                return f'[{text}](#{chapter_anchor})'
        else:
            # Unknown file — leave the link text but remove broken href
            return text

    def fix_same_file_anchor(match):
        text = match.group(1)
        anchor = match.group(2)
        anchor_id = anchor[1:]  # strip '#'
        if anchor_id in BROKEN_ANCHOR_FIXES:
            return f'[{text}](#{BROKEN_ANCHOR_FIXES[anchor_id]})'
        return match.group(0)

    content = link_pattern.sub(replace_link, content)
    content = same_file_pattern.sub(fix_same_file_anchor, content)
    return content


def clean_versetest_comments(content: str) -> str:
    """Remove versetest HTML comments used for testing."""

    # Remove <!--versetest ... --> blocks
    content = re.sub(r'<!--versetest\n.*?-->\n?', '', content, flags=re.DOTALL)

    # Remove simple <!-- XX --> markers
    content = re.sub(r'<!--\s*\d+\s*-->\n?', '', content)

    # Remove <!-- #> --> markers
    content = re.sub(r'<!--\s*#>\s*-->\n?', '', content)

    # Remove <# markers in comments
    content = re.sub(r'<#\n?', '', content)

    return content


MAX_CODE_LINE_LENGTH = 72


def shorten_code_line(line: str) -> str:
    """Shorten a single code line that exceeds MAX_CODE_LINE_LENGTH.

    Strategy: compress excessive whitespace before inline # comments.
    """
    # Match code followed by multiple spaces then a # comment
    m = re.match(r'^(.*\S)([ \t]{3,})(#\s.*)$', line)
    if m:
        code_part = m.group(1)
        comment_part = m.group(3)
        shortened = code_part + '  ' + comment_part
        if len(shortened) <= MAX_CODE_LINE_LENGTH:
            return shortened
        # Still too long — try just 1 space
        shortened = code_part + ' ' + comment_part
        if len(shortened) <= MAX_CODE_LINE_LENGTH:
            return shortened
    return line


def compress_long_code_lines(content: str) -> str:
    """Compress long lines in code blocks to fit within page width."""
    lines = content.split('\n')
    result = []
    in_code = False

    for line in lines:
        if line.startswith('```'):
            in_code = not in_code
            result.append(line)
            continue

        if in_code and len(line) > MAX_CODE_LINE_LENGTH:
            line = shorten_code_line(line)

        result.append(line)

    return '\n'.join(result)


def fix_code_blocks(content: str) -> str:
    """Ensure code blocks are properly formatted for Pandoc."""

    # Make sure verse code blocks have proper syntax marker
    content = re.sub(r'```verse\n', '```{.verse .numberLines}\n', content)

    # Compress long lines in code blocks
    content = compress_long_code_lines(content)

    return content


def convert_links_to_pagerefs(content: str) -> str:
    """Convert markdown links to page references for print.

    Replaces [Link Text](#anchor) with Link Text (p. \\pageref{anchor})
    using pandoc's raw LaTeX inline syntax. Used for the Concept Index
    so printed readers see page numbers instead of clickable hyperlinks.
    """
    def replace_with_pageref(match):
        text = match.group(1)
        anchor = match.group(2)
        return f'{text} (p.\\ `\\pageref{{{anchor}}}`{{=latex}})'

    return re.sub(r'\[([^\]]+)\]\(#([a-z0-9_-]+)\)', replace_with_pageref, content)


def make_subheadings_unnumbered(content: str) -> str:
    """Make all ## and ### headings unnumbered for appendix/unnumbered chapters.

    This prevents pandoc's --number-sections from continuing the previous
    chapter's numbering into unnumbered chapters like the Concept Index.
    """
    def add_unnumbered(match):
        hashes = match.group(1)
        title = match.group(2).rstrip()
        # Don't double-add if already has attributes
        if title.endswith('}'):
            return match.group(0)
        return f'{hashes} {title} {{.unnumbered}}'

    return re.sub(r'^(#{2,})\s+(.+)$', add_unnumbered, content, flags=re.MULTILINE)


def add_chapter_header(content: str, chapter_title: str, is_numbered: bool, chapter_num: int = None) -> str:
    """Add proper chapter header for LaTeX."""

    # Remove the first H1 heading if it exists (we'll replace it)
    content = re.sub(r'^#\s+[^\n]+\n+', '', content, count=1)

    if is_numbered and chapter_num is not None:
        header = f'# {chapter_title} {{#chapter-{chapter_num:02d}}}\n\n'
    else:
        header = f'# {chapter_title} {{.unnumbered}}\n\n'
        # Make all sub-headings unnumbered too
        content = make_subheadings_unnumbered(content)

    return header + content


def process_file(filepath: Path, chapter_title: str, is_numbered: bool,
                  chapter_num: int = None, anchor_map: dict = None) -> str:
    """Process a single markdown file."""

    content = filepath.read_text(encoding='utf-8')

    # Apply all transformations
    content = clean_versetest_comments(content)
    content = convert_admonitions(content)
    content = convert_cross_references(content, filepath.name, anchor_map or {})
    content = fix_code_blocks(content)
    # For the Concept Index, convert hyperlinks to page references for print
    if filepath.name == 'concept_index.md':
        content = convert_links_to_pagerefs(content)
    content = add_chapter_header(content, chapter_title, is_numbered, chapter_num)

    return content


def get_part_for_chapter(filename: str) -> str:
    """Get the part name for a chapter, or None if not in a part."""
    for part_name, chapters in PARTS:
        if filename in chapters and chapters[0] == filename:
            return part_name
    return None


def fix_print_overflows(content: str) -> str:
    """Apply line breaks to code lines that overflow the print margins.

    The 7x10" page with 0.875"/0.75" margins gives ~5.375" text width.
    At JetBrains Mono Scale=0.85, about 73 monospace chars fit per line.
    Lines longer than this overflow in the PDF.

    These are pure formatting changes — identical content wrapped differently.
    Each replacement is a specific long line → its line-broken equivalent.
    """
    # Each tuple is (original_line, replacement_with_breaks)
    # Only applied inside code blocks (``` fenced blocks)
    replacements = [
        # Ch1 Overview: FilterItems signature
        (
            '    FilterItems(Predicate:type{_(:game_item)<decides>:void}):[]game_item =',
            '    FilterItems(\n'
            '            Predicate:type{_(:game_item)<decides>:void}\n'
            '    ):[]game_item ='
        ),
        # Ch4 Containers: persistent_class with long specifier chain
        (
            'persistent_class := class<unique><allocates><computes><persistent><module_scoped_var_weak_map_key> {}',
            'persistent_class := class<unique><allocates>\n'
            '        <computes><persistent>\n'
            '        <module_scoped_var_weak_map_key> {}'
        ),
        # Ch4 Containers: key_class with same pattern
        (
            'key_class := class<unique><allocates><computes><persistent><module_scoped_var_weak_map_key> {}',
            'key_class := class<unique><allocates>\n'
            '        <computes><persistent>\n'
            '        <module_scoped_var_weak_map_key> {}'
        ),
        # Ch11 Classes: GetPhysicsComponent signature
        (
            'GetPhysicsComponent(Comp:component)<computes><decides>:physics_component =',
            'GetPhysicsComponent(Comp:component)\n'
            '        <computes><decides>:physics_component ='
        ),
        # Ch11 Classes: FindDescendantEntities signature
        (
            '      FindDescendantEntities(entity_type:castable_subtype(entity)):generator(entity_type)',
            '      FindDescendantEntities(\n'
            '              entity_type:castable_subtype(entity)\n'
            '      ):generator(entity_type)'
        ),
        # Ch14 Effects: SelectFunction return type
        (
            'SelectFunction(UseFailable:logic):type{_(:int)<computes><decides>:int} =',
            'SelectFunction(UseFailable:logic):\n'
            '        type{_(:int)<computes><decides>:int} ='
        ),
        # Ch17 Modules: Fully qualified Function
        (
            '(/YourPackage:)Function((local:)X:(/Verse.org/Verse:)int):(/Verse.org/Verse:)int = (local:)X',
            '(/YourPackage:)Function(\n'
            '        (local:)X:(/Verse.org/Verse:)int\n'
            '):(/Verse.org/Verse:)int = (local:)X'
        ),
        # Ch17 Modules: Fully qualified ProcessValue
        (
            '(/YourPackage:)ProcessValue((local:)Input:(/Verse.org/Verse:)int, (local:)Multiplier:(/Verse.org/Verse:)int):(/Verse.org/Verse:)int =',
            '(/YourPackage:)ProcessValue(\n'
            '        (local:)Input:(/Verse.org/Verse:)int,\n'
            '        (local:)Multiplier:(/Verse.org/Verse:)int\n'
            '):(/Verse.org/Verse:)int ='
        ),
        # Ch17 Modules: Fully qualified TakeDamage
        (
            '    (/YourPackage/player_class:)TakeDamage((local:)Amount:(/Verse.org/Verse:)float):(/Verse.org/Verse:)void =',
            '    (/YourPackage/player_class:)TakeDamage(\n'
            '            (local:)Amount:(/Verse.org/Verse:)float\n'
            '    ):(/Verse.org/Verse:)void ='
        ),
        # Ch17 Modules: set Health = Health - Amount (long qualified)
        (
            '        set (/YourPackage/player_class:)Health = (/YourPackage/player_class:)Health - (local:)Amount',
            '        set (/YourPackage/player_class:)Health =\n'
            '            (/YourPackage/player_class:)Health -\n'
            '            (local:)Amount'
        ),
        # Ch17 Modules: Fully qualified Calculate
        (
            '        (/YourGame/game_system/calculator:)Calculate((local:)Input:(/Verse.org/Verse:)int):(/Verse.org/Verse:)int =',
            '        (/YourGame/game_system/calculator:)Calculate(\n'
            '                (local:)Input:(/Verse.org/Verse:)int\n'
            '        ):(/Verse.org/Verse:)int ='
        ),
        # Ch17 Modules: long arithmetic with qualified names
        (
            '            (local:)Input * (/YourGame/game_system/calculator:)Multiplier + (/YourGame/game_system:)BaseValue',
            '            (local:)Input *\n'
            '                (/YourGame/game_system/calculator:)Multiplier +\n'
            '                (/YourGame/game_system:)BaseValue'
        ),
        # Ch17 Modules: Multiplier declaration
        (
            '        (/YourGame/game_system/calculator:)Multiplier:(/Verse.org/Verse:)int = 2',
            '        (/YourGame/game_system/calculator:)Multiplier:\n'
            '                (/Verse.org/Verse:)int = 2'
        ),
        # Ch17 Modules: GetPlayerLimit qualified
        (
            '    (/YourPackage/config:)GetPlayerLimit<public>():(/Verse.org/Verse:)int =',
            '    (/YourPackage/config:)GetPlayerLimit<public>():\n'
            '            (/Verse.org/Verse:)int ='
        ),
        # Ch17 Modules: MaxPlayers qualified declaration
        (
            '    (/YourPackage/config:)MaxPlayers<public>:(/Verse.org/Verse:)int = 100',
            '    (/YourPackage/config:)MaxPlayers<public>:\n'
            '            (/Verse.org/Verse:)int = 100'
        ),
        # Ch17 Modules: Error message
        (
            'Error: Cannot assign (/Verse.org/Verse:)string to (/Verse.org/Verse:)int at line 42',
            'Error: Cannot assign\n'
            '    (/Verse.org/Verse:)string to\n'
            '    (/Verse.org/Verse:)int at line 42'
        ),
    ]

    for old, new in replacements:
        content = content.replace(old, new)

    return content


def main():
    if len(sys.argv) < 2:
        print("Usage: preprocess.py <docs_directory> [output_file]")
        sys.exit(1)

    docs_dir = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    if not docs_dir.exists():
        print(f"Error: Directory {docs_dir} does not exist")
        sys.exit(1)

    # Build filename→anchor mapping before processing files
    anchor_map = build_filename_anchor_map()

    combined_content = []
    chapter_num = 1

    for filename, title, is_numbered in CHAPTERS:
        filepath = docs_dir / filename

        if not filepath.exists():
            print(f"Warning: {filepath} not found, skipping")
            continue

        # Check if this starts a new part
        part_name = get_part_for_chapter(filename)
        if part_name:
            combined_content.append(f'\n\\part{{{part_name}}}\n\n')

        print(f"Processing: {filename} -> {title}")

        content = process_file(
            filepath,
            title,
            is_numbered,
            chapter_num if is_numbered else None,
            anchor_map
        )

        combined_content.append(content)
        combined_content.append('\n\n\\newpage\n\n')

        if is_numbered:
            chapter_num += 1

    final_content = '\n'.join(combined_content)

    # Apply print-specific line breaks to code lines that overflow
    # the 7x10" page margins. These are formatting-only changes —
    # identical content, just wrapped differently for print.
    final_content = fix_print_overflows(final_content)

    if output_file:
        output_file.write_text(final_content, encoding='utf-8')
        print(f"Written to: {output_file}")
    else:
        print(final_content)


if __name__ == '__main__':
    main()
