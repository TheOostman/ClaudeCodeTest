import logging
import httpx
from config import ETSY_CLIENT_ID, ETSY_CLIENT_SECRET

log = logging.getLogger(__name__)
BASE = 'https://openapi.etsy.com/v3'

class EtsyClient:
    def __init__(self, access_token: str | None = None):
        self._token = access_token

    def _headers(self):
        h = {'x-api-key': ETSY_CLIENT_ID}
        if self._token:
            h['Authorization'] = f'Bearer {self._token}'
        return h

    async def get_open_orders(self) -> list:
        if not self._token:
            log.warning('Etsy: no access token — skipping order fetch')
            return []
        try:
            async with httpx.AsyncClient() as c:
                r = await c.get(
                    f'{BASE}/application/shops/me/receipts',
                    headers=self._headers(),
                    params={'was_paid': True, 'was_shipped': False},
                )
                r.raise_for_status()
                return r.json().get('results', [])
        except Exception as e:
            log.error(f'Etsy get_open_orders failed: {e}')
            return []

    async def get_listing_stats(self, listing_id: str) -> dict:
        if not self._token:
            return {}
        try:
            async with httpx.AsyncClient() as c:
                r = await c.get(
                    f'{BASE}/application/listings/{listing_id}/stats',
                    headers=self._headers(),
                )
                r.raise_for_status()
                return r.json()
        except Exception as e:
            log.error(f'Etsy listing stats failed: {e}')
            return {}
