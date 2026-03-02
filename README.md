# checkmk-portainer-license

![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Checkmk](https://img.shields.io/badge/Tested%20with-Checkmk%202.4.0-green)
![Release](https://img.shields.io/github/v/release/47k/checkmk-portainer-license)
![Status](https://img.shields.io/badge/status-beta-orange)

Checkmk special agent for monitoring Portainer license expiry and node usage via API.

---

## Overview

This Checkmk extension monitors:

- Portainer Business license expiration
- Remaining days until expiry
- Licensed vs. used nodes
- Node usage percentage
- API availability and authentication
- API response runtime

All monitoring is performed server-side using a Checkmk Special Agent.

---

## Compatibility

Tested with:

- Checkmk 2.4.0
- Portainer Business Edition

Compatible with:
- CEE
- CRE

---

## Features

- JWT authentication via `/api/auth`
- License inspection via `/api/licenses`
- Endpoint inspection via `/api/endpoints`
- Configurable warn/crit thresholds
- Hard CRIT if used_nodes > licensed_nodes
- Performance metrics included

---

## Prerequisites ##

Portainer User with Admin rights is necessary

---

## Installation (MKP – Recommended)

1. Download the `.mkp` file from the Releases section.
2. Install:

```bash
mkp add portainer_license-0.1.3.mkp
mkp enable portainer_license
omd restart
```

---

## Manual Installation

Copy the plugin structure into:

```
local/lib/python3/cmk_addons/plugins/
```

Then reload the site:

```bash
cmk -R
```

---

## Rule Configuration

### Special Agent Rule

Rule name: `Portainer License`

Parameters:

- `url`
- `username`
- `password`
- `timeout`
- `insecure`

---

### Check Parameters Rule

Rule name: `Portainer License`

Parameters:

- `warn` (default: 30)
- `crit` (default: 7)
- `nodes_warn`
- `nodes_crit`

---

## Metrics

- `days_left`
- `api_runtime`
- `licensed_nodes`
- `used_nodes`
- `node_usage_pct`

No perfdata thresholds are currently attached.

---

## Example Service Output

```
Portainer License OK - 120 days remaining | days_left=120 api_runtime=0.42 licensed_nodes=5 used_nodes=3 node_usage_pct=60
```

---

## Example API Test

```bash
curl -k -X POST https://portainer.example.com/api/auth   -H "Content-Type: application/json"   -d '{"Username":"admin","Password":"password"}'
```

---

## Screenshot(s) ##
<img width="1041" height="155" alt="Screenshot" src="https://github.com/user-attachments/assets/345293ec-6d4b-42cf-aa95-eaedb2edfbc2" />
<img width="771" height="114" alt="Screenshot_Parameters" src="https://github.com/user-attachments/assets/ea5a2196-7a59-4a35-bc85-85caa54cc4e1" />
<img width="674" height="1507" alt="Screenshot_Perfdata" src="https://github.com/user-attachments/assets/0710a7f1-f54d-47f8-85ac-7ca18d681046" />

---

## Error Handling

CRIT is returned if:

- Authentication fails
- License data missing
- Expiry date missing
- used_nodes > licensed_nodes

UNKNOWN is not used.

---

## Security

- HTTPS supported
- Self-signed certificates supported via `insecure`
- Password masked in output
- Special agent uses `replace_passwords()`

---

## Roadmap

- API Token authentication
- CE compatibility improvements
- Stable release (v1.0.0)

---

## Support

No commercial support.

Issues and Pull Requests welcome.

---

## Author

Manuel "Overlord" Michalski
47k - Professional IT Solutions
https://www.47k.de
