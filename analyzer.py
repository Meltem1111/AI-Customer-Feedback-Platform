from google import genai
from config import GEMINI_API_KEY, MODEL_NAME
import json

MY_API_KEY =""

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
                Sen profesyonel bir duygu analizi ve dil uzmanısın.
                Aşağıdaki metni analiz et.

                {text}
                Lütfen yanıtını SADECE (başka hiçbir açıklama olmadan) aşağıdaki JSON formatında ver:

                {
                    {
                        "sentiment":"Pozitif ,Negatif veya Nötr",
                        "score":"0 ile 100 arası bir sayı(100 =Çok olumlu)",
                        "summary":"Metnin ana fikri (Maksimum 10 kelime)",
                        "language":"Metnin dili (tr, en, de vb.)"
                    }
                }
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={
                    'response_mime_type':'application/json'
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
                "language":"Bilinmiyor",
                "error_detail":str(ex)
            }
        

if __name__ =="__main__":
    analizci =SentimentAnalyzer()

    #ornek_yorum ="Ürünü beğendim ama kargo çok geç geldi, biraz sinirlendim."
    #ornek_yorum = "Ürün çok güzel ancak bedeni bana olmadı bir beden büyük alıcam."
    ornek_yorum = "Berbat bir ürün çok kalitesiz, rengi de çok kötü"
    sonuc = analizci.analyze_text(ornek_yorum)

    print(sonuc)