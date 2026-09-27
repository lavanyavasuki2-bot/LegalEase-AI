import os
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LegalEase AI Backend")

GEMINI_API_KEY =("AQ.Ab8RN6I6_VTiBmu2axfZR_fxDWOW84JrFjaedECyYy_8rAiqwg")

class DocumentRequest(BaseModel):
    doc_type: str
    parties: str
    effective_date: str
    key_terms: str

@app.post("/generate")
def generate_doc(req: DocumentRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key is missing.")

    prompt = f"""
    You are an expert legal draft assistant.
    Generate a formal and legally structured document for a: {req.doc_type}

    Parties Involved: {req.parties}
    Effective Date: {req.effective_date}
    Key Terms & Conditions: {req.key_terms}

    Provide a complete draft with standard legal sections (Parties, Recitals, Terms, Signatures).
    Do not use raw html tags.
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()

        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return {"status": "success", "document_text": generated_text}
        else:
            raise HTTPException(status_code=500, detail=f"API Error: {response_json}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))