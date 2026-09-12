# Open WebUI

Web UI for chatting with LLMs (points at an Ollama server). Two ways to run this:

- `compose.yml` — Docker Compose, published on `localhost:3000`.
- `00-namespace.yaml`/`02-open-webui.yaml`/`03-ingress.yaml` — Kubernetes (K3s), namespace
  `open-webui`. No operator/CRD, so a plain Deployment.

## Kubernetes (K3s)

```bash
export KUBECONFIG=~/.kube/config-k3s-devops
kubectl apply -f 00-namespace.yaml -f 02-open-webui.yaml -f 03-ingress.yaml
```

```bash
kubectl get svc -n open-webui open-webui   # NodePort for the UI (port 8080)
```

Or via the cluster's Traefik ingress (`03-ingress.yaml`): add `<node-ip> open-webui.example.com` to
`/etc/hosts` and browse to `http://open-webui.example.com` — see `../sonar/README.md` for how this
works.

`WEBUI_AUTH=false` (same as `compose.yml`) — no login required, anyone who can reach the
NodePort/Ingress has full access.

### Points at an external Ollama, not `../ollama/`

`OLLAMA_BASE_URL` is `http://192.168.2.38:11434`, same as `compose.yml` — a specific LAN address for
wherever that Ollama instance runs, **not** the in-cluster `../ollama/` stack (which was out of
scope for this conversion) and **not** the `10.21.209.71` address `../tgwebui/`/`n8n/compose.yml`
use for their own Ollama backend. All three configs currently point at different addresses — worth
reconciling if they're meant to share one Ollama instance, but preserved as-is here since that
wasn't asked for.

### Persistence

`/app/backend/data` is Open WebUI's documented data directory (chat history, uploaded
documents/RAG embeddings, settings) — confirmed actively used, not a dead mount, by watching it
download and cache an embedding model there on first boot
(`/app/backend/data/cache/embedding/models/...`).

### Test model from container

```bash
curl http://10.21.213.16:11434/api/generate -d '{
  "model": "qwen3.8:27b",
  "prompt": "Why is the sky blue?",
  "stream": true
}'
```
