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

February 19th, 2024
- Fought with JSON serialization: needed to store JSON in an Ansible vault for the Keycloak config.  Turns out, I needed "| to_json" appended to my JSON (i.e. { ... json here ... } | to_json).  The configuration from Keycloak can be copied into the Ansible vault file, and "| to_json" needs to be appended in order for the K8s ConfigMap to ingest as JSON.
