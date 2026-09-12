import subprocess
from typing import Optional


MAX_OUTPUT = 20000


def run_kubectl(args: list[str]) -> str:
    """
    Run a READ-ONLY kubectl command.
    """

    blocked = {
        "apply",
        "create",
        "delete",
        "patch",
        "replace",
        "edit",
        "scale",
        "cordon",
        "uncordon",
        "drain",
        "rollout",
        "exec",
        "cp",
        "label",
        "annotate",
        "taint",
    }

    if not args:
        return "ERROR: Empty kubectl command."

    if args[0] in blocked:
        return f"BLOCKED: kubectl {args[0]} is not allowed."

    try:
        result = subprocess.run(
            ["kubectl"] + args,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = result.stdout

        if result.stderr:
            output += "\n" + result.stderr

        if len(output) > MAX_OUTPUT:
            output = output[:MAX_OUTPUT] + "\n...[output truncated]"

        return output

    except subprocess.TimeoutExpired:
        return "ERROR: kubectl command timed out."

    except Exception as exc:
        return f"ERROR: {exc}"


def get_pods(namespace: Optional[str] = None) -> str:
    """
    Get Kubernetes pods.
    """

    args = ["get", "pods"]

    if namespace:
        args += ["-n", namespace]
    else:
        args += ["-A"]

    args += ["-o", "wide"]

    return run_kubectl(args)


def get_deployments(namespace: Optional[str] = None) -> str:
    """
    Get Kubernetes deployments.
    """

    args = ["get", "deployments"]

    if namespace:
        args += ["-n", namespace]
    else:
        args += ["-A"]

    return run_kubectl(args)


def get_services(namespace: Optional[str] = None) -> str:
    """
    Get Kubernetes services.
    """

    args = ["get", "services"]

    if namespace:
        args += ["-n", namespace]
    else:
        args += ["-A"]

    return run_kubectl(args)


def get_events(namespace: Optional[str] = None) -> str:
    """
    Get Kubernetes events.
    """

    args = ["get", "events"]

    if namespace:
        args += ["-n", namespace]
    else:
        args += ["-A"]

    args += ["--sort-by=.lastTimestamp"]

    return run_kubectl(args)


def describe_pod(name: str, namespace: str) -> str:
    """
    Describe a Kubernetes pod.
    """

    return run_kubectl(
        [
            "describe",
            "pod",
            name,
            "-n",
            namespace,
        ]
    )


def get_logs(
    pod: str,
    namespace: str,
    container: Optional[str] = None,
    tail: int = 200,
) -> str:
    """
    Get logs from a Kubernetes pod.
    """

    args = [
        "logs",
        pod,
        "-n",
        namespace,
        f"--tail={tail}",
    ]

    if container:
        args += ["-c", container]

    return run_kubectl(args)
