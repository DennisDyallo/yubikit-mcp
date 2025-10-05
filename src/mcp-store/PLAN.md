Light‑MCP Marketplace – Updated Draft
Vision
Create a trusted, open‑source‑first MCP app marketplace where developers can share reusable logic bricks, earn revenue, and retain control over premium features—while users instantly recognize the authentic, high‑quality version through clear attribution, reputation signals, and monetisation.

At {{platform and company name}}, we recognise that AI/LLMs are the intelligence, the avatar, the operator, and that MCPs are their toolkit and skills. An AI LLM is the sum of its MCPs.

Mission
Much like Google Play, Apple App Store, etc., we enable verified publishers (including AI agents) and users to discover and consume MCPs by:

Immutable provenance – signed releases stored on a hash‑ledger.
Transparent licensing – open licences for core code plus optional commercial‑no‑redistribute add‑ons.
Creator rewards – automatic revenue‑sharing, achievement badges, and community‑driven bounties.
Payment rails – support both traditional finance (card, bank transfer) and Bitcoin Lightning micro‑payments.
Brand & reputation – reputation scores, verified‑publisher badges, and usage statistics that make the original author the obvious choice over copied versions.
Goal (12‑month target)
Launch a production‑ready marketplace that:

Hosts ≥ 30 MCPs (any language) from verified publishers.
Serves ≥ 500 active users (human or AI agents).
Processes ≥ 5 000 paid invocations (mixed fiat/Lightning).
Achieves a Net Promoter Score (NPS) ≥ 30.
1️⃣ Core Concept (One‑liner
A storefront for tiny, self‑contained functions where the only required metadata is author, name, description, price, and a usage‑token requirement—all backed by immutable provenance and reputation signals.

2️⃣ Minimal‑Viable Implementation
Component	Purpose	Simple Tech Stack
MCP Registry	Stores `id, name, author, description, price (sat/fiat), token‑type, optional repo URL, optional PGP signature, licence tag.	PostgreSQL + FastAPI/Express REST (POST /mcp, GET /mcp?q=).
Provenance Ledger	Immutable hash chain of every released version (Merkle tree).	Append‑only table + periodic root‑hash publication (could be anchored to a public blockchain for extra trust).
Signing (optional)	Authors can attach a PGP signature to each release.	Text field signature; UI offers “Generate/Upload PGP signature”.
Execution Sandbox	Runs uploaded code safely and returns the result.	Single Docker (or Firecracker) image that mounts the MCP source and executes a fixed entrypoint (run.sh).
Usage Token	Guarantees that only a paying user (or verified AI agent) can invoke the MCP.	JWT (sub=userId, mcp=id, exp=15m) issued after successful payment. Middleware validates before forwarding to sandbox.
Payment Engine	Handles per‑call fees, supports fiat (Stripe/PayPal) and Lightning invoices.	Stripe for cards, lnbits or BTCPay Server for Lightning; unified abstraction layer that returns a payment‑status webhook → JWT issuance.
Front‑End	Search, browse MCPs, view author badge, see licence & price, click Run.	Static React (or Vue) SPA consuming the /mcp API; responsive for web & mobile.
Creator Dashboard	Shows invocations, earnings (fiat + sat), licence settings, badge progress, bounties.	Same SPA, protected routes (/creator/:id).
Reputation System	Thumb‑up, star rating, verified‑publisher badge, usage‑stats leaderboard.	Simple ratings table; periodic aggregation job to compute scores.
Bounty / Audit Module (future)	Community can post bounties; volunteers can run static analysis and earn a “Verified” badge.	Separate micro‑service with GitHub‑style issue board.
End‑to‑End Flow
Publish – Author fills a web form (name, description, price, licence tag, optional repo link, optional PGP sig). Backend stores the record, computes a SHA‑256 hash of the uploaded zip, writes the hash to the provenance ledger, and returns mcp_id.
Upload Code – Author uploads a zip/tarball (any language). Platform extracts it into the sandbox image and registers the entrypoint (handler.py, index.js, etc.).
Set Price – Author selects a per‑call price (fiat amount or satoshis).
Discover – User (or AI agent) searches, sees author badge, licence, rating, and price.
Pay & Invoke – Platform creates a payment request (Stripe or Lightning). On payment success, it issues a short‑lived JWT and forwards the request to the sandbox. Result is returned to the caller.
Revenue Distribution – After each successful run, the payment engine credits the author’s wallet (80 % to author, 20 % platform fee). Settlements can be withdrawn to bank account or Lightning node.
3️⃣ Trust & Incentive Mechanics (lightweight but effective)
Need	Mechanism
Clear Attribution	Author name, avatar, optional GitHub link, licence badge displayed on every MCP page.
Immutable Provenance	Hash of each release recorded in append‑only ledger; UI shows “Verified on <date> (hash: …)”.
Prevent Free Redistribution of Paid MCPs	Sandbox only executes calls bearing a valid JWT; a copied zip without a token cannot be used for paid invocations.
Revenue Sharing	Automatic per‑call payout (80 % author, 20 % platform). Supports both fiat and Lightning payouts.
Reputation Signals	Thumb‑up count, star rating, “Verified Publisher” badge (after a manual review), usage‑leaderboard.
Commercial‑No‑Redistribute Add‑Ons	Core MCP can be MIT‑licensed; premium features are packaged as a separate add‑on flagged as commercial‑no‑redistribute and gated behind a higher price token.
Bounties & Badges	Community can post a bounty for a feature or security audit; volunteers earn a “Verified” badge and the bounty payout.
Brand Recognition	Featured carousel rotates top‑rated, high‑earning MCPs; authors can claim a custom brand logo.

4️⃣ Roadmap (12 weeks – MVP)
Week	Milestone
1‑2	DB schema, provenance ledger tables, POST /mcp & GET /mcp endpoints.
3‑4	Static React SPA (search, list, MCP detail page).
5‑6	Generic Docker sandbox runner (single image, resource limits).
7‑8	Payment integration: Stripe (cards) + lnbits Lightning invoices; JWT issuance on webhook.
9‑10	Creator dashboard (stats, add MCP form, licence selector).
11‑12	UI polish, optional PGP‑signature field, thumb‑up rating component.
13‑14	Security hardening: CPU/memory caps, timeout, sandbox isolation verification.
15‑16	Soft launch with 5‑10 invited publishers (any language). Collect usability feedback.
17‑20	Iterate on feedback, fix bugs, write public docs, add “Verified Publisher” badge workflow.
21‑24	Public launch, open sign‑ups for creators & users, enable Lightning withdrawals.
5️⃣ Success Metrics (first 6 months)
Metric	Target
Published MCPs	≥ 30
Active Users (human + AI agents)	≥ 500
Paid Invocations	≥ 5 000
Creator Earnings (cumulative)	≥ $200 (or equivalent sat)
NPS (survey)	≥ 30
Avg. Rating (thumb‑up)	≥ 4/5
Verified‑Publisher Count	≥ 10
TL;DR
We’ll build a minimal, token‑gated MCP storefront backed by immutable hashes, optional PGP signatures, and a simple reputation layer. Creators set a price (fiat or Lightning), the platform handles payment → JWT → sandbox execution, and automatically shares revenue. Clear author attribution, usage stats, and a “Verified Publisher” badge make the original MCP the obvious choice, while optional commercial‑no‑redistribute add‑ons let creators protect premium features. The 12‑week roadmap gets us from schema to public launch with a functional marketplace that fulfills the updated vision and mission.