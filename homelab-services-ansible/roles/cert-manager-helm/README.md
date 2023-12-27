# Cert-manager

## Overview

- Folders: `secrets` and `tasks`
- `secrets` should hold an API credentials file created from "https://console.getlocalcert.net/describe-zone?zone_name=andromeda.localhostcert.net."
    - getlocalcert.net is used to provide a cert for a homelab where the homelab owner does not want or need to have a proper domain registered to him
    - resources: 
        - https://news.ycombinator.com/item?id=38036203
        - https://github.com/robalexdev/getlocalcert-client-tests/blob/main/examples/cert-manager/test-resources.yaml
        - https://www.getlocalcert.net/
- `tasks` is the usual folder for cert-manager installation steps     

