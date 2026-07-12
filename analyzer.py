from google import genai
from config import GEMINI_API_KEY, MODEL_NAME,TEMPERATURE
import json

class SentimentAnalyzer:
    def __init__(self):
        try:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
            self.model_id = MODEL_NAME
        except Exception as e:
            print(f"Connection error: {e}")
    
    def analyze_text(self,text):
        if not text:
            return {"error": "Boş metin gönderildi."}
        
        prompt = f"""
                Sen profesyonel bir müşteri yorumu analiz uzmanısın.
                Aşağıdaki metni analiz et.

                {text}
                Lütfen yanıtını SADECE (başka hiçbir açıklama olmadan) aşağıdaki JSON formatında ver:

                {
                    {
                        "sentiment":"Pozitif ,Negatif veya Nötr",
                        "score":0 ,
                        "summary":"Metnin ana fikri (Maksimum 10 kelime)",
                        "keywords":[
                            "kelime1",
                            "kelime2",
                            "kelime3",
                            "kelime4",
                            "kelime5"
                        ],
                        "language":"Metnin dili (tr, en, de vb.)"
                    }
                }
        Kurallar:
        -keywords kısmına en önemli 5 anahtar kelimeyi yaz.
        -score 0-100 arasında sayı olsun.
        -Başka hiçbir açıklama yazma.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={
                    "response_mime_type":"application/json",
                    "temperature":TEMPERATURE
                })
            
            clean_text = (response.text.replace("```json","").replace("```","").strip())
            result = json.loads(clean_text)
            return result
        except Exception as ex:
            print(f"Hata oluştu: {ex}")

            return{
                "sentiment":"Hata",
                "score":0,
                "summary":"Analiz sırasında bir hata oluştu",
                "keywords": [],
                "language":"Bilinmiyor",
                "error_detail":str(ex)
            }
        

if __name__ =="__main__":
    analizci =SentimentAnalyzer()

    #ornek_yorum ="Ürünü beğendim ama kargo çok geç geldi, biraz sinirlendim."
    #ornek_yorum = "Ürün çok güzel ancak bedeni bana olmadı bir beden büyük alıcam."
    ornek_yorum = "Berbat bir ürün çok kalitesiz, rengi de çok kötü"
    sonuc = analizci.analyze_text(ornek_yorum)

    print(json.dumps(
    sonuc,
    indent=4, # json'ı daha okunabilir yapıyor.
    ensure_ascii=False # json'da türkçe karakter kullanımı için
))