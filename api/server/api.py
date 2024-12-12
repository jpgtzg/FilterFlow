from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from models.monitor import EmailMonitor

app = FastAPI()
monitors = {}

class MonitorCreate(BaseModel):
    username: str
    password: str
    filters: List[str]

class MonitorResponse(BaseModel):
    id: str
    username: str
    filters: List[str]
    is_running: bool

@app.get("/")
def read_root():
    return {"message": "Welcome to the email monitor API"}

@app.post("/monitors")
def create_monitor(monitor_data: MonitorCreate):
    monitor_id = str(len(monitors))
    monitor = EmailMonitor(
        username=monitor_data.username,
        password=monitor_data.password,
        monitor_id=monitor_id
    )
    monitor.filters = monitor_data.filters
    monitors[monitor_id] = monitor
    
    return {"monitor_id": monitor_id}

@app.get("/monitors")
def get_monitors():
    monitor_list = []
    for monitor_id, monitor in monitors.items():
        print(f"Monitor {monitor_id} status: {monitor.is_running}")
        monitor_list.append({
            "id": monitor_id,
            "username": monitor.username,
            "filters": monitor.filters,
            "is_running": monitor.is_running.is_set() if hasattr(monitor.is_running, 'is_set') else bool(monitor.is_running)
        })
    return monitor_list

@app.post("/monitors/{monitor_id}/start")
def start_monitor(monitor_id: str):
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    monitors[monitor_id].start_monitoring()
    return {"status": "success"}

@app.post("/monitors/{monitor_id}/stop")
def stop_monitor(monitor_id: str):
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    monitors[monitor_id].stop_monitoring()
    return {"status": "success"}

@app.get("/monitors/{monitor_id}")
def get_monitor(monitor_id: str):
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    monitor = monitors[monitor_id]
    return {
        "id": monitor_id,
        "username": monitor.username,
        "filters": monitor.filters,
        "is_running": monitor.is_running
    }

@app.post("/monitors/{monitor_id}/filters")
def update_filters(monitor_id: str, filters: List[str]):
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    monitors[monitor_id].filters = filters
    return {"status": "success"}
