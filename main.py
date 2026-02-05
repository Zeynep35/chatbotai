from fastapi import FastAPI
from pydantic import BaseModel 
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.responses import FileResponse
from fastapi import HTTPException

load_dotenv()

app = FastAPI() #web uygulamasının ana nesnesini oluşturur ve herşey buraya bağlanır.

#CORS middleware, tarayıcıdan gelen isteklerin hangi origin’lerden (domain/port/protokol) kabul edileceğini kontrol eder.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#api ile OpenAI servislerine istek gönderecek bir istemci oluşturur.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class AskRequest(BaseModel):   #gelen veriyi denetler ve metin içerip içermediğini kontrol eder.
    question: str 

class AskResponse(BaseModel):
    answer: str 

@app.get("/health")    #GET isteklerini yakalayan ve genelde servisin ayakta olup olmadığını kontrol eder.
def health():
    return {"status":"ok"}


@app.post("/ask", response_model=AskResponse)
def ask_ai(payload: AskRequest):
    return {"answer": f"(Mock cevap) Sen şunu sordun: {payload.question}"}

@app.get("/")
def home():
    return FileResponse("index.html")


#modelin nasıl davranıcağını belirleyen kısım.
#@app.post("/ask", response_model=AskResponse)
#def ask_ai(payload: AskRequest):
    #try:
        #response = client.chat.completions.create(
            #model= "gpt-4o-mini",
            #messages=[
                #{"role": "system", "content": "You are a helpful assistant."},
                #{"role": "user", "content": payload.question}
            #]
       # )

        #answer = response.choices[0].message.content
        #return {"answer": answer}
    #except Exception as e:
        #print("OPENAI ERROR:", repr(e))
        #raise HTTPException(status_code=500, detail=str(e))