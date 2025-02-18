import docker
import requests
import time
import re
import logging

from config import NPM_URL, NPM_API_URL, NPM_USER, NPM_PASSWORD, CERTIFICATE_ID, HOST_IP

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Docker client
client = docker.from_env()


def get_token(npm_user, npm_password):
    url = f"{NPM_URL}/api/tokens"
    payload = {"identity": npm_user, "secret": npm_password}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json().get("token")
    else:
        raise Exception(
            f"Failed to obtain token: {response.status_code} {response.text}"
        )


# Obtain the Bearer token
token = get_token(NPM_USER, NPM_PASSWORD)
logging.info("Successfully obtained token")

# Nginx Proxy Manager API headers
HEADERS = {
    "Content-Type": "application/json; charset=UTF-8",
    "Authorization": f"Bearer {token}",
}


def get_container_info(container):
    """Extract information from container."""
    name = container.name
    # Assuming the container name follows the pattern: {name}-{suffix}
    domain_name = re.split("-|_", name)[0] + ".awahrani.duckdns.org"
    port = list(container.attrs["NetworkSettings"]["Ports"].values())[0][0]["HostPort"]
    ip = HOST_IP
    logging.info(
        f"Container found - Name: {name}, Domain: {domain_name}, IP: {ip}, Port: {port}"
    )
    return domain_name, ip, port


def add_proxy_host(domain_name, ip, port):
    """Create a new proxy host."""
    payload = {
        "domain_names": [domain_name],
        "forward_scheme": "http",
        "forward_host": ip,
        "forward_port": port,
        "access_list_id": "0",
        "advanced_config": "",
        "allow_websocket_upgrade": True,
        "block_exploits": True,
        "caching_enabled": False,
        "certificate_id": CERTIFICATE_ID,
        "hsts_enabled": False,
        "hsts_subdomains": False,
        "http2_support": True,
        "locations": [],
        "meta": {"letsencrypt_agree": False, "dns_challenge": False},
        "ssl_forced": True,
    }
    response = requests.post(NPM_API_URL, headers=HEADERS, json=payload)
    if response.status_code == 201:
        logging.info(f"Successfully added proxy host for {domain_name}")
    else:
        logging.error(f"Failed to add proxy host for {domain_name}: {response.text}")
    return response


def main():
    """Main function to monitor new containers and add proxy hosts."""
    logging.info("Starting Docker container monitor")
    existing_containers = {c.id for c in client.containers.list()}
    while True:
        time.sleep(10)  # Check every 10 seconds
        current_containers = {c.id for c in client.containers.list()}
        new_containers = current_containers - existing_containers
        if new_containers:
            for container_id in new_containers:
                container = client.containers.get(container_id)
                domain_name, ip, port = get_container_info(container)
                response = add_proxy_host(domain_name, ip, port)
            existing_containers = current_containers
        else:
            logging.info("No new containers detected")


if __name__ == "__main__":
    main()
