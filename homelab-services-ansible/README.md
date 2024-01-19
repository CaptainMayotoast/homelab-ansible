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

# Development notes

Jan 14th, 2024
- I figured out how to see which initialization (init) container may be failing.  Gitea and Jenkins were both failing upon startup.  To do fine the actual error message(s), run `kubectl describe pod <podname, i.e. jenkins-0> -n <namespace of pod>`, several containers will show in the describe output.  Then, run `kubectl logs <failing pod name, i.e. jenkins-0> -n <namespace> -c <init container, i.e. init>`.

Jan 18th, 2024
- I tried generating [access tokens via the CLI](https://docs.gitea.com/next/development/api-usage), but [discovered](https://github.com/go-gitea/gitea/issues/23382) I could not do so with an oauth2 (OIDC) user.  Running `curl -H "Content-Type: application/json" -d '{"name":"aschwartz"}' -u username:password https://gitea.milkyway.localhostcert.net/api/v1/users/aschwartz/tokens` informed me that the `aschwartz` oauth2 user does not have a password set.
- After generating an access token with my oauth2 user, I was able to run `docker login gitea.milkyway.localhostcert.net`, which prompted me with a username field, and a password field, which is where the token was entered.
- To push an image, I had to tag an image on my system to match the following scheme: `gitea.milkyway.localhostcert.net/aschwartz/img:tag`, i.e., `gitea.milkyway.localhostcert.net/aschwartz/meson-build:latest`.
