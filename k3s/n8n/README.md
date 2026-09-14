# n8n

Two ways to run this:

- `compose.yml` — Docker Compose, no port published (only reachable over the `autoship` Docker
  network, presumably by other automation on that network).
- `00-namespace.yaml`/`02-n8n.yaml` — Kubernetes (K3s), namespace `n8n`. No operator/CRD for a
  simple single-instance n8n, so plain manifests.

## Kubernetes (K3s)

```bash
export KUBECONFIG=~/.kube/config-k3s-devops
kubectl apply -f k3s/n8n
```

```bash
kubectl get svc -n n8n n8n   # NodePort for the editor UI (port 5678)
```

Or via the cluster's Traefik ingress (`03-ingress.yaml`): add `<node-ip> n8n.example.com` to
`/etc/hosts` and browse to `http://n8n.example.com` — see `../sonar/README.md` for how this works.

No auth is configured (matches `compose.yml`) — anyone who can reach the NodePort/Ingress has full
access. Set `N8N_BASIC_AUTH_ACTIVE`/`N8N_BASIC_AUTH_USER`/`N8N_BASIC_AUTH_PASSWORD` env vars if this
needs to be reachable beyond a trusted network.

`OLLAMA_API_URL` points at `10.21.209.71:11434`, same as `compose.yml` — that's a specific LAN/VPN
address for wherever Ollama runs, not a Kubernetes service; it must be routable from the k3s node for
n8n's Ollama-backed nodes to work.
