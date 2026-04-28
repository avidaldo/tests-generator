# TODO: when is this used? is it an utility for 'prompts/summarize-sources.prompt.md'? In that case, is that documented? does the prompt knows that needs to use this? should I convert it to a skill? When analyzing this TODO, be careful and take some time in provide a detailed analysis for understanding the best options: I'm trying to achieve a deep undertanding of the use of primitives/customizations, and this seem a good example: should I use a skill for what a prompt does when it needs to convert XML to Markdown? does that mean that this script can be considered a tool?... document this analysis (and similar ones) in a new file.

import xml.etree.ElementTree as ET
import re
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python convert_xml_to_md.py <input_xml_file>")
    sys.exit(1)

input_file = sys.argv[1]

output_file = os.path.splitext(input_file)[0] + '.md'

# Basic cleaning regex
def clean_html(raw_html):
    if not raw_html: return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()

try:
    tree = ET.parse(input_file)
except FileNotFoundError:
    print(f"Error: File {input_file} not found.")
    sys.exit(1)

root = tree.getroot()

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"# Examen Review ({len(root.findall('question')) - 1} questions)\n\n")

    for i, question in enumerate(root.findall('question')):
        if question.get('type') == 'category':
            continue

        name = question.find('name/text').text
        qtext = clean_html(question.find('questiontext/text').text)

        f.write(f"## {i}. {name}\n")
        f.write(f"**Pregunta:** {qtext}\n\n")

        f.write("### Respuestas:\n")
        for answer in question.findall('answer'):
            fraction = float(answer.get('fraction'))
            text = clean_html(answer.find('text').text)
            feedback = clean_html(answer.find('feedback/text').text)

            icon = "✅" if fraction > 0 else "❌"
            bold = "**" if fraction > 0 else ""

            f.write(f"- {icon} {bold}{text}{bold}\n")
            f.write(f"  - *Feedback:* {feedback}\n")

        f.write("\n---\n\n")

print(f"Converted {input_file} to {output_file}")
