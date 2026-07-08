from google import genai
from config import GEMINI_API_KEY, MODEL_NAME
MY_API_KEY =""

client = genai.Client(api_key=MY_API_KEY)

try:
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents="Bana yazılımcılarla ilgili çok kısa,tek cümlelik komik bir şaka yap."
    ) 
    print(response.text)

except Exception as e:
    print("Hata oluştur.\n")
    print(f"Hata detayi: {e}")

