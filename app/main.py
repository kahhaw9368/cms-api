"""cms-api — web API for team cms-team.

Scaffolded from the web-api golden-path template (see .apex/context.yaml for
template version). Health endpoints below are wired to the WebService type's
probes — keep them fast and dependency-free.
"""

from fastapi import FastAPI

app = FastAPI(title="cms-api")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.get("/")
def root():
    return {"service": "cms-api", "team": "cms-team"}
