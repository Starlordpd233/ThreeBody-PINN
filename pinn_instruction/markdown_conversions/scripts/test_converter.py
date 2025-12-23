#!/usr/bin/env python3
"""Test the updated converter."""
import sys
sys.path.insert(0, '.')

from convert_latex_to_markdown import LaTeXToMarkdownConverter

input_file = "sampling_method_instruction.tex"
output_file = "sampling_method_instruction_TEST.md"

converter = LaTeXToMarkdownConverter(input_file, output_file)
converter.convert()

print("Test conversion completed.")
print(f"Output written to {output_file}")