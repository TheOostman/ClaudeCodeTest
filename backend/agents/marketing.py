import json
from .base import BaseAgent

class MarketingAgent(BaseAgent):
    name = 'marketing'

    async def run(self, context: dict) -> dict:
        title = context.get('title', 'our new shirt')
        niche = context.get('niche', 'trending')

        await self.set_status('working', 'Writing marketing copy')
        await self.emit('Generating social media captions and promotion copy…')

        system = (
            'You are a social media marketing agent for an Etsy shirt shop. '
            'Output JSON: {"twitter": "...", "instagram": "...", "tiktok": "...", "etsy_announcement": "..."}.'
        )
        prompt = f'Write promotional copy for this new Etsy listing: "{title}" (niche: {niche}).'

        try:
            raw    = await self.think(system, prompt, max_tokens=512)
            result = json.loads(raw)
        except Exception:
            result = {
                'twitter':           f'Just dropped: {title} 🔥 Shop now on Etsy! #etsy #{niche.replace(" ","")}',
                'instagram':         f'New drop! {title} ✨ Link in bio.',
                'tiktok':            f'Check out our new {niche} shirt — perfect gift idea!',
                'etsy_announcement': f'New listing alert: {title}',
            }

        await self.emit('Marketing copy ready for review')
        await self.set_status('idle')
        return result
