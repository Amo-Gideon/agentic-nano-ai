# Agent Prime — Multi-Agent AI Commerce on Arc

**Hackathon:** Agentic Economy on Arc — Nano Payments  
**Tracks:** 🧮 Usage-Based Compute Billing + 🤖 Agent-to-Agent Payment Loop  
**Builder:** Appau Amo Gideon Kofi (Solo)  

---

## What It Does

**Agent Prime** is a multi-agent orchestration platform that enables autonomous AI agents to hire and pay each other using real-time USDC nanopayments on Arc Testnet.

**Example flow:**
1. User: *"Write a blog post about AI agents"*
2. **Agent Prime** breaks this into 3 subtasks:
   - **Research Agent** ($0.001 USDC) — Gather 5 key facts
   - **Writer Agent** ($0.001 USDC) — Draft blog post
   - **Editor Agent** ($0.001 USDC) — Polish final text
3. Each agent is paid **separately** via on-chain Arc Testnet USDC transfer
4. Agent Prime combines all 3 outputs into the final deliverable

**Total cost: $0.003 USDC**  
**Arc gas: ~$0.027**  
**L1 equivalent gas: $4.50**

---

## Architecture

```
Client → GET /api/complex-task-requirement → Server returns payment breakdown
Client → Pays USDC on Arc Testnet → Gets real tx_hash
Client → POST /api/complex-task → Server verifies ON-CHAIN via web3.py → Runs 3 AI tasks → Returns combined result
```

**Key innovation:** Direct on-chain verification using `web3.py` (not Circle Sandbox mock data). The backend queries actual Arc Testnet RPC nodes, validates transaction receipts, decodes USDC Transfer events, and confirms amounts before executing any AI task.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **API Framework** | FastAPI |
| **AI Inference** | Featherless AI (Qwen/Qwen3-0.6B) |
| **Blockchain** | Arc Testnet (Chain ID: 5042002) |
| **Stablecoin** | USDC (native gas token on Arc) |
| **Payment Protocol** | x402 |
| **On-Chain Verification** | web3.py direct RPC calls |
| **Frontend** | HTML/CSS/JS (agent_prime.html) |

---

## Economic Proof

| Metric | Arc Nanopayments | Ethereum L1 |
|--------|-------------------|-------------|
| Fee per task | $0.001 | $0.001 |
| Gas per tx | ~$0.009 | $1.50 |
| 3-task workflow revenue | $0.003 | $0.003 |
| 3-task workflow gas | ~$0.027 | $4.50 |
| **Result** | **✅ Viable (~90% margin)** | **❌ -$4.497 LOSS** |

**This model is economically impossible on L1. Arc makes it viable.**

---

## Setup

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/agentic-nano-ai.git
cd agentic-nano-ai
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# Featherless AI
FEATHERLESS_API_KEY=your_featherless_key
FEATHERLESS_BASE_URL=https://api.featherless.ai/v1
AI_MODEL=Qwen/Qwen3-0.6B

# Circle API
CIRCLE_API_KEY=your_circle_key
CIRCLE_BASE_URL=https://api-sandbox.circle.com

# Arc Testnet
ARC_CHAIN=ARCBET
WALLET_ADDRESS=0xcF1DD1B3B2A682F7d7935bbbcFe9C5514b19E9f0
NANO_FEE_USDC=0.001

# Sandbox mode for demo (set false for real Arc transactions)
SANDBOX_MODE=true
```

### 3. Start Backend

```bash
python run.py
```

Server runs at `http://localhost:5000`

### 4. Open Frontend

Open `agent_prime.html` in any browser.

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Check service status |
| `/api/payment-requirement` | GET | Get payment details for simple task |
| `/api/execute-task` | POST | Submit payment proof + task, get AI result |
| `/api/complex-task-requirement` | GET | Get payment breakdown for multi-agent task |
| `/api/complex-task` | POST | Submit payment proof, Agent Prime orchestrates 3 sub-agents |

---

## Demo Scripts

| Script | What It Does |
|--------|-------------|
| `python demo_complex_task.py` | Full Agent Prime orchestration demo (3 agents) |
| `python send_real_usdc.py` | Send 50 real USDC transactions on Arc Testnet |
| `python demo_real.py` | Verify real Arc tx hashes on-chain + execute AI |
| `python test_usdc.py` | Check USDC balance via direct RPC |

---

## Real On-Chain Transactions

To send real USDC on Arc Testnet:

1. Get testnet USDC from [faucet.circle.com](https://faucet.circle.com)
2. Add Arc Testnet to MetaMask:
   - RPC: `https://rpc.testnet.arc.network`
   - Chain ID: `5042002`
   - Currency: `USDC`
3. Paste your private key in `send_real_usdc.py` (line 15)
4. Run: `python send_real_usdc.py`

All transaction hashes are saved to `tx_hashes.txt` and viewable on [Arcscan](https://testnet.arcscan.app).

---

## Project Structure

```
agentic-nano-ai/
├── .env                          # Environment variables (gitignored)
├── .gitignore                    # Git ignore rules
├── run.py                        # Start FastAPI server
├── requirements.txt              # Python dependencies
├── agent_prime.html              # Multi-agent orchestration frontend
├── backend/
│   └── app/
│       ├── main.py               # FastAPI app with routers
│       ├── core/
│       │   └── config.py         # Pydantic settings + .env loader
│       ├── models/
│       │   └── schema.py         # Pydantic request/response models
│       ├── routes/
│       │   ├── ai.py             # Simple task endpoints
│       │   └── orchestrator.py   # Agent Prime multi-agent endpoints
│       └── services/
│           ├── payment_service.py # On-chain USDC verification (web3.py)
│           └── ai_service.py      # Featherless AI integration
```

---

## License

MIT

---

*Built for the lablab.ai Agentic Economy on Arc Hackathon.*
*Solo project by Appau Amo Gideon Kofi.*
