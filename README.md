# Overview
Ansible playbooks to install tools on a Kubernetes cluster


# Features
- includes Jenkins, Longhorn, MetalLB, and the Kubernetes Dashboard


# Quickstart
```
ansible-galaxy collection install kubernetes.core
ansible-galaxy collection install cloud.common

# install it all
ansible-playbook -i inventory/dev playbooks/all.yaml --user appuser

ansible-playbook -i inventory/dev playbooks/helm.yaml --user appuser
ansible-playbook -i inventory/dev playbooks/longhorn.yaml --user appuser
ansible-playbook -i inventory/dev playbooks/jenkins.yaml --user appuser
```

Install kubernetes-dashboard
```
ansible-playbook -i inventory/dev playbooks/kubernetes-dashboard.yaml
```

# Update Nodes
```
ansible-playbook -i inventory/dev playbooks/update-and-reboot.yaml --user appuser
```

# Jenkins
To access Jenkins, login with `admin`/`changethisP455word!`
