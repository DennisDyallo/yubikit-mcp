# MCP Marketplace

> A discovery platform and payment gateway for MCPB (MCP Bundle) extensions

**Status:** 📋 Planning Phase - Architecture Complete

---

## Vision

Create a trusted marketplace where developers can publish, monetize, and distribute MCP servers built on Anthropic's official MCPB format.

**We're not creating a competing package format.** We extend the official `.mcpb` (MCP Bundle) standard with:

- 🔍 **Discovery** - Search registry with filters (category, platform, pricing, rating)
- 💰 **Monetization** - Per-call pricing, subscriptions, Lightning micropayments
- 🔐 **Trust** - SHA-256 provenance, verified publisher badges, ratings
- 🏢 **Enterprise** - Private registries, SSO, audit logs, compliance reporting

---

## Two-Tier Model

### Tier 1: Hobbyist (Platform-Hosted)

**For indie developers who want zero ops burden:**
- Publisher uploads `.mcpb` bundle
- Platform executes in sandboxed environment
- 20% platform fee (covers hosting, security, payments)
- Automatic scaling and monitoring

**Example:**
```bash
mcpstore publish my-extension.mcpb --pricing per_call --amount 0.10 --tier hobbyist
```

### Tier 2: Pro (Self-Hosted)

**For established publishers who want full control:**
- Publisher hosts their own MCP server
- Marketplace handles discovery + payments only
- 5% payment processing fee
- Publisher keeps 95% of revenue
- Full infrastructure control

**Example:**
```bash
mcpstore publish my-extension.mcpb --tier pro --endpoint https://my-server.com/mcp
```

---

## Quick Start Guide

### For Publishers

**1. Create MCPB Bundle (Standard Workflow):**
```bash
# Install official MCPB CLI
npm install -g @anthropic-ai/mcpb

# Initialize project
cd my-extension/
mcpb init          # Interactive manifest creation

# Develop your MCP server
# ... write server code ...

# Validate and pack
mcpb validate manifest.json
mcpb pack .        # Creates my-extension.mcpb
```

**2. Publish to Marketplace:**
```bash
# Install marketplace CLI
npm install -g @mcpstore/cli

# Authenticate
mcpstore login

# Publish with pricing
mcpstore publish my-extension.mcpb \
  --pricing per_call \
  --amount 0.10 \
  --tier hobbyist
```

**3. Track Performance:**
```bash
mcpstore stats my-extension
# Shows: invocations, revenue, ratings, top users
```

### For Consumers

**1. Discover Extensions:**
- Browse marketplace website: `https://mcpstore.io`
- Search by category, platform, rating
- Filter by pricing, compatibility

**2. Purchase & Install:**
```html
<!-- One-click installation via deep link -->
<a href="claude://install?url=https://mcpstore.io/bundles/my-ext.mcpb">
  Install in Claude Desktop
</a>
```

**Flow:**
1. Click "Install" on marketplace
2. Redirects to `claude://install?url=...`
3. Claude Desktop downloads `.mcpb`
4. Shows installation dialog with permissions
5. User configures fields (API keys, marketplace JWT)
6. Extension ready to use

---

## Key Features

### For Publishers

✅ **Instant Publishing** - No approval delay (unlike Anthropic's built-in directory)
✅ **Flexible Pricing** - Free, per-call ($0.01-$10), or subscription ($5-$100/month)
✅ **Revenue Analytics** - Dashboard showing invocations, earnings, top users
✅ **Automatic Updates** - Semver-based update notifications
✅ **Private Registries** - Enterprise feature for org-specific catalogs

### For Consumers

✅ **Powerful Search** - Filter by category, platform (macOS/Windows/Linux), rating
✅ **One-Click Install** - Deep link integration with Claude Desktop
✅ **Secure Payments** - Stripe (cards) + Lightning (micropayments)
✅ **Community Reviews** - Star ratings, comments, verified badges
✅ **Auto-Updates** - Patch/minor versions update automatically

### For Enterprises

✅ **Private Registries** - `https://acme.mcpstore.io` for internal extensions
✅ **SSO/SAML** - Enterprise authentication integration
✅ **Group Policy** - IT admins control approved extensions
✅ **Audit Logs** - Track who installed what, when
✅ **Compliance** - SOC2/ISO27001 reporting

---

## Technical Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│   Publisher     │ Upload  │   Marketplace    │ Browse  │   Consumer  │
│  (creates .mcpb)│────────►│  (registry + pay)│◄────────│  (installs) │
└─────────────────┘         └──────────────────┘         └─────────────┘
                                     │
                                     ├─ Discovery API (search, filter)
                                     ├─ Payment Gateway (Stripe, Lightning)
                                     ├─ Provenance Ledger (SHA-256 hashing)
                                     ├─ CDN (bundle hosting)
                                     └─ JWT Issuance (usage tokens)
```

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend API | FastAPI (Python) or Express (Node.js) |
| Database | PostgreSQL with JSONB (flexible manifest storage) |
| Bundle Storage | S3/Cloudflare R2 (CDN) |
| Payments | Stripe (fiat), lnbits/BTCPay (Lightning) |
| Auth | JWT (invocation tokens) + OAuth (user login) |
| Frontend | React SPA with Tailwind CSS |
| Hosting | Railway, Fly.io, or self-hosted VPS |
| CLI | Node.js (`@mcpstore/cli`) |

### Database Schema

```sql
CREATE TABLE packages (
  id UUID PRIMARY KEY,

  -- MCPB Manifest Fields (extracted from manifest.json)
  name TEXT NOT NULL,
  display_name TEXT,
  version TEXT NOT NULL,
  description TEXT,
  author_name TEXT,
  tools JSONB,           -- [{name, description}]
  keywords TEXT[],
  license TEXT,

  -- MCPB Compatibility
  platforms TEXT[],      -- darwin, win32, linux
  runtimes JSONB,        -- {node: ">=16.0.0", python: ">=3.8"}

  -- Marketplace Extensions
  tier TEXT DEFAULT 'hobbyist',  -- hobbyist | pro
  pricing_model TEXT,            -- free | per_call | subscription
  price_amount DECIMAL,
  price_currency TEXT,           -- usd | eur | sat

  bundle_hash TEXT UNIQUE,       -- SHA-256 of .mcpb file
  bundle_url TEXT,               -- CDN URL

  publisher_id UUID REFERENCES users(id),
  verified BOOLEAN DEFAULT FALSE,

  -- Tier 2 only
  self_hosted_endpoint TEXT,

  -- Stats
  total_invocations BIGINT DEFAULT 0,
  avg_rating DECIMAL,

  published_at TIMESTAMP,
  UNIQUE(publisher_id, name, version)
);
```

### Discovery API

**Endpoint:** `GET /api/packages?q=&category=&platform=&pricing=`

**Example Response:**
```json
{
  "results": [{
    "id": "abc-123",
    "name": "yubikey-signer",
    "display_name": "YubiKey Document Signer",
    "version": "1.2.0",
    "description": "Hardware-backed document signing",
    "author": {"name": "Alice", "email": "alice@example.com"},

    "tools": [
      {"name": "sign_document", "description": "Sign PDF/contract with YubiKey"},
      {"name": "verify_signature", "description": "Verify document authenticity"}
    ],

    "keywords": ["security", "signing", "yubikey", "pki"],
    "license": "MIT",

    "compatibility": {
      "platforms": ["darwin", "win32", "linux"],
      "runtimes": {"python": ">=3.11"}
    },

    "tier": "hobbyist",
    "pricing": {"model": "per_call", "amount": 0.10, "currency": "usd"},
    "rating": 4.7,
    "invocations": 8421,
    "verified": true,

    "bundle_url": "https://cdn.mcpstore.io/bundles/yubikey-signer-1.2.0.mcpb",
    "bundle_hash": "sha256:abc123..."
  }]
}
```

### Payment Flow

**Purchase & JWT Issuance:**
1. User clicks "Purchase Access" on package page
2. Marketplace creates Stripe Checkout / Lightning invoice
3. On payment success:
   - Issue JWT: `{sub: user_id, mcp: package_id, exp: 30_days, tier: "paid"}`
   - Store in database for validation
4. User receives JWT token

**Tier 1 (Platform-Hosted) Validation:**
```
User → https://api.mcpstore.io/invoke/yubikey-signer
       Authorization: Bearer {JWT}
     → Platform validates JWT
     → Executes in sandbox
     → Returns result
```

**Tier 2 (Self-Hosted) Validation:**
```javascript
// Publisher's server validates JWT
const { validateToken } = require('@mcpstore/jwt-validator');

server.setRequestHandler(async (request) => {
  const token = request.headers['authorization']?.split(' ')[1];
  const valid = await validateToken(token, {
    publicKey: MCPSTORE_PUBLIC_KEY,
    package: 'yubikey-signer'
  });

  if (!valid) throw new Error('Unauthorized');
  // Process request...
});
```

---

## MCPB Format Overview

### What is MCPB?

**MCP Bundle (MCPB)** is Anthropic's official packaging format for distributing MCP servers. It's spiritually similar to Chrome extensions (`.crx`) or VS Code extensions (`.vsix`).

**Package Structure:**
```
my-extension.mcpb (ZIP file)
├── manifest.json          # Required: metadata, server config, user_config
├── server/
│   └── index.js           # Entry point (Node/Python/Binary)
├── node_modules/          # Bundled dependencies
├── icon.png               # Optional icon
└── assets/                # Optional assets
```

### Manifest.json Required Fields

```json
{
  "manifest_version": "0.2",
  "name": "my-extension",
  "version": "1.0.0",
  "description": "Brief description",
  "author": {"name": "Author Name"},
  "server": {
    "type": "node",  // node | python | binary
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"],
      "env": {}
    }
  }
}
```

### Key MCPB Features

**Multi-Language Support:**
- Node.js (recommended - ships with Claude Desktop)
- Python (requires user to have Python installed)
- Binary (compiled executables, platform-specific)

**User Configuration:**
- 5 input types: `string`, `number`, `boolean`, `directory`, `file`
- Sensitive fields stored in OS keychain
- Variable substitution: `${user_config.api_key}`, `${HOME}`, `${__dirname}`

**Platform Compatibility:**
- Declare supported OS: `["darwin", "win32", "linux"]`
- Runtime version constraints: `{node: ">=16.0.0", python: ">=3.8"}`

**Signing & Verification:**
- PKCS#7 digital signatures
- Command: `mcpb sign my-extension.mcpb`

---

## Marketplace vs Anthropic's Built-In Directory

### Anthropic's Built-In Directory

**Pros:**
- ✅ Curated, high-quality extensions
- ✅ Free for users
- ✅ Installed by default with Claude Desktop

**Cons:**
- ❌ Limited selection
- ❌ Slow approval process
- ❌ No monetization for developers

### Our Marketplace (Complementary)

**Pros:**
- ✅ Open to all developers (instant publishing)
- ✅ Monetization (per-call, subscription)
- ✅ Enterprise features (private registries, SSO)
- ✅ Rich discovery (ratings, reviews, analytics)
- ✅ Automatic updates

**Positioning:**
We **don't compete** with Anthropic—we **complement** them:
- Users get free basics from Anthropic
- Users get premium/niche tools from marketplace
- Enterprises use private registries for internal tools

---

## Quality Assurance Pipeline

When publisher uploads `.mcpb`, marketplace automatically:

1. **Extract & Validate**
   - Unzip `.mcpb` file
   - Parse `manifest.json`
   - Validate against MCPB JSON schema (v0.2)

2. **Security Scan**
   - Check for known vulnerabilities (npm audit, safety)
   - Scan for bundled secrets (.env files, API keys)
   - Verify no external network calls during install

3. **Dependency Check**
   - Ensure all dependencies bundled (no runtime `npm install`)
   - Validate bundled `node_modules/` or `lib/` directory

4. **Sandbox Test** (Tier 1 only)
   - Run in network-isolated container
   - Test each declared tool, check for errors
   - Verify resource limits (512MB RAM, 5s timeout)

5. **Provenance**
   - Compute SHA-256 hash of entire `.mcpb` file
   - Store in immutable `package_versions` table
   - Return hash to publisher for verification

6. **Verified Badge** (Optional)
   - Manual review after automated checks pass
   - Code quality, security best practices
   - Responsive support, clear documentation

---

## Enterprise Features

### Private Registries

**Use Case:** Organizations want internal-only extensions

**Architecture:**
- URL: `https://{org-slug}.mcpstore.io`
- Isolated database schema (multi-tenancy)
- SSO/SAML authentication
- Per-seat or per-org pricing

**Workflow:**
```bash
# Publisher creates private extension
mcpstore publish my-internal-tool.mcpb \
  --visibility private \
  --organization acme-corp

# Only acme-corp employees can discover/install
```

### Group Policy Integration

**Use Case:** IT admins control approved extensions

**Features:**
- Pre-approved extension allowlists
- Publisher blocklisting
- Automatic deployment via MDM
- Audit logs (who installed what, when)

**Example Policy (JSON):**
```json
{
  "allowed_extensions": ["yubikey-signer", "database-connector"],
  "blocked_publishers": ["suspicious-dev"],
  "auto_install": ["company-internal-tools"],
  "require_verification": true
}
```

### Compliance & Audit Logs

**SOC2/ISO27001 Reporting:**
- Extension installation events
- User access logs
- Revenue transactions
- Security scan results

**Audit Log Schema:**
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  timestamp TIMESTAMP,
  organization_id UUID,
  user_id UUID,
  event_type TEXT,  -- install, uninstall, invoke, update
  package_id UUID,
  metadata JSONB,
  ip_address INET
);
```

---

## Automatic Updates

Extensions can auto-update based on semver:

**Update Check API:**
```http
GET /api/packages/{name}/latest
Authorization: Bearer {user_jwt}

Response:
{
  "current_version": "1.2.0",
  "latest_version": "1.3.0",
  "download_url": "https://cdn.mcpstore.io/bundles/my-ext-1.3.0.mcpb",
  "changelog": "## v1.3.0\n- Fixed critical bug\n- Added new tool",
  "breaking_changes": false,
  "requires_payment": false  // Free for existing 1.x users
}
```

**Version Policy:**
- **Patch** (1.2.0 → 1.2.1): Auto-update, free
- **Minor** (1.2.0 → 1.3.0): Auto-update, free
- **Major** (1.0.0 → 2.0.0): Notify user, may require re-purchase

---

## Success Metrics (12 Months)

| Metric | Target |
|--------|--------|
| Published Extensions (Tier 1) | ≥ 50 |
| Published Extensions (Tier 2) | ≥ 10 |
| Active Users | ≥ 1,000 |
| Total Invocations | ≥ 25,000 |
| Creator Earnings (cumulative) | ≥ $5,000 |
| Verified Publishers | ≥ 15 |
| NPS Score | ≥ 40 |
| Average Rating | ≥ 4.2/5 |

---

## Planning Documents

- **[PLAN_v2.md](PLAN_v2.md)** - Complete architecture, phased rollout, technical stack
- **[MCPB_ANALYSIS.md](MCPB_ANALYSIS.md)** - Deep dive into MCPB format, integration strategy
- **[ANTHROPIC_BLOG_NOTES.md](ANTHROPIC_BLOG_NOTES.md)** - Insights from Anthropic's engineering blog

---

## Next Steps

### Phase 1: MVP (Weeks 1-12)

**Backend:**
1. Set up FastAPI + PostgreSQL
2. Implement package upload endpoint
3. Build discovery API (search, filter)
4. Integrate Stripe payments
5. JWT issuance on payment success

**Frontend:**
1. Design React SPA (search, detail pages)
2. Build publisher dashboard (upload, stats)
3. Implement deep link handling (`claude://install?url=...`)

**Quality Pipeline:**
1. MCPB manifest validation (JSON schema)
2. Security scanning (npm audit, safety)
3. Sandbox execution testing (Tier 1)

### Phase 2: Growth (Weeks 13-24)

**Features:**
1. Lightning payment integration (lnbits)
2. Automatic updates (version check API)
3. Star ratings & reviews
4. Verified Publisher badge workflow

**Growth:**
1. Open public sign-ups
2. Onboard 30 publishers
3. Target 500 users

### Phase 3: Enterprise (Weeks 25-36)

**Enterprise Features:**
1. Private registries (multi-tenancy)
2. SSO/SAML integration
3. Group Policy support
4. Audit logs & compliance reporting

**Tier 2 Launch:**
1. Self-hosted publisher onboarding
2. JWT validation library (`@mcpstore/jwt-validator`)
3. Documentation for Tier 2 integration

---

## Contributing

This is a planning-phase project. Contributions welcome:

1. **Architecture Review** - Feedback on PLAN_v2.md
2. **Backend Development** - FastAPI/Express implementation
3. **Frontend Design** - React SPA, UX/UI
4. **CLI Tool** - `@mcpstore/cli` implementation
5. **Documentation** - Guides for publishers and consumers

---

## Resources

**MCPB Ecosystem:**
- [MCPB Specification](https://github.com/anthropics/mcpb) - Official bundle format
- [Anthropic Engineering Blog](https://www.anthropic.com/engineering/desktop-extensions) - MCPB deep dive
- [Claude Desktop](https://claude.ai/download) - Native MCPB support

**MCP Protocol:**
- [MCP Documentation](https://modelcontextprotocol.io/) - Official protocol docs
- [FastMCP Python SDK](https://github.com/jlowin/fastmcp) - Framework for MCP servers

**Marketplace Inspiration:**
- [npm Registry](https://www.npmjs.com/) - Package discovery
- [VS Code Marketplace](https://marketplace.visualstudio.com/) - Extension monetization
- [Chrome Web Store](https://chrome.google.com/webstore) - User trust signals

---

## License

[Specify your license here]

## Contact

- **Issues:** [GitHub Issues](https://github.com/yourusername/yubikit-mcp/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/yubikit-mcp/discussions)

---

**Built with ❤️ to empower MCP developers**

*Empowering developers to monetize their MCP innovations while maintaining the open ecosystem*
