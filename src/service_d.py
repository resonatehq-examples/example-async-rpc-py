from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

from resonate.resonate import Resonate

if TYPE_CHECKING:
    from resonate.context import Context


async def qux(ctx: Context, arg: int) -> None:
    print("running function qux")
    await ctx.options(target="service-e").detached("quz", arg + 1).id()


async def _main() -> None:
    r = Resonate(
        url=os.environ.get("RESONATE_URL", "http://localhost:8001"),
        group="service-d",
    )
    r.register(qux)
    print("service d is running", flush=True)
    await asyncio.Event().wait()


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
