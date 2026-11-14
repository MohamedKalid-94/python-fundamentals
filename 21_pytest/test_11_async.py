import asyncio
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

# LESSON 11: testing ASYNC code (Module 20, file 08) with pytest-asyncio.
# RUN:  pytest test_11_async.py -v
#
# In the default "strict" mode:
#   an async TEST needs      @pytest.mark.asyncio
#   an async FIXTURE needs   @pytest_asyncio.fixture      (not @pytest.fixture)
# Each test gets its own event loop. Never call asyncio.run() inside a test.


async def double_later(n):
    await asyncio.sleep(0)
    return n * 2


@pytest.mark.asyncio
async def test_double_later():
    assert await double_later(4) == 8


@pytest.mark.asyncio
async def test_gather():
    results = await asyncio.gather(double_later(1), double_later(2))
    assert results == [2, 4]


@pytest.mark.asyncio
async def test_timeout():
    with pytest.raises(TimeoutError):
        async with asyncio.timeout(0.01):       # Python 3.11+
            await asyncio.sleep(1)


@pytest_asyncio.fixture
async def queue():
    q = asyncio.Queue()
    await q.put("job")
    return q


@pytest.mark.asyncio
async def test_queue(queue):
    assert await queue.get() == "job"


# AsyncMock replaces a coroutine function
@pytest.mark.asyncio
async def test_asyncmock():
    fetch = AsyncMock(return_value={"ok": True})
    assert await fetch("url") == {"ok": True}
    fetch.assert_awaited_once_with("url")


# Testing FastAPI endpoints comes in the FastAPI module (TestClient and httpx).