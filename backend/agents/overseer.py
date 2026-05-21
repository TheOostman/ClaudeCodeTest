import json
from config import MODEL_SONNET
from .base import BaseAgent

class OverseerAgent(BaseAgent):
    name  = 'overseer'
    model = MODEL_SONNET

    def __init__(self):
        super().__init__()
        self.queue = []

    def get_state(self):
        return {**super().get_state(), 'queue': self.queue}

    async def plan(self, directive: str) -> list[dict]:
        await self.set_status('working', f'Planning tasks for: {directive}')
        await self.emit(f'Received directive: {directive}')

        system = (
            'You are the Overseer coordinating a team of AI agents for an Etsy shirt business. '
            'Break the directive into ordered tasks. Each task has: agent (research/design/listing/marketing/analytics/operations), '
            'type (string), payload (dict). Output JSON array only.'
        )
        prompt = f'Directive: {directive}\nProduce the task list.'

        try:
            raw = await self.think(system, prompt, max_tokens=512)
            tasks = json.loads(raw)
            if not isinstance(tasks, list):
                raise ValueError('Not a list')
        except Exception:
            tasks = [
                {'agent': 'research',   'type': 'find_niche',      'payload': {}},
                {'agent': 'design',     'type': 'generate_design',  'payload': {}},
                {'agent': 'listing',    'type': 'write_listing',    'payload': {}},
                {'agent': 'operations', 'type': 'publish_product',  'payload': {}},
            ]

        self.queue = [f"{t['agent']}: {t['type']}" for t in tasks]
        await self.emit(f'Planned {len(tasks)} tasks')
        await self.set_status('idle', 'Waiting for workers')
        return tasks

    async def run(self, context: dict) -> dict:
        return {}
