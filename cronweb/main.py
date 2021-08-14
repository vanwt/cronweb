from uvicorn import Server, Config
from api.api import app
from cron import loop

if __name__ == '__main__':
    config = Config(app=app, log_level="info", port=8888)
    serve = Server(config=config)
    loop.run_until_complete(serve.serve())
