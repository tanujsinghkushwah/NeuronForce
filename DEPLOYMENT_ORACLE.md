# Deploying NeuronForce to Oracle Cloud Infrastructure (Always Free)

This guide covers deploying NeuronForce on **Oracle Cloud Infrastructure (OCI) Always Free Tier** using the **Ampere A1 Compute (ARM64)** shape, which provides up to **4 OCPUs and 24 GB of RAM** at zero cost.

---

## Architecture Overview

```
                      Internet (:80 / :443)
                                │
                                ▼
                       ┌─────────────────┐
                       │   Caddy Proxy   │ (Automatic Free SSL)
                       └────────┬────────┘
                                │
               ┌────────────────┴────────────────┐
               ▼                                 ▼
      /api/* (Backend)                    /* (Frontend)
   ┌──────────────────────┐             ┌─────────────────────┐
   │ FastAPI Backend      │             │ Next.js App Router  │
   │ Port: 8000           │             │ Port: 3000          │
   │ SQLite / PostgreSQL  │             │ Standalone Node.js  │
   └──────────────────────┘             └─────────────────────┘
```

---

## Step 1: Provision the Oracle Free Compute Instance

1. Log into your [Oracle Cloud Console](https://cloud.oracle.com/).
2. In the navigation menu, go to **Compute** &rarr; **Instances** &rarr; **Create Instance**.
3. Configure the instance:
   - **Name**: `neuronforce-server`
   - **Image**: **Canonical Ubuntu 24.04** or **22.04** (Minimal or Standard).
   - **Shape**:
     - Click **Change shape** &rarr; select **Ampere (Arm-based)**.
     - Shape: **VM.Standard.A1.Flex** *(Always Free Eligible)*.
     - Allocate: **2 to 4 OCPUs** and **12 to 24 GB RAM** (e.g., 2 OCPU, 12 GB RAM is more than enough).
   - **Networking**:
     - Create new Virtual Cloud Network (VCN) or select existing.
     - Assign a public IPv4 address: **Yes**.
   - **SSH Keys**: Download and save your Private Key (`.key`) on your machine.
   - **Boot Volume**: Default (50 GB or up to 200 GB Always Free).
4. Click **Create** and wait for the instance status to change to **Running**.
5. Note your **Public IP Address** (e.g., `129.153.xx.xx`).

---

## Step 2: Open Ingress Ports in OCI Console

Oracle Cloud blocks inbound traffic at the VCN subnet level by default.

1. In the Instance details page, click on your **Subnet** link under **Primary VNIC**.
2. Click on the **Default Security List for `<your-vcn>`**.
3. Under **Ingress Rules**, click **Add Ingress Rules**:
   - **Rule 1 (HTTP)**:
     - Source CIDR: `0.0.0.0/0`
     - IP Protocol: `TCP`
     - Destination Port Range: `80`
     - Description: `HTTP traffic`
   - **Rule 2 (HTTPS)**:
     - Source CIDR: `0.0.0.0/0`
     - IP Protocol: `TCP`
     - Destination Port Range: `443`
     - Description: `HTTPS traffic`
4. Click **Add Ingress Rules**.

---

## Step 3: Connect via SSH & Configure Instance Firewall

Oracle Ubuntu instances come with strict host `iptables` rules that reject port 80/443 even after the VCN rule is created.

1. Connect to your instance:
   ```bash
   ssh -i /path/to/your-private-key.key ubuntu@<YOUR_PUBLIC_IP>
   ```

2. Open ports 80 and 443 in `iptables`:
   ```bash
   sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
   sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
   sudo netfilter-persistent save || sudo apt-get install -y iptables-persistent && sudo netfilter-persistent save
   ```

3. Update the package index and install Docker & Docker Compose:
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   sudo apt-get install -y git curl ca-certificates

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu

   # Apply group without re-login
   newgrp docker
   ```

---

## Step 4: Clone the Repo & Configure Environment Variables

1. Clone your repository:
   ```bash
   git clone https://github.com/tanujsinghkushwah/NeuronForce.git
   cd NeuronForce
   ```

2. Configure backend environment (`backend/.env`):
   ```bash
   cp backend/.env.example backend/.env
   nano backend/.env
   ```
   Ensure these key variables are set:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
   JWT_SECRET_KEY=generate_a_random_secure_secret_key_here
   DATABASE_URL=sqlite:///./neuronforce.db
   ALLOWED_ORIGINS=http://<YOUR_PUBLIC_IP>,http://localhost:3000
   ```

3. Configure frontend environment (`frontend/.env.local`):
   ```bash
   cp frontend/.env.example frontend/.env.local
   nano frontend/.env.local
   ```
   Set:
   ```env
   NEXT_PUBLIC_API_URL=/api
   ```
   *(If you are using Firebase SSO, also paste your Firebase web config keys here).*

---

## Step 5: (Optional) Configure Custom Domain & Free HTTPS

If you have a domain name (e.g. `crm.yourdomain.com`):
1. Point an `A` record for your domain to your Oracle Instance **Public IP**.
2. Edit `Caddyfile`:
   ```bash
   nano Caddyfile
   ```
   Replace `:80` on line 3 with your domain:
   ```caddy
   crm.yourdomain.com {
       encode gzip zstd

       handle /api/* {
           reverse_proxy backend:8000
       }

       handle /docs* {
           reverse_proxy backend:8000
       }

       handle /openapi.json {
           reverse_proxy backend:8000
       }

       handle {
           reverse_proxy frontend:3000
       }
   }
   ```
   *Caddy will automatically provision and renew a free Let's Encrypt SSL certificate!*

If you don't have a domain yet, leave `:80` in the `Caddyfile` and access directly via `http://<YOUR_PUBLIC_IP>`.

---

## Step 6: Launch NeuronForce

Start all services (Backend, Frontend, and Caddy) with a single command:

```bash
docker compose up -d --build
```

Monitor container health and startup logs:
```bash
docker compose logs -f
```

Check running containers:
```bash
docker compose ps
```

---

## Step 7: Verification

1. Open your browser and navigate to:
   - `http://<YOUR_PUBLIC_IP>` (or `https://crm.yourdomain.com`)
2. Verify API status:
   - `http://<YOUR_PUBLIC_IP>/api/health`
3. Verify interactive OpenAPI documentation:
   - `http://<YOUR_PUBLIC_IP>/docs`

---

## Useful Maintenance Commands

- **Restart containers**: `docker compose restart`
- **View live logs**: `docker compose logs -f --tail=100`
- **Stop containers**: `docker compose down`
- **Pull code updates & redeploy**:
  ```bash
  git pull origin main
  docker compose up -d --build
  ```
- **Backup database**:
  ```bash
  cp backend/neuronforce.db ~/backup_neuronforce_$(date +%F).db
  ```
