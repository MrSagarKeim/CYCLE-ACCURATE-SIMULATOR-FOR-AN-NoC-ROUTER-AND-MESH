import sys
from dataclasses import dataclass, field
from enum import Enum
from logging import INFO, FileHandler, Logger, StreamHandler
from typing import Dict, List, Optional

logger = Logger(name="NOC_SIMULATION", level=INFO)
fh = FileHandler("logs.txt", mode="w")
sh = StreamHandler(sys.stdout)
logger.addHandler(fh)
logger.addHandler(sh)

MESH_SIZE = 2


def id_to_xy(id: int):
    x = id % MESH_SIZE
    y = id // MESH_SIZE

    return x, y


class Model:
    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, item):
        return setattr(self, key, item)


class FlitType(Enum):
    HEAD = 0
    DATA = 1
    TAIL = 3

    def __str__(self):
        return self.name.capitalize()


class RoutingType(Enum):
    XY = "xy"
    YX = "yx"

    def __str__(self):
        return self.name.upper()


@dataclass
class Flit(Model):
    type: FlitType
    message: int


@dataclass
class HeadFlit(Flit):
    source: int
    destination: int


@dataclass
class Port(Model):
    buffer_out: Optional[List["Flit"]] = None
    buffer_in: List["Flit"] = field(default_factory=list)


@dataclass
class Router(Model):
    id: int
    pe: Optional["Port"] = None
    east: Optional["Port"] = None
    west: Optional["Port"] = None
    north: Optional["Port"] = None
    south: Optional["Port"] = None

    __sending_buffer: List = field(default_factory=list)

    xbar: Dict[str, "Port"] = field(default_factory=dict)

    def _offsets(self, destination: int):
        x, y = id_to_xy(self.id)
        dx, dy = id_to_xy(destination)

        offset_x = dx - x
        offset_y = dy - y

        return offset_x, offset_y

    def _try_routing_x(self, message: HeadFlit, src_port: str):
        offset_x, _ = self._offsets(message.destination)

        if offset_x < 0:
            if self.west and self.west.buffer_out is not None:
                self.xbar[src_port] = self.west
                logger.info(f"[ROUTER={self.id}] XBAR {src_port}->west")
                return True
        elif offset_x > 0:
            if self.east and self.east.buffer_out is not None:
                logger.info(f"[ROUTER={self.id}] XBAR {src_port}->east")
                self.xbar[src_port] = self.east
                return True

        return False

    def _try_routing_y(self, message: HeadFlit, src_port: str):
        _, offset_y = self._offsets(message.destination)

        if offset_y < 0:
            if self.south and self.south.buffer_out is not None:
                self.xbar[src_port] = self.south
                logger.info(f"[ROUTER={self.id}] XBAR {src_port}->south")
                return True
        elif offset_y > 0:
            if self.north and self.north.buffer_out is not None:
                self.xbar[src_port] = self.north
                logger.info(f"[ROUTER={self.id}] XBAR {src_port}->north")
                return True

        return False

    def _handle_head_flit(self, message: HeadFlit, src_port: str, routing_type: RoutingType):
        if message.destination == self.id:
            self.xbar[src_port] = self.pe
        else:
            if routing_type == RoutingType.XY:
                first_routing_method = self._try_routing_x
                second_routing_method = self._try_routing_y
            else:
                first_routing_method = self._try_routing_y
                second_routing_method = self._try_routing_x

            success = first_routing_method(message, src_port)
            if not success:
                second_routing_method(message, src_port)

    def cycle(self, routing_type: RoutingType = RoutingType.XY):
        while self.__sending_buffer:
            buffer_out, flit = self.__sending_buffer.pop(0)
            buffer_out.append(flit)

        ports = ["pe", "north", "east", "south", "west"]

        for port_n in ports:
            port: Port = self[port_n]
            if port and port.buffer_in:
                flit = port.buffer_in.pop(0)
                log_message = f"[ROUTER={self.id}] Got a {flit.type} Flit in {port_n.title()} Port"

                if isinstance(flit, HeadFlit) and flit.type == FlitType.HEAD:
                    log_message += f" from PE={flit.source} to PE={flit.destination}"

                logger.info(log_message)

                if isinstance(flit, HeadFlit) and flit.type == FlitType.HEAD:
                    self._handle_head_flit(flit, port_n, routing_type)

                port_out = self.xbar.get(port_n)
                if port_out is not None:
                    self.__sending_buffer.append((port_out.buffer_out, flit))


@dataclass
class ProcessingElement(Model):
    id: int
    router: Optional["Port"] = None

    def cycle(self, **kwargs):
        if self.router and self.router.buffer_in:
            flit = self.router.buffer_in.pop(0)
            logger.info(f"[PE={self.id}] Received flit {flit!r}")

    def send(self, destination: int, message: int):
        assert self.router.buffer_out is not None, "PE is not connected to a router"

        mask = (1 << 32) - 1

        f1 = HeadFlit(type=FlitType.HEAD, source=self.id, destination=destination, message=0)
        f2 = Flit(type=FlitType.DATA, message=message & mask)
        f3 = Flit(type=FlitType.DATA, message=(message >> 32) & mask)
        f4 = Flit(type=FlitType.DATA, message=(message >> 64) & mask)
        f5 = Flit(type=FlitType.TAIL, message=0)

        self.router.buffer_out.append(f1)
        self.router.buffer_out.append(f2)
        self.router.buffer_out.append(f3)
        self.router.buffer_out.append(f4)
        self.router.buffer_out.append(f5)


def connect(
    obj1: Router | ProcessingElement,
    port1: str,
    obj2: Router | ProcessingElement,
    port2: str,
):
    p1 = obj1[port1] = Port()
    p2 = obj2[port2] = Port()

    p1.buffer_out = p2.buffer_in
    p2.buffer_out = p1.buffer_in
