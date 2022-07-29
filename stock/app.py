from stock.model.conf import app,setup_routes
import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config

config = Config()
setup_routes()

config.bind = ["0.0.0.0:19093"]  
shutdown_event = asyncio.Event()

loop = asyncio.get_event_loop()
loop.run_until_complete(
    serve(app, config, shutdown_trigger=lambda: asyncio.Future())
)

if __name__ == "stock.app":
    asyncio.run(serve(app, config))
 