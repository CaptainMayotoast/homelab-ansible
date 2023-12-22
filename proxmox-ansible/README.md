https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_snap_module.html

Need the following Python packages:
- proxmoxer
- requests

Create a Proxmox user by CLI:
- `pveum role add terraform-role -privs "VM.Allocate VM.Clone VM.Config.CDROM VM.Config.CPU VM.Config.Cloudinit VM.Config.Disk VM.Config.HWType VM.Config.Memory VM.Config.Network VM.Config.Options VM.Monitor VM.Audit VM.PowerMgmt Datastore.AllocateSpace Datastore.Audit"`
- 
```
pveum user add terraform@pve
pveum aclmod / -user terraform@pve -role terraform-role
pveum user token add terraform@pve terraform-token --privsep=0
```

Run: `activate ansible_python_env/bin/activate`

Then run `ansible-playbook -i inventory/dev playbooks/proxmox-vm-snap.yaml --user ansible`

