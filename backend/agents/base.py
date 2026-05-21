import asyncio
import logging
from datetime import datetime
from typing import Callable, Awaitable

import anthropic
from config import ANTHROPIC_API_KEY

log = logging.getLogger(__name__)

class BaseAgent:
    name: str = 'base'
    model: str = 'claude-haiku-4-5-20251001'

    def __init__(self):
        self.status     = 'idle'
        self.task       = None
        self.last_action = None
        self._broadcast: Callable[[dict], Awaitable] | None = None
        self._client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

    def set_broadcast(self, fn: Callable[[dict], Awaitable]):
        self._broadcast = fn

    async def emit(self, message: str):
        log.info(f'[{self.name}] {message}')
        self.last_action = message
        if self._broadcast:
            await self._broadcast({
                'type':    'event',
                'agent':   self.name,
                'message': message,
                'ts':      datetime.utcnow().isoformat(),
            })
            await self._broadcast({
                'type':  'agent_update',
                'agent': self.name,
                'data':  self.get_state(),
            })

    async def set_status(self, status: str, task: str | None = None):
        self.status = status
        if task is not None:
            self.task = task
        if self._broadcast:
            await self._broadcast({
                'type':  'agent_update',
                'agent': self.name,
                'data':  self.get_state(),
            })

    async def think(self, system: str, prompt: str, max_tokens: int = 1024) -> str:
        if not self._client:
            return '[No API key configured]'
        msg = await self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return msg.content[0].text

    def get_state(self) -> dict:
        return {
            'status':     self.status,
            'task':       self.task,
            'lastAction': self.last_action,
            'model':      self.model,
        }

    async def run(self, context: dict) -> dict:
        raise NotImplementedError
