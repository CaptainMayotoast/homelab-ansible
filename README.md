# Overview
Ansible playbooks to install tools on a Kubernetes cluster

# Features
- :scroll: Cert-manager :scroll:
- :hammer: Gitea (with a runner, just enable Actions on each repo) :hammer:
- :door: Istio (HTTPS gateway) :door:
- :closed_lock_with_key: Keycloak (simple identity provider to allow friends to easily access Gitea) :closed_lock_with_key:
- 🗃️ Longhorn (underlying cluster block storage) 🗃️
- :metal: MetalLB (load balancer for bare metal clusters) :metal:
- 🚧 SonarQube 🚧
- 🛑 [FUTURE] PiHole (DNS sinkhole) 🛑

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
ansible-playbook -i inventory/dev playbooks/all.yaml --user ansible -e @secrets.enc --vault-password-file ./password_file

# pick up from a step
ansible-playbook -i inventory/dev playbooks/<playbook name>.yaml --user ansible --start-at-task="wait for Gitea pod to become available" -e @secrets.enc --vault-password-file ./password_file

# step through one at a time
ansible-playbook -i inventory/dev playbooks/<playbook name>.yaml --user ansible --start-at-task="wait for Gitea pod to become available" -e @secrets.enc --vault-password-file ./password_file --step
```

# Update Nodes
```
ansible-playbook -i inventory/dev playbooks/update-and-reboot.yaml --user ansible -e @secrets.enc --vault-password-file ./password_file
```

# Service notes

## Cert-manager

- Uses https://www.getlocalcert.net/ to provide HTTPS such that common browsers will not complain when presented with a certificate Istio provides.
- Let's Encrypt will rate limit per week, so keep deployments of this to a minimum (~5 queries to the official Let's Encrypt server weekly is the limit). 

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

# Ansible Vault fields

1. vault_domain_name
    - The top level domain and second level domain of the network this cluster runs on, such as `example.com`.
2. vault_third_level_domain
    - The third level domain, such as `app1`, in `app1.example.com`.
3. vault_firewall_hostname
    - The network name of the router, such as `homerouter`.
5. vault_firewall_credential_file
    - The credentials (key, secret) of the OpnSense API key.
6. vault_certmanager_email
    - An email address to provide CertManager.
7. vault_metallb_address_pool
    - A string that represents a range of IPs, i.e. `192.168.0.1-192.168.0.40`.  These IPs usually come from the routers static IP address ranges.
8. vault_kubernetes_dashboard_load_balancer_ip
    - An IP address from `vault_metallb_address_pool`.
9. vault_longhorn_load_balancer_ip
    - An IP address from `vault_metallb_address_pool`.
10. vault_pihole_admin_password
    - A password, i.e. `password`.
11. vault_pihole_network_dns_ip
    - A DNS server (IP) on the network.
12. vault_pihole_dns_load_balancer_ip
    - An IP address from `vault_metallb_address_pool`.
13. vault_pihole_time_zone
    - The IANA Time Zone Database format of "Region/City".
14. vault_gitea_admin_user
    - The name of the Gitea admin user, must not be "admin".
15. vault_gitea_admin_password
    - A password, i.e. `password`.
16. vault_gitea_ssh_load_balancer_ip
    - An IP address from `vault_metallb_address_pool`.
17. vault_istio_load_balancer_ip
    - An IP address from `vault_metallb_address_pool`.
18. vault_istio_cert_manager_credential_file
    - The path to the CertManager API credential file for https://www.getlocalcert.net/.
19. vault_keycloak_config_json
    - JSON representing the Keycloak configuration.
20. vault_keycloak_admin_user
    - The name of the Keycloak admin user.
21. vault_keycloak_admin_password
    - A password, i.e. `password`.
22. vault_keycloak_gitea_oidc_secret
    - The string of characters from Keycloak configuration representing the OIDC secret.
23. vault_keycloak_gitea_client_id
    - The (usually simple) string representing the OIDC ID of the client, i.e. `giteaclient`.
