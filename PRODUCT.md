# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

delegated: static HTML/CSS (no build step). Chosen because the brief scopes this stage to style capture, and the captured reference is a mobile-screen set that must be reproduced and inspected as plain markup; a framework adds nothing until there is product logic.

## Users

A deliberately wide CDMX audience, confirmed by the brief:

- **Chilango promedio** — the base case. Moves around the city regularly, knows the system partly, wants the answer without ceremony.
- **Personas mayores** — need larger type, generous targets, high contrast, no reliance on gesture or fine motor precision, no memory of previous screens required.
- **Nativos digitales** — expect immediate response, familiar mobile patterns, and no condescension in the interface.
- **Comerciantes y vendedores** — use it from inside a loud, crowded market, often one-handed, often while standing and serving someone.
- **Compradores** — arrive to find out where and when things are, and move on.

The unifying scene: outdoors or in a market, one hand on a phone, sun on the screen, noise and people around, network possibly poor, and no patience for a second try.

## Product Purpose

A CDMX tianguis information product: it tells people where the street markets are, when they open, and what they carry, so a buyer can decide where to go and a vendor can be found.

This stage delivers **style capture**, not the full product. The confirmed scope is to take the visual language already present in the nine reference captures and record it as a durable design system, so later screens generate on-brand instead of inventing a look.

## Positioning

Not a transit app. The reference captures are evidence of an established CDMX civic-mobility visual language — institutional, map-first, teal-led, icon-dense — not the product being copied. Tianguis borrows that civic trust and that map-first habit because the audience already reads it fluently, and spends them on market information instead of routes.

## Operating Context

- The map is the primary surface, not a decoration: the answer is a place, so the canvas that shows place leads.
- Results arrive as a persistent bottom sheet over that map, never as a full page navigation away from it.
- Filters are exposed as a small, visible, named row (Transporter / MI Taxi / Ecobici in the reference), and the equivalent here is a market-type filter — by day, by giro, by colonia.
- Line and station iconography is dense and color-coded. In the market product, giro categories inherit that role: food, produce, clothing, household, services.
- The bottom navigation carries five destinations at most, always visible, icon above label.

## Capabilities and Constraints

Confirmed by the brief:

- Read information about tianguis. That is the current functional scope.
- The audience spans elderly first-time users and digitally native users in the same product, so legibility constraints win every conflict with expression.

Explicitly undecided, and not to be invented:

- Whether vendors can publish listings, and how.
- Payments, ordering, reservations, or any transactional flow.
- Whether the data comes from official sources, crowd input, or both.
- Real market inventory, schedules, and colonia coverage.

## Brand Commitments

The following are binding because the brief designates the reference captures as the style to carry:

- Deep teal (`#166163`, nav `#104f55`) as the institutional primary. It carries navigation, headings, and the active state.
- A pale mint surface (`#f0fefe`) for content cards against white page ground.
- White circular controls floating over the map.
- Dense, single-color line iconography inside teal circles.
- Spanish, Mexican register, sentence case, no exclamation, no slang forced on the elderly user.

## Evidence on Hand

- Nine reference captures in the project root (`WhatsApp Image 2026-10-25 at *.jpeg`): a CDMX civic app with Pagos, WiFi and multi-line transit screens.

Absent, and not to be fabricated: any real tianguis data, schedules, colonias, vendor names, testimonials, market counts, official logos, or licensing.

## Product Principles

1. **Legibility before expression.** The elderly user sets the floor; the digitally native user is never slowed by it.
2. **The map keeps its place.** Information layers over the city; it never replaces it.
3. **Institutional, not promotional.** This is civic infrastructure to the eye, so trust comes from precision and repetition, not from delight.
4. **One visible action per screen.** Standing in a market, the user gets one obvious next thing.

## Accessibility & Inclusion

Confirmed audience includes older adults. The target is WCAG 2.2 AA at minimum, with a deliberate step past it in practice:

- Body text at 16px or larger, primary content at 18–20px.
- Interactive targets at least 48×48 CSS pixels.
- Teal-on-mint combinations must be checked; the pale card surface and the teal text pass, but mid-teal accents on mint do not, and are not used for text.
- No information carried by color alone: every colored line or category also carries a distinct icon and a text label.
