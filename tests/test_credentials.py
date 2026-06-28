from oss_impact_dashboard.credentials import (
    github_token_for_project,
    goatcounter_api_key_for_project,
    project_env_suffix,
)


def test_project_env_suffix_normalizes_ids():
    assert project_env_suffix("mole-local") == "MOLE_LOCAL"
    assert project_env_suffix("fivetran") == "FIVETRAN"


def test_github_token_for_project_prefers_project_specific(monkeypatch):
    monkeypatch.setenv("OSS_DASHBOARD_GITHUB_TOKEN_MOLE_LOCAL", "fork-token")
    monkeypatch.setenv("OSS_DASHBOARD_GITHUB_TOKEN", "shared-token")
    assert github_token_for_project("mole-local") == "fork-token"


def test_github_token_for_project_ignores_shared_secret(monkeypatch):
    monkeypatch.setenv("OSS_DASHBOARD_GITHUB_TOKEN", "shared-token")
    assert github_token_for_project("mole-local") is None


def test_github_token_for_production_requires_project_specific_secret(monkeypatch):
    monkeypatch.setenv("OSS_DASHBOARD_GITHUB_TOKEN", "shared-token")
    assert github_token_for_project("mole") is None


def test_goatcounter_api_key_for_project_prefers_project_specific(monkeypatch):
    monkeypatch.setenv("GOATCOUNTER_API_KEY_MOLE", "mole-key")
    monkeypatch.setenv("GOATCOUNTER_API_KEY", "shared-key")
    assert goatcounter_api_key_for_project("mole") == "mole-key"
    assert goatcounter_api_key_for_project("mole-local") is None
