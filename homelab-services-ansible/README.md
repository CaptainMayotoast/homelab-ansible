# Overview
Ansible playbooks to install tools on a Kubernetes cluster

# Features
- MetalLB
- Longhorn
- Cert-manager
- Gitea
- PiHole
- Jenkins

# Quickstart
```
ansible-galaxy collection install kubernetes.core
ansible-galaxy collection install cloud.common

# install it all
ansible-playbook -i inventory/dev playbooks/all.yaml --user ansible
```

Install kubernetes-dashboard
```
ansible-playbook -i inventory/dev playbooks/kubernetes-dashboard.yaml
```

# Update Nodes
```
ansible-playbook -i inventory/dev playbooks/update-and-reboot.yaml --user ansible
```

# Jenkins
To access Jenkins, login with `admin`/`changethisP455word!`

# Useful Kubernetes commands

1. `kubectl get service --all-namespaces`
2. `kubectl delete namespace <namespace>`
3. `kubectl get pods --all-namespaces -o wide`
4. `kubectl describe svc --all-namespaces`

# Resources

- Reference host variables from the 'dev' file https://stackoverflow.com/questions/40027847/accessing-inventory-host-variable-in-ansible-playbook
