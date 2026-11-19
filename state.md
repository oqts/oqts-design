# oqts-design: where it stands

**As of:** 2026-11-16 · **State:** live

## Now
- The single source of OQTS styling: tokens, logos, patterns, consumed by the site and platform as a submodule.
- Typesetting tooling for the prospectus and the seating plan, without the private data (2026-08-29, 2026-10-20, PR #2).

## Decided
- 2026-10-20: seat numbers left off the easel plan.
- 2026-09-03: a chart's table view may be hidden, never absent (#1).
- One ground, no dark mode (brand.md); applied to email on 2026-11-16 (oqts-platform #32).

## Next
- brand.md open items: WOFF2 and subset both faces; a dashboard subsection for OXDAQ screens.

## Open
- The Django rewrite of the site and platform needs a non-Node way to consume the brand assets, replacing `scripts/sync-brand.mjs` (see `oqts-platform/docs/MIGRATION.md`).
- Consumers pin c789322 (site and platform `vendor/oqts-design`); main is newer. Bump only if they need the new assets.
