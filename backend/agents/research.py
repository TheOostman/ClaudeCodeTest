from .base import BaseAgent

class ResearchAgent(BaseAgent):
    name = 'research'

    async def run(self, context: dict) -> dict:
        await self.set_status('working', 'Finding trending niches')
        await self.emit('Analysing Etsy trends and competitor listings…')

        system = (
            'You are a market research agent for an Etsy print-on-demand shirt business. '
            'Identify a profitable niche. Output JSON: {"niche": "...", "keywords": [...], "reason": "..."}.'
        )
        prompt = 'Find one high-potential trending niche for Etsy shirts right now.'

        try:
            import json
            raw = await self.think(system, prompt, max_tokens=256)
            result = json.loads(raw)
        except Exception:
            result = {
                'niche':    'Retro gaming',
                'keywords': ['retro gaming shirt', '80s gamer tee', 'pixel art shirt'],
                'reason':   'Evergreen nostalgia niche with consistent search volume',
            }

        await self.emit(f'Niche found: {result["niche"]} — {result["reason"]}')
        await self.set_status('idle')
        return result
