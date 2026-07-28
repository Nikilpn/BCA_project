"""Fix section order in Ch 3: 3.3 → 3.4 → 3.5 → 3.6 → 3.7
Uses direct XML manipulation via zipfile + lxml.
"""
from zipfile import ZipFile
from lxml import etree
from io import BytesIO
import shutil, os

SRC = '/home/nikhil/roombookings3/roombookings/Hoteliers_Myproject/projectreport/nikhilproject241.docx'
DST = SRC
TMP = SRC + '.tmp.docx'

ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
w = '{' + ns + '}'

def ptext(p):
    texts = p.findall('.//' + w + 't')
    return ''.join(t.text or '' for t in texts).strip()

# Read the docx
with ZipFile(SRC, 'r') as z:
    doc_xml = z.read('word/document.xml')
    # Also read all other files
    other_files = {}
    for name in z.namelist():
        if name != 'word/document.xml':
            other_files[name] = z.read(name)

tree = etree.fromstring(doc_xml)
body = tree.find(w + 'body')

# Get all paragraphs
all_paras = list(body.findall(w + 'p'))

# Define sections we need to reorder (heading text -> id)
section_ids = [
    '3.3 Use Case Diagram',
    '3.4 Software and Hardware Requirements',
    '3.5 Data Dictionary',
    '3.6 Entity Relationship Diagram',
    '3.7 Data Flow Diagram'
]

# Find index ranges for each section
sections = {}
for sid in section_ids:
    start = None
    for i, p in enumerate(all_paras):
        if ptext(p) == sid:
            start = i
            break
    if start is None:
        print(f"Section '{sid}' not found!")
        continue
    
    # Find end - next heading from our list or Ch 4
    end = len(all_paras)
    for i in range(start + 1, len(all_paras)):
        t = ptext(all_paras[i])
        if t in section_ids or t.startswith('4. Design Document'):
            end = i
            break
    
    sections[sid] = (start, end)
    print(f"  '{sid}': paragraphs {start}-{end-1}")

# Correct order
correct_order = ['3.3 Use Case Diagram', '3.4 Software and Hardware Requirements',
                 '3.5 Data Dictionary', '3.6 Entity Relationship Diagram', '3.7 Data Flow Diagram']

# Now we need to physically reorder the XML elements
# Collect all elements to reorder (flat list in correct order)
ordered_elements = []
for sid in correct_order:
    start, end = sections[sid]
    for i in range(start, end):
        ordered_elements.append(all_paras[i])

# Get the first element (3.3 heading) and what's before it
first_elem = all_paras[sections['3.3 Use Case Diagram'][0]]
prev_sibling = first_elem.getprevious()

# Remove all section elements from the tree
for sid in section_ids:
    start, end = sections[sid]
    for i in range(end - 1, start - 1, -1):  # remove in reverse order
        body.remove(all_paras[i])

# Re-insert in correct order
insert_point = prev_sibling
for elem in ordered_elements:
    if insert_point is None:
        body.insert(0, elem)
    else:
        insert_point.addnext(elem)
    insert_point = elem

# Write back
xml_bytes = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)

# Also renumber the Security/Implementation/Limitations chapters
# Find 8. Implementation Plan and renumber all after Security chapter
with ZipFile(SRC, 'r') as z:
    # Already read above
    pass

# Write to temp then replace
with ZipFile(TMP, 'w') as zout:
    zout.writestr('word/document.xml', xml_bytes)
    for name, data in other_files.items():
        zout.writestr(name, data)

os.replace(TMP, DST)
print("\nReorder complete!")

# Verify
from docx import Document
doc = Document(DST)
print("\nFinal Ch 3 section order:")
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if 'Heading' in p.style.name and t:
        if t.startswith('3.') or t.startswith('4.'):
            print(f"  P{i}: {t[:80]}")
