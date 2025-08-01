from flask import Flask, render_template
import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from parser import parse_product  # Импорт функции из parser.py

app = Flask(__name__)

# Конфигурация
WORK_DIR = Path("C:/Users/alink/OneDrive/Desktop/work")
CSV_PATH = WORK_DIR / "URL_list.csv"
MAX_URLS = 100  # Лимит URL для обработки (измени на нужное число)
THREADS = 15    # Количество потоков

def parse_batch(urls):
    """Многопоточный парсинг"""
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(filter(None, executor.map(parse_product, urls)))
    return results

@app.route("/")
def show_results():
    # Чтение CSV
    with open(CSV_PATH, encoding='utf-8') as f:
        urls = [row[0] for row in csv.reader(f) if row and row[0].startswith('http')][:MAX_URLS]
    
    # Парсинг с прогресс-баром в консоли
    print(f"🔍 Запуск парсинга {len(urls)} URL...")
    results = parse_batch(urls)
    print(f"✅ Готово! Обработано {len(results)} товаров")
    
    return render_template("results.html", products=results)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)  # Включен многопоточный режим