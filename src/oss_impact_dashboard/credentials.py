from __future__ import annotations

import os


def project_env_suffix(project_id: str) -> str:
    return project_id.upper().replace("-", "_")


def github_token_env_names(project_id: str) -> tuple[str, ...]:
    suffix = project_env_suffix(project_id)
    return (f"OSS_DASHBOARD_GITHUB_TOKEN_{suffix}",)


def github_token_for_project(project_id: str) -> str | None:
    suffix = project_env_suffix(project_id)
    return os.environ.get(f"OSS_DASHBOARD_GITHUB_TOKEN_{suffix}")


def goatcounter_api_key_env_names(project_id: str) -> tuple[str, ...]:
    suffix = project_env_suffix(project_id)
    return (f"GOATCOUNTER_API_KEY_{suffix}",)


def goatcounter_api_key_for_project(project_id: str) -> str | None:
    suffix = project_env_suffix(project_id)
    return os.environ.get(f"GOATCOUNTER_API_KEY_{suffix}")


def credential_source_label(project_id: str, *, kind: str) -> str:
    if kind == "github":
        suffix = project_env_suffix(project_id)
        if os.environ.get(f"OSS_DASHBOARD_GITHUB_TOKEN_{suffix}"):
            return f"OSS_DASHBOARD_GITHUB_TOKEN_{suffix}"
        return "missing"
    if kind == "goatcounter":
        suffix = project_env_suffix(project_id)
        if os.environ.get(f"GOATCOUNTER_API_KEY_{suffix}"):
            return f"GOATCOUNTER_API_KEY_{suffix}"
        return "missing"
    raise ValueError(f"Unsupported credential kind: {kind}")
