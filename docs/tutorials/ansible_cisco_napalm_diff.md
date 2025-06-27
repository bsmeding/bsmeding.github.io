## Why NAPALM + Ansible?

[NAPALM](https://napalm.readthedocs.io) gives you a vendor‑agnostic Python API for interacting with network devices, while **Ansible** gives you idempotent automation driven by human‑readable YAML.\
Together they let you:

- Retrieve facts or configuration from many vendors with a single module call.
- Safely push configuration changes with automatic diff and rollback.
- Validate compliance against source‑of‑truth data before (or after) a change window.

### A note on the old `napalm` connection plugin

The `ansible.netcommon.napalm` connection plugin was **deprecated** and removed from the collection starting in *ansible.netcommon 5.0*.\
Modern playbooks should instead use the dedicated NAPALM modules (`napalm_get_facts`, `napalm_install_config`, `napalm_validate`, and friends) which keep the NAPALM logic self‑contained.

## Prerequisites

| Component                 | Recommended Version                 | Notes                                              |
| ------------------------- | ----------------------------------- | -------------------------------------------------- |
| Python                    | 3.10+                               | NAPALM and Ansible now test primarily on 3.9+      |
| Ansible Core              | 2.16+                               | Install from `pip install ansible-core`            |
| ansible‑napalm collection | latest                              | `ansible-galaxy collection install napalm.ansible` |
| Python NAPALM library     | 4.x                                 | `pip install napalm`                               |
| Network devices           | IOS‑XE 17+, Junos 22+, EOS 4.30+, … | Anything supported by NAPALM                       |

If you prefer Docker, grab the ready‑made devcontainer from the [GitHub repo](https://github.com/bsmeding).

### Installing everything in one go

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install ansible-core napalm
ansible-galaxy collection install napalm.ansible
```

> **Tip:** Pin exact versions in a `requirements.txt` and `collections/requirements.yml` so your CI pipeline is repeatable.

## Project layout

```text
inventory/
  routers.yml
group_vars/
  all.yml
playbooks/
  gather-facts.yml
  backup-config.yml
  push-config.yml
validate/
  bgp.yml
```

### Inventory example

`inventory/routers.yml`:

```yaml
all:
  children:
    lab_routers:
      hosts:
        r1:
          ansible_host: 192.0.2.11
          ansible_user: ansible
          ansible_password: Cisco123
          ansible_network_os: ios
        r2:
          ansible_host: 192.0.2.12
          ansible_user: ansible
          ansible_password: Juniper123
          ansible_network_os: junos
```

### Global variables (group_vars/all.yml)

```yaml
napalm_username: "{{ ansible_user }}"
napalm_password: "{{ ansible_password }}"
napalm_optional_args:
  global_delay_factor: 2
```

## 1. Gathering device facts

Create `playbooks/gather-facts.yml`:

```yaml
---
- name: Collect baseline facts with NAPALM
  hosts: lab_routers
  gather_facts: no
  tasks:
    - name: Get facts
      napalm.ansible.napalm_get_facts:
        hostname: "{{ inventory_hostname }}"
        username: "{{ napalm_username }}"
        password: "{{ napalm_password }}"
        optional_args: "{{ napalm_optional_args | default({}) }}"
      register: result

    - name: Show facts
      debug:
        var: result.facts
```

Run it:

```bash
ansible-playbook -i inventory/ playbooks/gather-facts.yml
```

Sample output:

```
ok: [r1] => {
  "result.facts": {
    "hostname": "R1",
    "model": "CSR1000v",
    "os_version": "17.09.04",
    "serial_number": "9B0FD12ZABCDEFG",
    ...
  }
}
```

## 2. Backing up running‑config

`playbooks/backup-config.yml`:

```yaml
---
- name: Save configs to local backup directory
  hosts: lab_routers
  gather_facts: no
  tasks:
    - name: Fetch running config
      napalm.ansible.napalm_get_facts:
        filter: config
        hostname: "{{ inventory_hostname }}"
        username: "{{ napalm_username }}"
        password: "{{ napalm_password }}"
      register: config

    - name: Write file locally
      copy:
        content: "{{ config.facts.config.running }}"
        dest: "backups/{{ inventory_hostname }}-{{ lookup('pipe', 'date +%F') }}.cfg"
```

> **Idempotency note:** NAPALM modules set `changed: false` when there is no diff, so you can chain them in CI pipelines without side‑effects.

## 3. Pushing configuration safely

Create a candidate config file, e.g. `configs/r1_bgp.txt`:

```
router bgp 65001
 address-family ipv4 unicast
  network 10.0.0.0 mask 255.255.255.0
!
```

Playbook `playbooks/push-config.yml`:

```yaml
---
- name: Push candidate config with automatic diff + rollback
  hosts: r1
  gather_facts: no
  tasks:
    - name: Install configuration
      napalm.ansible.napalm_install_config:
        hostname: "{{ ansible_host }}"
        username: "{{ napalm_username }}"
        password: "{{ napalm_password }}"
        optional_args: "{{ napalm_optional_args | default({}) }}"
        candidate_filename: "configs/{{ inventory_hostname }}_bgp.txt"
        commit_changes: true
        replace_config: false
        diff_file: "diffs/{{ inventory_hostname }}-{{ lookup('pipe', 'date +%F-%H%M%S') }}.diff"
```

What happens next:

1. NAPALM loads the candidate file into the device’s *compare* engine.
2. If the diff is non‑empty, Ansible sets `changed: true` and commits.
3. On error, NAPALM triggers an automatic rollback, so you stay safe.

## 4. Validating state against source‑of‑truth

NAPALM ships a YAML‑based validation framework.

`validate/bgp.yml`:

```yaml
---
bgp_neighbors:
  global:
    router_id: 192.0.2.1
    peers:
      203.0.113.1:
        is_up: true
        address_family:
          ipv4 unicast:
            received_prefixes: 1
```

`playbooks/validate.yml`:

```yaml
---
- name: Check operational state
  hosts: r1
  gather_facts: no
  tasks:
    - name: Validate BGP
      napalm.ansible.napalm_validate:
        hostname: "{{ ansible_host }}"
        username: "{{ napalm_username }}"
        password: "{{ napalm_password }}"
        validation_file: "validate/bgp.yml"
      register: validate

    - name: Fail if non‑compliant
      assert:
        that:
          - validate.compliance
```

Add this to your CI/CD pipeline and you have continuous compliance testing.

## 5. Putting it all together in CI

```yaml
name: network-ci
on:
  push:
    paths:
      - "configs/**"
      - "validate/**"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          pip install ansible-core napalm
          ansible-galaxy collection install -r collections/requirements.yml
      - name: Dry‑run config
        run: ansible-playbook -i inventory/ playbooks/push-config.yml --check
      - name: Validate
        run: ansible-playbook -i inventory/ playbooks/validate.yml
```

## Troubleshooting checklist

| Symptom                        | Fix                                                                        |
| ------------------------------ | -------------------------------------------------------------------------- |
| `ModuleNotFoundError: napalm`  | Activate your virtualenv or `pip install napalm`                           |
| `ssh_exchange_identification`  | Check `ansible_host` IP and ACLs; NAPALM needs SSH access                  |
| Device shows changed every run | Use `replace_config: false` and make device config canonical               |
| Connection plugin not found    | Make sure you **don’t** set `ansible_connection: napalm` after its removal |

## Next steps

- Explore vendor‑specific optional args (e.g. EOS `transport: https`) in the [NAPALM docs](https://napalm.readthedocs.io).
- Combine NAPALM with **Ansible’s `delegate_to:`** for control‑plane orchestration.
- Look at `napalm_diff_yang` for data‑model‑driven compliance.

Happy automating! If you spot any issues, open a pull request or ping me on [Bluesky](https://bsky.app/profile/netdevops.it)

---

*Updated: 27 June 2025*