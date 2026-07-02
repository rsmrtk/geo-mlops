# geo-mlops

Geocoding REST API + CLI in Go, backed by an ML microservice that classifies
the type of a location (residential, commercial, park, transport, ...) from
its coordinates. Built as a hands-on MLOps project: train → register → serve
→ deploy, wired end to end.

Infra (Helm charts, ArgoCD apps) lives in a separate repo:
[geo-mlops-infra](https://github.com/rsmrtk/geo-mlops-infra).

## Architecture

```
client → geocoder (Go)  ──▶ Nominatim (reverse geocoding, address lookup)
              │
              ├──▶ ml-svc (Python/FastAPI) ──▶ MLflow Model Registry (alias: champion)
              │
              └──▶ Postgres (S2-cell keyed cache)
```

- **`cmd/server`** — HTTP API (`/geocode?lat=..&lng=..`). Resolves an address
  via Nominatim, asks `ml-svc` to classify the location type, caches the
  result in Postgres keyed by S2 cell ID (level 14), and returns everything
  as JSON.
- **`cmd/cli`** — same lookup as a one-shot CLI (`geocoder <lat> <lng>`).
- **`internal/geocoder`** — core package: Nominatim client, ML client, S2
  cell hashing, Postgres cache. No caching is used if `DATABASE_URL` is unset
  or unreachable — the server degrades gracefully instead of failing to boot.
- **`ml/service`** — FastAPI service that loads a model from the MLflow
  Registry at startup (`models:/location-classifier@champion`) and exposes
  `POST /classify`. If the model can't be loaded, it still starts and returns
  `"unknown"` instead of crashing.
- **`ml/training`** — training and promotion scripts, run as one-off
  Kubernetes Jobs (see `.github/workflows/ml-train.yaml`), not on a laptop.

## The ML model — what it actually is

Worth being upfront about this: it's a `RandomForestClassifier` (scikit-learn)
trained on two features — latitude and longitude — against ~160 hand-labeled
synthetic points across Ukrainian cities (`ml/training/data.py`). It predicts
one of 9 location-type classes and a confidence score.

This is intentionally the simplest model that could plug into a real MLOps
loop. The point of this project isn't classification accuracy — it's the
plumbing around the model: versioning, registry aliasing, promotion,
zero-downtime reload, and a caller that degrades gracefully when the model
or the ML service is unavailable. Swapping in a real feature set (OSM tags,
POI density, land-use polygons) wouldn't change anything downstream — that's
the point of the registry/alias boundary.

## MLOps loop

1. `training.train` fetches labeled samples, trains a `RandomForestClassifier`,
   logs params/metrics/model to MLflow, registers a new model version.
2. `training.promote` points the `champion` alias at a specific (or the
   latest) version — using [registry aliases](https://mlflow.org/docs/latest/model-registry.html#deploy-and-organize-models-with-aliases-and-tags),
   not the deprecated `stage` API.
3. `ml-svc` always loads `models:/location-classifier@champion` — promoting
   a new version means updating one pointer, no redeploy needed.
4. Both steps run as Kubernetes Jobs, triggered manually via
   `workflow_dispatch` (`ml-train.yaml`), with the workflow polling job
   status and dumping logs on failure.

## CI/CD

`ci.yaml` on every push to `main`:
1. `go vet` + `go test`
2. Build & push `geo-mlops` (Go server) and `geo-mlops-ml` (Python service)
   images to GHCR, tagged `sha-<short-sha>`
3. Bump the image tags in `geo-mlops-infra/envs/prod/values.yaml` via `yq`
   and push — ArgoCD picks up the change and syncs automatically

No manual `kubectl apply` in the deploy path — the Go repo's CI is what
writes to the infra repo.

## Running locally

```bash
go build -o geo-server ./cmd/server
NOMINATIM_URL=https://nominatim.openstreetmap.org \
ML_SVC_URL=http://localhost:5001 \
./geo-server
# curl localhost:8080/geocode?lat=50.4501&lng=30.5234
```

```bash
cd ml && pip install -r requirements.txt
MLFLOW_TRACKING_URI=http://localhost:5000 uvicorn service.main:app --port 5001
```

## Stack

Go 1.25 · FastAPI · scikit-learn · MLflow · PostgreSQL · S2 geometry ·
Docker · GitHub Actions · Kubernetes Jobs
