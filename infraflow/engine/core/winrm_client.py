from __future__ import annotations

import asyncio
import logging


logger = logging.getLogger(__name__)


class WinRMClient:
    """WinRM client for Windows hosts."""

    def __init__(self) -> None:
        self._sessions: dict[str, object] = {}

    def _get_session(self, host: str, username: str, password: str, use_ssl: bool = True) -> object:
        key = f'{host}:{username}:{use_ssl}'
        if key not in self._sessions:
            protocol = 'https' if use_ssl else 'http'
            port = 5986 if use_ssl else 5985
            import winrm
            self._sessions[key] = winrm.Session(
                f'{protocol}://{host}:{port}/wsman',
                auth=(username, password),
                transport='ntlm',
                server_cert_validation='ignore',
            )
        return self._sessions[key]

    async def run(self, host: str, command: str, username: str, password: str, use_ssl: bool = True) -> tuple[str, str, int]:
        def _execute() -> tuple[str, str, int]:
            try:
                session = self._get_session(host, username, password, use_ssl)
                ps_command = command if command.startswith('powershell') else f'powershell -Command "{command}"'
                result = session.run_ps(ps_command)
                stdout = result.std_out.decode('utf-8', errors='ignore').strip()
                stderr = result.std_err.decode('utf-8', errors='ignore').strip()
                return stdout, stderr, int(result.status_code)
            except Exception as exc:
                logger.error('WinRM error on %s: %s', host, exc)
                return '', str(exc), -1

        return await asyncio.to_thread(_execute)


winrm_client = WinRMClient()


async def run_winrm(host: str, command: str, username: str, password: str, use_ssl: bool = True) -> tuple[str, str, int]:
    return await winrm_client.run(host, command, username, password, use_ssl)
