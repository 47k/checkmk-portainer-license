from cmk.agent_based.v2 import *

def parse_portainer_license(string_table):
    if not string_table:
        return None

    # Rebuild full raw line from tokens
    raw = " ".join(string_table[0])

    if raw.startswith("error|"):
        return raw.split("|", 2)

    # Split valid payload into exactly 7 fields.
    parts = raw.split("|", 6)
    if len(parts) < 7 or parts[0] != "valid":
        return None

    return parts

agent_section_portainer_license = AgentSection(
    name="portainer_license",
    parse_function=parse_portainer_license,
)

def discover_portainer_license(section):
    if section is not None:
        yield Service()


def check_portainer_license(params, section):
    if section is None:
        yield Result(state=State.CRIT, summary="No data received")
        return

    status = section[0]

    if status == "error":
        message = section[1] if len(section) > 1 else "API error"
        yield Result(state=State.CRIT, summary=f"API error: {message}")
        return

    if status != "valid" or len(section) < 7:
        yield Result(state=State.CRIT, summary="Unexpected agent output")
        return

    days_left = int(section[1])
    expiry_str = section[2]
    company = section[3]
    licensed_nodes = int(section[4])
    used_nodes = int(section[5])
    runtime = float(section[6])

    warn = params.get("warn", 30)
    crit = params.get("crit", 7)
    nodes_warn = params.get("nodes_warn")
    nodes_crit = params.get("nodes_crit")

    if days_left < crit:
        expiry_state = State.CRIT
    elif days_left < warn:
        expiry_state = State.WARN
    else:
        expiry_state = State.OK

    nodes_state = State.OK
    if used_nodes > licensed_nodes:
        nodes_state = State.CRIT
    elif nodes_crit is not None and used_nodes > nodes_crit:
        nodes_state = State.CRIT
    elif nodes_warn is not None and used_nodes > nodes_warn:
        nodes_state = State.WARN

    usage_pct = (used_nodes / licensed_nodes * 100.0) if licensed_nodes > 0 else 0.0

    yield Result(state=expiry_state, summary=f"{days_left} days until expiration")
    yield Result(state=State.OK, summary=f"Valid until {expiry_str}")
    yield Result(state=State.OK, summary=company)
    yield Result(
        state=nodes_state,
        summary=f"Nodes: {used_nodes}/{licensed_nodes} ({usage_pct:.1f}%)",
    )

    yield Metric("days_left", days_left)
    yield Metric("api_runtime", runtime)
    yield Metric("licensed_nodes", licensed_nodes)
    yield Metric("used_nodes", used_nodes)
    yield Metric("node_usage_pct", usage_pct)

check_plugin_portainer_license = CheckPlugin(
    name="portainer_license",
    service_name="Portainer License",
    discovery_function=discover_portainer_license,
    check_function=check_portainer_license,
    check_default_parameters={"warn": 30, "crit": 7},
    check_ruleset_name="portainer_license",
)
