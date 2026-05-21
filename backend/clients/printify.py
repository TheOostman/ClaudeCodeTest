import logging
import httpx
from config import PRINTIFY_API_KEY

log = logging.getLogger(__name__)
BASE = 'https://api.printify.com/v1'

class PrintifyClient:
    def __init__(self):
        self._headers = {
            'Authorization': f'Bearer {PRINTIFY_API_KEY}',
            'Content-Type': 'application/json',
        }

    async def _get_shop_id(self) -> str | None:
        async with httpx.AsyncClient() as c:
            r = await c.get(f'{BASE}/shops.json', headers=self._headers)
            r.raise_for_status()
            shops = r.json()
            return str(shops[0]['id']) if shops else None

    async def create_product(self, image_url: str | None, listing: dict) -> dict | None:
        if not PRINTIFY_API_KEY or not image_url:
            log.warning('Printify skipped: missing API key or image URL')
            return None
        try:
            shop_id = await self._get_shop_id()
            if not shop_id:
                log.warning('No Printify shop found')
                return None

            # Upload image
            async with httpx.AsyncClient() as c:
                img_r = await c.post(
                    f'{BASE}/uploads/images.json',
                    headers=self._headers,
                    json={'url': image_url, 'file_name': 'design.png'},
                )
                img_r.raise_for_status()
                image_id = img_r.json()['id']

            # Gildan 64000 blueprint_id=6, US print provider=29
            product_payload = {
                'title':        listing.get('title', 'Custom Shirt'),
                'description':  listing.get('description', ''),
                'blueprint_id': 6,
                'print_provider_id': 29,
                'variants': [
                    {'id': 17390, 'price': int(listing.get('price', 24.99) * 100), 'is_enabled': True},
                ],
                'print_areas': [{
                    'variant_ids': [17390],
                    'placeholders': [{'position': 'front', 'images': [{'id': image_id, 'x': 0.5, 'y': 0.5, 'scale': 1, 'angle': 0}]}],
                }],
            }

            async with httpx.AsyncClient() as c:
                prod_r = await c.post(
                    f'{BASE}/shops/{shop_id}/products.json',
                    headers=self._headers,
                    json=product_payload,
                )
                prod_r.raise_for_status()
                return prod_r.json()

        except Exception as e:
            log.error(f'Printify create_product failed: {e}')
            return None

    async def publish(self, product_id: str) -> bool:
        if not PRINTIFY_API_KEY:
            return False
        try:
            shop_id = await self._get_shop_id()
            async with httpx.AsyncClient() as c:
                r = await c.post(
                    f'{BASE}/shops/{shop_id}/products/{product_id}/publish.json',
                    headers=self._headers,
                    json={'title': True, 'description': True, 'images': True, 'variants': True, 'tags': True},
                )
                return r.status_code == 200
        except Exception as e:
            log.error(f'Printify publish failed: {e}')
            return False
