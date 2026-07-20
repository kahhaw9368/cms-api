"""cms-api — web API for team cms-team.

Scaffolded from the web-api golden-path template (see .apex/context.yaml for
template version). Health endpoints below are wired to the WebService type's
probes — keep them fast and dependency-free.
"""

import base64
import json
import os

from fastapi import FastAPI

app = FastAPI(title="cms-api")

# Demo: environment detection without per-env config.
# The platform promotes the SAME image from dev to prod (pinned tag, ADR-0007),
# so the environment can't be baked in at build time. Instead we read the pod's
# projected service-account token: its `iss` claim is the EKS cluster's OIDC
# issuer, which differs per cluster. Known issuers below map to env names.
# An ENVIRONMENT env var, if ever provided by the platform, takes precedence.
_KNOWN_ISSUERS = {
    "DA1988624DE65BEB5AF863F5103DE24F": "dev",   # platform-nonprod
    "3E3886DABD8FED22FA609F7EC2B46AF5": "prod",  # platform-prod
}
_SA_TOKEN_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/token"


def detect_environment() -> str:
    """Best-effort environment detection: env var override, then SA token issuer."""
    override = os.getenv("ENVIRONMENT")
    if override:
        return override
    try:
        with open(_SA_TOKEN_PATH) as f:
            token = f.read().strip()
        payload = token.split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        issuer = claims.get("iss", "")
        for issuer_id, env in _KNOWN_ISSUERS.items():
            if issuer_id in issuer:
                return env
        return "unknown-cluster"
    except (OSError, ValueError, IndexError):
        return "local"


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.get("/")
def root():
    return {"service": "cms-api", "team": "cms-team", "environment": detect_environment()}


@app.get("/api/sample")
def sample():
    env = detect_environment()
    return {
        "message": f"this is sample api sitting in {env} environment",
        "service": "cms-api",
        "environment": env,
    }
