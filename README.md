# AI-Powered DevSecOps Platform

A local, privacy-first AI-powered DevSecOps platform for investigating, securing, and operating Kubernetes environments.

The platform uses **Qwen3-Coder**, **Ollama**, Kubernetes tooling, security scanners, GitOps, and policy enforcement to help DevOps and security engineers detect issues, investigate incidents, analyze vulnerabilities, and recommend safe remediation actions.

The project is designed to demonstrate practical experience across:

* Kubernetes administration and troubleshooting
* Cloud-native infrastructure
* CI/CD automation
* Infrastructure as Code
* Container and Kubernetes security
* Observability and incident response
* GitOps-based remediation
* AI-assisted operations
* Secure automation with human approval

AI is used as an assistant, not as an unrestricted production operator.

## Project Goals

The goal is to build an end-to-end DevSecOps platform that can:

1. Monitor Kubernetes workloads and infrastructure
2. Investigate application and platform failures
3. Analyze logs, events, metrics, and traces
4. Detect container, dependency, IaC, and Kubernetes vulnerabilities
5. Correlate security and operational findings
6. Recommend remediation steps
7. Generate GitHub issues or pull requests
8. Enforce policy before changes are deployed
9. Deploy approved changes through GitOps
10. Maintain auditability and human control

## Architecture

```text
                              Developer / Operator
                                      │
                                      ▼
                         Open WebUI / Chat Interface
                                      │
                                      ▼
                         AI DevSecOps Orchestrator
                              Python / FastAPI
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
          Kubernetes Agent      Security Agent       CI/CD Agent
                 │                    │                    │
                 ▼                    ▼                    ▼
              kubectl              Trivy              GitHub API
              Helm                 Kubescape           CI Pipelines
              Kustomize            Checkov              Pull Requests
                                   Semgrep
                                   Wazuh
                 │                    │                    │
                 └────────────────────┼────────────────────┘
                                      ▼
                              MCP Tool Layer
                                      │
                                      ▼
                              Qwen3-Coder
                                Ollama
                                      │
                                      ▼
                         Local M2 Max Inference Server

                                      │
                                      ▼
                         Recommendations / Findings
                                      │
                                      ▼
                         Human Approval and Review
                                      │
                                      ▼
                         GitHub / GitOps Repository
                                      │
                                      ▼
                         Argo CD or Flux
                                      │
                                      ▼
                              Kubernetes Cluster
```

## Core Design Principle

> AI should have enough access to understand the problem, but not enough access to become the problem.

The platform follows this workflow:

```text
Observe
   ↓
Collect Evidence
   ↓
Analyze
   ↓
Correlate
   ↓
Recommend
   ↓
Human Review
   ↓
Approved Change
   ↓
GitOps Deployment
   ↓
Verify
```

The AI does not directly modify production infrastructure.

## Key Capabilities

### Kubernetes Operations

* Investigate Pods, Deployments, Services, Nodes, Jobs, and Events
* Analyze CrashLoopBackOff, ImagePullBackOff, Pending, and OOMKilled states
* Inspect Kubernetes logs and container restart patterns
* Identify scheduling, networking, storage, and configuration issues
* Analyze Helm releases and Kustomize overlays
* Review resource requests, limits, probes, and autoscaling configuration
* Compare desired state with live cluster state
* Generate troubleshooting reports

### DevSecOps Security

* Scan container images for vulnerabilities
* Scan Kubernetes manifests and Helm charts
* Scan Terraform and Infrastructure as Code
* Detect secrets in source code and configuration
* Analyze dependency vulnerabilities
* Review RBAC permissions and excessive privileges
* Detect insecure Kubernetes configurations
* Analyze admission policy violations
* Correlate security findings with running workloads
* Prioritize findings based on severity and runtime exposure

### CI/CD and GitOps

* Investigate failed CI/CD pipelines
* Analyze build and deployment logs
* Review pull requests for security and operational risks
* Generate remediation pull requests
* Validate manifests before deployment
* Enforce policy gates
* Deploy only approved changes through GitOps
* Verify rollout health after deployment
* Provide deployment evidence and audit history

### Observability and Incident Response

* Correlate logs, metrics, events, and traces
* Investigate service availability issues
* Analyze alert context
* Identify likely root causes
* Generate incident timelines
* Recommend rollback or mitigation steps
* Create incident reports
* Integrate with monitoring and security platforms

## Example Kubernetes Investigation

```text
User:
Why is payments-api failing in production?

Agent:
1. Inspect Deployment status
2. Inspect Pod conditions
3. Review container restart count
4. Analyze recent Kubernetes Events
5. Inspect application logs
6. Check Service and Endpoint configuration
7. Review resource limits and probes
8. Correlate the findings with recent deployments

Diagnosis:
payments-api is in CrashLoopBackOff.
The application cannot connect to the PostgreSQL service.
The failure started after the latest deployment.
The PostgreSQL Service has no healthy endpoints.

Risk:
The payments workload is unavailable, which may affect transaction processing.

Recommendation:
1. Verify PostgreSQL Pod health.
2. Check PostgreSQL Service selectors.
3. Review the latest deployment change.
4. Create a pull request if a configuration correction is required.

Action:
No cluster modification was performed.
```

## Example Security Investigation

```text
User:
Which vulnerabilities require immediate attention?

Agent:
1. Collect image scan results
2. Identify workloads using affected images
3. Check vulnerability severity and exploitability
4. Determine whether the vulnerable package is reachable
5. Check whether the workload is internet-facing
6. Correlate findings with runtime permissions

Finding:
The checkout-api image contains a critical vulnerability.
The workload is exposed through an external Ingress and runs with excessive permissions.

Recommendation:
1. Upgrade the affected dependency.
2. Rebuild and rescan the image.
3. Remove unnecessary Linux capabilities.
4. Apply a restricted security context.
5. Create a pull request with the proposed changes.

Action:
No production change was applied automatically.
```

## Security and Control Model

The platform uses least privilege, separation of duties, and explicit approval gates.

### Read-Only Kubernetes Operations

The investigation agent may use:

```text
kubectl get
kubectl describe
kubectl logs
kubectl events
kubectl top
helm list
helm status
```

### Restricted Operations

The agent must not directly execute:

```text
kubectl delete
kubectl apply
kubectl patch
kubectl exec
kubectl scale
kubectl edit
helm upgrade
helm uninstall
```

### Approved Remediation Workflow

```text
AI Recommendation
        ↓
Evidence and Risk Review
        ↓
GitHub Issue or Pull Request
        ↓
Automated Tests and Security Scans
        ↓
Policy Validation
        ↓
Human Approval
        ↓
GitOps Synchronization
        ↓
Kubernetes Deployment
        ↓
Post-Deployment Verification
```

## Security Boundaries

The platform should enforce the following controls:

* Read-only Kubernetes service accounts for investigation
* Separate identities for scanning and deployment
* Namespace-level access where possible
* No unrestricted cluster-admin credentials
* Network restrictions between components
* Secrets stored outside source code
* Audit logging for all tool calls
* Command allowlists and deny lists
* Input validation for AI-generated commands
* Human approval for infrastructure changes
* Policy enforcement before deployment
* Rollback procedures for failed changes
* Full traceability from finding to remediation

## Technology Stack

| Area                   | Technology                      |
| ---------------------- | ------------------------------- |
| AI Model               | Qwen3-Coder                     |
| Model Runtime          | Ollama                          |
| AI Interface           | Open WebUI                      |
| Agent API              | Python / FastAPI                |
| Tool Protocol          | Model Context Protocol          |
| Container Runtime      | Docker                          |
| Orchestration          | Kubernetes                      |
| Kubernetes CLI         | kubectl                         |
| Packaging              | Helm                            |
| Configuration          | Kustomize                       |
| GitOps                 | Argo CD or Flux                 |
| CI/CD                  | GitHub Actions                  |
| Image Scanning         | Trivy                           |
| Kubernetes Security    | Kubescape                       |
| IaC Scanning           | Checkov                         |
| SAST                   | Semgrep                         |
| Secret Scanning        | Gitleaks                        |
| Policy Engine          | Kyverno or Open Policy Agent    |
| Runtime Security       | Falco                           |
| Security Monitoring    | Wazuh                           |
| Metrics                | Prometheus                      |
| Dashboards             | Grafana                         |
| Logs                   | Loki                            |
| Tracing                | OpenTelemetry                   |
| Infrastructure as Code | Terraform                       |
| Cloud Platform         | AWS, Azure, or GCP              |
| Deployment Model       | Local, private, and cloud-ready |

## Repository Structure

```text
ai-devsecops-platform/
├── README.md
├── LICENSE
├── docs/
│   ├── architecture.md
│   ├── security-model.md
│   ├── threat-model.md
│   ├── incident-response.md
│   └── runbooks/
├── agent/
│   ├── api/
│   ├── orchestration/
│   ├── prompts/
│   ├── policies/
│   └── models/
├── mcp-servers/
│   ├── kubernetes/
│   ├── security/
│   ├── github/
│   ├── observability/
│   └── terraform/
├── kubernetes/
│   ├── namespaces/
│   ├── rbac/
│   ├── network-policies/
│   ├── policies/
│   └── workloads/
├── helm/
│   └── ai-devsecops-agent/
├── gitops/
│   ├── applications/
│   ├── environments/
│   └── policies/
├── security/
│   ├── trivy/
│   ├── kubescape/
│   ├── checkov/
│   ├── semgrep/
│   └── gitleaks/
├── terraform/
│   ├── modules/
│   └── environments/
├── observability/
│   ├── prometheus/
│   ├── grafana/
│   ├── loki/
│   └── opentelemetry/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── security/
└── .github/
    └── workflows/
```

## Local AI Inference

The local model runs on an M2 Max through Ollama.

```text
MacBook Air
    │
    │ Claude Code / Open WebUI / Agent Client
    │
    ▼
MacBook Pro M2 Max
    │
    │ Ollama API
    ▼
Qwen3-Coder
```

Example environment configuration:

```bash
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
export ANTHROPIC_BASE_URL=http://10.21.214.137:11434
export ANTHROPIC_MODEL=qwen3-coder:30b
```

The local inference architecture provides:

* Private source-code analysis
* No mandatory external LLM API
* Reduced data exposure
* Offline or isolated-environment support
* Centralized model hosting
* Reproducible development workflows

## DevSecOps Pipeline

```text
Developer Commit
       ↓
Pull Request
       ↓
Unit Tests
       ↓
SAST
       ↓
Dependency Scan
       ↓
Secret Scan
       ↓
Container Build
       ↓
Container Image Scan
       ↓
IaC and Kubernetes Manifest Scan
       ↓
Policy Validation
       ↓
Image Signing
       ↓
Registry Push
       ↓
GitOps Update
       ↓
Argo CD / Flux
       ↓
Kubernetes Deployment
       ↓
Runtime Monitoring
       ↓
AI-Assisted Verification
```

## Policy and Compliance

The platform should support policy checks such as:

* Containers must not run as root
* Privileged containers are prohibited
* Host networking is prohibited unless explicitly approved
* Images must use approved registries
* Images must not contain critical vulnerabilities
* Kubernetes workloads must define resource requests and limits
* Network policies must be present
* Secrets must not be stored in Git
* RBAC permissions must follow least privilege
* Production changes require pull-request approval
* Deployments must be traceable to a Git commit
* Images must be signed and verified

## Observability Workflow

```text
Metrics ───────┐
Logs ──────────┼──► Correlation Layer ───► AI Investigation
Events ────────┤
Traces ────────┘
                                      │
                                      ▼
                              Root Cause Analysis
                                      │
                                      ▼
                              Recommended Action
```

The agent should use observability data as evidence rather than relying only on model-generated assumptions.

## Incident Response Workflow

```text
Alert
  ↓
Incident Classification
  ↓
Evidence Collection
  ↓
Impact Assessment
  ↓
Root Cause Analysis
  ↓
Mitigation Recommendation
  ↓
Human Approval
  ↓
Remediation
  ↓
Verification
  ↓
Post-Incident Report
```

The platform should preserve:

* Alert details
* Relevant logs and events
* Timeline of investigation
* Commands executed
* AI reasoning summary
* Human decisions
* Remediation changes
* Verification results

## Roadmap

### Phase 1 — Local AI Assistant ✅

* Run Qwen3-Coder through Ollama
* Integrate Open WebUI
* Validate local model access
* Establish private inference architecture

### Phase 2 — Kubernetes Investigation 🚧

* Implement read-only Kubernetes tools
* Add Pod, Deployment, Service, Node, and Event inspection
* Add log analysis
* Add namespace and RBAC controls
* Generate structured investigation reports

### Phase 3 — MCP Tool Layer

* Implement Kubernetes MCP server
* Implement security scanning MCP server
* Implement GitHub MCP server
* Implement observability MCP server
* Add tool authentication and authorization
* Add tool-call audit logging

### Phase 4 — Security Scanning

* Integrate Trivy
* Integrate Kubescape
* Integrate Checkov
* Integrate Semgrep
* Integrate Gitleaks
* Normalize findings into a common schema
* Add severity and risk prioritization

### Phase 5 — CI/CD and GitOps

* Build GitHub Actions workflows
* Add security gates
* Add image signing and verification
* Deploy Argo CD or Flux
* Implement environment promotion
* Add automated rollback verification

### Phase 6 — Observability and Incident Response

* Deploy Prometheus and Grafana
* Deploy Loki and OpenTelemetry
* Integrate alerting
* Add Wazuh findings analysis
* Generate incident timelines
* Create operational runbooks

### Phase 7 — AI-Assisted Remediation

* Generate remediation recommendations
* Create GitHub issues automatically
* Generate pull requests with evidence
* Run tests and security scans on generated changes
* Require human approval
* Deploy only through GitOps
* Verify post-deployment health

### Phase 8 — Cloud and Enterprise Readiness

* Add AWS, Azure, or GCP integration
* Add Terraform analysis
* Add multi-cluster support
* Add tenant and namespace isolation
* Add centralized audit reporting
* Add compliance dashboards
* Add disaster recovery procedures

## TODO

The following items are planned to strengthen the project and demonstrate broader DevSecOps, Kubernetes, cloud, security, and automation experience.

### Kubernetes

* [ ] Build a local Kubernetes lab using kind, k3d, or Minikube
* [ ] Deploy a multi-service sample application
* [ ] Configure namespaces and resource quotas
* [ ] Implement read-only service accounts
* [ ] Add NetworkPolicies
* [ ] Configure Ingress and TLS
* [ ] Add readiness, liveness, and startup probes
* [ ] Configure Horizontal Pod Autoscaler
* [ ] Test rolling updates and rollback scenarios
* [ ] Document Kubernetes troubleshooting runbooks

### Kubernetes Security

* [ ] Implement Pod Security Standards
* [ ] Add Kyverno or OPA Gatekeeper policies
* [ ] Prevent privileged containers
* [ ] Enforce non-root execution
* [ ] Restrict hostPath and host networking
* [ ] Enforce approved image registries
* [ ] Add RBAC least-privilege validation
* [ ] Add Kubernetes audit logging
* [ ] Integrate Kubescape
* [ ] Integrate Falco runtime detection

### Container and Supply Chain Security

* [ ] Build minimal container images
* [ ] Add multi-stage Docker builds
* [ ] Scan images with Trivy
* [ ] Add SBOM generation
* [ ] Sign images with Cosign
* [ ] Verify signatures during deployment
* [ ] Add dependency scanning
* [ ] Add Gitleaks secret scanning
* [ ] Add vulnerability severity gates
* [ ] Document vulnerability exception handling

### Infrastructure as Code

* [ ] Create Terraform modules for the platform
* [ ] Add remote state configuration
* [ ] Add Terraform formatting and validation
* [ ] Add Checkov scanning
* [ ] Add Terraform plan review
* [ ] Add drift detection
* [ ] Add cloud networking configuration
* [ ] Add IAM least-privilege controls
* [ ] Document infrastructure provisioning and destruction

### CI/CD

* [ ] Create GitHub Actions workflows
* [ ] Add unit and integration tests
* [ ] Add SAST with Semgrep
* [ ] Add dependency scanning
* [ ] Add container image scanning
* [ ] Add Kubernetes manifest validation
* [ ] Add Terraform validation
* [ ] Add policy checks
* [ ] Add artifact retention controls
* [ ] Add deployment approval gates
* [ ] Add rollback testing

### GitOps

* [ ] Deploy Argo CD or Flux
* [ ] Create development, staging, and production environments
* [ ] Implement Kustomize overlays or Helm values
* [ ] Configure repository-based deployments
* [ ] Add environment promotion
* [ ] Add sync policies
* [ ] Add drift detection
* [ ] Add rollback procedures
* [ ] Document GitOps operating model

### Observability

* [ ] Deploy Prometheus
* [ ] Create Grafana dashboards
* [ ] Deploy Loki
* [ ] Add OpenTelemetry instrumentation
* [ ] Configure alert rules
* [ ] Add service-level indicators
* [ ] Define service-level objectives
* [ ] Correlate logs, metrics, traces, and events
* [ ] Create operational dashboards
* [ ] Document alert response procedures

### Security Operations

* [ ] Integrate Wazuh findings
* [ ] Normalize security findings
* [ ] Add finding deduplication
* [ ] Add risk-based prioritization
* [ ] Map findings to affected workloads
* [ ] Add incident classification
* [ ] Create security investigation runbooks
* [ ] Generate incident reports
* [ ] Add audit evidence collection
* [ ] Document incident escalation procedures

### AI Agent

* [ ] Implement structured tool schemas
* [ ] Add MCP servers
* [ ] Add command allowlists
* [ ] Add tool authorization
* [ ] Add prompt-injection defenses
* [ ] Add sensitive-data redaction
* [ ] Add model output validation
* [ ] Add confidence scoring
* [ ] Add evidence citations
* [ ] Add investigation session history
* [ ] Add human approval workflows
* [ ] Add AI tool-call audit logs
* [ ] Evaluate model accuracy against known incidents
* [ ] Measure false positives and false negatives
* [ ] Add regression tests for prompts and tools

### Cloud and Platform Engineering

* [ ] Deploy the platform to AWS, Azure, or GCP
* [ ] Add managed Kubernetes support
* [ ] Configure cloud IAM
* [ ] Add private networking
* [ ] Add secrets management
* [ ] Add centralized logging
* [ ] Add backup and disaster recovery
* [ ] Add multi-cluster support
* [ ] Document high-availability architecture
* [ ] Document cost and capacity management

### Documentation and Demonstration

* [ ] Add architecture diagrams
* [ ] Add threat model
* [ ] Add security control matrix
* [ ] Add deployment guide
* [ ] Add troubleshooting guide
* [ ] Add incident-response examples
* [ ] Add CI/CD screenshots
* [ ] Add Grafana dashboard screenshots
* [ ] Add sample vulnerability reports
* [ ] Add sample AI investigation reports
* [ ] Add demo videos
* [ ] Add performance benchmarks
* [ ] Add a project portfolio summary
* [ ] Map completed features to relevant job requirements

## Success Criteria

The project will be considered successful when it can:

* Investigate a Kubernetes incident using read-only access
* Identify likely root causes from multiple evidence sources
* Detect vulnerabilities in images and manifests
* Analyze Terraform and CI/CD security issues
* Generate a remediation pull request
* Validate the proposed change automatically
* Require human approval before deployment
* Deploy through GitOps
* Verify application health after deployment
* Produce an auditable investigation and remediation record
* Operate with a local private AI model
* Demonstrate secure, controlled, and explainable automation

## Project Positioning

This project demonstrates an AI-assisted DevSecOps operating model rather than a simple Kubernetes chatbot.

It combines:

* Kubernetes operations
* Platform engineering
* Cloud infrastructure
* Infrastructure as Code
* CI/CD
* GitOps
* Container security
* Kubernetes security
* Vulnerability management
* Observability
* Incident response
* AI agents
* MCP-based tool integration
* Human-in-the-loop automation

The intended outcome is a secure platform where AI accelerates investigation and remediation while engineering teams retain control over production changes.

## Final Principle

```text
AI observes.
AI analyzes.
AI explains.
AI recommends.
Humans approve.
GitOps deploys.
Policy enforces.
Monitoring verifies.
```

This project is intended to showcase practical experience building a secure, automated, and AI-assisted Kubernetes DevSecOps platform suitable for modern cloud-native engineering environments.

### Application URL

```text
# hostentry
10.21.209.71 n8n.adnlocal.com openwebui.adnlocal.com

# n8n
URL : https://n8n.adnlocal.com/
Username : jignesh.makwana@adnovum.sg
Password : Welcome#1

# openwebui
URL : https://openwebui.adnlocal.com
Username : jignesh.makwana@adnovum.sg
Password : Welcome#1

```
