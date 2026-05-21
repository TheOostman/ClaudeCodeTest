from .base import BaseAgent
from clients.imagegen import ImageGenClient

class DesignAgent(BaseAgent):
    name = 'design'

    async def run(self, context: dict) -> dict:
        niche    = context.get('niche', 'retro gaming')
        keywords = context.get('keywords', [])

        await self.set_status('working', f'Creating design for "{niche}"')
        await self.emit(f'Generating shirt design for niche: {niche}')

        # Build image prompt
        system = 'You are a graphic design prompt engineer for print-on-demand shirts.'
        prompt = (
            f'Write a detailed DALL-E 3 image generation prompt for a shirt design. '
            f'Niche: {niche}. Keywords: {", ".join(keywords)}. '
            f'The design should look great on a t-shirt. Output only the image prompt, nothing else.'
        )
        img_prompt = await self.think(system, prompt, max_tokens=200)

        await self.emit(f'Design prompt: {img_prompt[:80]}…')

        client = ImageGenClient()
        img_url = await client.generate(img_prompt)

        await self.emit(f'Design generated: {img_url[:60]}…' if img_url else 'Design generation skipped (no API key)')
        await self.set_status('idle')
        return {'image_url': img_url, 'prompt': img_prompt, 'niche': niche}
