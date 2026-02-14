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


def fix_code_blocks(content: str) -> str:
    """Ensure code blocks are properly formatted for Pandoc."""

    # Make sure verse code blocks have proper syntax marker
    content = re.sub(r'```verse\n', '```{.verse .numberLines}\n', content)

    return content


def add_chapter_header(content: str, chapter_title: str, is_numbered: bool, chapter_num: int = None) -> str:
    """Add proper chapter header for LaTeX."""

    # Remove the first H1 heading if it exists (we'll replace it)
    content = re.sub(r'^#\s+[^\n]+\n+', '', content, count=1)

    if is_numbered and chapter_num is not None:
        header = f'# Chapter {chapter_num}: {chapter_title} {{#chapter-{chapter_num:02d}}}\n\n'
    else:
        header = f'# {chapter_title}\n\n'

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
    content = add_chapter_header(content, chapter_title, is_numbered, chapter_num)

    return content


def get_part_for_chapter(filename: str) -> str:
    """Get the part name for a chapter, or None if not in a part."""
    for part_name, chapters in PARTS:
        if filename in chapters and chapters[0] == filename:
            return part_name
    return None


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

    if output_file:
        output_file.write_text(final_content, encoding='utf-8')
        print(f"Written to: {output_file}")
    else:
        print(final_content)


if __name__ == '__main__':
    main()
