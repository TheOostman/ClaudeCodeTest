import asyncio
import json
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import BACKEND_PORT
from db import init_db, get_recent_events, get_all_products
from agents.manager import AgentManager

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

# Shared state
connected_clients: set[WebSocket] = set()
agent_manager = AgentManager()

async def broadcast(msg: dict):
    dead = set()
    data = json.dumps(msg)
    for ws in connected_clients:
        try:
            await ws.send_text(data)
        except Exception:
            dead.add(ws)
    connected_clients.difference_update(dead)

agent_manager.set_broadcast(broadcast)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    log.info('Database initialised')
    await agent_manager.start()
    log.info('Agent manager started')
    yield
    await agent_manager.stop()

app = FastAPI(title='Agent Business Backend', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.websocket('/ws')
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    connected_clients.add(ws)
    log.info(f'Client connected ({len(connected_clients)} total)')

    # Send full state snapshot on connect
    events   = await get_recent_events(50)
    products = await get_all_products()
    await ws.send_text(json.dumps({
        'type':     'state',
        'agents':   agent_manager.get_state(),
        'events':   events,
        'products': products,
        'revenue':  {},
    }))

    try:
        while True:
            raw = await ws.receive_text()
            cmd = json.loads(raw)
            await handle_command(cmd)
    except WebSocketDisconnect:
        connected_clients.discard(ws)
        log.info(f'Client disconnected ({len(connected_clients)} remaining)')

async def handle_command(cmd: dict):
    t = cmd.get('type')
    if t == 'ping':
        await broadcast({'type': 'pong'})
    elif t == 'start':
        await agent_manager.run_cycle()
    elif t == 'stop':
        await agent_manager.stop_cycle()

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=BACKEND_PORT, reload=False)
