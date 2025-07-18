from pdf2docx import Converter
import pyttsx3
from docx import Document

pdf_file = "text_to_speech.pdf"
docx_file = "text_to_speech.docx"

converted = Converter(pdf_file)
converted.convert(docx_file, start=0, end=None)
converted.close()

doc = Document(docx_file)
full_text = ""
for para in doc.paragraphs:
    full_text += para.text + "\n"

engine = pyttsx3.init()
engine.say(full_text)
engine.runAndWait()