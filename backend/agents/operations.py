from .base import BaseAgent
from clients.printify import PrintifyClient
from clients.etsy import EtsyClient

class OperationsAgent(BaseAgent):
    name = 'operations'

    async def run(self, context: dict) -> dict:
        task_type = context.get('type', 'publish_product')

        if task_type == 'publish_product':
            return await self._publish(context)
        elif task_type == 'check_orders':
            return await self._check_orders()
        return {}

    async def _publish(self, context: dict) -> dict:
        image_url   = context.get('image_url')
        listing_data = context.get('listing', {})

        await self.set_status('working', 'Publishing product to Printify + Etsy')
        await self.emit('Uploading design to Printify…')

        printify = PrintifyClient()
        product  = await printify.create_product(image_url, listing_data)

        if product:
            await self.emit(f'Printify product created: {product.get("id")}')
            await self.emit('Publishing to Etsy via Printify…')
            published = await printify.publish(product['id'])
            await self.emit('Product live on Etsy!' if published else 'Publish skipped (no API key)')
        else:
            await self.emit('Printify skipped (no API key configured)')

        await self.set_status('idle')
        return {'product': product}

    async def _check_orders(self) -> dict:
        await self.set_status('working', 'Checking open orders')
        await self.emit('Polling Etsy for new orders…')
        etsy   = EtsyClient()
        orders = await etsy.get_open_orders()
        await self.emit(f'{len(orders)} open orders found')
        await self.set_status('idle')
        return {'orders': orders}
