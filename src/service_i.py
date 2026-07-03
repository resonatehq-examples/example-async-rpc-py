from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

from resonate.resonate import Resonate

if TYPE_CHECKING:
    from resonate.context import Context


async def dop(ctx: Context) -> int:
    print("running function baz")
    return 1


async def _main() -> None:
    r = Resonate(
        url=os.environ.get("RESONATE_URL", "http://localhost:8001"),
        group="service-i",
    )
    r.register(dop)
    print("service-i is running", flush=True)
    await asyncio.Event().wait()


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
