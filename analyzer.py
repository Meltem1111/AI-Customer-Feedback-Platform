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

                    { {
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
                            "language":"Metnin dili (tr, en, de vb.)",
                            "category":"Ürün"
                    }}
        Kurallar:
        -keywords kısmına en önemli 5 anahtar kelimeyi yaz.
        - score 0 ile 100 arasında tam sayı olmalıdır.
        - score, yorumun pozitiflik veya negatiflik derecesini yansıtmalıdır.
        - Score verirken her yorum için aynı veya benzer sabit değerleri kullanma.
        - Yorumun ifade ettiği duygu, memnuniyet düzeyi, olumlu/olumsuz ifadelerin şiddeti ve varsa karşıt ifadeleri birlikte değerlendir.
        - Hafif olumlu yorumlarda yaklaşık 55-70 aralığı,
        belirgin olumlu yorumlarda yaklaşık 70-85 aralığı,
        çok güçlü olumlu yorumlarda yaklaşık 85-100 aralığı kullan.
        - Hafif olumsuz yorumlarda yaklaşık 30-45 aralığı,
        belirgin olumsuz yorumlarda yaklaşık 15-30 aralığı,
        çok güçlü olumsuz yorumlarda yaklaşık 0-15 aralığı kullan.
        - Nötr yorumlarda yaklaşık 45-55 aralığını kullan.
        - Aynı sentiment kategorisindeki farklı yorumlara otomatik olarak aynı score'u verme.
        - Score'u yalnızca sentiment etiketine göre değil, yorumun içeriğine göre belirle.
        -Başka hiçbir açıklama yazma.
        - category yalnızca şu değerlerden biri olabilir:
        "Ürün"
        "Restoran/Yemek"
        "Kargo/Teslimat"
        "Hizmet"
        "Diğer"

        - Yorumun ana konusuna göre en uygun kategoriyi seç.
        - Ürün kalitesi, özellikleri, fiyatı, bedeni, rengi veya kullanım deneyimi ile ilgili yorumları "Ürün" olarak sınıflandır.
        - Yemek, restoran, kafe, servis veya yemek deneyimi ile ilgili yorumları "Restoran/Yemek" olarak sınıflandır.
        - Kargo, teslimat, gönderim veya siparişin ulaşma süresi ile ilgili yorumları "Kargo/Teslimat" olarak sınıflandır.
        - Müşteri hizmetleri, destek, çalışan davranışı veya verilen hizmet ile ilgili yorumları "Hizmet" olarak sınıflandır.
        - Yorum yalnızca genel bir fikir, tasarım, uygulama arayüzü, marka, logo veya benzeri bir konu hakkında ise ve doğrudan satın alınan/kullanılan fiziksel veya dijital bir ürünün deneyimini anlatmıyorsa "Diğer" olarak sınıflandır.
        - "Ürün" kategorisini yalnızca belirli bir ürünün kalitesi, özellikleri, fiyatı, bedeni, rengi veya kullanım deneyimi açıkça anlatılıyorsa kullan.
        - Bir yorumda "tasarım", "logo", "uygulama", "marka" gibi kelimelerin geçmesi tek başına "Ürün" kategorisi için yeterli değildir.
        - Yukarıdaki kategorilerden hiçbirine uygun olmayan yorumları "Diğer" olarak sınıflandır.
        - category alanında bu liste dışında başka bir değer kullanma.
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

            return {
                "error": "AI analizi sırasında bir hata oluştu.",
                "error_detail": str(ex)
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