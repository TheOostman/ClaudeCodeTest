import asyncio
import logging
from typing import Callable, Awaitable

from .board import BoardAgent
from .overseer import OverseerAgent
from .research import ResearchAgent
from .design import DesignAgent
from .listing import ListingAgent
from .marketing import MarketingAgent
from .analytics import AnalyticsAgent
from .operations import OperationsAgent

log = logging.getLogger(__name__)

AGENT_MAP = {
    'research':   ResearchAgent,
    'design':     DesignAgent,
    'listing':    ListingAgent,
    'marketing':  MarketingAgent,
    'analytics':  AnalyticsAgent,
    'operations': OperationsAgent,
}

class AgentManager:
    def __init__(self):
        self.board    = BoardAgent()
        self.overseer = OverseerAgent()
        self.workers  = {name: cls() for name, cls in AGENT_MAP.items()}
        self._all     = [self.board, self.overseer, *self.workers.values()]
        self._running = False
        self._cycle_task: asyncio.Task | None = None

    def set_broadcast(self, fn: Callable[[dict], Awaitable]):
        for agent in self._all:
            agent.set_broadcast(fn)

    async def start(self):
        log.info('AgentManager started (idle)')

    async def stop(self):
        await self.stop_cycle()

    def get_state(self) -> dict:
        state = {
            'board':    self.board.get_state(),
            'overseer': self.overseer.get_state(),
        }
        for name, agent in self.workers.items():
            state[name] = agent.get_state()
        return state

    async def run_cycle(self):
        if self._running:
            log.info('Cycle already running')
            return
        self._cycle_task = asyncio.create_task(self._cycle())

    async def stop_cycle(self):
        self._running = False
        if self._cycle_task:
            self._cycle_task.cancel()
            try:
                await self._cycle_task
            except asyncio.CancelledError:
                pass
        for agent in self._all:
            agent.status = 'idle'

    async def _cycle(self):
        self._running = True
        try:
            # Board sets strategy
            board_result = await self.board.run({})

            # Overseer plans tasks
            tasks = await self.overseer.plan(board_result.get('directive', ''))

            # Execute tasks sequentially, passing results forward as context
            context = board_result.copy()
            for task in tasks:
                if not self._running:
                    break
                agent_name = task.get('agent')
                agent = self.workers.get(agent_name)
                if not agent:
                    log.warning(f'Unknown agent: {agent_name}')
                    continue
                # Remove completed task from overseer queue
                label = f"{agent_name}: {task.get('type')}"
                if label in self.overseer.queue:
                    self.overseer.queue.remove(label)
                    await self.overseer.set_status(self.overseer.status)

                task_context = {**context, **task.get('payload', {}), 'type': task.get('type')}
                result = await agent.run(task_context)
                context.update(result or {})

            log.info('Business cycle complete')
        except asyncio.CancelledError:
            log.info('Cycle cancelled')
            raise
        except Exception as e:
            log.exception(f'Cycle error: {e}')
        finally:
            self._running = False
