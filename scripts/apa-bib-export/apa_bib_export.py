#!/usr/bin/env python3
"""
export_bib.py

Reads a BibTeX file, optionally filters by group, sorts by publication year and author,
formats entries in APA style (with first-name initials), includes journal, volume,
number, pages, and generates Markdown or HTML output with clickable DOIs.

Usage:
    python3 export_bib.py --file /path/to/library.bib [--group GroupName] [--output md|html]
"""

import argparse
import sys
import datetime
import shutil
from pathlib import Path

import bibtexparser
from bibtexparser.customization import convert_to_unicode
from pylatexenc.latex2text import LatexNodes2Text


def format_authors(author_field: str) -> str:
    """
    Convert BibTeX author field into APA formatted author list with initials.
    E.g. "Haar, Tori and Brownlow, Charlotte" -> "Haar, T. & Brownlow, C."
    """
    authors = [a.strip() for a in author_field.replace('\n', ' ').split(' and ') if a.strip()]
    formatted = []
    for a in authors:
        if ',' in a:
            last, firsts = [s.strip() for s in a.split(',', 1)]
        else:
            parts = a.split()
            last = parts[-1]
            firsts = ' '.join(parts[:-1])
        initials = ' '.join(f"{n[0]}." for n in firsts.split())
        formatted.append(f"{last}, {initials}")
    if not formatted:
        return ''
    if len(formatted) == 1:
        return formatted[0]
    if len(formatted) == 2:
        return ' & '.join(formatted)
    return ', '.join(formatted[:-1]) + f", & {formatted[-1]}"


import re
from pylatexenc.latex2text import LatexNodes2Text

def clean_text(latex_str: str) -> str:
    """
    Convert LaTeX markup into plain text.  
    Falls back to removing braces and backslashes if pylatexenc fails.
    """
    if not latex_str:
        return ''
    try:
        converter = LatexNodes2Text()
        return converter.latex_to_text(latex_str).strip()
    except Exception:
        # Simple fallback: remove braces and backslashes
        text = re.sub(r'[{}\\\\]', '', latex_str)
        return text.strip()



def entry_to_apa(entry: dict) -> str:
    """
    Format a single BibTeX entry into an APA citation string.
    Includes journal, volume(issue), pages and DOI.
    """
    author = format_authors(entry.get('author', ''))
    year = entry.get('year', 'n.d.')
    title = clean_text(entry.get('title', ''))
    journal = clean_text(entry.get('journal', entry.get('booktitle', '')))
    volume = entry.get('volume', '')
    number = entry.get('number', '')
    pages = entry.get('pages', '')
    doi = entry.get('doi', '')

    citation = f"{author} ({year}). *{title}*."
    if journal:
        citation += f" {journal}"
        if volume:
            citation += f", {volume}"
            if number:
                citation += f"({number})"
        if pages:
            citation += f", {pages}"
        citation += "."
    if doi:
        citation += f" doi:[{doi}](https://doi.org/{doi})"
    return citation


def main():
    parser = argparse.ArgumentParser(
        description="Export BibTeX entries to Markdown or HTML in APA style with initials and full journal details"
    )
    parser.add_argument(
        '-f', '--file',
        dest='bibfile',
        type=Path,
        required=True,
        help='Path to the BibTeX (.bib) file'
    )
    parser.add_argument(
        '-g', '--group',
        dest='group',
        default=None,
        help='(Optional) BibTeX group name to filter entries'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_format',
        choices=['md', 'html'],
        default='md',
        help='Output format: "md" (Markdown) or "html"'
    )
    args = parser.parse_args()

    bib_path = args.bibfile.resolve()
    if not bib_path.exists():
        print(f"Error: File not found: {bib_path}")
        sys.exit(1)

    # Prepare export directory
    export_dir = bib_path.parent / 'Export'
    if export_dir.exists():
        shutil.rmtree(export_dir)
    export_dir.mkdir()

    # Load BibTeX data
    with open(bib_path, encoding='utf-8') as bibtex_file:
        bib_parser = bibtexparser.bparser.BibTexParser()
        bib_parser.customization = convert_to_unicode
        bib_db = bibtexparser.load(bibtex_file, parser=bib_parser)

    entries = bib_db.entries
    # Filter by group if provided
    if args.group:
        entries = [
            e for e in entries
            if 'groups' in e and args.group in [g.strip() for g in e['groups'].split(',')]
        ]

    # Sort by year (desc) then author
    def sort_key(e):
        y = int(e.get('year', '0')) if e.get('year', '').isdigit() else 0
        return (-y, e.get('author', ''))

    entries.sort(key=sort_key)

    # Group by year
    grouped = {}
    for entry in entries:
        year = entry.get('year', 'n.d.')
        grouped.setdefault(year, []).append(entry)

    # Header with timestamp
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = f"# Export of `{bib_path.name}`"
    if args.group:
        header += f" (group: {args.group})"
    header += f"\n> Generated on {timestamp}\n"
    header += "> **This file was automatically generated by [apa_bib_export python script](../../../scripts/apa-bib-export/) in this repository**\n"
    header += "> **This list will be regularly updated as the project progresses.**\n"
    
    # Build content
    lines = [header]
    for year in sorted(grouped.keys(), reverse=True):
        lines.append(f"\n---- {year} ----\n")
        for entry in sorted(grouped[year], key=lambda x: x.get('author', '')):
            lines.append(f"- {entry_to_apa(entry)}")
    content = "\n".join(lines)

    # Write output
    output_filename = f"{bib_path.stem}_list.{args.output_format}"
    output_path = export_dir / output_filename
    if args.output_format == 'md':
        output_path.write_text(content, encoding='utf-8')
    else:
        import markdown  # pip install markdown
        html = markdown.markdown(content)
        output_path.write_text(html, encoding='utf-8')

    print(f"✔ Export created: {output_path}")

    # Clean up virtualenv if present
    venv_dir = export_dir / 'env'
    if venv_dir.exists():
        shutil.rmtree(venv_dir)


if __name__ == '__main__':
    main()
