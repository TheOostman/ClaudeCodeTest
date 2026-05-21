import logging
from config import OPENAI_API_KEY

log = logging.getLogger(__name__)

class ImageGenClient:
    async def generate(self, prompt: str, size: str = '1024x1024') -> str | None:
        if not OPENAI_API_KEY:
            log.warning('OPENAI_API_KEY not set — skipping image generation')
            return None
        try:
            from openai import AsyncOpenAI
            client   = AsyncOpenAI(api_key=OPENAI_API_KEY)
            response = await client.images.generate(
                model='dall-e-3',
                prompt=prompt,
                size=size,
                quality='standard',
                n=1,
            )
            return response.data[0].url
        except Exception as e:
            log.error(f'Image generation failed: {e}')
            return None
