#!/usr/bin/env python3

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager

from pprint import pprint
import os

# https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html

ldr = DataLoader()

#  Ansible: Load inventory
inventory = InventoryManager(
    loader = ldr,
    sources = 'inventory/dev',
    parse = True
)

vm = VariableManager(loader=ldr, inventory=inventory)
control_plane_vars = vm.get_vars(host=inventory.groups['control_planes'].get_hosts()[0])
pprint(control_plane_vars['groups']['all'])

# issues ssh-keyscan to produce trust among all hosts in the dev invetory file
for ip in control_plane_vars['groups']['all']:
    os.popen(f"ssh-keyscan -H -t ed25519 {ip} >> ~/.ssh/known_hosts")