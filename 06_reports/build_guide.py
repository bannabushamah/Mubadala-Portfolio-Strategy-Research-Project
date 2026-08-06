import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_style import DocTemplate
import build_guide_p1, build_guide_p2
HERE=os.path.dirname(os.path.abspath(__file__))
doc=DocTemplate(os.path.join(HERE,"Beginner_Guide_Booklet.pdf"),
    "How I Built This Project - Beginner's Guide","Beginner's Guide Booklet")
doc.build(build_guide_p1.build() + build_guide_p2.build())
print("Built Beginner_Guide_Booklet.pdf")
