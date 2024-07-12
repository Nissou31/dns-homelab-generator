# dns-homelab-generator

## Description

This project monitors new Docker containers and automatically creates proxy hosts on Nginx Proxy Manager using the container's information.

## Features

- Monitors Docker containers for new instances.
- Automatically creates proxy hosts in Nginx Proxy Manager.
- Customizable via environment variables.

## Setup

### Prerequisites

- Docker and Docker Compose installed on your system.
- Nginx Proxy Manager setup and running.
- Obtain the Nginx Proxy Manager API credentials (`email` and `password`).

### Clone the Repository

```sh
git clone https://github.com/Nissou31/dns-homelab-generator.git
cd dns-homelab-generator
```

### Configuration

Set up the environment variables:

- `NPM_URL`: The URL of your Nginx Proxy Manager (e.g., `http://192.168.1.100:81`).
- `NPM_API_URL`: The API URL of your Nginx Proxy Manager (e.g., `https://proxy.fqdn.duckdns.org/api/nginx/proxy-hosts`).
- `NPM_USER`: Your Nginx Proxy Manager user email.
- `NPM_PASSWORD`: Your Nginx Proxy Manager password.
- `CERTIFICATE_ID`: The certificate ID to be used. This can be obtained by looking at the payload of the certificates in Nginx Proxy Manager or can be known if keeping track (the first one is always `id=0` and it increments).

You can set these variables in your environment or in a `.env` file.

### Example .env file

Create a `.env` file in the project root with the following content:

```env
NPM_URL=http://192.168.1.100:81
NPM_API_URL=https://proxy.fqdn.duckdns.org/api/nginx/proxy-hosts
NPM_USER=your-email@example.com
NPM_PASSWORD=your-password
CERTIFICATE_ID=1
```

### Build and Run with Docker Compose

```sh
docker-compose up --build
```

## Project Structure

```
my-project/
│
├── src/
│   ├── app.py
│   ├── config.py
│   └── requirements.txt
│
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Explanation of Files

- **src/app.py**: Main application script that monitors Docker containers and creates proxy hosts.
- **src/config.py**: Configuration file that loads environment variables.
- **src/requirements.txt**: List of Python dependencies.
- **Dockerfile**: Dockerfile to build the Docker image.
- **docker-compose.yml**: Docker Compose configuration file.
- **.gitignore**: Gitignore file to exclude unnecessary files from version control.
- **README.md**: This readme file.

## Notes

- The certificate ID can be obtained by looking at the payload of the certificates in Nginx Proxy Manager. It can also be known by keeping track, as the first certificate is always `id=0` and it increments with each new certificate.
- Ensure that the Docker daemon is running and accessible to the Docker client in the container.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
