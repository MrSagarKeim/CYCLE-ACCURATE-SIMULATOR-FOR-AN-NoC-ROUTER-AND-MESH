import sys
from typing import List, Tuple

from models import ProcessingElement, Router, connect, logger, RoutingType


def generate_mesh():
    ## Mesh
    # 2 3
    # 0 1

    r0 = Router(id=0)
    r1 = Router(id=1)
    r2 = Router(id=2)
    r3 = Router(id=3)

    pe0 = ProcessingElement(id=0)
    pe1 = ProcessingElement(id=1)
    pe2 = ProcessingElement(id=2)
    pe3 = ProcessingElement(id=3)

    connect(r0, "east", r1, "west")
    connect(r2, "east", r3, "west")
    connect(r2, "south", r0, "north")
    connect(r3, "south", r1, "north")

    connect(r0, "pe", pe0, "router")
    connect(r1, "pe", pe1, "router")
    connect(r2, "pe", pe2, "router")
    connect(r3, "pe", pe3, "router")

    cycleables: List[Router | ProcessingElement] = [r0, r1, r2, r3, pe0, pe1, pe2, pe3]
    return cycleables


def run_simulation(
    cycleables: List[Router | ProcessingElement],
    packets: List[Tuple[int, int, int, int]],
    max_cycles: int = 1000,
    routing_type: RoutingType = RoutingType.XY,
):
    packets.sort(key=lambda p: p[0])

    for cycle in range(max_cycles):
        logger.info(f"[CLOCK] Running cycle {cycle}")
        for cycleable in cycleables:
            if packets and packets[0][0] <= cycle:
                packet = packets.pop(0)
                _, src, dest, msg = packet
                cycleables[4 + src].send(dest, msg)

            cycleable.cycle(routing_type=routing_type)


def load_packets(packet_fp: str = "packets.txt"):
    with open(packet_fp) as packet_f:
        packets = packet_f.read().splitlines()

    packets = list(map(lambda p: list(map(int, p.split(" "))), packets))
    return packets


def main():
    routing_type = RoutingType.XY
    if len(sys.argv) > 1:
        routing_type = RoutingType(sys.argv[1])

    print(f"[*] Running simulation with {routing_type} routing")

    cycleables = generate_mesh()
    packets = load_packets()

    run_simulation(cycleables, packets, max_cycles=20, routing_type=routing_type)


if __name__ == "__main__":
    main()
