# Overview
Ansible playbooks to install tools on a Kubernetes cluster

# Features
- :scroll: **Cert-manager** :scroll:
- :hammer: **Gitea** (with a runner, just enable Actions on each repo) :hammer:
- :door: **Istio** (HTTPS gateway) :door:
- :collision: ~~Jenkins~~ (replaced with Gitea Actions) :collision:
- :closed_lock_with_key: **Keycloak** (simple identity provider to allow friends to easily access Gitea) :closed_lock_with_key:
- 🗃️ Longhorn (block storage) 🗃️
- :metal: MetalLB (load balancer for bare metal clusters) :metal:
- 🛑 **PiHole** (DNS sinkhole, WIP) 🛑
- 🚧 [FUTURE] SonarQube 🚧

# Credits
- [Mark Perdue's](https://github.com/markperdue/homelab-ansible) work initially contained Jenkins, Longhorn, MetalLB and the Kubernetes Dashboard.  I wanted to learn Ansible and Terraform, and I found his Ansible deployments for K8s and services on K8s to be very organized and straightforward to understand. 

- I've since added several services which are mentioned [above](#features).

# Quickstart
```
ansible-galaxy collection install ansibleguy.opnsense
ansible-galaxy collection install kubernetes.core

# print variables from Ansible Vault to ensure all needed variables exist and are what is expected
ansible-playbook -i inventory/dev playbooks/print_variables.yaml --user ansible -e @secrets.enc --vault-password-file ./password_file

# install it all
ansible-playbook -i inventory/dev playbooks/all.yaml --user ansible

# pick up from a step
ansible-playbook -i inventory/dev playbooks/<playbook name>.yaml --user ansible --start-at-task="wait for Gitea pod to become available"

# step through one at a time
ansible-playbook -i inventory/dev playbooks/<playbook name>.yaml --user ansible --start-at-task="wait for Gitea pod to become available" --step
```

# Update Nodes
```
ansible-playbook -i inventory/dev playbooks/update-and-reboot.yaml --user ansible
```

# Service notes

## Cert-manager

- Uses https://www.getlocalcert.net/ to provide HTTPS such that common browsers will not complain when presented with a certificate Istio provides.
- Let's Encrypt will rate limit per week, so keep deployments of this to a minimum. 

## Gitea

- Discovered to be a generally useful git visualization and CI/CD solution (Gitea Actions).

## Istio

- My mentor suggested I pursue Istio as a gateway.  Seems straightforward for providing HTTPS and I can eventually integrate with OAuth2-Proxy to do some interesting security minded things (mTLS, WebAuthN, etc).

## Keycloak

- Also suggested by my mentor as an alternative to my difficulties with integrating an on-cluster LDAP solution.  Setting Keycloak up for simple identity management for me and my friends was straightforward.

## Longhorn

- Provides storage for this cluster.

## MetalLB

- Provides IP addresses that are within the static IP ranges of my router.

## PiHole

- A work in progress application to integrate, would block ads network wide.

# Playbook notes

- `router_dns.yaml` is OpnSense specific and uses `ansibleguy.opnsense` Ansible module.

# Role notes

- `cert-manager-helm` contains a `secrets` folder, where a singular JSON file lives (not intended to be committed to the repo) containing API token info.  This JSON file is rsync-ed to control_plane nodes (although, I am not sure that is needed, exactly...another TODO for the list).

- `gitea-helm` should be run before `gitea-actions`, as the former will hold an Ansible `fact` that is used in the creation of a Gitea instance wide runner.

# Useful Kubernetes commands

1. `kubectl get service --all-namespaces`
2. Clear all resources for a particular app 
- `kubectl delete namespace <namespace>`
- Not recommended to be performed on:
    1. Longhorn 
    2. MetalLB
- Intended to be paired with:
    - `ansible-playbook -i inventory/dev playbooks/<playbook name>.yaml --user ansible`
3. `kubectl get pods --all-namespaces -o wide`

# Development notes

Jan 14th, 2024
- I figured out how to see which initialization (init) container may be failing.  Gitea and Jenkins were both failing upon startup.  To do fine the actual error message(s), run `kubectl describe pod <podname, i.e. jenkins-0> -n <namespace of pod>`, several containers will show in the describe output.  Then, run `kubectl logs <failing pod name, i.e. jenkins-0> -n <namespace> -c <init container, i.e. init>`.

Jan 18th, 2024
- I tried generating [access tokens via the CLI](https://docs.gitea.com/next/development/api-usage), but [discovered](https://github.com/go-gitea/gitea/issues/23382) I could not do so with an oauth2 (OIDC) user.  Running `curl -H "Content-Type: application/json" -d '{"name":"<username>"}' -u username:password https://gitea.<tld>/api/v1/users/<username>/tokens` informed me that the `<username>` oauth2 user does not have a password set.
- After generating an access token with my oauth2 user, I was able to run `docker login gitea.<tld>`, which prompted me with a username field, and a password field, which is where the token was entered.
- To push an image, I had to tag an image on my system to match the following scheme: `gitea.<tld>/<username>/img:tag`, i.e., `gitea.<tld>/<username>/meson-build:latest`.
- For cloning with SSH, use `git@gitea-ssh.<tld>:<username>/<repo name>.git`.  (This assumes that the user has copied in the SSH public key from his machine).

Jan 19th, 2024
- Gitea token permissions for the container registry appear to only require "misc" permissions to be set to "read/write".
- Verified an image (my Meson build image) can be pulled and pushed from seperate machines.
- Revised the "wait" condition with awk and regex to properly wait for the right Gitea container to enter STATUS "running"

Jan 21, 2024
- Connected Gitea to Jenkins by the Gitea plugin
- Stepped through the "all" playbook starting somewhere in the Gitea role, because fact setting is stored in memory, so running Gitea and Jenkins playbooks separately was not working.  It appears that JCasC is correct for setting the right Gitea API token

Jan 22, 2024
- Performed some minor tweaks on Gitea installation.  There seems to be a weird state Gitea enters with enough modification of the `Jenkins` user.
- [Mirroring](https://docs.gitea.com/usage/repo-mirror) is simple.  Create a personal access token (in BitBucket) and add as a migration (repo settings, "Mirror Settings").  Once the repo is migrated, [convert](https://github.com/go-gitea/gitea/issues/7609#issuecomment-1469560266) the repo to a "regular" repo (otherwise, the repo is read-only).  Then, add under "Mirror Settings", a "push mirror".  The same access token from the git service (i.e. BitBucket) can be used as the password.

February 3rd, 2024
- Cleanup code base, removed Jenkins in favor of Gitea Actions.
- Added additional versions for software installed within this cluster in `version.yaml`.

February 5th, 2024
- Placed many variables into an Ansible Vault