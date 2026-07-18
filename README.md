# cms-api

Web API for team **cms-team**, scaffolded from the platform's `web-api` golden-path template.

## Run locally
```
pip install -r requirements-dev.txt
uvicorn main:app --app-dir app --reload
```

## How this ships
Push to `main` → CI builds the image, pushes to ECR, and opens a PR bumping the image tag in
the GitOps repo → managed Argo CD deploys to nonprod. Promote with: ask Apex to
"promote cms-api to prod".

Health endpoints `/healthz` and `/ready` are wired to the platform's probes — keep them fast.
