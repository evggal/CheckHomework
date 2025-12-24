# README - Handwriting Recognition System

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run backend
```bash
python app.py
```

You should see:
```
==================================================
Starting server on http://localhost:8000
WebSocket: ws://localhost:8000/ws/recognize
==================================================
```

### 3. Open frontend
Open `frontend.html` in your browser

That's it! The system is ready to use.

---

## How It Works

1. **Upload Image**: Click or drag an image file (JPG, PNG, GIF)
2. **Auto-Detection**: System automatically detects category from filename:
   - "matrix" in filename -> Matrix category
   - "complex" in filename -> Complex numbers category
   - "unreadable" in filename -> Unreadable category
3. **Process**: Click "Process Image" button
4. **Real-time Updates**: Watch progress bar update in real-time (5 stages)
5. **Results**: See if text was recognized, if solution is correct, and step-by-step solution

---

## System Architecture

### Backend (app.py)
- FastAPI application with WebSocket support
- File upload endpoint for handling images
- 18 test images database (hardcoded)
- 5-stage processing simulation
- Real-time progress updates

### Frontend (frontend.html)
- Drag-and-drop file upload
- Real-time progress visualization
- Results display with solution content
- Connection status indicator
- Responsive design

### Communication
- WebSocket for real-time updates
- REST API for file uploads
- CORS configured for cross-origin requests

---

## API Endpoints

### WebSocket
```
ws://localhost:8000/ws/recognize

Send:
{
    "image_path": "/path/to/file",
    "filename": "matrix_1.jpg"
}

Receive:
{
    "status": "completed",
    "text_recognized": true/false,
    "solution_correct": true/false/null,
    "solution_content": "..."
}
```

### REST
```
POST /api/upload
GET /api/status
GET /
```

---

## Processing Stages (5 seconds)

1. Loading neural network model (1.0 sec) -> 15%
2. Image preprocessing (1.2 sec) -> 35%
3. OCR text recognition (1.5 sec) -> 60%
4. Solution analysis and verification (0.8 sec) -> 85%
5. Finalizing results (0.5 sec) -> 100%

---

## Test Scenarios

### Scenario 1: Matrix Image
1. Upload file with "matrix" in filename
2. System detects: Matrix category
3. Processes for 5 seconds
4. Shows result: Text recognized, and solution status

### Scenario 2: Complex Numbers
1. Upload file with "complex" in filename
2. Category: Complex numbers
3. Random solution correctness (for demo)

### Scenario 3: Unreadable
1. Upload file with "unreadable" in filename
2. Result: Text NOT recognized

---

## File Structure

```
project/
├── app.py                 # Backend server
├── frontend.html          # Web interface
├── requirements.txt       # Dependencies
└── README.md             # This file
```

---

## Features

- No emojis/symbols (clean ASCII only)
- Real file upload from browser
- Automatic category detection
- WebSocket real-time updates
- Progress visualization
- Solution display
- Connection status indicator
- Responsive design
- Error handling

---

## Supported File Types

- JPG, JPEG
- PNG
- GIF
- Maximum: 10MB

---

## Customization

### Add More Solutions
Edit `SOLUTIONS` dictionary in `app.py`:
```python
SOLUTIONS = {
    "solutions/custom_solution.txt": """
    Your solution here
    """
}
```

### Change Processing Time
Modify `PROCESSING_STAGES` in `app.py`:
```python
PROCESSING_STAGES = [
    {"name": "stage_name", "duration": 1.5, "progress": 50},
    ...
]
```

### Modify Database
Update `IMAGES_DB` in `app.py` with your own data.

---

## Technical Stack

- **Backend**: FastAPI, Uvicorn, Python 3.8+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Communication**: WebSocket, REST API
- **Async**: asyncio for non-blocking operations

---

## Troubleshooting

### "Connection refused"
- Make sure backend is running: `python app.py`
- Check port 8000 is available

### "File upload fails"
- Check file size is under 10MB
- Browser console (F12) for error details
- Verify `uploads` directory exists

### "WebSocket closes immediately"
- Backend might be down
- Frontend automatically reconnects every 3 seconds

### "No solution displayed"
- Solution may not exist for that category
- Check SOLUTIONS dictionary in app.py

---

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

```bash
docker build -t handwriting-recognition .
docker run -p 8000:8000 handwriting-recognition
```

---

## Security Notes

- No authentication (development only)
- CORS allows all origins (for development)
- File size limit: 10MB
- Upload directory: `./uploads`

For production, add:
- Authentication/JWT
- Rate limiting
- HTTPS/WSS
- Input validation
- File type checking
- Antivirus scanning

---

## Version
1.0 - December 2024

## Status
Production Ready (for demo/testing)
