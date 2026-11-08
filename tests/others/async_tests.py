import asyncio
import time

import httpx
import pytest

from fastapi import FastAPI


app = FastAPI()


def fake_factusmart_call() -> dict:
    # Simula SDK síncrono esperando red/SUNAT
    time.sleep(2)

    return {
        "success": True,
    }


@app.post("/receipt/blocking")
async def issue_receipt_blocking():
    result = fake_factusmart_call()

    return result


@app.post("/receipt/threaded")
async def issue_receipt_threaded():
    result = await asyncio.to_thread(
        fake_factusmart_call
    )

    return result


@app.get("/ping")
async def ping():
    return {
        "message": "pong",
    }


@pytest.mark.asyncio
async def test_blocking_sdk_blocks_event_loop():

    transport = httpx.ASGITransport(
        app=app,
    )

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        started_at = time.perf_counter()

        receipt_task = asyncio.create_task(
            client.post(
                "/receipt/blocking"
            )
        )

        ping_started_at = time.perf_counter()

        ping_task = asyncio.create_task(
            client.get("/ping")
        )

        ping_response = await ping_task

        ping_elapsed = (
            time.perf_counter()
            - ping_started_at
        )

        await receipt_task

        total_elapsed = (
            time.perf_counter()
            - started_at
        )

        print("\nWITHOUT to_thread")
        print(
            f"Ping: {ping_elapsed:.2f}s"
        )
        print(
            f"Total: {total_elapsed:.2f}s"
        )

        assert (
            ping_response.status_code
            == 200
        )

        assert ping_elapsed >= 1.9

@pytest.mark.asyncio
async def test_to_thread_does_not_block_event_loop():

    transport = httpx.ASGITransport(
        app=app,
    )

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        started_at = time.perf_counter()

        receipt_task = asyncio.create_task(
            client.post(
                "/receipt/threaded"
            )
        )

        ping_started_at = time.perf_counter()

        ping_task = asyncio.create_task(
            client.get("/ping")
        )

        ping_response = await ping_task

        ping_elapsed = (
            time.perf_counter()
            - ping_started_at
        )

        await receipt_task

        total_elapsed = (
            time.perf_counter()
            - started_at
        )

        print("\nWITH to_thread")
        print(
            f"Ping: {ping_elapsed:.2f}s"
        )
        print(
            f"Total: {total_elapsed:.2f}s"
        )

        assert (
            ping_response.status_code
            == 200
        )

        assert ping_elapsed < 0.5
        assert total_elapsed >= 1.9