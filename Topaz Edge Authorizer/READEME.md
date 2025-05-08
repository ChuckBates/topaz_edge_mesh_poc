# 🛡️ Topaz Edge Authorization Server with Python Directory Service

This project sets up a Python-based server alongside a distributed [Topaz](https://www.aserto.com/topaz/) authorization mesh. It demonstrates local REBAC authorization backed by a centralized control node and multiple authorizers, all orchestrated via Docker. 

The project consists of:
- A Topaz `control-node` that is not responsible for making any authorization decisions, but housing the Console UI and maintaining the source of truth directory authorization data. 
- Two Topaz nodes which are identical but separate authorization decision points. 
    - Each regularly syncs it's local data with the `control-node` for evaluation during authorization decisions, and each regularly checks the external `ghcr.io` repo for policy (rego) updates. 
    - Each of the two Topaz authorizors responsible for decisions should behave identically, and demonstrate a distributed authorization mesh with consistent decision results. 
- A python server that is for convienence in abstracting away the (sometimes confusing) shape of direct Topaz requests. This python server:
    - Acts as the intermediary by taking a simplified authorization request, translating it to the Topaz format, and asking one of the authorizors (in this PoC it asks `topaz-authorizor-node-1`). 
    - When being asked to generate SQL search filters, takes the extensive `OPA AST` output (often 10s of thousand of lines of json) and translates it to concise SQL `WHERE` clauses. (See the example insomina requests). 
    - Abstracts the complicated schema of objects and relations when modifying the Topaz directory authorization data and allows the caller to interact with REST endpoints suited to Transport4 (e.g. AddSubscriber, GrantPermission, etc.).


---

## Project Structure

```
.
├── server.py                                   # Flask API server for resource checks & directory ops
├── directory/                                  # Core resource logic (user, roles, actions, etc.)
├── docker-compose.yml                          # Orchestrates control node, authorizers, and server
├── config.json                                 # API config for Topaz endpoints
├── tests/                                      # Pytest suite with mock-based unit tests
├── control-node/                               # Topaz control node with certs, config, db, and seed data
├── authorizer1/, authorizer2/                  # Authorizers with unique config and DBs
└── topaz_edge_authorizer_poc.insomnia.json     # Full API collection (see below)
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for test execution)
- [Insomnia](https://insomnia.rest/download) (for exploring the API)

### Launch the Stack

```bash
docker-compose up --build
```

This will start:

| Container               | Description                        | Key Ports      |
|------------------------|------------------------------------|----------------|
| `authorization-server` | Flask + OPA query proxy            | `5000` (REST)  |
| `topaz-control-node`             | Central Topaz control node         | `9393`, `9292` |
| `topaz-authorizer-node-1` | Edge Authorizer instance       | `29393`, `29292` |
| `topaz-authorizer-node-2` | Edge Authorizer instance       | `39393`, `39292` |

Each authorizer pulls its policy bundle from a configured [GitHub Container Registry](https://ghcr.io) image via its `config.yaml`.

---

## Exploring the Console UI

Once started, the local UI will be available at [https://localhost:19393](https://localhost:19393)

## API Testing with Insomnia

The file [`topaz_edge_authorizer_poc.insomnia.json`](./topaz_edge_authorizer_poc.insomnia.json) contains a complete [Insomnia](https://insomnia.rest/) workspace with:

- All API calls to the Python server (`/api/user`, `/api/nomination/check`, etc.)
- Direct requests to each Topaz authorizer
- Pre-configured examples for nominations, tickets, roles, and permissions

### To use:
1. Open Insomnia
2. Go to **Application Menu > Import**
3. Select `topaz_edge_authorizer_poc.insomnia.json`
4. Start sending requests!

This is the recommended way to explore the system.

---

## Running Unit Tests

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Then run from the `tests/directory_tests` directory:

```bash
python -m pytest -v -s
```

The test suite mocks directory services and validates user, permission, and relation logic using `pytest-mock`.

---

## Certificate Management

Each Topaz node loads certificates from its `certs/` directory:

| Cert File         | Purpose                  |
|-------------------|--------------------------|
| `gateway.crt/key` | REST API server          |
| `grpc.crt/key`    | gRPC communication       |
| `*-ca.crt`        | CA root trust for both   |

These can install to local keychain/key store for better console browsing experience.

---

## Notes

- Flask server configuration lives in `config.json`
- All authorization checks use OPA-compatible JSON payloads and route through the Topaz Edge Authorizer mesh
- `directory/` implements logical operations for entity modeling
