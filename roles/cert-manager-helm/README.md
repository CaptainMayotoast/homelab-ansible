# Cert-manager

## Overview

- Folders: `secrets` and `tasks`
    - `secrets` should hold an API credentials file created from "https://console.getlocalcert.net/"
        - The contents of the file looks [like](https://docs.getlocalcert.net/acme-clients/cert-manager/#api-keys)
        ```json
        {
            "<yourSubdomain>.localhostcert.net": {
                "username": "<yourApiKeyId>",
                "password": "<yourApiKeySecret>",
                "fulldomain": "<yourSubdomain>.localhostcert.net",
                "subdomain": "<yourSubdomain>",
                "server_url": "https://api.getlocalcert.net/api/v1/acme-dns-compat",
                "allowfrom": []
            }
        }
        ```
        - This file gets rysnc-ed to control_plane nodes.
        - getlocalcert.net is used to provide a cert for a homelab where the homelab owner does not want or need to have a proper domain registered
        - resources: 
            - https://news.ycombinator.com/item?id=38036203
            - https://github.com/robalexdev/getlocalcert-client-tests/blob/main/examples/cert-manager/test-resources.yaml
            - https://www.getlocalcert.net/
    - `tasks` is the usual folder for cert-manager installation steps     

