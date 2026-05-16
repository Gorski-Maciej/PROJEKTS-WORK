import subprocess

def run_ansible_playbook(playbook_path, inventory=None, extra_vars=None):
    cmd=['ansible-playbook', playbook_path]
    if inventory: cmd.extend(['-i', inventory])
    if extra_vars:
        for k,v in extra_vars.items(): cmd.extend(['-e', f'{k}={v}'])
    p=subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr
