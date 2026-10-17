
# ==============================
# Library Imports
# ==============================

import asyncio

import psutil
import jwt

from fastapi import (
    APIRouter,
    Query,
    WebSocket,
    WebSocketDisconnect,
    status,
)


# ==============================
# Application Imports
# ==============================

from app.routers.dependencies import jwt_manager
from app.schemas.metrics import SystemMetricsResponse


# ==============================
# Metrics Router
# ==============================

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics services"],
)


# ==============================
# Server Metrics WebSocket
# ==============================

@router.websocket("/ws/stats")
async def metrics_websocket(
    websocket: WebSocket,
    token: str | None = Query(default=None),
):
    """
    Send server process metrics over a WebSocket connection.
    """

    # Reject connections without an access token.
    if token is None:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION
        )
        return

    # Validate the access token using the shared JWT manager.
    try:
        payload = jwt_manager.validate_access_token(token)

        if "admin" not in payload.get("roles", []):
            await websocket.close(
                code=status.WS_1008_POLICY_VIOLATION
            )
            return

    except jwt.InvalidTokenError:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION
        )
        return
    except Exception:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION
        )
        return

    # Accept the connection after authorization.
    await websocket.accept()

    process = psutil.Process()

    try:
        while True:
            cpu_percent = process.cpu_percent()
            memory = process.memory_info()

            data: SystemMetricsResponse = {
                "cpu_percent": cpu_percent,
                "memory_percent": round(
                    process.memory_percent(),
                    2,
                ),
                "memory_used_mb": round(
                    memory.rss / (1024 ** 2)
                ),
            }

            await websocket.send_json(data)
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        pass
