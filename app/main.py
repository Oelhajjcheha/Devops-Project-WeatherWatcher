from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Weather Watcher", version="0.1.0")

@app.get("/")
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather Watcher - DevOps Project</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 900px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }
            h1 { 
                color: #667eea; 
                margin-bottom: 10px;
            }
            .status {
                background: #10b981;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                display: inline-block;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌤️ Weather Watcher</h1>
            <p><strong>Sprint 1:</strong> Foundation & Deployment</p>
            <div class="status">✓ Status: Running</div>
            <p>DevOps Group Project - Cloud Native Application</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "0.1.0",
        "sprint": 1
    }

@app.get("/api/info")
def get_info():
    return {
        "project": "Weather Watcher",
        "sprint": 1,
        "tech_stack": ["FastAPI", "Azure", "Docker", "GitHub Actions"]
    }