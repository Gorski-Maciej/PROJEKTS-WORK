from __future__ import annotations

from typing import Optional, Tuple


class SSHClientError(RuntimeError):
    pass


async def run_ssh(host: str, command: str, username: str = 'root', key_file: Optional[str] = None, password: Optional[str] = None) -> Tuple[str, str, int]:
    """Execute command over SSH and return (stdout, stderr, exit_status).

    Import is lazy so unit tests can run without asyncssh installed.
    """
    try:
        import asyncssh  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise SSHClientError('asyncssh is required at runtime') from exc

    try:
        async with asyncssh.connect(
            host=host,
            username=username,
            client_keys=[key_file] if key_file else None,
            password=password,
            known_hosts=None,
        ) as conn:
            result = await conn.run(command, check=False)
            return result.stdout.strip(), result.stderr.strip(), result.exit_status
    except Exception as exc:  # pragma: no cover
        return '', str(exc), 255
