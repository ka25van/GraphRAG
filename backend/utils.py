import fitz #to work with pdf files
import spacy 

nlp=spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    return " ".join([page.get_text() for page in doc])

def extract_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        sentence = ent.sent.text  
        entities.append((ent.text, ent.label_, sentence))
    return entities