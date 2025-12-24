# app.py - FastAPI с WebSocket для распознавания рукописных работ
from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import time
from datetime import datetime
from pathlib import Path
import shutil
import os
import random

app = FastAPI()

# CORS конфиг для связи с фронтэндом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Директория для загрузки файлов
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ============================================
# БАЗА ДАННЫХ: 18 картинок
# ============================================

IMAGES_DB = {
    # ===== МАТРИЦЫ (6) =====
    "matrix_1.jpg": {
        "category": "matrix",
        "text_recognized": True,
        "solution_correct": True,
        "solution_path": "solutions/matrix_1_steps.txt",
        "description": "Matrix 2x2 - inversion"
    },
    "matrix_2.jpg": {
        "category": "matrix",
        "text_recognized": True,
        "solution_correct": False,
        "solution_path": "solutions/matrix_2_steps.txt",
        "description": "Matrix 3x3 - wrong solution"
    },
    "matrix_3.jpg": {
        "category": "matrix",
        "text_recognized": True,
        "solution_correct": True,
        "solution_path": "solutions/matrix_3_steps.txt",
        "description": "Matrix 2x3 - multiplication"
    },
    "matrix_4.jpg": {
        "category": "matrix",
        "text_recognized": True,
        "solution_correct": True,
        "solution_path": "solutions/matrix_4_steps.txt",
        "description": "Matrix 4x4 - determinant"
    },
    "matrix_5.jpg": {
        "category": "matrix",
        "text_recognized": True,
        "solution_correct": False,
        "solution_path": "solutions/matrix_5_steps.txt",
        "description": "Matrix 3x3 - calculation error"
    },
    "matrix_6.jpg": {
        "category": "matrix",
        "text_recognized": True,
        "solution_correct": True,
        "solution_path": "solutions/matrix_6_steps.txt",
        "description": "Matrix 2x2 - correct solution"
    },

    # ===== КОМПЛЕКСНЫЕ ЧИСЛА (6) =====
    "complex_1.jpg": {
        "category": "complex",
        "text_recognized": True,
        "solution_correct": True,
        "solution_path": "solutions/complex_1_steps.txt",
        "description": "Complex number: (3+4i)^2 = ?"
    },
    "complex_2.jpg": {
        "category": "complex",
        "text_recognized": True,
        "solution_correct": False,
        "solution_path": "solutions/complex_2_steps.txt",
        "description": "Complex number: division - wrong"
    },
    "complex_3.jpg": {
        "category": "complex",
        "text_recognized": True,
        "solution_correct": True,
        "solution_path": "solutions/complex_3_steps.txt",
        "description": "Complex number: modulus and argument"
    },
    "complex_4.jpg": {
        "category": "complex",
        "text_recognized": True,
        "solution_correct": True,
        "solution_path": "solutions/complex_4_steps.txt",
        "description": "Complex number: multiplication"
    },
    "complex_5.jpg": {
        "category": "complex",
        "text_recognized": True,
        "solution_correct": False,
        "solution_path": "solutions/complex_5_steps.txt",
        "description": "Complex number: formula error"
    },
    "complex_6.jpg": {
        "category": "complex",
        "text_recognized": True,
        "solution_correct": True,
        "solution_path": "solutions/complex_6_steps.txt",
        "description": "Complex number: cube root extraction"
    },

    # ===== НЕРАЗБОРЧИВЫЕ РАБОТЫ (6) =====
    "unreadable_1.jpg": {
        "category": "unreadable",
        "text_recognized": False,
        "solution_correct": None,
        "solution_path": None,
        "description": "Unreadable - cannot recognize"
    },
    "unreadable_2.jpg": {
        "category": "unreadable",
        "text_recognized": False,
        "solution_correct": None,
        "solution_path": None,
        "description": "Poor image quality"
    },
    "unreadable_3.jpg": {
        "category": "unreadable",
        "text_recognized": False,
        "solution_correct": None,
        "solution_path": None,
        "description": "Blurred photo"
    },
    "unreadable_4.jpg": {
        "category": "unreadable",
        "text_recognized": False,
        "solution_correct": None,
        "solution_path": None,
        "description": "Text written very small"
    },
    "unreadable_5.jpg": {
        "category": "unreadable",
        "text_recognized": False,
        "solution_correct": None,
        "solution_path": None,
        "description": "Smudged writing"
    },
    "unreadable_6.jpg": {
        "category": "unreadable",
        "text_recognized": False,
        "solution_correct": None,
        "solution_path": None,
        "description": "Poor camera angle"
    },
}

# Решения в виде строк (псевдографика)
SOLUTIONS = {
    "solutions/matrix_1_steps.txt": """
+-------------------------------------+
| SOLUTION: Matrix Inversion 2x2      |
+-------------------------------------+

A = |a  b|
    |c  d|

Step 1: Determinant
det(A) = ad - bc
det(A) = 1*4 - 2*3 = 4 - 6 = -2

Step 2: Inverse matrix
A^-1 = 1/det(A) * |d  -b|
                  |-c   a|

A^-1 = -1/2 * |4  -2|
             |-3   1|

A^-1 = |-2   1  |
       |3/2 -1/2|

CORRECT SOLUTION
""",

    "solutions/matrix_2_steps.txt": """
+-------------------------------------+
| SOLUTION: Matrix 3x3 - Error        |
+-------------------------------------+

System of linear equations:
x + 2y + 3z = 14
2x + y + z = 11
3x + 3y + 2z = 20

Gauss method:
Step 1: R2 - 2R1
Step 2: R3 - 3R1

Student got: x = 2, y = 3, z = 4

Check:
1*2 + 2*3 + 3*4 = 2 + 6 + 12 = 20 != 14

INCORRECT SOLUTION
Correct answer: x = 1, y = 2, z = 3
""",

    "solutions/matrix_3_steps.txt": """
+-------------------------------------+
| SOLUTION: Matrix Multiplication 2x3 |
+-------------------------------------+

A = |1 2 3|    B = |4 5|
    |4 5 6|        |6 7|
                   |8 9|

A*B = |1*4+2*6+3*8  1*5+2*7+3*9|
      |4*4+5*6+6*8  4*5+5*7+6*9|

     = |4+12+24   5+14+27|
       |16+30+48  20+35+54|

     = |40  46|
       |94 109|

CORRECT SOLUTION
""",

    "solutions/matrix_4_steps.txt": """
+-------------------------------------+
| SOLUTION: Determinant 4x4           |
+-------------------------------------+

Matrix:
|1 2 3 4|
|5 6 7 8|
|9 8 7 6|
|4 3 2 1|

Expansion by first row:
det = 1*M11 - 2*M12 + 3*M13 - 4*M14

Computing 3x3 minors...

det(A) = 288

CORRECT SOLUTION
""",

    "solutions/matrix_5_steps.txt": """
+-------------------------------------+
| SOLUTION: Matrix 3x3 - Error        |
+-------------------------------------+

Computing determinant:

det = |2 1 1|
      |1 2 1|
      |1 1 2|

Sarrus formula:
det = 2*2*2 + 1*1*1 + 1*1*1 
    - 1*2*1 - 1*1*2 - 1*1*2

Student calculated = 0
Correct = 4

INCORRECT SOLUTION
Error in computing diagonals
""",

    "solutions/matrix_6_steps.txt": """
+-------------------------------------+
| SOLUTION: Matrix Inversion 2x2      |
+-------------------------------------+

A = |3 1|
    |2 5|

det(A) = 3*5 - 1*2 = 15 - 2 = 13

A^-1 = 1/13 * |5  -1|
              |-2   3|

     = |5/13  -1/13|
       |-2/13  3/13|

CORRECT SOLUTION
""",

    "solutions/complex_1_steps.txt": """
+-------------------------------------+
| SOLUTION: (3+4i)^2 = ?              |
+-------------------------------------+

(3+4i)^2 = (3+4i)*(3+4i)

= 3^2 + 2*3*4i + (4i)^2
= 9 + 24i + 16i^2
= 9 + 24i - 16
= -7 + 24i

CORRECT SOLUTION
""",

    "solutions/complex_2_steps.txt": """
+-------------------------------------+
| SOLUTION: Division of Complex       |
+-------------------------------------+

(5+3i)/(2-i) = ?

Student: (5+3i)/(2-i) = 5/2 + 3i/(-i) = 2.5 - 3

Correct:
= (5+3i)(2+i) / ((2-i)(2+i))
= (10+5i+6i+3i^2) / (4-i^2)
= (10+11i-3) / (4+1)
= (7+11i) / 5
= 1.4 + 2.2i

INCORRECT SOLUTION
""",

    "solutions/complex_3_steps.txt": """
+-------------------------------------+
| SOLUTION: Modulus and Argument      |
+-------------------------------------+

z = 1 + i*sqrt(3)

|z| = sqrt(1^2 + (sqrt(3))^2) = sqrt(1+3) = sqrt(4) = 2

arg(z) = arctan(sqrt(3)/1) = arctan(sqrt(3)) = pi/3

Trigonometric form:
z = 2(cos(pi/3) + i*sin(pi/3))
z = 2*e^(i*pi/3)

CORRECT SOLUTION
""",

    "solutions/complex_4_steps.txt": """
+-------------------------------------+
| SOLUTION: Multiplication of Complex |
+-------------------------------------+

z1 = 2+i
z2 = 3-2i

z1*z2 = (2+i)(3-2i)
      = 2*3 + 2*(-2i) + i*3 + i*(-2i)
      = 6 - 4i + 3i - 2i^2
      = 6 - i + 2
      = 8 - i

CORRECT SOLUTION
""",

    "solutions/complex_5_steps.txt": """
+-------------------------------------+
| SOLUTION: De Moivre's Formula       |
+-------------------------------------+

(1+i)^10 = ?

Student applied formula incorrectly:
(1+i)^10 = 1 + 10i (WRONG)

Correct:
z = 1+i = sqrt(2)*e^(i*pi/4)
z^10 = (sqrt(2))^10*e^(i*10*pi/4)
     = 2^5*e^(i*5*pi/2)
     = 32*i

INCORRECT SOLUTION
""",

    "solutions/complex_6_steps.txt": """
+-------------------------------------+
| SOLUTION: Cube Root of Complex      |
+-------------------------------------+

^3*sqrt(8i) = ?

8i = 8*e^(i*(pi/2+2*pi*k))

^3*sqrt(8i) = 2*e^(i*(pi/6+2*pi*k/3)), k=0,1,2

k=0: 2e^(i*pi/6) = sqrt(3) + i
k=1: 2e^(i*5*pi/6) = -sqrt(3) + i
k=2: 2e^(i*3*pi/2) = -2i

CORRECT SOLUTION
""",
}


# ============================================
# ОПРЕДЕЛЕНИЕ КАТЕГОРИИ ПО НАЗВАНИЮ ФАЙЛА
# ============================================

def detect_image_category(filename: str) -> str:
    """Определяет категорию по названию файла"""
    filename_lower = filename.lower()

    if 'matrix' in filename_lower:
        return 'matrix'
    elif 'complex' in filename_lower:
        return 'complex'
    elif 'unreadable' in filename_lower:
        return 'unreadable'
    else:
        return 'unreadable'


# ============================================
# FILE UPLOAD ENDPOINT
# ============================================

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Загрузить файл на сервер"""
    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            'status': 'success',
            'filename': file.filename,
            'file_path': str(file_path),
            'message': 'File uploaded successfully'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Upload failed: {str(e)}'
        }


# ============================================
# FILE PROCESS ENDPOINT (НОВЫЙ!)
# ============================================

@app.post("/api/process")
async def process_file(data: dict):
    """Обработать загруженный файл"""
    try:
        image_path = data.get('image_path', '')
        filename = data.get('filename', '')

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Processing: {filename}")

        # Проверка наличия файла
        if not os.path.exists(image_path):
            return {
                'status': 'error',
                'message': 'File not found on server'
            }

        # Определяем категорию
        category = detect_image_category(filename)

        # Имитация обработки
        await asyncio.sleep(2)

        # Определяем результаты на основе категории
        if category == 'unreadable':
            text_recognized = False
            solution_correct = None
            solution_content = None
        else:
            text_recognized = True
            solution_correct = random.choice([True, False])
            solution_key = f"solutions/{category}_1_steps.txt"
            if solution_key in SOLUTIONS:
                solution_content = SOLUTIONS[solution_key]
            else:
                solution_content = None

        result = {
            'status': 'success',
            'filename': filename,
            'category': category,
            'text_recognized': text_recognized,
            'solution_correct': solution_correct,
            'solution_content': solution_content,
            'processing_time_seconds': 2.0
        }

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Processing completed: {filename}")

        return result

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {str(e)}")
        return {
            'status': 'error',
            'message': f'Processing error: {str(e)}'
        }


# ============================================
# STATUS ENDPOINT
# ============================================

@app.get("/api/status")
async def get_status():
    """Проверка статуса сервера"""
    return {
        'status': 'online',
        'available_images': len(IMAGES_DB),
        'matrices': len([x for x in IMAGES_DB.values() if x['category'] == 'matrix']),
        'complex_numbers': len([x for x in IMAGES_DB.values() if x['category'] == 'complex']),
        'unreadable': len([x for x in IMAGES_DB.values() if x['category'] == 'unreadable']),
        'server_time': datetime.now().isoformat()
    }


@app.get("/")
async def root():
    """Главная страница с информацией"""
    return {
        'name': 'Neural Network Handwriting Recognition API',
        'version': '1.0',
        'endpoints': {
            'upload': 'POST /api/upload',
            'process': 'POST /api/process',
            'get_status': 'GET /api/status'
        },
        'description': '18 images: 6 matrices, 6 complex numbers, 6 unreadable'
    }


# ============================================
# ЗАПУСК СЕРВЕРА
# ============================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 50)
    print("Starting server on http://localhost:8000")
    print("Upload: POST /api/upload")
    print("Process: POST /api/process")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)
