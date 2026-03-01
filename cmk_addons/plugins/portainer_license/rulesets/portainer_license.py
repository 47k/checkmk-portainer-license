from cmk.rulesets.v1 import *
from cmk.rulesets.v1.form_specs import *
from cmk.rulesets.v1.rule_specs import *
from cmk.rulesets.v1.form_specs import Password

def _special_agent_parameter_form() -> Dictionary:
    return Dictionary(
        title=Title("Portainer License Monitoring"),
        elements={
            "url": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Portainer URL"),
                ),
            ),
            "username": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Username"),
                ),
            ),
            "password": DictElement(
                required=True,
                parameter_form=Password(
                    title=Title("Password"),
                ),
            ),
            "timeout": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("API Timeout (seconds)"),
                ),
            ),
            "insecure": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Disable TLS certificate verification"),
                    prefill=DefaultValue(False),
                ),
            ),
        },
    )


def _check_parameter_form() -> Dictionary:
    return Dictionary(
        elements={
            "warn": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("Warning if license expires in less than (days)"),
                ),
            ),
            "crit": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("Critical if license expires in less than (days)"),
                ),
            ),
            "nodes_warn": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("Warning if used nodes are more than"),
                ),
            ),
            "nodes_crit": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("Critical if used nodes are more than"),
                ),
            ),
        },
    )


rule_spec_portainer_license = SpecialAgent(
    name="portainer_license",
    title=Title("Portainer License"),
    topic=Topic.APPLICATIONS,
    parameter_form=_special_agent_parameter_form,
)

rule_spec_check_parameters_portainer_license = CheckParameters(
    name="portainer_license",
    title=Title("Portainer License"),
    topic=Topic.APPLICATIONS,
    parameter_form=_check_parameter_form,
    condition=HostCondition(),
)
