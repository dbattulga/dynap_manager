import json
import logging

import enoslib as en

from enoslib.api import run_command #, wait_ssh
from enoslib.api import run_ansible
from enoslib.infra.enos_g5k.provider import G5k
from enoslib.infra.enos_g5k.configuration import Configuration, NetworkConfiguration


logging.basicConfig(level=logging.INFO)


prod_network = en.G5kNetworkConf(
    id="n1",
    type="prod",
    roles=["my_network"],
    site="rennes"
)

conf = (
    en.G5kConf
    .from_settings(
        job_type="allow_classic_ssh",
        job_name="WTestLatency",
        walltime="01:00:00"
    )
    .add_network_conf(prod_network)
    .add_machine(
        roles=["start"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["end"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["10"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["20"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["30"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["40"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["50"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["60"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["70"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["80"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["90"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    .add_machine(
        roles=["100"],
        cluster="parasilo",
        nodes=1,
        primary_network=prod_network,
    )
    # .add_machine(
    #     roles=["110"],
    #     cluster="parasilo",
    #     nodes=1,
    #     primary_network=prod_network,
    # )
    # .add_machine(
    #     roles=["120"],
    #     cluster="parasilo",
    #     nodes=1,
    #     primary_network=prod_network,
    # )
    # .add_machine(
    #     roles=["130"],
    #     cluster="parasilo",
    #     nodes=1,
    #     primary_network=prod_network,
    # )
    # .add_machine(
    #     roles=["140"],
    #     cluster="parasilo",
    #     nodes=1,
    #     primary_network=prod_network,
    # )
    # .add_machine(
    #     roles=["150"],
    #     cluster="parasilo",
    #     nodes=1,
    #     primary_network=prod_network,
    # )
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
        .add_constraints("delay 40ms", roles["40"], symetric=True)
        .add_constraints("delay 50ms", roles["50"], symetric=True)
        .add_constraints("delay 60ms", roles["60"], symetric=True)
        .add_constraints("delay 70ms", roles["70"], symetric=True)
        .add_constraints("delay 80ms", roles["80"], symetric=True)
        .add_constraints("delay 90ms", roles["90"], symetric=True)
        .add_constraints("delay 100ms", roles["100"], symetric=True)
        # .add_constraints("delay 110ms", roles["110"], symetric=True)
        # .add_constraints("delay 120ms", roles["120"], symetric=True)
        # .add_constraints("delay 130ms", roles["130"], symetric=True)
        # .add_constraints("delay 140ms", roles["140"], symetric=True)
        # .add_constraints("delay 150ms", roles["150"], symetric=True)
)

netem.deploy()
netem.validate()

# install docker
run_command("apt update", roles=roles)
run_command("apt install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common", roles=roles)
run_command("curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -", roles=roles)
run_command('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"', roles=roles)
run_command("apt update && apt-cache policy docker-ce", roles=roles)
run_command("apt install -y docker-ce", roles=roles)

#install docker-compose
run_command("sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose", roles=roles)
run_command("sudo chmod +x /usr/local/bin/docker-compose", roles=roles)

#pull and run Dynap
run_command("rm -rf dynap", roles=roles)
run_command("git clone https://github.com/jazz09/dynap.git", roles=roles)
run_command("cd dynap/ && sudo-g5k docker-compose up -d", roles=roles)
run_command("cat dynap/hosts.txt", roles=roles)

nodes = []
for role, hosts in roles.items():
    print(role)
    for host in hosts:
        print(f"{host.alias}")
        node = {
            "role": role,
            "host": host.alias
        }
        nodes.append(node)

json_nodes = json.dumps(nodes)
print(json_nodes)


