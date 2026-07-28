import docx
doc = docx.Document('/home/nikhil/roombookings3/roombookings/Hoteliers_Myproject/projectreport/nikhilproject241.docx')

renames = [
    ("8. Implementation Plan", "9. Implementation Plan"),
    ("9. Limitations", "10. Limitations"),
    ("10. Future Application", "11. Future Application"),
    ("11. Conclusion", "12. Conclusion"),
    ("12. Bibliography", "13. Bibliography"),
]

for p in doc.paragraphs:
    t = p.text.strip()
    for old, new in renames:
        if t == old or t.startswith(old):
            for run in p.runs:
                if old in run.text:
                    run.text = run.text.replace(old, new)

doc.save('/home/nikhil/roombookings3/roombookings/Hoteliers_Myproject/projectreport/nikhilproject241.docx')
print("Renumbered!")
