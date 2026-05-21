import json
from .base import BaseAgent

class ListingAgent(BaseAgent):
    name = 'listing'

    async def run(self, context: dict) -> dict:
        niche    = context.get('niche', 'retro gaming')
        keywords = context.get('keywords', [])

        await self.set_status('working', f'Writing Etsy listing for "{niche}"')
        await self.emit('Crafting SEO-optimised title, description and tags…')

        system = (
            'You are an Etsy SEO expert writing listings for print-on-demand shirts. '
            'Output JSON: {"title": "...", "description": "...", "tags": [...13 tags max...], "price": 24.99}.'
        )
        prompt = (
            f'Write a complete Etsy listing for a {niche} shirt. '
            f'Use these keywords naturally: {", ".join(keywords)}.'
        )

        try:
            raw    = await self.think(system, prompt, max_tokens=512)
            result = json.loads(raw)
        except Exception:
            result = {
                'title':       f'{niche.title()} Shirt — Funny Graphic Tee Gift',
                'description': f'Show off your love of {niche} with this premium graphic tee.',
                'tags':        keywords[:13] or ['shirt', 'graphic tee', 'gift'],
                'price':       24.99,
            }

        await self.emit(f'Listing written: "{result["title"][:50]}"')
        await self.set_status('idle')
        return result
