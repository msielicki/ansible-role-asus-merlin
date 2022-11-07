#!/usr/bin/python
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: nvram

short_description: Get, set and commit values to NVRAM

version_added: "1.0.0"

description: Get, set and commit values to NVRAM

options:
    name:
        description: Key name.
        required: false
        type: str
    command:
        description:
            - get - get value for the key name.
            - set - set value for the key name.
            - getall - return all key-value data from nvram.
            - commit - apply changes to nvram.
        required: false
        default: get
        type: str
    value:
        description: Value to be set for key name.
        required: false
        type: str
    apply:
        description: Auto commit any change to nvram.
        required: false
        default: false
        type: bool
    force:
        description: Force update even key has the same value.
        required: false
        default: false
        type: bool

author:
    - Mariusz Sielicki (@msielicki)
"""

EXAMPLES = r"""
- name: Return model from nvram
  nvram:
    name: model

- name: Set new LAN hostname
  nvram:
    name: lan_hostname
    value: my_router
    command: set
    apply: true

- name: Get all key-values from nvram
  nvram:
    command: getall
"""

RETURN = r"""
key:
    desciption: Key name
    type: str
    returned: for get/set command
    sample: lan_hostname
value:
    desciption: Key name
    type: str
    returned: for get/set command
    sample: my_router
diff:
    desciption: Key name
    type: (new, old)
    returned: for set command
    sample: lan_hostname
results:
    desciption: Dict with key-values from nvram
    type: dict
    returned: for getall command
    sample: {lan_hostname: my_router, ....}
message:
    description: The output message that the nvram module generates.
    type: str
    returned: always
    sample: 'Key lan_hostname has been changed, but not committed'
"""

from ansible.module_utils.basic import AnsibleModule


class Nvram(object):
    def __init__(self, module, auto_commit=False):
        self._module = module
        self._commit = auto_commit

    def get(self, key):
        cmd = "nvram get {}".format(key)
        _, out, err = self._module.run_command(cmd)
        if not out:
            self._module.fail_json(msg="Key {} not found.".format(key))
        return out.rstrip()

    def set(self, key, value):
        cmd = "nvram set '{}'='{}'".format(key, value)
        _, out, err = self._module.run_command(cmd)
        if self._commit:
            self.commit()

    def getall(self):
        _, out, err = self._module.run_command("nvram getall")
        result = {}
        for line in out.split("\n"):
            if "=" in line:
                k, v = line.split("=", maxsplit=1)
                result[k] = v
        return result

    def commit(self):
        _, out, err = self._module.run_command("nvram commit")


def run_module():
    module_args = dict(
        name=dict(type="str", aliases=["key"], required=False),
        command=dict(
            type="str",
            aliases=["action"],
            choices=["get", "set", "getall", "commit"],
            default="get",
        ),
        value=dict(type="str", default=None),
        apply=dict(type="bool", default=False),
        force=dict(type="bool", default=False),
    )

    result = dict(changed=False, message="")

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    nvram = Nvram(module=module, auto_commit=module.params["apply"])
    command = module.params["command"]

    if command == "getall":
        result["result"] = nvram.getall()

    elif command == "get":
        key = module.params["name"]
        value = nvram.get(key)

        result["key"] = key
        result["value"] = value

    elif command == "set":
        force = module.params["force"]
        key = module.params["name"]
        value = module.params["value"]
        value_old = nvram.get(key)

        if force or value != value_old:
            nvram.set(key, value)
            result["key"] = key
            result["diff"] = {"new": value, "old": value_old}
            if module.params["apply"]:
                msg = "Key {} has been changed and committed.".format(key)
            else:
                msg = "Key {} has been changed, but not committed.".format(key)
            result["message"] = msg
            result["changed"] = True
    elif command == "commit":
        nvram.commit()
        result["changed"] = True
        result["message"] = "NVRAM has been committed."

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
