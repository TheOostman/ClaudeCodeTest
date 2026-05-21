from .base import BaseAgent
from db import get_all_products

class AnalyticsAgent(BaseAgent):
    name = 'analytics'

    async def run(self, context: dict) -> dict:
        await self.set_status('working', 'Pulling sales & performance data')
        await self.emit('Fetching Etsy analytics and reviewing product performance…')

        products = await get_all_products()
        total_sales   = sum(p.get('sales', 0) for p in products)
        total_revenue = sum((p.get('sales', 0) * (p.get('price') or 0)) for p in products)

        low_performers = [p for p in products if p.get('views', 0) > 50 and p.get('sales', 0) == 0]
        if low_performers:
            await self.emit(f'{len(low_performers)} listings with views but no sales — flagging for review')

        summary = {
            'total_products': len(products),
            'total_sales':    total_sales,
            'total_revenue':  round(total_revenue, 2),
            'low_performers': [p.get('title') for p in low_performers],
        }

        await self.emit(f'Analytics: {total_sales} total sales, ${total_revenue:.2f} revenue')
        await self.set_status('idle')
        return summary
