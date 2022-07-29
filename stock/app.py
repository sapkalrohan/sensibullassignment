from stock.model.conf import app,setup_routes
import asyncio

# def main():
  # if __name__ == "stock.app":
  #   setup_routes()
  #   app.run()

# asyncio.run(main())

if __name__ == "stock.app":
    setup_routes()
    app.run()