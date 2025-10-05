# MCP Marketplace – V2 Draft

## Vision

Create a trusted MCP marketplace that empowers developers to publish and monetize reusable AI agent tools—starting with a **zero-ops hobbyist tier** (platform-hosted) and growing into a **pro tier** (self-hosted) for established publishers.

**Core Philosophy:**
AI/LLMs are the intelligence; MCPs are their toolkit. A capable AI agent is the sum of its available MCPs. We make MCP discovery, distribution, and monetization frictionless.

---

## Two-Tier Model

### Tier 1: Hobbyist (Platform-Hosted)
**Target Audience:** Indie developers, researchers, side-project builders who want to publish and earn without managing infrastructure.

**Publisher Experience:**
- Upload code (Python FastMCP initially, expand to Node/Go)
- Declare entrypoint, dependencies, metadata
- Set price (free, per-call fee, or subscription)
- Platform handles execution, scaling, monitoring

**Consumer Experience:**
- Browse/search marketplace
- Pay for access → receive time-limited JWT
- Invoke via platform endpoint: `https://api.mcpstore.io/invoke/{mcp_id}`
- Uniform performance, sandboxed security

**Economics:**
- 20% platform fee (covers hosting, sandboxing, payment processing)
- Publisher earns 80% of every invocation
- Automatic payouts (weekly/monthly settlements)

---

### Tier 2: Pro (Self-Hosted)
**Target Audience:** Established publishers who want full control, custom infrastructure, or enterprise features.

**Publisher Experience:**
- Register MCP in marketplace with self-hosted endpoint URL
- Platform handles discovery, payments, JWT issuance
- Publisher's server validates JWT (platform provides public key or webhook)
- Full control over stack, scaling, uptime, pricing models

**Consumer Experience:**
- Same discovery/payment flow
- Receives JWT, calls publisher's endpoint directly
- Performance/reliability varies by publisher (shown in ratings)

**Economics:**
- 3-5% payment processing fee only
- Publisher keeps 95-97%
- Can offer direct billing for enterprise customers

**Migration Path:**
Start on Tier 1 → grow audience → upgrade to Tier 2 when ready for ops burden.

---

## Core Components

### 1. MCP Registry (Database + API)
**Schema:**
```sql
CREATE TABLE mcps (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  author_id UUID REFERENCES users(id),
  description TEXT,
  category TEXT[], -- e.g., ['security', 'data', 'communication']
  language TEXT, -- 'python', 'javascript', 'go'
  tier TEXT, -- 'hobbyist' or 'pro'

  -- Tier 1 (platform-hosted)
  code_hash TEXT, -- SHA-256 of uploaded code
  entrypoint TEXT, -- 'server.py', 'index.js'
  runtime_version TEXT, -- 'python:3.11', 'node:20'

  -- Tier 2 (self-hosted)
  endpoint_url TEXT, -- Publisher's MCP server URL

  -- Pricing
  pricing_model TEXT, -- 'free', 'per_call', 'subscription'
  price_amount DECIMAL,
  price_currency TEXT, -- 'usd', 'sat'

  -- Metadata
  repo_url TEXT,
  license TEXT,
  pgp_signature TEXT,
  verified BOOLEAN DEFAULT FALSE,

  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE mcp_versions (
  id UUID PRIMARY KEY,
  mcp_id UUID REFERENCES mcps(id),
  version TEXT,
  code_hash TEXT, -- Immutable provenance
  changelog TEXT,
  published_at TIMESTAMP
);

CREATE TABLE ratings (
  id UUID PRIMARY KEY,
  mcp_id UUID REFERENCES mcps(id),
  user_id UUID REFERENCES users(id),
  stars INT CHECK (stars BETWEEN 1 AND 5),
  comment TEXT,
  created_at TIMESTAMP
);

CREATE TABLE invocations (
  id UUID PRIMARY KEY,
  mcp_id UUID REFERENCES mcps(id),
  user_id UUID REFERENCES users(id),
  timestamp TIMESTAMP,
  duration_ms INT,
  success BOOLEAN,
  revenue_usd DECIMAL -- For analytics
);
```

**API Endpoints:**
- `POST /mcp` – Publish new MCP
- `PUT /mcp/{id}` – Update MCP (creates new version)
- `GET /mcp?q=&category=&tier=&sort=` – Search/browse
- `GET /mcp/{id}` – Get details + version history
- `POST /mcp/{id}/rate` – Submit rating

---

### 2. Execution Sandbox (Tier 1 Only)

**Architecture:**
```
User Request → API Gateway → Payment Check → JWT Issue → Sandbox Executor → Response
```

**Sandbox Stack (Initial: Python Only):**
- **Runtime:** Docker container with Python 3.11 + FastMCP
- **Resource Limits:** 512MB RAM, 5s timeout, no network (initially)
- **Isolation:** One container per invocation (consider warm pool later)
- **Entrypoint:** `python /mcp/server.py` (MCP runs in stdio mode)

**Request Flow:**
```python
# User calls with JWT
POST https://api.mcpstore.io/invoke/abc-123
Authorization: Bearer <jwt>
Content-Type: application/json

{
  "tool": "analyze_document",
  "arguments": {
    "text": "..."
  }
}

# Platform validates JWT, spawns sandbox
# Sandbox runs: echo '{"method":"tools/call",...}' | python /mcp/server.py
# Returns result
```

**Future Enhancements:**
- Multi-language support (Node, Go, Rust)
- Warm container pool (reduce cold start)
- Network-enabled MCPs (with user consent)
- GPU support for ML MCPs

---

### 3. Provenance Ledger

**Purpose:** Immutable record of every published version to prove authenticity and prevent tampering.

**Implementation:**
- Append-only `mcp_versions` table
- Each version records SHA-256 hash of code
- Optional: Periodic Merkle root published to public blockchain (Bitcoin/Ethereum) for extra trust

**Usage:**
- MCP detail page shows: "v1.2.3 verified on 2025-01-15 (hash: sha256:abc123...)"
- Users can download code and verify hash matches
- Prevents silent updates (new version = new hash)

**Optional PGP Signing:**
- Authors can sign releases with PGP key
- Platform stores signature, users can verify: `gpg --verify release.sig`

---

### 4. Payment Engine

**Supported Methods:**
- **Fiat:** Stripe (cards, bank transfers)
- **Crypto:** Bitcoin Lightning (instant microtransactions)

**Flow:**
1. User selects MCP, clicks "Purchase Access"
2. Platform creates payment request (Stripe Checkout or Lightning invoice)
3. On payment success → webhook triggers JWT issuance
4. JWT payload: `{sub: user_id, mcp: mcp_id, tier: 'paid', exp: 15min}`
5. User presents JWT on invocation

**Revenue Distribution:**
- **Tier 1:** 80% to author, 20% to platform (deducted at payment)
- **Tier 2:** 95% to author, 5% to platform

**Settlement:**
- Authors can withdraw earnings via bank transfer or Lightning
- Minimum payout threshold: $10 or 10,000 sats

---

### 5. Discovery & Front-End

**Web App (React/Vue SPA):**

**Homepage:**
- Featured MCPs (top-rated, trending, new)
- Search bar with autocomplete
- Category filters (Security, Data, Communication, etc.)

**MCP Detail Page:**
- Name, description, author badge
- Pricing (free / $0.10 per call / $5/month)
- Rating (stars + review count)
- Usage stats (X invocations this month)
- Provenance: "v2.1.0 verified 2025-10-01 (hash: ...)"
- License badge (MIT, Apache, Commercial-No-Redistribute)
- "Try Now" button (for free tier) or "Purchase Access"

**Search API (for AI Agents):**
```http
GET /api/search?q=document%20signing&category=security

Response:
{
  "results": [
    {
      "id": "abc-123",
      "name": "YubiKey Document Signer",
      "description": "Sign documents with hardware-backed security",
      "author": "alice",
      "verified": true,
      "price": 0.10,
      "currency": "usd",
      "rating": 4.8,
      "tier": "hobbyist"
    }
  ]
}
```

**MCP-as-Discovery Tool:**
Platform itself can be an MCP server that AI agents query:
```python
# Agent uses mcpstore MCP to find tools
@mcp.tool()
async def search_mcps(query: str, category: str = None) -> list[dict]:
    """Search the MCP marketplace for relevant tools."""
    # Returns matching MCPs with metadata
```

---

### 6. Creator Dashboard

**Features:**
- Upload new MCP / update existing
- View analytics:
  - Total invocations (graph over time)
  - Revenue (fiat + Lightning, broken down)
  - Top users (anonymized)
  - Error rate, avg latency (Tier 1 only)
- Manage pricing: change per-call fee, enable subscriptions
- License selector (MIT, Apache, GPL, Commercial-No-Redistribute)
- Badge progress: "5 more 5-star reviews to unlock Verified Publisher"
- Withdraw earnings

**Tier Comparison Widget:**
```
Current: Hobbyist (20% fee)
Upgrade to Pro:
✓ Keep 95% of revenue
✓ Custom infrastructure
✓ Enterprise pricing options
⚠ Requires server management
[Upgrade to Pro] button
```

---

### 7. Trust & Reputation System

**Mechanisms:**

| Need | Solution |
|------|----------|
| Clear Attribution | Author name, avatar, GitHub link on every MCP page |
| Immutable Provenance | Append-only version ledger with SHA-256 hashes |
| Prevent Unauthorized Use | JWT-gated execution (no token = no invocation) |
| Revenue Sharing | Automatic per-call payouts (80/20 or 95/5 split) |
| Quality Signals | Star ratings, review count, verified badge |
| Security Audits | Community bounties for code review, "Audited" badge |
| Brand Recognition | Top earners featured on homepage, custom publisher logos |

**Verified Publisher Badge:**
- Manual review after 10 successful invocations + 5 positive reviews
- Checks: Code quality, no malicious behavior, responsive support
- Displayed prominently on MCP listings

**Community Bounties (Future):**
- Users post bounty: "Audit this MCP for security - $50"
- Volunteer auditors submit reports
- Publisher fixes issues → auditor earns bounty + "Auditor" badge
- MCP earns "Community Audited" badge

---

## Success Metrics (12 Months)

| Metric | Target |
|--------|--------|
| Published MCPs (Tier 1) | ≥ 50 |
| Published MCPs (Tier 2) | ≥ 10 |
| Active Users (human + AI agents) | ≥ 1,000 |
| Total Invocations | ≥ 25,000 |
| Creator Earnings (cumulative) | ≥ $5,000 |
| Verified Publishers | ≥ 15 |
| NPS Score | ≥ 40 |
| Average Rating | ≥ 4.2/5 |

---

## Phased Rollout

### Phase 1: Hobbyist MVP (Weeks 1-12)
**Goal:** Launch Tier 1 with 10 invited publishers

**Deliverables:**
- Registry API (POST/GET /mcp)
- Python-only sandbox executor
- Stripe payment integration
- Basic React SPA (search, detail, purchase)
- Provenance ledger (append-only versions table)
- Creator dashboard (upload, view stats)

**Launch:**
- Invite 10 developers from MCP community
- Onboard 5 sample MCPs (free + paid)
- Collect feedback, iterate

---

### Phase 2: Expand & Polish (Weeks 13-24)
**Enhancements:**
- Multi-language support (Node.js, Go)
- Lightning payments (lnbits integration)
- Star ratings + reviews
- Verified Publisher badge workflow
- Usage analytics dashboard

**Growth:**
- Open public sign-ups
- Marketing: blog posts, demos at AI conferences
- Target: 30 MCPs, 500 users

---

### Phase 3: Pro Tier Launch (Weeks 25-36)
**New Feature:** Self-hosted MCP registration

**Publisher Flow:**
1. Register MCP with endpoint URL
2. Platform provides JWT validation library (Python/JS/Go)
3. Publisher integrates JWT check into their server
4. Platform sends paid users to publisher's endpoint

**Revenue Model:**
- 5% payment processing fee
- Publisher can offer direct billing to enterprises

**Migration:**
- Invite top 5 Tier 1 publishers to pilot Tier 2
- Document upgrade process
- Target: 10 Pro MCPs by end of phase

---

### Phase 4: Ecosystem Growth (Months 10-12)
**Advanced Features:**
- MCP chaining/composability (invoke multiple MCPs in sequence)
- Subscription bundles ("Security Toolkit: 5 MCPs for $20/month")
- Community bounties for audits
- AI agent-driven discovery (MCP-as-MCP)
- Enterprise SLAs for Tier 2 publishers

**Scale Targets:**
- 50 Tier 1 + 10 Tier 2 MCPs
- 1,000+ active users
- $5k+ creator earnings

---

## Technical Stack Summary

| Component | Technology |
|-----------|-----------|
| Registry Database | PostgreSQL (with JSON columns for flexible metadata) |
| API Backend | FastAPI (Python) or Express (Node.js) |
| Sandbox Runtime | Docker with resource limits (Python, Node, Go images) |
| Payment Processing | Stripe (fiat), lnbits (Lightning) |
| Front-End | React SPA with Tailwind CSS |
| Auth | JWT (short-lived tokens for invocations) + OAuth for user login |
| Hosting | Railway, Fly.io, or self-hosted VPS |
| Monitoring | Prometheus + Grafana for invocation metrics |
| Logging | Structured JSON logs to stdout (Tier 1 only) |

---

## Why This Model Works

**For Hobbyist Publishers:**
- Zero ops burden → focus on code
- Instant distribution to AI agents
- Passive income from invocations

**For Pro Publishers:**
- Keep 95% of revenue
- Own customer relationships
- Scale independently

**For Consumers:**
- Tier 1 MCPs: reliable, sandboxed, uniform UX
- Tier 2 MCPs: premium features, enterprise SLAs
- Single marketplace for discovery

**For the Ecosystem:**
- Decentralized resilience (no single point of failure)
- Natural competition drives quality
- Clear attribution + provenance prevents rug-pulls
- Bitcoin Lightning enables global micropayments

---

## Next Steps

1. **Validate Assumptions:** Interview 5 MCP developers about pain points, willingness to pay 20% fee
2. **Build Prototype:** Registry API + Python sandbox + Stripe integration (4 weeks)
3. **Recruit Alpha Testers:** 10 publishers, 50 users
4. **Iterate to Beta:** Fix UX issues, add ratings, launch Verified Publisher program
5. **Public Launch:** Blog post, Show HN, AI conference demos

---

## Open Questions

1. **Sandbox networking:** Should Tier 1 MCPs have internet access? (Security vs functionality trade-off)
2. **Pricing models:** Should we support subscriptions in Phase 1, or just per-call?
3. **Lightning node:** Self-host or use custodial service (lnbits.com) initially?
4. **MCP chaining:** Does this belong in the platform, or is it a user-side concern?
5. **Enterprise features:** Should Tier 2 include dedicated support, or is that publisher's responsibility?

---

**TL;DR**

Launch a two-tier MCP marketplace:
- **Tier 1 (Hobbyist):** Platform-hosted, upload code, 20% fee, zero ops
- **Tier 2 (Pro):** Self-hosted, 5% fee, full control

Start with Python-only sandbox, Stripe payments, and provenance ledger. Grow into multi-language, Lightning, verified badges, and community bounties. Empower developers to monetize AI agent tools while keeping the ecosystem decentralized and resilient.
