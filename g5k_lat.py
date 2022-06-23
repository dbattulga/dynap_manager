import logging

import enoslib as en

logging.basicConfig(level=logging.DEBUG)


prod_network = en.G5kNetworkConf(id="n1", type="prod", roles=["my_network"], site="rennes")
conf = (
    en.G5kConf.from_settings(job_type="allow_classic_ssh", job_name="DTestLatency", walltime="00:30:00")
    .add_network_conf(prod_network)
    .add_machine(
        roles=["city", "10"],
        cluster="paravance",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["city", "20"],
        cluster="paravance",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["city", "30"],
        cluster="paravance",
        nodes=1,
        primary_network=prod_network,
    )

    .finalize()
)
provider = en.G5k(conf)
roles, networks = provider.init()
roles = en.sync_info(roles, networks)

netem = en.Netem()
(
    netem
    .add_constraints("delay 10ms", roles["10"], symetric=True)
    .add_constraints("delay 20ms", roles["20"], symetric=True)
    .add_constraints("delay 30ms", roles["30"], symetric=True)
)

netem.deploy()
netem.validate()
#netem.destroy()

for role, hosts in roles.items():
    print(role)
    for host in hosts:
        print(f"{host.alias}")