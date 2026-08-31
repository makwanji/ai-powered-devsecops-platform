import os
from typing import Optional

from fastmcp import FastMCP
from kubernetes import client, config
from kubernetes.client.rest import ApiException


KUBECONFIG = os.getenv(
    "KUBECONFIG",
    "/app/.kube/config",
)

mcp = FastMCP(
    name="Kubernetes MCP Server"
)


def load_kube_config():
    """
    Load Kubernetes configuration from the mounted kubeconfig.
    """
    config.load_kube_config(config_file=KUBECONFIG)


def get_core_api():
    load_kube_config()
    return client.CoreV1Api()


def get_apps_api():
    load_kube_config()
    return client.AppsV1Api()


@mcp.tool
def get_nodes() -> str:
    """Get all Kubernetes nodes and their status."""
    try:
        v1 = get_core_api()
        nodes = v1.list_node()

        if not nodes.items:
            return "No Kubernetes nodes found."

        result = []

        for node in nodes.items:
            name = node.metadata.name
            version = node.status.node_info.kubelet_version

            status = "Unknown"

            if node.status.conditions:
                for condition in node.status.conditions:
                    if condition.type == "Ready":
                        status = condition.status
                        break

            roles = []

            labels = node.metadata.labels or {}

            for label in labels:
                if label.startswith("node-role.kubernetes.io/"):
                    roles.append(label.split("/", 1)[1])

            if not roles:
                roles.append("worker")

            result.append(
                f"Node: {name}\n"
                f"Status: {status}\n"
                f"Roles: {', '.join(roles)}\n"
                f"Kubernetes Version: {version}"
            )

        return "\n\n".join(result)

    except ApiException as e:
        return f"Kubernetes API error: {e}"


@mcp.tool
def get_namespaces() -> str:
    """List all Kubernetes namespaces."""
    try:
        v1 = get_core_api()
        namespaces = v1.list_namespace()

        if not namespaces.items:
            return "No namespaces found."

        return "\n".join(
            f"- {ns.metadata.name}"
            for ns in namespaces.items
        )

    except ApiException as e:
        return f"Kubernetes API error: {e}"


@mcp.tool
def get_pods(
    namespace: Optional[str] = None,
) -> str:
    """
    List Kubernetes pods.

    If namespace is provided, only pods in that namespace are returned.
    Otherwise, pods from all namespaces are returned.
    """
    try:
        v1 = get_core_api()

        if namespace:
            pods = v1.list_namespaced_pod(namespace)
        else:
            pods = v1.list_pod_for_all_namespaces()

        if not pods.items:
            return "No pods found."

        result = []

        for pod in pods.items:
            result.append(
                f"Namespace: {pod.metadata.namespace}\n"
                f"Pod: {pod.metadata.name}\n"
                f"Status: {pod.status.phase}\n"
                f"Node: {pod.spec.node_name or 'Not scheduled'}"
            )

        return "\n\n".join(result)

    except ApiException as e:
        return f"Kubernetes API error: {e}"


@mcp.tool
def get_deployments(
    namespace: Optional[str] = None,
) -> str:
    """
    List Kubernetes deployments.

    If namespace is provided, only deployments in that namespace are returned.
    Otherwise, deployments from all namespaces are returned.
    """
    try:
        apps = get_apps_api()

        if namespace:
            deployments = apps.list_namespaced_deployment(namespace)
        else:
            deployments = apps.list_deployment_for_all_namespaces()

        if not deployments.items:
            return "No deployments found."

        result = []

        for deployment in deployments.items:
            desired = deployment.spec.replicas or 0
            ready = deployment.status.ready_replicas or 0

            result.append(
                f"Namespace: {deployment.metadata.namespace}\n"
                f"Deployment: {deployment.metadata.name}\n"
                f"Ready: {ready}/{desired}"
            )

        return "\n\n".join(result)

    except ApiException as e:
        return f"Kubernetes API error: {e}"


@mcp.tool
def get_services(
    namespace: Optional[str] = None,
) -> str:
    """
    List Kubernetes services.

    If namespace is provided, only services in that namespace are returned.
    Otherwise, services from all namespaces are returned.
    """
    try:
        v1 = get_core_api()

        if namespace:
            services = v1.list_namespaced_service(namespace)
        else:
            services = v1.list_service_for_all_namespaces()

        if not services.items:
            return "No services found."

        result = []

        for service in services.items:
            ports = []

            if service.spec.ports:
                for port in service.spec.ports:
                    ports.append(
                        f"{port.port}/{port.protocol}"
                    )

            result.append(
                f"Namespace: {service.metadata.namespace}\n"
                f"Service: {service.metadata.name}\n"
                f"Type: {service.spec.type}\n"
                f"ClusterIP: {service.spec.cluster_ip}\n"
                f"Ports: {', '.join(ports)}"
            )

        return "\n\n".join(result)

    except ApiException as e:
        return f"Kubernetes API error: {e}"


@mcp.tool
def get_events(
    namespace: Optional[str] = None,
) -> str:
    """
    Get Kubernetes events.

    If namespace is provided, events from that namespace are returned.
    Otherwise, events from all namespaces are returned.
    """
    try:
        v1 = get_core_api()

        if namespace:
            events = v1.list_namespaced_event(namespace)
        else:
            events = v1.list_event_for_all_namespaces()

        if not events.items:
            return "No Kubernetes events found."

        result = []

        sorted_events = sorted(
            events.items,
            key=lambda e: e.last_timestamp or e.event_time or e.first_timestamp,
            reverse=True,
        )

        for event in sorted_events[:100]:
            result.append(
                f"Namespace: {event.metadata.namespace}\n"
                f"Reason: {event.reason}\n"
                f"Type: {event.type}\n"
                f"Message: {event.message}\n"
                f"Object: {event.involved_object.kind}/"
                f"{event.involved_object.name}"
            )

        return "\n\n".join(result)

    except ApiException as e:
        return f"Kubernetes API error: {e}"


@mcp.tool
def get_pod_logs(
    pod_name: str,
    namespace: str = "default",
    tail_lines: int = 100,
) -> str:
    """
    Get logs from a Kubernetes pod.

    pod_name: Kubernetes pod name.
    namespace: Kubernetes namespace.
    tail_lines: Number of recent log lines to return.
    """
    try:
        v1 = get_core_api()

        # Prevent accidentally requesting huge log output.
        tail_lines = max(1, min(tail_lines, 1000))

        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=tail_lines,
        )

        return logs or "Pod has no logs."

    except ApiException as e:
        return f"Kubernetes API error: {e}"


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8001,
    )
