# MCP Marketplace MVP Plan

> A modern web platform for MCP developers to publish and monetize MCPB extensions

**Timeline:** 3-4 weeks to launch
**Goal:** Enable publishers to upload MCPB files and consumers to discover/purchase extensions

---

## Product Vision (MVP Scope)

### What We're Building

A **marketplace website** where:
- **Publishers** can upload `.mcpb` files and set pricing (free or paid)
- **Consumers** can browse, search, and download/purchase extensions
- **Installation** is manual (copy commands) - no deep linking yet

### What We're NOT Building (Post-MVP)

- ❌ Automatic updates
- ❌ Reviews/ratings system (just download counts)
- ❌ Advanced analytics dashboard
- ❌ Subscription pricing (only one-time purchases)
- ❌ Lightning payments (Stripe only)
- ❌ Deep linking (`claude://install`)
- ❌ Automated security scanning
- ❌ Verified badges
- ❌ Enterprise features (private registries, SSO)

---

## Tech Stack

### Frontend + Backend (Single Codebase)
- **Framework:** Next.js 14 (App Router) with TypeScript
- **Styling:** Tailwind CSS + shadcn/ui components
- **Auth:** Clerk or Auth.js

### Data & Storage
- **Database:** Neon (serverless PostgreSQL) or Supabase
- **File Storage:** Cloudflare R2 (S3-compatible, CDN included)
- **Payments:** Stripe Checkout (hosted payment pages)

### Deployment
- **Hosting:** Vercel (Next.js optimized, free tier)
- **CDN:** Cloudflare R2 (built-in for `.mcpb` files)

### Why This Stack?

✅ **Single codebase** - Frontend + backend in Next.js
✅ **Minimal DevOps** - Vercel handles deployments
✅ **Modern DX** - TypeScript, hot reload, Tailwind
✅ **Generous free tiers** - Vercel, Neon, Cloudflare R2
✅ **Fast iteration** - shadcn/ui for beautiful components out-of-the-box

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Next.js Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Frontend (React)              Backend (API Routes)          │
│  ┌─────────────────┐          ┌─────────────────┐          │
│  │ /               │          │ POST /api/      │          │
│  │ /browse         │          │   packages      │          │
│  │ /publish        │──────────│ GET /api/       │          │
│  │ /package/[id]   │          │   packages      │          │
│  │ /dashboard      │          │ POST /api/      │          │
│  │ /purchases      │          │   checkout      │          │
│  └─────────────────┘          │ POST /api/      │          │
│                                │   webhooks      │          │
│                                └─────────────────┘          │
└─────────────────────────────────────────────────────────────┘
           │                              │
           │                              │
           ▼                              ▼
    ┌──────────────┐            ┌──────────────────┐
    │  Cloudflare  │            │  PostgreSQL      │
    │  R2 Storage  │            │  (Neon/Supabase) │
    │  (.mcpb CDN) │            │  (metadata)      │
    └──────────────┘            └──────────────────┘
                                         │
                                         ▼
                                  ┌─────────────┐
                                  │   Stripe    │
                                  │  (payments) │
                                  └─────────────┘
```

---

## Database Schema

```sql
-- Publishers use Clerk/Auth.js users table (managed by auth provider)

-- Packages
CREATE TABLE packages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- MCPB Manifest Fields (extracted from manifest.json)
  name TEXT NOT NULL,
  display_name TEXT,
  version TEXT NOT NULL,
  description TEXT,
  author_name TEXT,
  author_email TEXT,

  -- MCPB Capabilities
  tools JSONB,          -- [{name, description}]
  prompts JSONB,        -- [{name, description}]
  resources JSONB,      -- [{name, uri, description}]

  -- Files
  bundle_hash TEXT UNIQUE NOT NULL,  -- SHA-256 of .mcpb file
  bundle_url TEXT NOT NULL,          -- Cloudflare R2 CDN URL
  icon_url TEXT,                     -- Optional icon

  -- Metadata
  publisher_id TEXT NOT NULL,  -- Clerk/Auth.js user ID
  is_public BOOLEAN DEFAULT true,

  -- Pricing (MVP: one-time purchase only)
  price_usd DECIMAL DEFAULT 0,  -- 0 = free
  stripe_price_id TEXT,          -- Stripe Price ID for paid extensions

  -- Stats
  downloads INTEGER DEFAULT 0,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(name, version)
);

-- Purchases (for paid extensions)
CREATE TABLE purchases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,      -- Clerk/Auth.js user ID
  package_id UUID REFERENCES packages(id),
  stripe_session_id TEXT,
  amount_usd DECIMAL,
  purchased_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_packages_publisher ON packages(publisher_id);
CREATE INDEX idx_packages_public ON packages(is_public);
CREATE INDEX idx_purchases_user ON purchases(user_id);
CREATE INDEX idx_purchases_package ON purchases(package_id);
```

---

## User Flows

### Publisher Flow

1. **Sign up/login** via Clerk
2. Navigate to `/publish`
3. **Upload `.mcpb` file** (drag-drop or file picker)
4. System auto-extracts `manifest.json`, shows preview
5. Publisher sets **pricing**:
   - Free (default)
   - Paid: Enter amount in USD
6. Click **"Publish"**
   - Uploads to Cloudflare R2
   - Computes SHA-256 hash
   - Creates database record
7. Redirect to `/package/[id]` (package detail page)

### Consumer Flow (Free Extension)

1. Browse `/browse` or use search
2. Click extension → `/package/[id]`
3. See details: description, tools, installation instructions
4. Click **"Download"** → direct download from R2
5. Follow manual installation instructions:
   ```bash
   # Extract MCPB
   unzip my-extension.mcpb -d ~/.config/claude/extensions/my-extension

   # Add to Claude Desktop config
   # (show JSON snippet to copy)
   ```

### Consumer Flow (Paid Extension)

1. Browse → click paid extension
2. See price, click **"Purchase for $X"**
3. Redirected to **Stripe Checkout**
4. After payment → webhook creates `purchases` record
5. Redirect back to `/package/[id]` with **"Download"** button unlocked
6. Download + installation instructions

---

## MVP Pages

### Public Pages

**`/` - Landing Page**
- Hero section: "Discover MCP Extensions"
- Featured extensions (3-6 cards)
- How it works (3-step process)
- CTA: "Browse Extensions" + "Publish Your Extension"

**`/browse` - Extension Marketplace**
- Grid of extension cards
- Search bar (full-text search on name, description, tools)
- Filters: Category, Pricing (All/Free/Paid)
- Sorting: Latest, Most Downloaded, Price

**`/package/[id]` - Extension Detail**
- Icon, name, version, author
- Description (markdown rendering)
- **Tools** list (from `manifest.json`)
- **Prompts** list
- **Resources** list
- Installation instructions (auto-generated)
- Download/Purchase button
- Download count

### Protected Pages (Require Login)

**`/publish` - Upload Extension**
- Drag-drop upload zone
- File validation (must be `.mcpb`)
- Manifest preview (auto-extracted)
- Pricing form (free or USD amount)
- "Publish" button

**`/dashboard` - Publisher Dashboard**
- List of publisher's extensions
- Stats: Downloads per extension
- Edit/Unpublish actions

**`/purchases` - User's Purchases**
- List of purchased extensions
- Re-download links
- Purchase date, amount

---

## Component Mockups

### `/browse` Page (using shadcn/ui)

```
┌────────────────────────────────────────────────────────────┐
│ MCP Marketplace              [Search...]      [Sign In]    │
├────────────────────────────────────────────────────────────┤
│ [All] [Security] [Productivity] [Developer Tools]          │
│ [All Prices ▾] [Sort: Latest ▾]                            │
├────────────────────────────────────────────────────────────┤
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│ │ 🔐           │ │ 📝           │ │ 🗄️           │        │
│ │ YubiKey      │ │ Notion MCP   │ │ PostgreSQL   │        │
│ │ Signer       │ │              │ │ Query Tool   │        │
│ │              │ │              │ │              │        │
│ │ Hardware-    │ │ Sync notes   │ │ Natural      │        │
│ │ backed doc   │ │ and docs     │ │ language DB  │        │
│ │ signing      │ │              │ │ queries      │        │
│ │              │ │              │ │              │        │
│ │ $0.10/call   │ │ Free         │ │ $5.00        │        │
│ │ 1.2k ↓       │ │ 3.5k ↓       │ │ 890 ↓        │        │
│ └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                             │
│ [Load More]                                                 │
└────────────────────────────────────────────────────────────┘
```

### `/package/[id]` Detail Page

```
┌────────────────────────────────────────────────────────────┐
│ ← Back to Browse                          [Sign In]        │
├────────────────────────────────────────────────────────────┤
│ 🔐                                                          │
│ YubiKey Signer                                v1.2.0       │
│ by Yubico                                                   │
│                                                             │
│ Hardware-backed cryptographic document signing using       │
│ YubiKey PIV certificates. Sign PDFs, contracts, and        │
│ reports with FIPS 140-2 Level 2 certified security.        │
│                                                             │
│ ┌────────────────┐                                         │
│ │ Purchase $0.10 │  (or Download for free extensions)     │
│ └────────────────┘                                         │
│                                                             │
│ 📊 1,234 downloads                                          │
│                                                             │
│ ## Tools Provided                                           │
│ • sign_document - Sign PDF/file with YubiKey PIV           │
│ • list_certificates - List available signing certificates  │
│ • verify_signature - Verify document signature             │
│                                                             │
│ ## Installation                                             │
│ 1. Download the .mcpb file                                  │
│ 2. Extract to: ~/.config/claude/extensions/yubikey-signer  │
│ 3. Add to Claude Desktop config:                            │
│    {                                                        │
│      "mcpServers": {                                        │
│        "yubikey-signer": {                                  │
│          "command": "node",                                 │
│          "args": ["..."]                                    │
│        }                                                    │
│      }                                                      │
│    }                                                        │
└────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)

**Goal:** Set up project structure and authentication

- [ ] Initialize Next.js 14 project with TypeScript
- [ ] Configure Tailwind CSS + shadcn/ui
- [ ] Set up Clerk authentication
- [ ] Create Neon PostgreSQL database
- [ ] Run database migrations (create tables)
- [ ] Create basic page structure:
  - `/` (landing)
  - `/browse` (marketplace)
  - `/publish` (upload - protected)
  - `/dashboard` (publisher - protected)

### Phase 2: Upload & Storage (Week 1-2)

**Goal:** Enable MCPB upload and storage

- [ ] Implement file upload to Cloudflare R2
- [ ] Extract `manifest.json` from ZIP
- [ ] Validate MCPB format (check required fields)
- [ ] Compute SHA-256 hash
- [ ] Store metadata in PostgreSQL
- [ ] Display uploaded packages on `/browse`
- [ ] Create API routes:
  - `POST /api/packages` (upload)
  - `GET /api/packages` (list with search/filter)
  - `GET /api/packages/[id]` (get one)

### Phase 3: Discovery & Detail Pages (Week 2)

**Goal:** Build browsing and search experience

- [ ] Build package detail page (`/package/[id]`)
- [ ] Add search functionality (PostgreSQL full-text search)
- [ ] Add filtering (free/paid, category)
- [ ] Implement download logic (direct link to R2)
- [ ] Generate installation instructions dynamically
- [ ] Add shadcn/ui components:
  - Card component for extensions
  - Search input with debounce
  - Badge for free/paid

### Phase 4: Payments (Week 3)

**Goal:** Enable paid extensions

- [ ] Set up Stripe account + API keys
- [ ] Create Stripe Products/Prices for extensions
- [ ] Implement Checkout Session creation
- [ ] Add webhook handler (`POST /api/webhooks/stripe`)
- [ ] Handle payment success:
  - Create `purchases` record
  - Unlock download for user
- [ ] Add purchase verification logic
- [ ] Build `/purchases` page (user's purchased extensions)

### Phase 5: Polish & Deploy (Week 3-4)

**Goal:** Launch MVP

- [ ] Style landing page with hero + featured extensions
- [ ] Add publisher dashboard (`/dashboard`)
  - List extensions
  - Show download stats
  - Add delete/unpublish action
- [ ] Add error handling (upload failures, payment errors)
- [ ] Add loading states (skeleton screens)
- [ ] Write README for deployment
- [ ] Deploy to Vercel
- [ ] Configure custom domain (optional)
- [ ] Test end-to-end flows:
  - Publisher upload → Consumer download (free)
  - Publisher upload → Consumer purchase (paid)

---

## API Routes

### `POST /api/packages`

**Purpose:** Upload and publish a new extension

**Request:**
```typescript
// multipart/form-data
{
  file: File,  // .mcpb file
  pricing: {
    isFree: boolean,
    priceUsd?: number
  }
}
```

**Response:**
```typescript
{
  id: string,
  name: string,
  version: string,
  bundleUrl: string
}
```

**Steps:**
1. Validate user is authenticated
2. Upload file to Cloudflare R2
3. Extract `manifest.json` from ZIP
4. Validate manifest schema
5. Compute SHA-256 hash
6. If paid: Create Stripe Price
7. Insert into `packages` table
8. Return package ID

### `GET /api/packages`

**Purpose:** List/search extensions

**Query Params:**
- `q` (string): Search query
- `pricing` (free|paid): Filter by pricing
- `category` (string): Future use
- `limit` (number): Pagination
- `offset` (number): Pagination

**Response:**
```typescript
{
  packages: [{
    id: string,
    name: string,
    displayName: string,
    description: string,
    iconUrl: string,
    priceUsd: number,
    downloads: number,
    tools: [{name: string, description: string}]
  }],
  total: number
}
```

### `GET /api/packages/[id]`

**Purpose:** Get extension details

**Response:**
```typescript
{
  id: string,
  name: string,
  version: string,
  description: string,
  tools: [...],
  prompts: [...],
  resources: [...],
  bundleUrl: string,
  priceUsd: number,
  downloads: number,
  hasPurchased: boolean  // if user is authenticated
}
```

### `POST /api/checkout`

**Purpose:** Create Stripe Checkout session

**Request:**
```typescript
{
  packageId: string
}
```

**Response:**
```typescript
{
  sessionUrl: string  // Redirect to this URL
}
```

### `POST /api/webhooks/stripe`

**Purpose:** Handle Stripe webhooks (payment success)

**Steps:**
1. Verify webhook signature
2. Handle `checkout.session.completed` event
3. Extract `packageId` from metadata
4. Create `purchases` record
5. Return 200 OK

---

## Installation Instructions Generator

**Function:** Auto-generate installation instructions based on `manifest.json`

**Example Output:**

```markdown
## Installation

### 1. Download Extension
Click the "Download" button above to get `yubikey-signer.mcpb`

### 2. Extract Bundle
```bash
mkdir -p ~/.config/claude/extensions/yubikey-signer
unzip yubikey-signer.mcpb -d ~/.config/claude/extensions/yubikey-signer
```

### 3. Configure Claude Desktop
Add the following to your Claude Desktop configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "yubikey-signer": {
      "command": "node",
      "args": [
        "/Users/you/.config/claude/extensions/yubikey-signer/server/index.js"
      ],
      "env": {}
    }
  }
}
```

### 4. Restart Claude Desktop
Quit and reopen Claude Desktop to load the extension.

### 5. Verify Installation
In Claude, ask: "List my MCP tools"
You should see `sign_document`, `list_certificates`, `verify_signature` in the response.
```

**Implementation:** Template literals with variable substitution from `manifest.json`

---

## File Upload Flow (Technical)

### Client-Side (`/publish` page)

```typescript
async function handleUpload(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('pricing', JSON.stringify({ isFree: true }))

  const res = await fetch('/api/packages', {
    method: 'POST',
    body: formData,
  })

  const { id } = await res.json()
  router.push(`/package/${id}`)
}
```

### Server-Side (`/api/packages` route)

```typescript
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'
import { createHash } from 'crypto'
import AdmZip from 'adm-zip'

export async function POST(req: Request) {
  const formData = await req.formData()
  const file = formData.get('file') as File

  // 1. Upload to R2
  const buffer = await file.arrayBuffer()
  const s3 = new S3Client({ /* R2 config */ })
  const key = `bundles/${crypto.randomUUID()}.mcpb`
  await s3.send(new PutObjectCommand({
    Bucket: 'mcp-marketplace',
    Key: key,
    Body: buffer,
  }))

  // 2. Extract manifest
  const zip = new AdmZip(Buffer.from(buffer))
  const manifestEntry = zip.getEntry('manifest.json')
  const manifest = JSON.parse(manifestEntry.getData().toString('utf8'))

  // 3. Compute hash
  const hash = createHash('sha256').update(Buffer.from(buffer)).digest('hex')

  // 4. Insert into DB
  const { data } = await db.packages.insert({
    name: manifest.name,
    version: manifest.version,
    description: manifest.description,
    tools: manifest.tools,
    bundleHash: hash,
    bundleUrl: `https://cdn.example.com/${key}`,
    publisherId: user.id,
  })

  return Response.json({ id: data.id })
}
```

---

## Deployment Checklist

### Vercel Setup
- [ ] Create Vercel account
- [ ] Connect GitHub repo
- [ ] Set environment variables:
  - `DATABASE_URL` (Neon connection string)
  - `CLERK_SECRET_KEY`
  - `STRIPE_SECRET_KEY`
  - `STRIPE_WEBHOOK_SECRET`
  - `R2_ACCESS_KEY_ID`
  - `R2_SECRET_ACCESS_KEY`
  - `R2_BUCKET_NAME`
  - `R2_ENDPOINT`

### Cloudflare R2
- [ ] Create R2 bucket (`mcp-marketplace`)
- [ ] Enable public access for downloads
- [ ] Configure CORS (allow downloads from marketplace domain)
- [ ] Get access keys

### Stripe
- [ ] Create Stripe account
- [ ] Enable Checkout
- [ ] Configure webhook endpoint: `https://yoursite.com/api/webhooks/stripe`
- [ ] Copy webhook signing secret

### Database (Neon)
- [ ] Create Neon project
- [ ] Run schema migrations
- [ ] Copy connection string

### Custom Domain (Optional)
- [ ] Register domain (e.g., `mcpstore.io`)
- [ ] Configure DNS in Vercel
- [ ] Enable SSL (automatic via Vercel)

---

## Success Metrics (MVP)

**Launch Goals (First Month):**
- 📦 ≥ 10 published extensions
- 👥 ≥ 100 registered users
- 💰 ≥ 5 paid transactions
- 📈 ≥ 500 total downloads

**User Satisfaction:**
- Upload process ≤ 2 minutes
- Search returns results in ≤ 500ms
- Zero payment failures

---

## Post-MVP Roadmap

**Phase 6: Community Features**
- Reviews/ratings (5-star + text review)
- Comments on extension pages
- "Report extension" functionality

**Phase 7: Advanced Discovery**
- Categories/tags (auto-extracted from manifest)
- Trending extensions (algorithm: recent downloads + recency)
- Related extensions recommendations

**Phase 8: Monetization Enhancements**
- Subscription pricing (monthly/yearly)
- Usage-based pricing (per-invocation with JWT validation)
- Lifetime deals
- Coupons/discounts

**Phase 9: Enterprise**
- Private registries
- SSO/SAML
- Audit logs
- Team accounts (shared purchases)

**Phase 10: Quality & Trust**
- Automated security scanning (dependency vulnerabilities)
- Verified badges (manual review)
- Provenance ledger (blockchain or immutable log)
- Sandbox testing (automated QA)

---

## Open Questions

1. **Categories:** Auto-detect from manifest or require publisher to select?
   - **Proposal:** Start with tags (free-form), migrate to categories post-MVP

2. **Versioning:** Allow multiple versions of same extension?
   - **Proposal:** MVP = latest version only, add versioning in Phase 6

3. **Installation:** Should we build a CLI for one-command install?
   - **Proposal:** Post-MVP (Week 5-6), focus on manual install first

4. **Revenue Share:** Platform fee for paid extensions?
   - **Proposal:** 10% platform fee (covers Stripe 2.9% + hosting + ops)

---

## Resources

**Next.js:**
- https://nextjs.org/docs

**shadcn/ui:**
- https://ui.shadcn.com/

**Clerk (Auth):**
- https://clerk.com/docs

**Cloudflare R2:**
- https://developers.cloudflare.com/r2/

**Stripe Checkout:**
- https://stripe.com/docs/payments/checkout

**Neon (PostgreSQL):**
- https://neon.tech/docs

---

**Built for the MCP ecosystem**
*Extending Anthropic's official MCPB format with discovery and monetization*
