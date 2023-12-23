# Overview

0. Code examples originally adapted from https://perdue.dev/installing-your-kubernetes-homelab-cluster-in-minutes-with-ansible/

1. Update inventory/dev with IPs for each master/slave nodes

2. Install a Python virtual envrionment:

```python
python3 -m venv ./venv
```

3. Install `ansible` within the venv

`python3 -m pip install ansible`

4. Run `keyscan.py`

Output will look like:

```bash
['192.168.20.115', '192.168.20.116', '192.168.20.117', '192.168.20.118']
# 192.168.20.117:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4
# 192.168.20.115:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4
# 192.168.20.118:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4
# 192.168.20.116:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4
```

5. Run `ansible -i inventory/dev all -m ping --user ansible`

Output will look like:

```bash
192.168.20.115 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
192.168.20.118 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
192.168.20.117 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
192.168.20.116 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

6. Run `ansible-playbook -i inventory/dev playbooks/k8s_all.yaml --user ansible`
