from pydantic import AliasChoices, AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
import requests

from rule import Rule

# GET  /v1/security/runtime/rules
# POST /v1/security/runtime/rules
# POST /v1/security/runtime/rules/delete
# { "ids": [ "string" ] }
# POST /v1/security/runtime/rules/toggle
# { "enabled": true, "ids": [ "string" ] }
# POST /v1/security/runtime/rules/validate
# { "type": "VALIDATE_UNKNOWN", "ruleText": "string" }
# GET /v1/security/runtime/rules/{id}
# PUT /v1/security/runtime/rules/{id}


def test(str) -> str:
    return to_camel(str)


class CastAiRule(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field: AliasChoices(field, to_camel(field)),
            serialization_alias=to_camel,
        )
    )

    id: str
    enabled: bool
    name: str
    type: str
    category: str
    anomalies_count: int = Field(
        default=0,
    )
    severity: str
    is_built_in: bool = False
    resource_selector: str
    rule_text: str
    rule_engine_type: str = "RULE_ENGINE_TYPE_CEL"
    labels: dict[str, str]


def convert_rule(rule: Rule) -> CastAiRule:
    rule_text = rule.query
    for k, value in rule.variables.items():
        if isinstance(value, list):
            value = "[" + ", ".join(f'"{v}"' for v in value) + "]"
        rule_text = f"cel.bind({k}, {value}, {rule_text})"

    category = "event" if rule.data_source.get("category", "event") == "process_creation" else "event"

    return CastAiRule(
        id=rule.id,
        enabled=True,  # Assuming the rule is enabled by default
        name=rule.name,
        type="custom",  # Assuming a default type
        category=category,
        severity="SEVERITY_" + rule.level.upper(),
        resource_selector="",  # Assuming no resource selector
        rule_text=rule_text,
        labels={
            "author": rule.author,
            "version": rule.version,
            "confidence": str(rule.confidence),
            "robustness": rule.robustness,
        },
    )


class CastAiApi:
    def __init__(self, server: str, token: str):
        self.server = server
        self.token = token
        self.headers = {"X-API-Key": self.token}
        self.base_url = server + "/v1/security/runtime/rules"

    def get_rules(self) -> list[CastAiRule]:
        response = requests.get(self.base_url, headers=self.headers)
        data = response.json()
        rules = [CastAiRule(**r) for r in data.get("rules", [])]
        return rules

    def upsert_rules(self, rules: list[Rule]) -> bool:
        for r in rules:
            cast_rule = convert_rule(r)
            data = cast_rule.model_dump_json(
                exclude=[
                    "id",
                    "type",
                    "anomalies_count",
                ],
                exclude_none=True,
            )
            result = requests.post(self.base_url, data, headers=self.headers)
            if result.status_code >= 400:
                print(result.reason)
        return result.status_code == 200
