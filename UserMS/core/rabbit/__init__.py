"""
Rabbit Manager Plugin

This is a plugin for managing rabbit publisher and consumer with an ideal 
way and oop based.

reduces connection's and optimizes created objects, we can say so this 
provides singleton connection objects.

**How to use it?**

with rabbit manager you can add unlimit tasks for callback based on 
rest api syntax.

**Request methods**

``GET`` 
``POST``
``PUT``
``DELETE``

For publishin the message to aimed task at consumer you have to specify the 
method in both side (PUBLISHER/SUBSCRIBER) and send the url for finding the
task in subscriber registered url's. 

**server side**

.. code-block:: python

    @route("/url, method="GET")
    async def do_task(request: Request, message: IncomingMessage):
        return Response(status=Status.ack, result="Hello World")

***client side**

.. code-block:: python

    from rabbit import RabbitCall
    request = RabbitCall(url="/hello", method="GET", data={"name": "John"}).jsonify()
    rabbit_manager.publish(Message(request), routing_key="test")

.. code-block:: python

    import asyncio
    from aio_pika import IncomingMessage
    from aio_pika import Channel
    from rabbit import RabbitManager
    from rabbit import QueueDeclarationProperties as QDP
    from rabbit import RabbitCall
    from rabbit.responses import RabbitResponse as Response
    from rabbit.request import RabbitRequest as Request
    rabbit_manager = RabbitManager("amqp://guest:guest@127.0.0.1/")

    router = rabbit_manager.router

    @router.route("/hello", method="GET")
    async def add_user(request: Request, message: IncomingMessage):
        message.ack()
        name = request.body['name']
        return Response(status=0, detail="message recieved successfully", result=f"Hello {name}")

    async def main():

        # Creating connections
        await rabbit_manager.create_connection()

        # Creating a channel
        channel = await rabbit_manager.connection.channel()

        # Creating a queue
        queue = await channel.declare_queue("test", durable=True)

        # Start consuming
        await rabbit_manager.consume(queue=queue)

        for i in range(100):
            await asyncio.gather(
                [
                    rabbit_manager.publish(
                        Message(
                            RabbitCall(
                                url="/hello", method="GET", data={"name": "John"}
                            ).jsonify()
                        ),
                        routing_key="test",
                    )
                    for _ in range(100)
                ]
            )
        try:
            # Wait until terminate
            await asyncio.Future()
        finally:
            await rabbit_manager.connection.close()

    if __name__ == "__main__":
        asyncio.run(main())


**How to declare queue and exchange?** 

.. code-block:: python
    
    # Your codes

    @rabbit_manager.declare
    async def base_declarations(channel: Chennel):
        channel.declare_queue("test")
        channel.declare_exhange("test")


**How to use in FastApi?**

.. code-block:: python

    from fastapi import FastAPI
    from aio_pika import IncomingMessage
    from aio_pika import Channel
    from rabbit import RabbitManager
    from rabbit import QueueDeclarationProperties as QDP
    from rabbit import RabbitCall
    from rabbit.responses import RabbitResponse as Response
    from rabbit.request import RabbitRequest as Request
    
    app = FastAPI()
    rabbit_manager = RabbitManager("amqp://guest:guest@127.0.0.1/")

    router = rabbit_manager.router

    @router.route("/hello", method="GET")
    async def add_user(request: Request, message: IncomingMessage):
        message.ack()
        name = request.body['name']
        return Response(status=0, detail="message recieved successfully", result=f"Hello {name}")

    @app.on_event("startup")

    # Creating connections
    await rabbit_manager.create_connection()

    # Creating a channel
    channel = await rabbit_manager.connection.channel()

    # Creating a queue
    queue = await channel.declare_queue("test", durable=True)

    # Start consuming
    await rabbit_manager.consume(queue=queue)

    @app.get("/")
    async def index():
        for i in range(100):
            await asyncio.gather(
                [
                    rabbit_manager.publish(
                        Message(
                            RabbitCall(
                                url="/hello", method="GET", data={"name": "John"}
                            ).jsonify()
                        ),
                        routing_key="test",
                    )
                    for _ in range(100)
                ]
            )
        return "Done"
"""

from datetime import datetime, timedelta
from aio_pika.pool import Pool
from typing import Any, Union
from .manager import RabbitManager
from .handler import Handler
from .router import RabbitRouter
from .properties import QueueDeclarationProperties
from .properties import RabbitCall
