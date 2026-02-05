# ChatbotAI (FastAPI + Basit HTML Arayüz)

Bu proje, FastAPI ile yazılmış basit bir backend ve tek sayfalık (`index.html`) bir arayüzden oluşur.  
`/ask` endpoint’i üzerinden soru gönderip cevap alırsın.

Projeyi iki modda çalıştırabilirsin:

- **Ücretsiz / Mock Modu (Önerilen)**: OpenAI kredisi olmadan çalışır, sahte cevap döndürür.
- **Ücretli / OpenAI Modu**: OpenAI API Key + kredi/billing ile gerçek modelden cevap döndürür.

---

## Özellikler

- FastAPI backend
- HTML + JS frontend (tek dosya)
- `/health` ile servis kontrolü
- `/` üzerinden `index.html` servis edilir
- `/ask` üzerinden soru/cevap (Mock veya OpenAI)

---

## Proje Yapısı

chatbotai/

main.py

index.html

.env (Git'e eklenmez)

.gitignore

requirements.txt

README.md


---

## Kurulum

### 1) Sanal ortam oluştur ve aktif et

Windows PowerShell:

```bash
python -m venv venv
venv\Scripts\activate

2) Bağımlılıkları yükle
pip install -r requirements.txt

3) Uygulamayı başlat
uvicorn main:app --reload --port 8000

Tarayıcı:

Arayüz: http://127.0.0.1:8000/

Sağlık kontrolü: http://127.0.0.1:8000/health

API dokümantasyonu: http://127.0.0.1:8000/docs

Kullanım Modları
A) Ücretsiz Kullanım — Mock Modu ✅ (Kredi yoksa bunu kullan)

Bu mod OpenAI çağrısı yapmaz. /ask endpoint’i şuna benzer cevap döndürür:

(Mock cevap) Sen şunu sordun: ...

main.py içinde açık olan kısım:

@app.post("/ask", response_model=AskResponse)
def ask_ai(payload: AskRequest):
    return {"answer": f"(Mock cevap) Sen şunu sordun: {payload.question}"}

Bu modda:

✅ OpenAI API key gerekmez

✅ kredi/billing gerekmez

✅ arayüz + backend akışı test edilir

❌ gerçek yapay zeka cevabı üretmez

B) Ücretli Kullanım — OpenAI Modu 💳 (API Key + Kredi/Billing gerekir)

Bu modda OpenAI API çağrısı yapılır ve gerçek cevap döner.

1) .env dosyası oluştur

Proje klasöründe .env dosyası aç:

OPENAI_API_KEY=sk-...

Not: .env dosyası .gitignore ile Git’e gönderilmez.

2) OpenAI kodunu aktif et

main.py içinde yorum satırı olan OpenAI bloğunu aç (uncomment), mock bloğunu kapat.

Mock bloğunu kapat:

# @app.post("/ask", response_model=AskResponse)
# def ask_ai(payload: AskRequest):
#     return {"answer": f"(Mock cevap) Sen şunu sordun: {payload.question}"}

OpenAI bloğunu aç:
@app.post("/ask", response_model=AskResponse)
def ask_ai(payload: AskRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": payload.question},
            ],
        )

        answer = response.choices[0].message.content
        return {"answer": answer}

    except Exception as e:
        print("OPENAI ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))

Bu modda:

✅ gerçek model cevabı gelir

✅ mock yerine gerçek “AI” çalışır

❌ OpenAI API key şart

❌ OpenAI kredi/billing şart (aksi halde 429 insufficient_quota alırsın)

Frontend (index.html) Nasıl Çalışır?

Arayüzdeki butona basınca şu istek gider:

POST /ask

JSON body: { "question": "..." }

Projede frontend ve backend aynı server üzerinde çalıştığı için:

const API_BASE = "";

kullanılır ve istek doğrudan /ask’a gider.

Sık Karşılaşılan Hatalar
Hata: Internal Server Error

Genelde OpenAI çağrısı sırasında backend’de hata olmuştur.
Terminaldeki uvicorn loglarını kontrol et.

429 insufficient_quota

OpenAI tarafında kredi/billing yoktur veya kredi bitmiştir.
Çözüm:

Mock moduna geç

veya Billing/Credit Balance ekle

GET / 404

/ route’u tanımlı değilse olur. Bu projede FileResponse("index.html") ile tanımlıdır.

Lisans

Bu proje eğitim/öğrenme amaçlıdır.

