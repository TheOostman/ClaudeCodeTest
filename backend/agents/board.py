from config import MODEL_OPUS
from .base import BaseAgent

class BoardAgent(BaseAgent):
    name  = 'board'
    model = MODEL_OPUS

    def get_state(self):
        return {
            **super().get_state(),
            'strategy':  self.strategy,
            'directive': self.directive,
        }

    def __init__(self):
        super().__init__()
        self.strategy  = None
        self.directive = None

    async def run(self, context: dict) -> dict:
        await self.set_status('working', 'Setting business strategy')
        await self.emit('Convening board session…')

        system = (
            'You are the Board of Directors for an Etsy print-on-demand shirt business. '
            'Your job is to set high-level strategy and give one clear directive to the Overseer each cycle. '
            'Be concise. Output JSON: {"strategy": "...", "directive": "..."}.'
        )
        prompt = f'Current context: {context}. What is our strategy and directive for this cycle?'

        try:
            raw = await self.think(system, prompt, max_tokens=256)
            import json
            parsed = json.loads(raw)
            self.strategy  = parsed.get('strategy',  'Grow Etsy presence with trending niche shirts')
            self.directive = parsed.get('directive', 'Research top trending niches and produce 3 new designs')
        except Exception as e:
            self.strategy  = 'Grow Etsy presence with trending niche shirts'
            self.directive = 'Research top trending niches and produce 3 new designs'

        await self.emit(f'Strategy set: {self.strategy}')
        await self.set_status('idle')
        return {'strategy': self.strategy, 'directive': self.directive}
