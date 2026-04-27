"""Tests for the Hugging Face deployment shell helper."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def run_prepare_hf_deployment(
    *args: str, openenv_version: str = "main"
) -> subprocess.CompletedProcess[str]:
    """Run the deployment helper in dry-run mode for test assertions."""
    repo_root = Path(__file__).resolve().parents[2]
    script_path = repo_root / "scripts" / "prepare_hf_deployment.sh"

    env = os.environ.copy()
    env["OPENENV_VERSION"] = openenv_version

    return subprocess.run(
        [
            "bash",
            str(script_path),
            *args,
            "--dry-run",
            "--skip-collection",
        ],
        cwd=repo_root,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def test_prepare_hf_deployment_repo_id_override(tmp_path: Path) -> None:
    """An exact repo override should target the canonical repo and README URLs."""
    staging_dir = tmp_path / "hf-staging"

    result = run_prepare_hf_deployment(
        "--env",
        "repl_env",
        "--repo-id",
        "openenv/repl",
        "--staging-dir",
        str(staging_dir),
    )

    assert result.returncode == 0, result.stderr
    assert "[dry-run] Would create/update space: openenv/repl" in result.stdout

    generated_readme = staging_dir / "openenv" / "repl" / "README.md"
    assert generated_readme.exists()
    readme_text = generated_readme.read_text()
    assert "https://huggingface.co/spaces/openenv/repl" in readme_text
    assert "https://huggingface.co/spaces/openenv/repl_env" not in readme_text


def test_prepare_hf_deployment_stages_only_selected_env(tmp_path: Path) -> None:
    """Staging should include the selected environment, not the whole envs tree."""
    staging_dir = tmp_path / "hf-staging"

    result = run_prepare_hf_deployment(
        "--env",
        "repl_env",
        "--staging-dir",
        str(staging_dir),
    )

    assert result.returncode == 0, result.stderr

    staged_space = next((staging_dir / "openenv").iterdir())
    assert staged_space.name.startswith("repl_env")
    assert (staged_space / "envs" / "repl_env").is_dir()
    assert not (staged_space / "envs" / "echo_env").exists()

    dockerfile_text = (staged_space / "Dockerfile").read_text()
    assert "ARG ENV_NAME=repl_env" in dockerfile_text
    assert "ENV ENABLE_WEB_INTERFACE=true" in dockerfile_text


def test_prepare_hf_deployment_applies_env_specific_prepare_hook(
    tmp_path: Path,
) -> None:
    """Environment-specific prepare hooks should own Dockerfile customization."""
    staging_dir = tmp_path / "hf-staging"

    result = run_prepare_hf_deployment(
        "--env",
        "openspiel_env",
        "--staging-dir",
        str(staging_dir),
    )

    assert result.returncode == 0, result.stderr

    staged_space = next((staging_dir / "openenv").iterdir())
    assert staged_space.name.startswith("openspiel_env")

    dockerfile_text = (staged_space / "Dockerfile").read_text()
    assert "ARG OPENSPIEL_BASE_IMAGE=" not in dockerfile_text
    assert "FROM ${OPENSPIEL_BASE_IMAGE}" not in dockerfile_text
    assert (
        "FROM ghcr.io/meta-pytorch/openenv-openspiel-base:sha-e622c7e"
        in dockerfile_text
    )
    assert "ENV ENABLE_WEB_INTERFACE=true" in dockerfile_text
