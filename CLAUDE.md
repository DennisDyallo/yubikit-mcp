# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains **two distinct projects**:

1. **YubiKey MCP Server** (`src/hello-world/`) - An MCP server for YubiKey hardware integration
2. **MCP Marketplace** (`src/mcp-store/`) - A marketplace platform for discovering and monetizing MCPB extensions

---

## Project 1: YubiKey MCP Server

### Overview
An MCP (Model Context Protocol) server that brings hardware-backed cryptographic security to AI agent workflows through YubiKey hardware tokens.

**Backend**: Uses [yubikey-manager](https://github.com/Yubico/yubikey-manager) (ykman) as the underlying library/CLI tool for YubiKey operations.

### Design Philosophy

**Workflow-First Approach**: Design tools around complete user workflows rather than exposing low-level technical operations. Consolidate multi-step processes into single, cohesive tools.

**Example**: Instead of separate `get_certificate`, `sign_hash`, `verify_signature` tools, provide `sign_document` that handles the complete workflow.

### Tool Categories (Workflow-Oriented)
1. **Identity & Authentication**: `authenticate_to_service`, `generate_attestation_certificate`, `verify_identity_proof`
2. **Document Security**: `sign_document`, `encrypt_document`, `verify_document_signature`
3. **Communication Security**: `sign_message`, `encrypt_agent_communication`, `establish_secure_channel`
4. **Credential Management**: `provision_new_credential`, `rotate_expiring_credentials`, `audit_credential_usage`
5. **Two-Factor Operations**: `generate_otp_for_service`, `setup_totp_account`, `backup_oath_credentials`

### MCP Implementation Stack
- **MCP SDK**: Python MCP SDK (`mcp[cli]` package)
- **Server Framework**: FastMCP (high-level) or low-level Server for advanced use
- **Backend**: yubikey-manager (ykman) for YubiKey operations
- **Transport**: stdio (for Claude Desktop) or Streamable HTTP (for remote access)

### Critical MCP Implementation Rules

**Logging (CRITICAL for stdio transport):**
- ❌ NEVER use `print()` - corrupts JSON-RPC messages
- ✅ Use `logging` module which writes to stderr
- ✅ Use `await ctx.info()`, `await ctx.debug()` within tools

**Tool Design:**
- Use workflow-first approach: one tool = one complete workflow
- Example: `sign_document` handles certificate selection, signing, and verification - not separate tools
- Include device_serial parameter with smart defaults (auto-select if only one device)

See full implementation details in original CLAUDE.md sections (omitted for brevity).

---

## Project 2: MCP Marketplace

### Overview

A **registry, discovery platform, and payment gateway** for MCPB (MCP Bundle) extensions. We build on top of Anthropic's official MCPB format rather than creating a competing standard.

**Key Documents:**
- `src/mcp-store/PLAN_v2.md` - Complete marketplace architecture and roadmap
- `src/mcp-store/MCPB_ANALYSIS.md` - MCPB format specification and integration strategy
- `src/mcp-store/ANTHROPIC_BLOG_NOTES.md` - Insights from Anthropic's engineering blog

### Core Philosophy

**Extend, Don't Replace**: Use Anthropic's official MCPB format (`.mcpb` = ZIP with `manifest.json`). The marketplace adds:
- Discovery & search (registry API)
- Monetization (pricing, payments, JWT tokens)
- Provenance & trust (SHA-256 hashing, verified badges, ratings)
- Hosting tiers (platform-hosted vs self-hosted)
- Enterprise features (private registries, SSO, audit logs)

### Two-Tier Model

**Tier 1: Hobbyist (Platform-Hosted)**
- Publisher uploads `.mcpb` bundle
- Platform executes in sandboxed environment
- 20% platform fee (covers hosting, security, payments)
- Zero ops burden for publisher

**Tier 2: Pro (Self-Hosted)**
- Publisher hosts their own MCP server
- Marketplace handles discovery + payments only
- 5% payment processing fee
- Publisher keeps 95% of revenue

### MCPB Format (Official Anthropic Spec)

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

**Manifest.json Required Fields:**
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

**Key MCPB Features:**
- **Multi-language**: Node.js, Python, binary executables
- **User configuration**: 5 input types (string, number, boolean, directory, file)
- **Variable substitution**: `${__dirname}`, `${user_config.api_key}`, `${HOME}`
- **Platform compatibility**: Specify OS (darwin/win32/linux) and runtime versions
- **Tools/prompts**: Declare MCP capabilities in manifest
- **Signing**: PKCS#7 signatures via `mcpb sign`

### Marketplace Architecture

**Database Schema:**
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

**Discovery API:**
```http
GET /api/packages?q=document%20signing&category=security&platform=darwin

Response:
{
  "results": [{
    "id": "uuid",
    "name": "yubikey-signer",
    "version": "1.2.0",
    "description": "Hardware-backed document signing",
    "tools": [{"name": "sign_document", "description": "..."}],
    "tier": "hobbyist",
    "pricing": {"model": "per_call", "amount": 0.10, "currency": "usd"},
    "rating": 4.7,
    "verified": true,
    "bundle_url": "https://cdn.mcpstore.io/bundles/yubikey-signer-1.2.0.mcpb"
  }]
}
```

**Payment Flow:**
1. User purchases extension → Stripe/Lightning payment
2. Marketplace issues JWT: `{sub: user_id, mcp: package_id, exp: 30_days}`
3. **Tier 1**: Platform validates JWT before sandbox execution
4. **Tier 2**: Publisher's server validates JWT (marketplace provides validation library)

### Publisher Workflow

**1. Create MCPB Bundle (Standard Tooling):**
```bash
npm install -g @anthropic-ai/mcpb
cd my-extension/
mcpb init          # Interactive manifest creation
# ... develop server code ...
mcpb validate manifest.json
mcpb pack .        # Creates my-extension.mcpb
```

**2. Publish to Marketplace:**
```bash
npm install -g @mcpstore/cli
mcpstore login
mcpstore publish my-extension.mcpb \
  --pricing per_call \
  --amount 0.10 \
  --tier hobbyist
```

**3. Marketplace Processing:**
- Extract `manifest.json` from `.mcpb`
- Validate MCPB spec compliance (schema version 0.2)
- Compute SHA-256 hash
- Upload to CDN
- Index for search (keywords, tools, description)
- Publish to discovery API

### Consumer Workflow

**Discovery:**
- Browse marketplace website or query API
- Filter by category, platform, pricing, rating

**Installation (Claude Desktop):**
```html
<!-- Deep link from marketplace -->
<a href="claude://install?url=https://mcpstore.io/bundles/my-ext.mcpb">
  Install in Claude Desktop
</a>
```

Claude Desktop:
1. Downloads `.mcpb`
2. Extracts, shows installation dialog
3. User configures fields (API keys, directories, **marketplace JWT**)
4. Auto-registers MCP server in config
5. Server validates JWT on each invocation

### Enterprise Features (High Priority)

**Private Registries:**
- Organizations can host private extension catalogs
- URL: `https://{org-slug}.mcpstore.io`
- SSO/SAML authentication
- Per-seat or per-org licensing

**Security & Compliance:**
- Automated security scans (dependency vulnerabilities)
- Sandbox execution testing (Tier 1)
- Audit logs (who installed what, when)
- SOC2/ISO27001 compliance reporting

**Group Policy Integration:**
- IT admins pre-approve extension allowlists
- Block specific publishers
- Deploy private extensions via MDM

### Quality Assurance Pipeline

When publisher uploads `.mcpb`:
1. **Extract & Validate**: Check manifest against JSON schema
2. **Security Scan**: Check for known vulnerabilities, bundled secrets
3. **Dependency Check**: Ensure all deps bundled (no runtime `npm install`)
4. **Sandbox Test**: Run in network-isolated container, test each tool
5. **Provenance**: Compute SHA-256, store in immutable ledger
6. **Verified Badge**: Manual review after automated checks pass

### Automatic Updates

Extensions can auto-update:

**Update Check API:**
```http
GET /api/packages/{name}/latest
Authorization: Bearer {user_jwt}

Response:
{
  "current_version": "1.2.0",
  "latest_version": "1.3.0",
  "download_url": "https://cdn.mcpstore.io/bundles/my-ext-1.3.0.mcpb",
  "changelog": "## v1.3.0\n- Fixed bug...",
  "breaking_changes": false,
  "requires_payment": false  // Free for existing 1.x users
}
```

**Version Policy:**
- **Patch updates** (1.2.0 → 1.2.1): Free, auto-update
- **Minor updates** (1.2.0 → 1.3.0): Free, auto-update
- **Major updates** (1.0.0 → 2.0.0): Notify user, may require re-purchase

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend API | FastAPI (Python) or Express (Node.js) |
| Database | PostgreSQL with JSONB (for flexible manifest storage) |
| Bundle Storage | S3/Cloudflare R2 (CDN) |
| Payments | Stripe (fiat), lnbits/BTCPay (Lightning) |
| Auth | JWT (short-lived invocation tokens) + OAuth (user login) |
| Frontend | React SPA with Tailwind CSS |
| Hosting | Railway, Fly.io, or self-hosted VPS |
| CLI | Node.js (`@mcpstore/cli`) |

### Competitive Positioning

**Anthropic's Built-In Directory:**
- Curated, free, high-quality
- Slow approval process
- No monetization

**Our Marketplace (Complementary, Not Competing):**
- Open to all developers (instant publishing)
- Monetization (per-call, subscription)
- Enterprise features (private registries, SSO)
- Rich discovery (ratings, reviews, analytics)
- Automatic updates

**Users get:**
- Free basics from Anthropic
- Premium/niche tools from marketplace
- Enterprise features from our private registry tier

### Key Insights from Anthropic Engineering

**From Official Blog Post:**
1. **Deep Linking**: `claude://install?url=...` enables one-click installation
2. **Secrets Management**: Claude Desktop stores `sensitive: true` fields in OS keychain
3. **Enterprise Controls**: Group Policy, MDM, pre-approved lists, publisher blocklisting
4. **Multi-Platform**: macOS, Windows, Linux support via `compatibility.platforms`
5. **Community Evolution**: Spec versioned as 0.1 → 0.2 → future versions (open to contributions)

### Implementation Guidelines

**When Working on Marketplace:**
1. **Use official MCPB tooling**: Don't reinvent `@anthropic-ai/mcpb` CLI
2. **Store metadata separately**: Don't modify `.mcpb` files, keep marketplace data in database
3. **Validate against schema**: Support multiple manifest versions (0.1, 0.2, future)
4. **Respect MCPB spec**: Backward compatibility is critical
5. **Focus on value-add**: Discovery, payments, trust, not packaging format

**When Building Features:**
- **Discovery**: User-friendly categories (not technical jargon)
- **Security**: Automated scans, sandbox testing, verified badges
- **UX**: One-click install, clear pricing, screenshot requirements
- **Enterprise**: SSO, audit logs, private registries, compliance reporting

### Success Metrics (12 Months)

| Metric | Target |
|--------|--------|
| Published Extensions (Tier 1) | ≥ 50 |
| Published Extensions (Tier 2) | ≥ 10 |
| Active Users | ≥ 1,000 |
| Total Invocations | ≥ 25,000 |
| Creator Earnings | ≥ $5,000 |
| Verified Publishers | ≥ 15 |
| NPS Score | ≥ 40 |

---

## Development Workflow

### For YubiKey MCP Server:
```bash
cd src/hello-world/
uv sync
uv run mcp dev server.py
```

### For MCP Marketplace:
```bash
cd src/mcp-store/
# Future: Backend API, database setup, frontend build
```

### Configuration Files

- `.mcp.json` - Claude Code MCP server config (YubiKey server)
- `.vscode/mcp.json` - VS Code/Copilot MCP config
- `src/mcp-store/PLAN_v2.md` - Marketplace architecture doc
- `src/mcp-store/MCPB_ANALYSIS.md` - MCPB spec deep dive

---

## Important Reminders

**For YubiKey MCP Development:**
- Never use `print()` in MCP servers (use `logging`)
- Handle multiple devices gracefully (`device_serial` parameter)
- Design workflow-first tools (complete user workflows)

**For Marketplace Development:**
- Don't create competing package format (use MCPB)
- Store marketplace metadata separately (not in `.mcpb`)
- Validate against official MCPB JSON schema
- Focus on discovery, payments, trust (not packaging)
- Build for enterprise from day one (private registries = high ROI)

---

## Next Steps

**YubiKey MCP Server:**
1. Expand beyond hello-world (OATH, PIV, signing tools)
2. Add authentication (OAuth 2.1 + JWT)
3. Implement audit logging

**MCP Marketplace:**
1. Prototype discovery API (FastAPI + PostgreSQL)
2. Design marketplace website (React SPA)
3. Build quality pipeline (security scans, sandbox testing)
4. Implement payment flow (Stripe integration)
5. Create publisher CLI (`@mcpstore/cli`)
6. Launch enterprise tier (private registries, SSO)

Both projects share the MCP ecosystem but serve different purposes:
- **YubiKey MCP**: Example extension (can be published to marketplace)
- **Marketplace**: Platform for all MCPB extensions (including YubiKey MCP)
