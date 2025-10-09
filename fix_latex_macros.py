#!/usr/bin/env python3
"""
Fix LaTeX macros in converted Jupyter notebooks.
Replace custom macros from macros.tex with standard LaTeX equivalents.
"""

import json
import glob
import re
from pathlib import Path

# Macro replacement mappings based on workbook/tex/macros.tex
# Order matters! More specific patterns first
MACRO_REPLACEMENTS = [
    # Algorithms and schemes
    (r'\\algo\{([^}]+)\}', r'\\mathsf{\1}'),

    # Variables
    (r'\\params', r'\\mathit{pp}'),
    (r'\\state', r'\\mathit{state}'),
    (r'\\var\{([^}]+)\}', r'\\mathit{\1}'),

    # Keys
    (r'\\sk', r'\\mathit{sk}'),
    (r'\\pk', r'\\mathit{pk}'),

    # Adversaries
    (r'\\adv', r'\\mathcal{A}'),
    (r'\\bdv', r'\\mathcal{B}'),

    # Security parameter
    (r'\\secpar', r'\\lambda'),
    (r'\\secparam', r'1^\\lambda'),

    # Groups
    (r'\\GG', r'\\mathbb{G}'),
    (r'\\ZZ', r'\\mathbb{Z}'),
    (r'\\NN', r'\\mathbb{N}'),

    # Operators
    (r'\\defeq', r':='),
    (r'\\sample', r'\\leftarrow_R'),
    (r'\\gets', r'\\leftarrow'),

    # Probability - handle \pr{...}
    (r'\\pr\{', r'\\Pr['),
    (r'\\pr\\{', r'\\Pr['),

    # Functions
    (r'\\negl', r'\\mathrm{negl}'),
    (r'\\advantage\{([^}]+)\}\{([^}]+)\}', r'\\mathrm{Adv}^{\\text{\1}}_{\2}'),

    # Games - just remove \game macro, keep content
    (r'\\Game', r'\\mathsf{Game}'),

    # Cryptocode commands
    (r'\\pcassert', r'\\mathbf{assert}'),
    (r'\\pcif', r'\\mathbf{if}'),
    (r'\\pcthen', r'\\mathbf{then}'),
    (r'\\pcreturn', r'\\mathbf{return}'),

    # Group parameters
    (r'\\gparam', r'(\\mathbb{G}, p, g)'),
    (r'\\grgen', r'\\mathsf{GrGen}'),
]

def find_matching_brace(s, start):
    """Find the matching closing brace for an opening brace at position start."""
    count = 1
    i = start + 1
    while i < len(s) and count > 0:
        if s[i] == '{' and (i == 0 or s[i-1] != '\\'):
            count += 1
        elif s[i] == '}' and (i == 0 or s[i-1] != '\\'):
            count -= 1
        i += 1
    return i - 1 if count == 0 else -1

def fix_game_macro(text):
    """Replace \game{arg1}{arg2} with arg1_{arg2}."""
    result = []
    i = 0
    while i < len(text):
        # Look for \game{
        if text[i:i+6] == r'\game{':
            # Find first argument
            start1 = i + 5
            end1 = find_matching_brace(text, start1)
            if end1 == -1:
                result.append(text[i])
                i += 1
                continue

            arg1 = text[start1+1:end1]

            # Find second argument
            if end1 + 1 < len(text) and text[end1+1] == '{':
                start2 = end1 + 1
                end2 = find_matching_brace(text, start2)
                if end2 == -1:
                    result.append(text[i])
                    i += 1
                    continue

                arg2 = text[start2+1:end2]

                # Replace with arg1_{arg2}
                result.append(f'{arg1}_{{{arg2}}}')
                i = end2 + 1
            else:
                result.append(text[i])
                i += 1
        else:
            result.append(text[i])
            i += 1

    return ''.join(result)

def fix_latex_in_cell(cell_content):
    """Apply all macro replacements to cell content."""
    # First handle \game macro (before other replacements)
    cell_content = fix_game_macro(cell_content)

    # Then apply all other replacements
    for pattern, replacement in MACRO_REPLACEMENTS:
        cell_content = re.sub(pattern, replacement, cell_content)

    return cell_content

def fix_notebook(notebook_path):
    """Fix all LaTeX macros in a Jupyter notebook."""
    print(f"Processing {notebook_path}...")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Track if any changes were made
    changed = False

    # Process each cell
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'markdown':
            source = cell.get('source', [])
            if isinstance(source, list):
                new_source = []
                for line in source:
                    new_line = fix_latex_in_cell(line)
                    if new_line != line:
                        changed = True
                    new_source.append(new_line)
                cell['source'] = new_source
            elif isinstance(source, str):
                new_source = fix_latex_in_cell(source)
                if new_source != source:
                    changed = True
                cell['source'] = new_source

    if changed:
        # Write back to file
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        print(f"  ✓ Fixed {notebook_path}")
        return True
    else:
        print(f"  - No changes needed for {notebook_path}")
        return False

def main():
    """Fix all notebooks in the wiki directory."""
    wiki_dir = Path(__file__).parent / 'wiki'
    notebooks = list(wiki_dir.glob('**/*.ipynb'))

    print(f"Found {len(notebooks)} notebooks to process\n")

    fixed_count = 0
    for notebook_path in sorted(notebooks):
        if fix_notebook(notebook_path):
            fixed_count += 1

    print(f"\n{'='*60}")
    print(f"Summary: Fixed {fixed_count} out of {len(notebooks)} notebooks")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
