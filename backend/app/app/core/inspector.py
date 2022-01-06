import asyncio
import logging
import time
from collections import defaultdict
from typing import Any, Dict, Optional

from celery import Celery

logger = logging.getLogger(__name__)


class Inspector:
    """Celery worker inspector object.
    Keeps track of worker stats and contains methods to retrieve stats.
    """

    methods = (
        "active",
        "active_queues",
        "conf",
        "registered",
        "reserved",
        "revoked",
        "scheduled",
        "stats",
    )

    def __init__(self, celery_app: Celery, timeout: int = 5):
        """Initializer for the Inspector object.
        :param celery_app: An instance of the Celery class
        :param timeout: Timeout for retrieving stats on celery workers
        """
        self._app = celery_app
        self._timeout = timeout
        self._workers = defaultdict(dict)

    @property
    def workers(self):
        return self._workers

    async def inspect_worker(self, workername: Optional[str] = None):
        dest = [workername] if workername else None
        methods = (self._inspect(method, dest) for method in self.methods)

        return await asyncio.gather(*methods, return_exceptions=True)

    async def _inspect(self, method: str, dest: str) -> None:
        loop = asyncio.get_running_loop()
        inspect = self._app.control.inspect(timeout=self._timeout, destination=dest)

        start = time.time()
        # Send debug message and run blocking inspection in another thread
        logger.debug(f"{dest}: Sending {method} inspect command")
        result = await loop.run_in_executor(None, getattr(inspect, method))
        logger.debug(f"{dest}: Command {method} took {time.time() - start}")

        # Update internal worker dictionary
        for dest, response in result.items():
            if response is not None:
                info = self._workers[dest]
                info[method] = response
                info["timestamp"] = time.time()

        return self.workers[dest] if dest else self.workers

    async def inspect_tasks(self, *ids: str) -> Dict[str, Any]:
        loop = asyncio.get_running_loop()
        inspect = self._app.control.inspect(timeout=self._timeout)

        start = time.time()
        # Send debug message and run blocking inspection in another thread
        logger.debug(f"Querying task(s): {', '.join(ids)}")
        result = await loop.run_in_executor(None, inspect.query_tasks, *ids)
        logger.debug(f"Query took {time.time() - start} seconds")

        return result
