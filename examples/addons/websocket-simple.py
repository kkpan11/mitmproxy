"""Process individual messages from a WebSocket connection."""

import logging
import re

from mitmproxy import http


def websocket_message(flow: http.HTTPFlow):
    assert flow.websocket is not None  # make type checker happy
    # get the latest message
    message = flow.websocket.messages[-1]

    # was the message sent from the client or server?
    if message.from_client:
        logging.info(f"Client sent a message: {message.content!r}")
    else:
        logging.info(f"Server sent a message: {message.content!r}")

    # manipulate the message content
    message.content = re.sub(rb"^Hello", b"HAPPY", message.content)

    if b"FOOBAR" in message.content:
        # kill the message and not send it to the other endpoint
        message.drop()
