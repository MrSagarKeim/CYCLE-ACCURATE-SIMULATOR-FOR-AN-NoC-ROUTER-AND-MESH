## Cycle Accurate Simulator for a NoC Router

### Running

Just execute the following command to run the simulator.
`python3 main.py`

It will save the logs to logs.txt.

#### Specifying the Routing Mode to Follow

Pass either `xy` or `yx` after the script name.

For example,

-   Run in XY Mode: `python3 main.py xy`
-   Run in YX Mode: `python3 main.py yx`

## Mesh

This is how the Routers with id 0-2 are connected with one another.
Here North means Up & East means Right.

```
2 3
0 1
```

## Testing

Input Packets:

```
0 0 3 65
10 1 2 10293942005418276
```

Number of Cycles: 20

Ouptut:

```
[CLOCK] Running cycle 0
[ROUTER=0] Got a Head Flit in Pe Port from PE=0 to PE=3
[ROUTER=0] XBAR pe->east
[CLOCK] Running cycle 1
[ROUTER=0] Got a Data Flit in Pe Port
[ROUTER=1] Got a Head Flit in West Port from PE=0 to PE=3
[ROUTER=1] XBAR west->north
[CLOCK] Running cycle 2
[ROUTER=0] Got a Data Flit in Pe Port
[ROUTER=1] Got a Data Flit in West Port
[ROUTER=3] Got a Head Flit in South Port from PE=0 to PE=3
[CLOCK] Running cycle 3
[ROUTER=0] Got a Data Flit in Pe Port
[ROUTER=1] Got a Data Flit in West Port
[ROUTER=3] Got a Data Flit in South Port
[PE=3] Received flit HeadFlit(type=<FlitType.HEAD: 0>, message=0, source=0, destination=3)
[CLOCK] Running cycle 4
[ROUTER=0] Got a Tail Flit in Pe Port
[ROUTER=1] Got a Data Flit in West Port
[ROUTER=3] Got a Data Flit in South Port
[PE=3] Received flit Flit(type=<FlitType.DATA: 1>, message=65)
[CLOCK] Running cycle 5
[ROUTER=1] Got a Tail Flit in West Port
[ROUTER=3] Got a Data Flit in South Port
[PE=3] Received flit Flit(type=<FlitType.DATA: 1>, message=0)
[CLOCK] Running cycle 6
[ROUTER=3] Got a Tail Flit in South Port
[PE=3] Received flit Flit(type=<FlitType.DATA: 1>, message=0)
[CLOCK] Running cycle 7
[PE=3] Received flit Flit(type=<FlitType.TAIL: 3>, message=0)
[CLOCK] Running cycle 8
[CLOCK] Running cycle 9
[CLOCK] Running cycle 10
[ROUTER=1] Got a Head Flit in Pe Port from PE=1 to PE=2
[ROUTER=1] XBAR pe->west
[CLOCK] Running cycle 11
[ROUTER=1] Got a Data Flit in Pe Port
[CLOCK] Running cycle 12
[ROUTER=0] Got a Head Flit in East Port from PE=1 to PE=2
[ROUTER=0] XBAR east->north
[ROUTER=1] Got a Data Flit in Pe Port
[CLOCK] Running cycle 13
[ROUTER=0] Got a Data Flit in East Port
[ROUTER=1] Got a Data Flit in Pe Port
[ROUTER=2] Got a Head Flit in South Port from PE=1 to PE=2
[CLOCK] Running cycle 14
[ROUTER=0] Got a Data Flit in East Port
[ROUTER=1] Got a Tail Flit in Pe Port
[ROUTER=2] Got a Data Flit in South Port
[PE=2] Received flit HeadFlit(type=<FlitType.HEAD: 0>, message=0, source=1, destination=2)
[CLOCK] Running cycle 15
[ROUTER=0] Got a Data Flit in East Port
[ROUTER=2] Got a Data Flit in South Port
[PE=2] Received flit Flit(type=<FlitType.DATA: 1>, message=613566756)
[CLOCK] Running cycle 16
[ROUTER=0] Got a Tail Flit in East Port
[ROUTER=2] Got a Data Flit in South Port
[PE=2] Received flit Flit(type=<FlitType.DATA: 1>, message=2396745)
[CLOCK] Running cycle 17
[ROUTER=2] Got a Tail Flit in South Port
[PE=2] Received flit Flit(type=<FlitType.DATA: 1>, message=0)
[CLOCK] Running cycle 18
[PE=2] Received flit Flit(type=<FlitType.TAIL: 3>, message=0)
[CLOCK] Running cycle 19



```
