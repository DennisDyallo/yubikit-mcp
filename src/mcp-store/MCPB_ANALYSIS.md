# MCPB Format Analysis for Marketplace Integration

## Overview

Anthropic's official **MCP Bundle (MCPB)** format is the standard for distributing MCP servers. Our marketplace should build on this foundation rather than creating a competing format.

---

## MCPB Specification Summary

### Package Structure

**File Format:** `.mcpb` files are **ZIP archives** (not tarballs) containing:
- `manifest.json` (required) - metadata and configuration
- Server code (entry point specified in manifest)
- Dependencies (bundled node_modules, Python lib/, or static binaries)
- Optional assets (icon.png, screenshots, docs)

**Example Structure:**
```
my-extension.mcpb (ZIP)
├── manifest.json          # Required manifest
├── server/
│   └── index.js           # Entry point
├── node_modules/          # Bundled dependencies
├── icon.png               # Optional icon
└── assets/                # Optional assets
```

---

## Manifest.json Schema (v0.2)

### Required Fields

```json
{
  "manifest_version": "0.2",
  "name": "my-extension",                    // Machine-readable (lowercase, hyphens)
  "version": "1.0.0",                        // Semantic versioning
  "description": "Brief description",
  "author": {
    "name": "Author Name"                    // Required
  },
  "server": {
    "type": "node",                          // node | python | binary
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"],
      "env": {}
    }
  }
}
```

### Key Optional Fields

```json
{
  "display_name": "Human-Friendly Name",
  "long_description": "Markdown-supported detailed description",
  "icon": "icon.png",
  "screenshots": ["assets/screenshot1.png"],
  "homepage": "https://example.com",
  "repository": {"type": "git", "url": "..."},
  "documentation": "https://docs.example.com",
  "keywords": ["search", "terms"],
  "license": "MIT",

  "tools": [
    {"name": "tool_name", "description": "What it does"}
  ],
  "tools_generated": true,  // Server generates additional tools at runtime

  "prompts": [
    {
      "name": "prompt_name",
      "description": "What it does",
      "arguments": ["arg1", "arg2"],
      "text": "Prompt template with ${arguments.arg1}"
    }
  ],
  "prompts_generated": true,

  "compatibility": {
    "claude_desktop": ">=0.10.0",
    "platforms": ["darwin", "win32", "linux"],
    "runtimes": {
      "node": ">=16.0.0",
      "python": ">=3.8"
    }
  },

  "user_config": {
    "api_key": {
      "type": "string",              // string | number | boolean | directory | file
      "title": "API Key",
      "description": "Your API key",
      "sensitive": true,             // Mask input, store securely
      "required": true,
      "default": "value"
    }
  },

  "privacy_policies": ["https://example.com/privacy"]
}
```

### Server Types

1. **Node.js** (`type: "node"`)
   - Entry point: JavaScript file
   - Dependencies: Bundled `node_modules/`
   - Runtime: Node.js (version in `compatibility.runtimes.node`)

2. **Python** (`type: "python"`)
   - Entry point: Python file
   - Dependencies: `server/lib/` or `server/venv/`
   - Runtime: Python (version in `compatibility.runtimes.python`)
   - Set `PYTHONPATH` in `mcp_config.env`

3. **Binary** (`type: "binary"`)
   - Entry point: Compiled executable
   - Dependencies: Statically linked or bundled
   - Platform-specific binaries supported
   - No runtime requirements

### Variable Substitution

Manifest supports template variables in `mcp_config`:

- `${__dirname}` - Extension's installation directory
- `${HOME}` - User's home directory
- `${DESKTOP}`, `${DOCUMENTS}`, `${DOWNLOADS}` - User directories
- `${/}` or `${pathSeparator}` - Platform path separator
- `${user_config.KEY}` - User-configured values

**Example:**
```json
"mcp_config": {
  "command": "python",
  "args": ["${__dirname}/server/main.py"],
  "env": {
    "CONFIG_PATH": "${__dirname}/config.json",
    "API_KEY": "${user_config.api_key}"
  }
}
```

### User Configuration

Supports 5 input types:

| Type | Use Case | Properties |
|------|----------|------------|
| `string` | Text input | `sensitive` (bool), `default` |
| `number` | Numeric input | `min`, `max`, `default` |
| `boolean` | Toggle/checkbox | `default` |
| `directory` | Directory picker | `multiple` (bool), `default` |
| `file` | File picker | `multiple` (bool), `default` |

**Array Expansion:**
If `user_config.dirs` has `multiple: true` and user selects `["/path1", "/path2"]`:
```json
"args": ["${user_config.dirs}"]
// Expands to: ["/path1", "/path2"]
```

---

## CLI Tool: `@anthropic-ai/mcpb`

### Installation
```bash
npm install -g @anthropic-ai/mcpb
```

### Key Commands

```bash
mcpb init [directory]          # Interactive manifest creation
mcpb validate <manifest.json>  # Validate manifest
mcpb pack <directory>          # Create .mcpb bundle (ZIP)
mcpb sign <file.mcpb>          # PGP/PKCS#7 signing
mcpb verify <file.mcpb>        # Verify signature
mcpb info <file.mcpb>          # Display bundle metadata
mcpb unsign <file.mcpb>        # Remove signature
```

### Workflow
1. `mcpb init` → Create `manifest.json`
2. Develop server code
3. `mcpb validate manifest.json`
4. `mcpb pack .` → Generate `.mcpb` file
5. (Optional) `mcpb sign bundle.mcpb`

---

## Integration Points for Marketplace

### What MCPB Already Provides

✅ **Standard package format** (.mcpb = ZIP with manifest.json)
✅ **Rich metadata** (author, description, tools, keywords)
✅ **Dependency bundling** (node_modules, Python libs, binaries)
✅ **User configuration** (5 input types, sensitive fields, validation)
✅ **Compatibility checks** (platform, runtime, client version)
✅ **Signing/verification** (PKCS#7 signatures)
✅ **Multi-language support** (Node, Python, binaries)
✅ **Variable substitution** (portable paths)
✅ **Tool/prompt discovery** (static + dynamic generation)

### What Marketplace Adds

Our marketplace layers on top of MCPB:

1. **Discovery & Search**
   - Registry API indexing manifest metadata (keywords, tools, categories)
   - Search by tool name, description, author, category
   - Filtering by platform, runtime, pricing

2. **Monetization**
   - Pricing metadata (not in MCPB spec)
   - Payment processing (Stripe, Lightning)
   - Usage-token (JWT) for paid invocations
   - Revenue sharing (80/20 or 95/5 split)

3. **Provenance & Trust**
   - SHA-256 hash of entire `.mcpb` file
   - Append-only ledger of versions
   - Verified Publisher badges
   - Community ratings/reviews

4. **Hosting Tiers**
   - **Tier 1 (Hobbyist):** Platform-hosted execution sandbox
   - **Tier 2 (Pro):** Self-hosted, marketplace handles discovery + payments

5. **Analytics**
   - Invocation tracking
   - Revenue dashboards
   - Usage statistics

---

## Extended Manifest Schema for Marketplace

We **extend** (not replace) MCPB manifest with marketplace-specific fields:

```json
{
  // Standard MCPB fields (unchanged)
  "manifest_version": "0.2",
  "name": "my-extension",
  "version": "1.0.0",
  // ... all MCPB fields ...

  // MARKETPLACE EXTENSIONS (new fields)
  "marketplace": {
    "tier": "hobbyist",                    // hobbyist | pro
    "pricing": {
      "model": "per_call",                 // free | per_call | subscription
      "amount": 0.10,
      "currency": "usd"                    // usd | eur | sat
    },
    "categories": ["security", "crypto"],  // Marketplace-specific categories
    "bundle_hash": "sha256:abc123...",     // Computed by marketplace
    "published_at": "2025-10-05T14:00:00Z",
    "publisher_id": "user-uuid",
    "verified": false,                     // Verified Publisher badge
    "self_hosted_endpoint": null           // For Tier 2: publisher's URL
  }
}
```

**Storage Strategy:**
- Original MCPB manifest remains untouched in `.mcpb` file
- Marketplace metadata stored in **separate database table**
- Linked by `bundle_hash` or `marketplace.publisher_id + name + version`

---

## Marketplace Architecture (MCPB-Compatible)

### 1. Package Upload Flow

```
Publisher → mcpb pack . → my-extension.mcpb
         → Upload to marketplace
         → Marketplace extracts manifest.json
         → Validates MCPB spec compliance
         → Computes SHA-256 hash
         → Stores .mcpb file + metadata in registry
         → Publishes to discovery API
```

### 2. Discovery API

**Endpoint:** `GET /api/packages?q=&category=&tier=&platform=`

**Response:**
```json
{
  "results": [
    {
      "id": "uuid",
      "name": "yubikey-signer",
      "display_name": "YubiKey Document Signer",
      "version": "1.2.0",
      "description": "Hardware-backed document signing",
      "author": {"name": "Alice", "url": "..."},
      "icon": "https://cdn.mcpstore.io/icons/yubikey-signer.png",

      // MCPB metadata
      "tools": [
        {"name": "sign_document", "description": "..."}
      ],
      "keywords": ["security", "signing"],
      "license": "MIT",
      "compatibility": {
        "platforms": ["darwin", "win32", "linux"],
        "runtimes": {"python": ">=3.11"}
      },

      // Marketplace metadata
      "tier": "hobbyist",
      "pricing": {"model": "per_call", "amount": 0.10, "currency": "usd"},
      "rating": 4.7,
      "invocations": 8421,
      "verified": true,
      "bundle_url": "https://cdn.mcpstore.io/bundles/yubikey-signer-1.2.0.mcpb",
      "bundle_hash": "sha256:abc123..."
    }
  ]
}
```

### 3. Installation Flow

**Tier 1 (Platform-Hosted):**
```
User → Search marketplace → Select package → Pay
     → Marketplace issues JWT (valid 30 days)
     → User downloads .mcpb OR uses platform endpoint
     → Platform executes in sandbox, validates JWT
```

**Tier 2 (Self-Hosted):**
```
User → Search marketplace → Select package → Pay
     → Marketplace issues JWT
     → User downloads .mcpb
     → Installs locally (Claude Desktop or custom client)
     → MCP server validates JWT via marketplace public key
```

### 4. Payment & JWT

**Flow:**
1. User clicks "Purchase Access" on package page
2. Marketplace creates Stripe Checkout / Lightning invoice
3. On payment success:
   ```json
   JWT Payload:
   {
     "sub": "user-uuid",
     "mcp": "yubikey-signer",
     "version": "1.2.0",
     "tier": "paid",
     "exp": 1735689600,  // 30 days
     "iss": "mcpstore.io"
   }
   ```
4. **Tier 1:** Platform sandbox validates JWT before execution
5. **Tier 2:** Publisher's server validates JWT (marketplace provides validation library)

---

## Database Schema (Marketplace Layer)

### Packages Table

```sql
CREATE TABLE packages (
  id UUID PRIMARY KEY,

  -- MCPB Manifest Fields (extracted from manifest.json)
  name TEXT NOT NULL,
  display_name TEXT,
  version TEXT NOT NULL,
  description TEXT,
  long_description TEXT,
  author_name TEXT,
  author_email TEXT,
  author_url TEXT,
  homepage TEXT,
  repository_url TEXT,
  documentation TEXT,
  icon TEXT,
  screenshots TEXT[],
  keywords TEXT[],
  license TEXT,

  -- MCPB Server Config
  server_type TEXT,  -- node | python | binary
  entry_point TEXT,
  tools JSONB,       -- Array of {name, description}
  tools_generated BOOLEAN DEFAULT FALSE,
  prompts JSONB,
  prompts_generated BOOLEAN DEFAULT FALSE,

  -- MCPB Compatibility
  platforms TEXT[],  -- darwin, win32, linux
  runtimes JSONB,    -- {node: ">=16.0.0", python: ">=3.8"}

  -- Marketplace Extensions
  tier TEXT NOT NULL DEFAULT 'hobbyist',  -- hobbyist | pro
  pricing_model TEXT,  -- free | per_call | subscription
  price_amount DECIMAL,
  price_currency TEXT,

  bundle_hash TEXT UNIQUE NOT NULL,  -- SHA-256 of .mcpb file
  bundle_url TEXT,  -- CDN URL to .mcpb file
  bundle_size_bytes BIGINT,

  publisher_id UUID REFERENCES users(id),
  verified BOOLEAN DEFAULT FALSE,
  published_at TIMESTAMP,

  -- Tier 2 only
  self_hosted_endpoint TEXT,  -- Publisher's MCP server URL

  -- Stats (computed)
  total_invocations BIGINT DEFAULT 0,
  avg_rating DECIMAL,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(publisher_id, name, version)
);

CREATE INDEX idx_packages_search ON packages USING GIN(to_tsvector('english', name || ' ' || description || ' ' || keywords));
CREATE INDEX idx_packages_tier ON packages(tier);
CREATE INDEX idx_packages_pricing ON packages(pricing_model);
```

### Version History (Provenance Ledger)

```sql
CREATE TABLE package_versions (
  id UUID PRIMARY KEY,
  package_id UUID REFERENCES packages(id),
  version TEXT NOT NULL,
  bundle_hash TEXT NOT NULL,  -- Immutable provenance
  manifest_json JSONB,        -- Full manifest snapshot
  changelog TEXT,
  published_at TIMESTAMP,

  -- Optional PGP signature
  signature_algorithm TEXT,
  signature_fingerprint TEXT,
  signature TEXT,

  UNIQUE(package_id, version)
);
```

### Ratings & Reviews

```sql
CREATE TABLE ratings (
  id UUID PRIMARY KEY,
  package_id UUID REFERENCES packages(id),
  user_id UUID REFERENCES users(id),
  stars INT CHECK (stars BETWEEN 1 AND 5),
  comment TEXT,
  created_at TIMESTAMP,

  UNIQUE(package_id, user_id)
);
```

### Invocations (Analytics)

```sql
CREATE TABLE invocations (
  id UUID PRIMARY KEY,
  package_id UUID REFERENCES packages(id),
  user_id UUID REFERENCES users(id),
  timestamp TIMESTAMP,
  duration_ms INT,
  success BOOLEAN,
  tier TEXT,  -- hobbyist | pro
  revenue_usd DECIMAL,  -- For revenue tracking

  INDEX idx_invocations_package (package_id, timestamp),
  INDEX idx_invocations_user (user_id, timestamp)
);
```

---

## Publisher Workflow

### 1. Create MCPB Bundle (Standard)

```bash
cd my-mcp-server/
mcpb init  # Interactive manifest creation
# ... develop server code ...
mcpb validate manifest.json
mcpb pack .  # Creates my-extension.mcpb
```

### 2. Publish to Marketplace

**Option A: Web Upload**
```
1. Login to mcpstore.io
2. Click "Publish Extension"
3. Upload .mcpb file
4. Set pricing (free / $0.10 per call / etc.)
5. Select tier (Hobbyist / Pro)
6. Submit for review
```

**Option B: CLI**
```bash
npm install -g @mcpstore/cli

mcpstore login
mcpstore publish my-extension.mcpb \
  --pricing per_call \
  --amount 0.10 \
  --tier hobbyist
```

### 3. Marketplace Processing

```
1. Extract manifest.json from .mcpb
2. Validate MCPB spec compliance
3. Compute SHA-256 hash
4. Upload .mcpb to CDN (S3/Cloudflare)
5. Insert metadata into packages table
6. Index for search (keywords, tools, description)
7. Publish to discovery API
```

---

## Consumer Workflow

### 1. Discovery

**Web:**
```
Browse mcpstore.io → Search "document signing"
→ Find "YubiKey Document Signer" → View details
```

**API (for AI agents):**
```bash
GET /api/packages?q=document%20signing&category=security

# Returns: [{name, description, tools, pricing, bundle_url, ...}]
```

**MCP-as-Discovery:**
```python
# Marketplace itself as an MCP server
@mcp.tool()
async def search_packages(query: str) -> list[dict]:
    """Search MCP marketplace for extensions."""
    # AI agent queries marketplace via MCP protocol
```

### 2. Purchase Access

**For Paid Extensions:**
```
1. Click "Purchase Access" ($0.10/call)
2. Stripe Checkout / Lightning invoice
3. On success → JWT issued (30-day validity)
4. Download .mcpb OR use platform endpoint
```

### 3. Installation

**Tier 1 (Platform-Hosted):**
```
User → Downloads .mcpb (or uses platform directly)
     → Platform extracts, validates, deploys to sandbox
     → User calls via: https://api.mcpstore.io/invoke/{package_id}
     → Authorization: Bearer {JWT}
```

**Tier 2 (Self-Hosted) - Claude Desktop:**
```
User → Downloads my-extension.mcpb
     → Double-click (or drag to Claude)
     → Claude extracts to ~/.mcp/packages/my-extension/
     → Reads manifest.json
     → Adds to MCP server config
     → Server validates JWT on each call
```

**Tier 2 (Self-Hosted) - Manual:**
```bash
# Unzip bundle
unzip my-extension.mcpb -d ~/.mcp/my-extension/

# Add to Claude config
code ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Add server entry (auto-generated from manifest.mcp_config):
{
  "mcpServers": {
    "my-extension": {
      "command": "node",
      "args": ["~/.mcp/my-extension/server/index.js"],
      "env": {
        "API_KEY": "user-provided-value",
        "MCPSTORE_JWT": "eyJhbGc..."
      }
    }
  }
}
```

---

## Security Considerations

### 1. Bundle Integrity

**MCPB Signing (Already Supported):**
- Publishers run `mcpb sign bundle.mcpb` with PGP/X.509 cert
- Signature embedded in `.mcpb` ZIP
- Clients verify: `mcpb verify bundle.mcpb`

**Marketplace Provenance:**
- SHA-256 hash of `.mcpb` file
- Stored in immutable `package_versions` table
- Users can verify: `sha256sum bundle.mcpb` matches registry

### 2. Sandboxing (Tier 1 Only)

Platform enforces restrictions based on manifest:
```json
"user_config": {
  "allowed_dirs": {"type": "directory", "multiple": true}
}
// → Sandbox only mounts these directories
```

**Capabilities Matrix:**
| Permission | Default | Declaration |
|------------|---------|-------------|
| Network | ❌ | `server.mcp_config.env.ALLOW_NET=true` |
| Filesystem | ❌ | Via `user_config` (directory/file types) |
| Subprocess | ❌ | Blocked unless binary type |

### 3. User Consent

Marketplace shows permissions before purchase:
```
This extension requires:
✓ Read access to selected directories
✓ Network access (API calls)
✓ API key (stored securely)

[Authorize] [Cancel]
```

### 4. JWT Validation (Tier 2)

Publishers integrate validation library:
```javascript
// @mcpstore/jwt-validator (provided by marketplace)
const { validateToken } = require('@mcpstore/jwt-validator');

server.setRequestHandler(async (request) => {
  const token = request.headers['authorization']?.split(' ')[1];
  const valid = await validateToken(token, {
    publicKey: MCPSTORE_PUBLIC_KEY,
    package: 'my-extension'
  });

  if (!valid) throw new Error('Unauthorized');

  // Process request...
});
```

---

## Compatibility with Claude Desktop

**Claude Desktop (v0.10.0+) natively supports MCPB:**
- Double-click `.mcpb` → Installation dialog
- Auto-extracts to `~/.mcp/packages/`
- Reads `manifest.json` → Generates MCP server config
- Handles `user_config` via UI forms
- Validates `compatibility.claude_desktop` version

**Marketplace Integration:**
1. User browses marketplace → finds extension
2. Clicks "Install in Claude Desktop"
3. Downloads `.mcpb` with embedded JWT (in ZIP comment or separate file)
4. Claude extracts, configures, adds JWT to `env`
5. Server validates JWT on startup

**Alternative Flow (Direct Link):**
```html
<a href="claude://install?url=https://mcpstore.io/bundles/my-ext.mcpb">
  Install in Claude Desktop
</a>
```

---

## Migration Path

### Phase 1: Leverage Existing MCPB Ecosystem
- Accept **any valid `.mcpb` file** from `mcpb pack`
- Extract manifest, index in registry
- No custom packaging format needed
- Publishers use official `@anthropic-ai/mcpb` CLI

### Phase 2: Add Marketplace Extensions
- Introduce `marketplace` field in manifest (optional, backward-compatible)
- Or store marketplace metadata **separately** in database
- Build discovery API, search, ratings

### Phase 3: Monetization Layer
- Add pricing to package metadata
- Implement payment flow → JWT issuance
- Provide JWT validation library for Tier 2 publishers

### Phase 4: Advanced Features
- Automated updates (MCPB supports versioning)
- Subscription bundles
- Community bounties
- Enterprise SLAs

---

## Key Takeaways

1. **Don't reinvent packaging:** Use MCPB `.mcpb` (ZIP with `manifest.json`)
2. **Extend, don't replace:** Add marketplace metadata as layer on top
3. **Reuse tooling:** Publishers use official `mcpb` CLI
4. **Native compatibility:** Works with Claude Desktop out-of-the-box
5. **Focus on value-add:** Discovery, payments, provenance, ratings
6. **Multi-tier support:** Hobbyist (platform-hosted) + Pro (self-hosted)

The marketplace becomes a **registry + payment gateway + trust layer** for the existing MCPB ecosystem, not a competing format.
