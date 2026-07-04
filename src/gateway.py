from __future__ import annotations

import asyncio
import os
import threading
from typing import Any

from flask import Flask, jsonify
from resonate.resonate import Resonate

# ---------------------------------------------------------------------------
# Asyncio event loop running in a background thread.
# Resonate uses asyncio internally, so we keep a dedicated loop alive for the
# lifetime of the process and dispatch coroutines into it from Flask's sync
# route handlers via run_coroutine_threadsafe.
# ---------------------------------------------------------------------------

_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
_resonate: Resonate


def _start_loop() -> None:
    asyncio.set_event_loop(_loop)
    _loop.run_forever()


_loop_thread = threading.Thread(target=_start_loop, daemon=True)
_loop_thread.start()


def _run_async(coro: Any) -> Any:
    """Run a coroutine on the background loop and block until it completes."""
    future = asyncio.run_coroutine_threadsafe(coro, _loop)
    return future.result()


async def _create_resonate() -> Resonate:
    # Resonate.__init__ calls asyncio.create_task() and asyncio.Future(), so
    # it must be constructed while the event loop is running.
    return Resonate(
        url=os.environ.get("RESONATE_URL", "http://localhost:8001"),
        group="gateway",
    )


_resonate = _run_async(_create_resonate())


# ---------------------------------------------------------------------------
# Helper: rpc() also creates asyncio primitives internally, so every call to
# it must happen on the background loop too.  This coroutine dispatches the
# rpc and awaits the result in one shot, keeping Flask handlers loop-free.
# ---------------------------------------------------------------------------


async def _rpc_and_await(target: str, promise_id: str, func: str, *args: Any) -> Any:
    handle = _resonate.options(target=target).rpc(promise_id, func, *args)
    return await handle.result()


async def _rpc_fire_and_forget(target: str, promise_id: str, func: str, *args: Any) -> None:
    _resonate.options(target=target).rpc(promise_id, func, *args)


# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------

app_node_id = "gateway"
app_node_group = "gateway"

app = Flask(app_node_id)


@app.route("/await-chain", methods=["POST"])
def await_chain_route_handler() -> Any:
    try:
        print("running await_chain_route_handler")
        promise_id = "await-chain"
        message = _run_async(_rpc_and_await("service-a", promise_id, "foo"))
        print("waiting on result")
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route("/detached-chain", methods=["POST"])
def detached_chain_route_handler() -> Any:
    try:
        print("running detached_chain_route_handler")
        promise_id = "detached-chain"
        _run_async(_rpc_fire_and_forget("service-d", promise_id, "qux", 1))
        message = "detached-chain started"
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route("/fan-out-workflow", methods=["POST"])
def fan_out_workflow_route_handler() -> Any:
    try:
        print("running fan-out-workflow_route_handler")
        promise_id = "fan-out-workflow"
        message = _run_async(_rpc_and_await("service-g", promise_id, "zim", 1))
        print("waiting on result")
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


def main() -> None:
    print(
        f"app node id {app_node_id} | app node group {app_node_group} | http capable | running",
        flush=True,
    )
    app.run(port=5000)


if __name__ == "__main__":
    main()
