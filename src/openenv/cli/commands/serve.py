# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Serve OpenEnv environments locally (TO BE IMPLEMENTED)."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from .._cli_utils import console

app = typer.Typer(help="Serve OpenEnv environments locally")


@app.command()
def serve(
    env_path: Annotated[
        str | None,
        typer.Argument(
            help="Path to the environment directory (default: current directory)"
        ),
    ] = None,
    port: Annotated[
        int,
        typer.Option("--port", "-p", help="Port to serve on"),
    ] = 8000,
    host: Annotated[
        str,
        typer.Option("--host", help="Host to bind to"),
    ] = "0.0.0.0",
    reload: Annotated[
        bool,
        typer.Option("--reload", help="Enable auto-reload on code changes"),
    ] = False,
) -> None:
    """
    Serve an OpenEnv environment locally.

    This command starts the environment server in the current or specified directory using uvicorn.
    Supports host, port, and reload options for development.
    """
    import subprocess
    import sys

    # Determine environment path
    if env_path is None:
        env_path_obj = Path.cwd()
    else:
        env_path_obj = Path(env_path)

    # Try to find the server entry point (server/app.py)
    server_app = env_path_obj / "server" / "app.py"
    if not server_app.exists():
        console.print(f"[red]Could not find server/app.py in {env_path_obj}[/red]")
        raise typer.Exit(1)

    # Build uvicorn command
    uvicorn_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "server.app:app",
        "--host",
        host,
        "--port",
        str(port),
    ]
    if reload:
        uvicorn_cmd.append("--reload")

    console.print(
        f"[green]Starting environment server with:[/green] {' '.join(uvicorn_cmd)}"
    )
    try:
        subprocess.run(uvicorn_cmd, cwd=str(env_path_obj), check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Failed to start server: {e}[/red]")
        raise typer.Exit(e.returncode)
