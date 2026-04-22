from __future__ import annotations

import random
import string
from dataclasses import dataclass, field


@dataclass
class ContextInfo:
    context: str = "minikube"
    cluster: str = "minikube-cluster"
    user: str = "minikube-user"
    namespace: str = "default"
    k8s_version: str = "v1.32.0"
    cpu_usage: str = "42%"
    mem_usage: str = "61%"


@dataclass
class PodRow:
    namespace: str
    name: str
    pf: str
    ready: str
    status: str
    restarts: int
    cpu: str
    cpu_pct_r: str
    cpu_pct_l: str
    mem: str
    mem_pct_r: str
    mem_pct_l: str
    ip: str
    node: str
    age: str


NAMESPACES = (
    "default",
    "platform-system",
    "data-pipelines",
    "monitoring",
    "kube-system",
    "istio-system",
    "cert-manager",
    "ingress-nginx",
)

POD_PREFIXES = {
    "default": ("api-gateway", "web-frontend", "auth-service", "scheduler"),
    "platform-system": ("platform-api", "controller-mgr", "platform-worker", "event-bus"),
    "data-pipelines": ("spark-executor", "airflow-sched", "airflow-worker", "pipeline-runner"),
    "monitoring": ("prometheus", "grafana", "alertmanager", "thanos-compactor"),
    "kube-system": ("coredns", "etcd", "kube-apiserver", "kube-proxy", "kube-scheduler"),
    "istio-system": ("istiod", "istio-ingress", "istio-cni"),
    "cert-manager": ("cert-manager", "cert-manager-webhook", "cert-manager-cainjector"),
    "ingress-nginx": ("nginx-ingress-controller", "nginx-default-backend"),
}

STATUSES = ("Running",) * 7 + ("Completed", "Pending", "CrashLoopBackOff", "ContainerCreating")

NODES = (
    "node-pool-a-1",
    "node-pool-a-2",
    "node-pool-a-3",
    "node-pool-b-1",
    "node-pool-b-2",
    "node-pool-b-3",
)


def _rand_suffix() -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=5))


def _rand_cpu() -> str:
    cores = random.choice([1, 2, 4, 8])
    m = random.randint(1, cores * 1000)
    if m >= 1000:
        return f"{m / 1000:.1f}"
    return f"{m}m"


def _rand_mem() -> str:
    return f"{random.randint(32, 8192)}Mi"


def _rand_pct() -> str:
    return f"{random.randint(0, 100)}%"


def _rand_ip() -> str:
    return f"10.244.{random.randint(0, 3)}.{random.randint(1, 254)}"


def _rand_age() -> str:
    units = random.choice(["m", "h", "d"])
    if units == "m":
        return f"{random.randint(1, 59)}m"
    if units == "h":
        h = random.randint(1, 72)
        d, h = divmod(h, 24)
        return f"{d}d{h}h" if d else f"{h}h"
    d = random.randint(1, 30)
    return f"{d}d"


def _ready(status: str) -> str:
    if status in ("Running", "Completed"):
        total = random.choice([1, 2, 3])
        return f"{total}/{total}"
    if status == "CrashLoopBackOff":
        return f"0/{random.randint(1, 2)}"
    return f"0/{random.randint(1, 2)}"


def generate_pods(count: int = 60) -> list[PodRow]:
    rows: list[PodRow] = []
    for _ in range(count):
        ns = random.choice(NAMESPACES)
        prefix = random.choice(POD_PREFIXES.get(ns, POD_PREFIXES["default"]))
        name = f"{prefix}-{_rand_suffix()}"
        status = random.choice(STATUSES)
        rows.append(
            PodRow(
                namespace=ns,
                name=name,
                pf="●" if random.random() < 0.1 else "",
                ready=_ready(status),
                status=status,
                restarts=random.randint(0, 12),
                cpu=_rand_cpu(),
                cpu_pct_r=_rand_pct(),
                cpu_pct_l=_rand_pct(),
                mem=_rand_mem(),
                mem_pct_r=_rand_pct(),
                mem_pct_l=_rand_pct(),
                ip=_rand_ip(),
                node=random.choice(NODES),
                age=_rand_age(),
            )
        )
    return rows


def generate_context() -> ContextInfo:
    return ContextInfo()


ALL_COLUMNS = (
    "NAMESPACE",
    "NAME",
    "PF",
    "READY",
    "STATUS",
    "RESTARTS",
    "CPU",
    "%CPU/R",
    "%CPU/L",
    "MEM",
    "%MEM/R",
    "%MEM/L",
    "IP",
    "NODE",
    "AGE",
)