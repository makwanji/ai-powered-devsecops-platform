# AI-Powered DevOps Agent

# AI-Powered Kubernetes DevOps Agent

A local, privacy-first AI Agent that uses **Qwen3-Coder** to investigate Kubernetes environments and assist DevOps engineers with troubleshooting.

The project demonstrates how **AI Agents can augment DevOps workflows** while maintaining explicit security boundaries and operational control.

## Architecture

```text
                    Open WebUI
                 AI Agent Interface
                        │
                        ▼
              Kubernetes Troubleshooting
                       Agent
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
        Qwen3-Coder             kubectl
        (Local LLM)                │
             │                     ▼
             │                 Kubernetes
             │
             ▼
        MacBook Pro
        M2 Max / Ollama
```

## Key Capabilities

* 🔎 Investigate Kubernetes workloads using natural language
* 🧠 Use a locally hosted coding model for reasoning and analysis
* 📋 Inspect Pods, Deployments, Services, Nodes and Events
* 📜 Analyze Kubernetes logs and identify potential root causes
* 💬 Access the Agent through Open WebUI
* 🔒 No external LLM API required
* 🌐 Designed to operate in an isolated / offline environment

## Security & Control

The Agent follows a **read-only by design** approach.

### Allowed

```text
kubectl get
kubectl describe
kubectl logs
kubectl events
```

### Not allowed

```text
kubectl delete
kubectl apply
kubectl patch
kubectl exec
kubectl scale
```

The Agent therefore **cannot directly modify the Kubernetes environment**.

This separation is intentional:

```text
AI
 │
 ▼
Observe
 │
 ▼
Analyze
 │
 ▼
Recommend
 │
 ▼
Human Decision
```

rather than:

```text
AI ───────► Production
```

## AI + DevOps Concept

The goal is not to replace the DevOps engineer.

The Agent acts as an **AI troubleshooting assistant** that can correlate Kubernetes information and reduce the time required to identify issues.

Example:

```text
User:
Why is payments-api failing?

Agent:
1. Inspect Pod status
2. Inspect Deployment
3. Inspect recent Events
4. Analyze container logs
5. Correlate the findings

Diagnosis:
payments-api is in CrashLoopBackOff.
The container is failing because it cannot connect
to the PostgreSQL service.

Recommendation:
Verify PostgreSQL availability and service configuration.
```

## Technology Stack

| Component         | Technology       |
| ----------------- | ---------------- |
| AI Model          | Qwen3-Coder      |
| Model Runtime     | Ollama           |
| AI Interface      | Open WebUI       |
| Agent             | Python / FastAPI |
| Infrastructure    | Kubernetes       |
| Container Runtime | Docker           |
| Kubernetes Access | kubectl          |
| Deployment Model  | Local / Private  |

## Roadmap

### Phase 1 — AI Assistant ✅

Local LLM + Open WebUI.

### Phase 2 — Kubernetes Agent 🚧

Controlled Kubernetes investigation and troubleshooting.

### Phase 3 — MCP

Replace direct tool integration with a standardized **Model Context Protocol (MCP)** tool layer.

### Phase 4 — AI-Assisted Remediation

Generate remediation actions without allowing the Agent to directly modify infrastructure.

```text
Detection
    ↓
AI Investigation
    ↓
Root Cause
    ↓
Recommended Fix
    ↓
GitHub Issue / Pull Request
    ↓
Human Approval
    ↓
GitOps / Ansible
    ↓
Kubernetes
```

### Phase 5 — DevSecOps Agents

Extend the architecture to:

* Security vulnerability investigation
* Wazuh findings analysis
* Terraform analysis
* Cloud infrastructure troubleshooting
* CI/CD failure analysis
* Automated remediation through GitOps

## Design Principle

> **AI should have enough access to understand the problem, but not enough access to become the problem.**

This project explores a practical approach to **AI-assisted DevOps with controlled autonomy, local inference, and human approval**.
