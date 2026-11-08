from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyVersions:
    terms: str = "1.0"
    privacy: str = "1.0"
    cookies: str = "1.0"


POLICY_VERSIONS = PolicyVersions()