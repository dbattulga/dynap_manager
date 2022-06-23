import logging

from enoslib import *

logging.basicConfig(level=logging.DEBUG)


prod_network = G5kNetworkConf(id="n1", type="prod", roles=["my_network"], site="rennes")
conf = (
    G5kConf.from_settings(job_name="DaTestLatency", job_type="allow_classic_ssh", walltime="00:30:00")
    .add_network_conf(prod_network)
    .add_machine(
        roles=["city", "paris"],
        cluster="paravance",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["city", "berlin"],
        cluster="paravance",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["city", "londres"],
        cluster="paravance",
        nodes=1,
        primary_network=prod_network,
    )
    .finalize()
)
provider = G5k(conf)
roles, networks = provider.init()

sources = []
for idx, host in enumerate(roles["city"]):
    delay = 5 * idx
    print(f"{host.alias} <-> {delay}")
    inbound = NetemOutConstraint(device="br0", options=f"delay {delay}ms")
    outbound = NetemInConstraint(device="br0", options=f"delay {delay}ms")
    sources.append(NetemInOutSource(host, constraints=[inbound, outbound]))

netem(sources)