import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Referer': 'https://google.com/'
}

def parse_product(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=8)
        response.encoding = 'utf-8'
        
        # Фильтр не-мебели
        if any(word in url.lower() for word in ["gift", "card", "voucher"]):
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Название
        name = (
            soup.find("h1").get_text(strip=True) 
            or soup.find("title").get_text(strip=True)
            or "Название не распознано"
        )
        
        # Цена (улучшенный поиск)
        price = "Не найдена"
        for tag in soup.find_all(class_=re.compile("price|cost|amount", re.I)):
            text = tag.get_text(strip=True)
            if any(c.isdigit() for c in text):
                price = re.sub(r"\s+", " ", text[:100])  # Обрезаем длинные цены
                break
                
        return {"url": url, "name": name, "price": price}
        
    except Exception as e:
        print(f"⚠️ Ошибка: {url} — {str(e)}")
        return None