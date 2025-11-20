import asyncio
import itertools
from typing import Any, Dict

import websockets
from websockets.server import WebSocketServerProtocol

from packets import (
    CHAT_MESSAGE,
    HEARTBEAT_PING,
    HEARTBEAT_PONG,
    PLAYER_CONNECT,
    PLAYER_DISCONNECT,
    PLAYER_MOVE,
    SECTOR_UPDATE,
    decode_packet,
    encode_packet,
    is_heartbeat,
)

connected_players: Dict[str, WebSocketServerProtocol] = {}
player_state: Dict[str, Dict[str, Any]] = {}

_player_id_counter = itertools.count(1)


async def broadcast(packet: str) -> None:
    """Send an encoded packet to all connected players."""
    if not connected_players:
        return

    send_coroutines = [ws.send(packet) for ws in connected_players.values()]
    await asyncio.gather(*send_coroutines, return_exceptions=True)


def _next_player_id() -> str:
    return f"player-{next(_player_id_counter)}"


async def handle_connection(websocket: WebSocketServerProtocol, path: str) -> None:  # noqa: ARG001
    player_id = _next_player_id()
    connected_players[player_id] = websocket
    player_state.setdefault(player_id, {})

    await broadcast(encode_packet(PLAYER_CONNECT, {"player_id": player_id}))

    try:
        async for message in websocket:
            packet_type, payload = decode_packet(message)

            if is_heartbeat(packet_type):
                await websocket.send(encode_packet(HEARTBEAT_PONG, {}))
                continue

            if packet_type == PLAYER_MOVE:
                player_state[player_id].update(payload or {})
                await broadcast(
                    encode_packet(
                        SECTOR_UPDATE,
                        {"player_id": player_id, "state": player_state[player_id]},
                    )
                )
            elif packet_type == CHAT_MESSAGE:
                await broadcast(
                    encode_packet(
                        CHAT_MESSAGE, {"player_id": player_id, "message": payload.get("message")}
                    )
                )
            elif packet_type == HEARTBEAT_PING:
                await websocket.send(encode_packet(HEARTBEAT_PONG, {}))
    finally:
        connected_players.pop(player_id, None)
        player_state.pop(player_id, None)
        await broadcast(encode_packet(PLAYER_DISCONNECT, {"player_id": player_id}))


async def game_loop() -> None:
    while True:
        await asyncio.sleep(0.1)


async def main() -> None:
    server = await websockets.serve(handle_connection, "localhost", 8765)
    game_task = asyncio.create_task(game_loop())

    await asyncio.gather(server.wait_closed(), game_task)


if __name__ == "__main__":
    asyncio.run(main())
