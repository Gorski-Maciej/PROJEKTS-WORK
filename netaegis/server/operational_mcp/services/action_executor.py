import paramiko

class ActionExecutor:
    async def execute_block_ip(self, host: str, ip: str, username: str, password: str) -> bool:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password, timeout=5)
            ssh.exec_command(f"iptables -A INPUT -s {ip} -j DROP")
            ssh.close()
            return True
        except Exception:
            return False
