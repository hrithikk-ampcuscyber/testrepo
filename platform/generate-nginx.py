import docker
from pathlib import Path

client = docker.from_env()

output = []

containers = client.containers.list()

for container in containers:

    labels = container.labels

    if labels.get("platform.enable") != "true":
        continue

    host = labels["platform.host"]
    port = labels["platform.port"]

    #
    # Docker DNS name
    #

    network_alias = list(container.attrs["NetworkSettings"]["Networks"].values())[0]["Aliases"][0]

    server = f"""
server {{

    listen 80;

    server_name {host};

    location / {{

        proxy_pass http://{network_alias}:{port};

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    }}

}}
"""

    output.append(server)

config = "\n".join(output)

Path("../proxy/generated/apps.conf").write_text(config)

print("Generated apps.conf")