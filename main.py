from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import video_to_text as vtt
import os
from pathlib import Path
import json
from termcolor import colored

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    try:
        # Startup
        print(colored("Starting up...", "yellow"))
        vtt.check_ffmpeg()
        vtt.setup_directories()
        print(colored("✓ Startup complete", "green"))
        yield
    except Exception as e:
        print(colored(f"Startup Error: {str(e)}", "red"))
        raise
    finally:
        # Shutdown
        print(colored("Shutting down...", "yellow"))

app = FastAPI(lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML template
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

@app.get("/")
async def get():
    return HTMLResponse(html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            data = json.loads(data)
            
            if data["action"] == "process":
                directory = data["directory"]
                
                # Validate directory
                if not os.path.exists(directory):
                    await websocket.send_json({
                        "status": "error",
                        "error": "Directory not found"
                    })
                    continue
                    
                if not os.path.isdir(directory):
                    await websocket.send_json({
                        "status": "error",
                        "error": "Not a valid directory"
                    })
                    continue
                
                # Get video files
                video_files = list(Path(directory).glob("*.mp4"))
                if not video_files:
                    await websocket.send_json({
                        "status": "error",
                        "error": "No MP4 files found in directory"
                    })
                    continue
                
                total_files = len(video_files)
                processed_files = 0
                
                # Process each video
                for video_file in video_files:
                    try:
                        # Update progress
                        await websocket.send_json({
                            "status": "processing",
                            "current_file": video_file.name,
                            "progress": int((processed_files / total_files) * 100)
                        })
                        
                        # Process video
                        vtt.process_video(str(video_file))
                        processed_files += 1
                        
                    except Exception as e:
                        await websocket.send_json({
                            "status": "error",
                            "error": f"Error processing {video_file.name}: {str(e)}"
                        })
                        return
                
                # Send completion message
                await websocket.send_json({
                    "status": "completed",
                    "progress": 100
                })
                
    except WebSocketDisconnect:
        print(colored("Client disconnected", "yellow"))
    except Exception as e:
        print(colored(f"WebSocket error: {str(e)}", "red"))
        try:
            await websocket.send_json({
                "status": "error",
                "error": str(e)
            })
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 