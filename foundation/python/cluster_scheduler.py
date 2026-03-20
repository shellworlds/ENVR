from dataclasses import dataclass


@dataclass
class Node:
    name: str
    cpu_free: int
    ram_free_gb: int


def pick_node(nodes: list[Node], cpu_req: int, ram_req: int) -> str:
    ranked = sorted(nodes, key=lambda n: (n.cpu_free, n.ram_free_gb), reverse=True)
    for n in ranked:
        if n.cpu_free >= cpu_req and n.ram_free_gb >= ram_req:
            return n.name
    return "NO_NODE_AVAILABLE"


if __name__ == "__main__":
    pool = [Node("qnode-a", 32, 64), Node("qnode-b", 12, 24), Node("qnode-c", 48, 96)]
    print(pick_node(pool, 16, 32))
