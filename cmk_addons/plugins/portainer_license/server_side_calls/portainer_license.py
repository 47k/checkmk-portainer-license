#!/usr/bin/env python3
from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from cmk.server_side_calls.v1 import SpecialAgentCommand, SpecialAgentConfig, noop_parser

def _agent_arguments(params, _host_config):
    arguments = [
        "--url", params["url"],
        "--username", params["username"],
        "--password", params["password"],
        "--timeout", str(params.get("timeout", 10)),
    ]

    if params.get("insecure"):
        arguments.append("--insecure")

    yield SpecialAgentCommand(command_arguments=arguments)

special_agent_portainer_license = SpecialAgentConfig(
    name="portainer_license",
    parameter_parser=noop_parser,
    commands_function=_agent_arguments,
)
