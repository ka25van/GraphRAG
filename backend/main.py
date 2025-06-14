from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from rag_chain import answer_question
from utils import extract_text_from_pdf, extract_entities
from graph_builder import query_graph


app=FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(await file.read())
    entities = extract_entities(text)
    query_graph(entities)
    return {"status": "Graph built",
            "text": text,
            "entities": entities}

@app.post("/ask_question")
async def ask_question(question: str = Form(...)):
    answer = answer_question(question)
    return {
        "question": question,
        "answer": answer}