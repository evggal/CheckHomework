# examples.py - Примеры интеграции и расширения

"""
Примеры того как использовать API из разных контекстов
и как расширить функциональность
"""

import asyncio
import json
import time
from datetime import datetime

# ============================================
# 1. PYTHON WEBSOCKET CLIENT
# ============================================

async def example_websocket_client():
    """Пример клиента на Python"""
    try:
        import websockets
    except ImportError:
        print("pip install websockets")
        return
    
    async with websockets.connect('ws://localhost:8000/ws/recognize') as ws:
        # Отправляем картинку
        await ws.send(json.dumps({'image_name': 'matrix_1.jpg'}))
        
        # Получаем результаты
        while True:
            response = await ws.recv()
            data = json.loads(response)
            
            if data['status'] == 'processing':
                print(f"[{data['stage_display']}] Прогресс: {data['progress']}%")
            
            elif data['status'] == 'completed':
                print(f"✓ Распознано: {data['text_recognized']}")
                print(f"✓ Верно: {data['solution_correct']}")
                print(f"⏱️  Время: {data['processing_time_seconds']} сек")
                break

# Запуск: asyncio.run(example_websocket_client())


# ============================================
# 2. REQUESTS (REST API)
# ============================================

def example_rest_api():
    """Пример использования REST API"""
    import requests
    
    # Получить список картинок
    response = requests.get('http://localhost:8000/api/images')
    print("Доступные картинки:")
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    # Получить статус
    response = requests.get('http://localhost:8000/api/status')
    print("\nСтатус сервера:")
    print(json.dumps(response.json(), indent=2))
    
    # Получить информацию о конкретной картинке
    response = requests.get('http://localhost:8000/api/image/matrix_1.jpg')
    print("\nИнформация о matrix_1.jpg:")
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

# Запуск: example_rest_api()


# ============================================
# 3. ЗАГРУЗКА РЕАЛЬНЫХ ИЗОБРАЖЕНИЙ (РАСШИРЕНИЕ)
# ============================================

import os
from pathlib import Path
from typing import Dict, List, Optional

class ImageRecognitionService:
    """Сервис для работы с реальными изображениями"""
    
    def __init__(self, db_path: str = "data/images"):
        self.db_path = Path(db_path)
        self.images_metadata = {}
    
    def scan_directory(self) -> Dict[str, List[str]]:
        """Сканировать директорию и создать индекс картинок"""
        categories = {
            'matrix': [],
            'complex': [],
            'unreadable': []
        }
        
        # Примеры: matrix_*.jpg, complex_*.jpg, unreadable_*.jpg
        for category in categories:
            pattern = f"{category}_*.jpg"
            images = list(self.db_path.glob(pattern))
            categories[category] = [img.name for img in images]
        
        return categories
    
    def get_image_metadata(self, image_name: str) -> Optional[Dict]:
        """Получить метаданные изображения"""
        # В реальной системе можно читать из базы данных или файлов
        return self.images_metadata.get(image_name)
    
    def add_image(self, filename: str, category: str, 
                  text_recognized: bool, solution_correct: Optional[bool],
                  solution_path: Optional[str]):
        """Добавить новое изображение в систему"""
        self.images_metadata[filename] = {
            'category': category,
            'text_recognized': text_recognized,
            'solution_correct': solution_correct,
            'solution_path': solution_path,
            'created_at': datetime.now().isoformat()
        }
        print(f"✓ Добавлено изображение: {filename}")


# ============================================
# 4. БАТЧ ОБРАБОТКА (РАСШИРЕНИЕ)
# ============================================

class BatchProcessor:
    """Обработка нескольких картинок подряд"""
    
    def __init__(self, ws_url: str = 'ws://localhost:8000/ws/recognize'):
        self.ws_url = ws_url
        self.results = []
    
    async def process_batch(self, image_names: List[str]):
        """Обработать список картинок"""
        try:
            import websockets
        except ImportError:
            print("pip install websockets")
            return
        
        for image_name in image_names:
            print(f"\n⏳ Обработка: {image_name}")
            async with websockets.connect(self.ws_url) as ws:
                await ws.send(json.dumps({'image_name': image_name}))
                
                while True:
                    response = await ws.recv()
                    data = json.loads(response)
                    
                    if data['status'] == 'completed':
                        self.results.append(data)
                        print(f"✓ {image_name}: "
                              f"Распознано={data['text_recognized']}, "
                              f"Верно={data['solution_correct']}")
                        break
        
        return self.results
    
    def get_statistics(self) -> Dict:
        """Получить статистику"""
        total = len(self.results)
        recognized = sum(1 for r in self.results if r['text_recognized'])
        correct = sum(1 for r in self.results if r['solution_correct'] is True)
        
        return {
            'total': total,
            'recognized': recognized,
            'correct': correct,
            'recognition_rate': f"{recognized/total*100:.1f}%" if total > 0 else "N/A",
            'correctness_rate': f"{correct/recognized*100:.1f}%" if recognized > 0 else "N/A"
        }

# Запуск батч обработки:
# async def run_batch():
#     processor = BatchProcessor()
#     images = ['matrix_1.jpg', 'matrix_2.jpg', 'complex_1.jpg']
#     await processor.process_batch(images)
#     print(processor.get_statistics())
# asyncio.run(run_batch())


# ============================================
# 5. КЕШИРОВАНИЕ РЕЗУЛЬТАТОВ (ОПТИМИЗАЦИЯ)
# ============================================

from functools import lru_cache

class ResultCache:
    """Кеширование результатов обработки"""
    
    def __init__(self, ttl_seconds: int = 3600):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get(self, image_name: str) -> Optional[Dict]:
        """Получить результат из кеша"""
        if image_name not in self.cache:
            return None
        
        timestamp, data = self.cache[image_name]
        if time.time() - timestamp > self.ttl:
            del self.cache[image_name]
            return None
        
        return data
    
    def set(self, image_name: str, data: Dict):
        """Сохранить результат в кеш"""
        self.cache[image_name] = (time.time(), data)
        print(f"✓ Результат закеширован: {image_name}")
    
    def clear(self):
        """Очистить кеш"""
        self.cache.clear()
        print("✓ Кеш очищен")


# ============================================
# 6. ЛОГИРОВАНИЕ И МОНИТОРИНГ (РАСШИРЕНИЕ)
# ============================================

class ProcessingLogger:
    """Логирование обработки"""
    
    def __init__(self, log_file: str = "processing.log"):
        self.log_file = log_file
    
    def log_start(self, image_name: str):
        """Логировать начало обработки"""
        message = f"[{datetime.now().isoformat()}] START: {image_name}"
        self._write(message)
    
    def log_completion(self, image_name: str, data: Dict):
        """Логировать завершение"""
        message = (f"[{datetime.now().isoformat()}] COMPLETED: {image_name} | "
                  f"recognized={data['text_recognized']} | "
                  f"correct={data['solution_correct']}")
        self._write(message)
    
    def log_error(self, image_name: str, error: str):
        """Логировать ошибку"""
        message = f"[{datetime.now().isoformat()}] ERROR: {image_name} | {error}"
        self._write(message)
    
    def _write(self, message: str):
        """Записать в файл"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
        print(message)


# ============================================
# 7. СТАТИСТИКА И ОТЧЕТЫ (РАСШИРЕНИЕ)
# ============================================

class StatisticsCollector:
    """Сбор и анализ статистики"""
    
    def __init__(self):
        self.data = []
    
    def add_result(self, result: Dict):
        """Добавить результат"""
        self.data.append({
            'image_name': result['image_name'],
            'category': result['category'],
            'text_recognized': result['text_recognized'],
            'solution_correct': result['solution_correct'],
            'timestamp': datetime.now().isoformat()
        })
    
    def get_summary(self) -> Dict:
        """Получить сводку"""
        if not self.data:
            return {'error': 'No data'}
        
        total = len(self.data)
        by_category = {}
        
        for item in self.data:
            cat = item['category']
            if cat not in by_category:
                by_category[cat] = {'total': 0, 'recognized': 0, 'correct': 0}
            
            by_category[cat]['total'] += 1
            if item['text_recognized']:
                by_category[cat]['recognized'] += 1
            if item['solution_correct']:
                by_category[cat]['correct'] += 1
        
        return {
            'total_processed': total,
            'by_category': by_category,
            'overall_recognition_rate': f"{sum(1 for d in self.data if d['text_recognized'])/total*100:.1f}%"
        }
    
    def export_csv(self, filename: str = "stats.csv"):
        """Экспортировать в CSV"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['image_name', 'category', 
                                                     'text_recognized', 'solution_correct', 
                                                     'timestamp'])
            writer.writeheader()
            writer.writerows(self.data)
        
        print(f"✓ Статистика экспортирована в {filename}")


# ============================================
# 8. ИНТЕГРАЦИЯ С БАЗОЙ ДАННЫХ (РАСШИРЕНИЕ)
# ============================================

class DatabaseBackend:
    """Интеграция с базой данных"""
    
    def __init__(self, db_url: str = "sqlite:///recognition.db"):
        # Пример для SQLite
        import sqlite3
        self.conn = sqlite3.connect(db_url.replace('sqlite:///', ''))
        self._init_tables()
    
    def _init_tables(self):
        """Инициализировать таблицы"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                image_name TEXT,
                category TEXT,
                text_recognized BOOLEAN,
                solution_correct BOOLEAN,
                processing_time FLOAT,
                created_at TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def save_result(self, result: Dict):
        """Сохранить результат в БД"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO results 
            (image_name, category, text_recognized, solution_correct, processing_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            result['image_name'],
            result['category'],
            result['text_recognized'],
            result['solution_correct'],
            result['processing_time_seconds'],
            result['timestamp']
        ))
        self.conn.commit()
    
    def get_stats(self) -> Dict:
        """Получить статистику из БД"""
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM results')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM results WHERE text_recognized = 1')
        recognized = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM results WHERE solution_correct = 1')
        correct = cursor.fetchone()[0]
        
        return {
            'total': total,
            'recognized': recognized,
            'correct': correct
        }


# ============================================
# 9. ПРИМЕР ИСПОЛЬЗОВАНИЯ ВСЕГО
# ============================================

def complete_example():
    """Полный пример использования всех компонентов"""
    
    print("=" * 50)
    print("ПОЛНЫЙ ПРИМЕР СИСТЕМЫ")
    print("=" * 50)
    
    # 1. Логирование
    logger = ProcessingLogger()
    logger.log_start('matrix_1.jpg')
    
    # 2. Кеширование
    cache = ResultCache()
    
    # 3. Сбор статистики
    stats = StatisticsCollector()
    
    # 4. Симуляция результата
    simulated_result = {
        'image_name': 'matrix_1.jpg',
        'category': 'matrix',
        'text_recognized': True,
        'solution_correct': True,
        'processing_time_seconds': 5.0,
        'timestamp': datetime.now().isoformat()
    }
    
    # 5. Обработка результата
    cache.set('matrix_1.jpg', simulated_result)
    stats.add_result(simulated_result)
    logger.log_completion('matrix_1.jpg', simulated_result)
    
    # 6. Получение сводки
    print("\n" + "=" * 50)
    print("СВОДКА")
    print("=" * 50)
    summary = stats.get_summary()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    # 7. Экспорт
    stats.export_csv()


if __name__ == '__main__':
    # Раскомментируйте нужный пример:
    
    # example_rest_api()
    # asyncio.run(example_websocket_client())
    complete_example()