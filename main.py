import os
import uvicorn

from api.app import create_app

app = create_app()


if __name__ == "__main__":

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "7000"))

    uvicorn.run(app, host=host, port=port)
