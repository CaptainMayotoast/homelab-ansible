# Overview
Ansible playbooks to install tools on a Kubernetes cluster


# Features
- includes Jenkins, Longhorn, MetalLB, and the Kubernetes Dashboard


# Quickstart
```
ansible-galaxy collection install kubernetes.core
ansible-galaxy collection install cloud.common
ansible-galaxy install andrewrothstein.kubernetes-helm

# install it all
ansible-playbook -i inventory/dev playbooks/all.yaml

ansible-playbook -i inventory/dev playbooks/helm.yaml
ansible-playbook -i inventory/dev playbooks/longhorn.yaml
```

Install kubernetes-dashboard
```
ansible-playbook -i inventory/dev playbooks/kubernetes-dashboard.yaml
```

# Update Nodes
```
ansible-playbook -i inventory/dev playbooks/update-and-reboot.yaml
```

# Jenkins
To access Jenkins, login with `admin`/`adminpassword`
