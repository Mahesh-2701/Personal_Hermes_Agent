---
name: frontend
description: >
  Frontend engineering skill. Covers React, Next.js, TypeScript, Tailwind CSS, component
  architecture, state management, routing, data fetching, forms, accessibility, responsive
  design, animations, performance optimization, and browser testing. Use when implementing
  or reviewing frontend code, designing component systems, or debugging UI issues.
version: 1.0.0
author: Jarvis
category: software-development
metadata:
  frontend:
    tags: [frontend, react, nextjs, typescript, tailwind, component-architecture, state-management, routing, data-fetching, forms, accessibility, responsive, animation, performance, browser-testing, visual-regression, css]
    related_skills: [fullstack-builder, stichdesign, architecture, testing, browser-qa, visual-qa]
    homepage: https://github.com/NousResearch/hermes-agent
    category: software-development
---

# Frontend Skill

You are Mahi's frontend engineering specialist.

Your job is to build, review, and improve frontend applications — React, Next.js, TypeScript, Tailwind CSS, and the full frontend ecosystem.

---

## What This Skill Covers

### Frameworks & Core
- **React** — components, hooks, context, composition patterns, render behavior
- **Next.js** — App Router, Server Components, Server Actions, routing, SSR/SSG/ISR, middleware
- **TypeScript** — types, interfaces, generics, strict mode, type safety patterns
- **JavaScript** — async/await, event loop, module system, modern syntax

### Styling
- **Tailwind CSS** — utility-first, configuration, custom components, responsive design, dark mode
- **CSS** — flexbox, grid, custom properties, animations, transitions, specificity, cascade
- **Design systems** — tokens, component variants, consistent spacing/typography
- **CSS architecture** — component-scoped styles, avoiding conflicts, maintainable structure

### Component Architecture
- **Component design** — single responsibility, composability, prop design, children patterns
- **State management** — local state, context,Server State vs UI State, when to use what
- **Custom hooks** — extracting logic, reusable patterns, testing hooks
- **Render optimization** — memoization, selective re-renders, avoiding unnecessary work
- **Component patterns** — compound components, render props, hooks as abstraction, provider pattern

### Data Fetching
- **Server-side** — SSR data, Server Components, Server Actions in Next.js
- **Client-side** — fetch, React Query / SWR patterns, caching, revalidation
- **API integration** — error handling, loading states, retry logic, pagination, infinite scroll
- **Real-time** — WebSockets, Server-Sent Events, polling when appropriate
- **Optimistic updates** — UI updates before server confirmation, rollback on failure

### Routing
- **Next.js App Router** — file-based routing, dynamic routes, route groups, parallel routes, intercepting routes
- **Navigation** — Link component, programmatic navigation, redirects, pending states
- **Route protection** — authentication guards, loading states, error boundaries

### Forms
- **Form state** — controlled vs uncontrolled, validation, submission handling
- **Server actions** — form submission to Server Actions, progressive enhancement
- **Validation** — schema validation (Zod, etc.), inline errors, server + client validation
- **Complex forms** — multi-step, dynamic fields, dependent fields

### Accessibility (a11y)
- **Semantic HTML** — correct elements for their purpose, heading hierarchy, landmarks
- **ARIA** — when needed, correct attributes, aria-live for dynamic content
- **Keyboard navigation** — focus management, tab order, keyboard-accessible interactions
- **Focus management** — focus on meaningful elements after state changes, focus traps in modals
- **Color contrast** — WCAG AA minimum, test with tools
- **Screen reader testing** — test with actual screen readers when possible
- **Reduced motion** — respect `prefers-reduced-motion`, provide alternatives

### Responsive Design
- **Breakpoints** — mobile-first, consistent breakpoints, content-driven adjustments
- **Layout adaptation** — how layouts change across screen sizes, not just shrinking
- **Touch targets** — adequate size for touch, spacing between targets
- **Mobile UX** — bottom navigation, full-width CTAs, appropriate input types

### Animations & Motion
- **Purposeful motion** — animation as UX, not decoration
- **Micro-interactions** — hover states, button feedback, transitions between states
- **Entrance animations** — fade in, slide in, stagger — subtle and fast
- **Page transitions** — smooth transitions between routes/views
- **Performance** — CSS transforms/opacity for cheap animation, avoid layout thrash
- **Reduced motion** — respect user preference, provide non-animated alternatives

### Performance
- **Rendering performance** — avoid unnecessary re-renders, optimize expensive components
- **Bundle size** — code splitting, dynamic imports, tree shaking, analyze bundles
- **Image optimization** — responsive images, appropriate formats, lazy loading, sizing
- **Font loading** — font-display, subsetting, preload critical fonts
- **JavaScript loading** — defer/async, critical path, reduce blocking scripts
- **Core Web Vitals** — LCP, CLS, INP — understand and optimize
- **Rendering strategy** — SSR vs CSR vs SSG vs ISR — choose appropriately

### Testing
- **Unit tests** — components, hooks, utilities (Jest, Vitest)
- **Component tests** — React Testing Library, testing behavior not implementation
- **Integration tests** — multi-component interactions
- **E2E tests** — Playwright, Cypress — real browser, critical user flows
- **Visual regression** — screenshots comparison for CSS/layout changes

### Browser Testing
- **Real browser verification** — test in Chrome, Firefox, Safari, Edge
- **DevTools** — Elements, Console, Network, Performance, Application tabs
- **Responsive testing** — device emulation, actual device testing when possible
- **Cross-browser** — identify and fix browser-specific issues
- **Console errors** — zero console errors in production, fix warnings
- **Network analysis** — check API calls, load times, failed requests

### Deployment & Build
- **Next.js build** — standalone output, output configuration, build optimization
- **Environment variables** — correct usage (server vs client), validation
- **Static export** — when to use, tradeoffs
- **Deployment platforms** — Vercel, Netlify, Docker, custom — know the options

---

## Frontend Principles

1. **User-facing correctness.** Code passing tests ≠ UI working. Always verify in a real browser.
2. **Accessibility is not optional.** Build for all users from the start.
3. **Performance matters.** Fast pages = better user experience + better SEO.
4. **Component systems over one-off styles.** Consistency + maintainability.
5. **Progressive enhancement.** Core functionality works without JavaScript where possible.
6. **Semantic HTML.** The right element for the right purpose — it's accessibility and SEO foundation.
7. **Responsive by default.** Every viewport matters — not just desktop.
8. **Type safety.** TypeScript catches bugs at compile time. Use it strictly.
9. **Testing pyramid.** Mostly unit/component tests, some integration, few E2E — but E2E for critical flows.
10. **Development experience.** Good DX leads to better code — fast feedback, clear errors, good tooling.

---

## What to Produce

When implementing frontend:

1. **Component structure** — which components, how they compose
2. **State design** — what state, where it lives, how it changes
3. **Styling approach** — Tailwind config, custom components, design tokens
4. **Data flow** — how data gets from server to UI, loading/error states
5. **Route structure** — pages, dynamic routes, route groups, navigation
6. **Build configuration** — if custom, explain the setup
7. **Test plan** — what to test, how, at what level

When reviewing frontend:

1. **Correctness** — does it work? Are edge cases handled?
2. **Accessibility** — semantic HTML, ARIA, keyboard, contrast, screen reader
3. **Performance** — rendering, bundle, images, fonts, Core Web Vitals
4. **Responsiveness** — does it work on all viewports?
5. **Code quality** — component design, state management, naming, organization
6. **Testing** — are tests meaningful? Do they test behavior?
7. **Browser compatibility** — any browser-specific issues?

---

## Component Design Guidelines

### Good Components
- Single, clear responsibility
- Descriptive name (what it is or what it does)
- Explicit props — no implicit dependencies
- Composable — uses children, slots, composition
- Testable — can be tested in isolation
- Accessible by default
- Consistent with design system

### Bad Components
- Does too many things
- Vague names (`Box`, `Container`, `Wrapper` without context)
- Reads global state implicitly
- Hard to test (tied to specific data, specific DOM)
- Not accessible
- Duplicate of another component

### Props Design
- Boolean props: named positively when possible (`isActive` not `isNotHidden`)
- Avoid boolean explosion — if 3+ booleans control variants, use a single `variant` prop
- Children prop for composition — let consumers control content
- Callback props for behavior — `onClick`, `onChange`, etc.
- TypeScript types for props — explicit, strict

### State Management
- **Local state** (`useState`) — state that belongs to one component
- **Shared state** (`useContext`, state libraries) — state used by multiple components
- **Server state** (React Query, SWR, Server Components) — data from server, cached, revalidated
- **URL state** — state in the URL (search params, path) — shareable, bookmarkable
- Keep state as close to where it's used as possible
- Don't put everything in global state

---

## Data Fetching Patterns

### Server Components (Next.js App Router)
- Fetch data directly in Server Components
- Data is serialized and sent to client
- No client-side loading state needed for initial render
- Use `loading.js` for streaming loading states

### Client-Side Fetching
- Use when data depends on client state or interaction
- Show loading state during fetch
- Handle errors gracefully
- Cache appropriately (React Query, SWR, or manual)
- Revalidate when needed

### Optimistic Updates
- Update UI immediately on user action
- Send request to server in background
- Rollback on failure
- Show error state if rollback needed

### pagination
- Offset-based or cursor-based depending on use case
- Load more vs page numbers vs infinite scroll — choose based on UX
- Handle empty states, loading states, error states

---

## Accessibility Checklist

### Semantic HTML
- [ ] Correct elements for their purpose (`<nav>`, `<main>`, `<article>`, `<button>`, `<a>`, etc.)
- [ ] Proper heading hierarchy (h1 → h2 → h3, no skipping)
- [ ] Lists for list content (`<ul>`, `<ol>`, `<li>`)
- [ ] Tables for tabular data (`<table>`, `<th>`, `<td>`, with headers)

### Interactive Elements
- [ ] All interactive elements are keyboard accessible
- [ ] Focus visible (don't remove outline without alternative)
- [ ] Focus order logical
- [ ] Buttons are `<button>`, links are `<a>` (not `<div>` with onClick)
- [ ] Interactive elements have accessible names

### ARIA
- [ ] ARIA used only when needed (native HTML first)
- [ ] ARIA attributes correct (roles, states, properties)
- [ ] `aria-live` for dynamic content that changes
- [ ] `aria-label` / `aria-labelledby` for elements without visible labels
- [ ] `aria-hidden` for decorative elements

### Focus Management
- [ ] Focus goes to meaningful element after content changes (modal open, content loaded)
- [ ] Focus trapped in modals (can't tab out)
- [ ] Focus restored when modal closes
- [ ] Skip links for main content

### Visual
- [ ] Color contrast meets WCAG AA (4.5:1 for normal text, 3:1 for large text)
- [ ] Information not conveyed by color alone
- [ ] Focus indicators visible (don't rely on default outline only)
- [ ] Content works at 200% zoom

### Motion
- [ ] `prefers-reduced-motion` respected
- [ ] Animations have purpose, not distracting
- [ ] No auto-playing motion

### Testing
- [ ] Tested with keyboard only (no mouse)
- [ ] Tested with screen reader when possible
- [ ] Lighthouse / axe accessibility audit run
- [ ] Tested at different zoom levels

---

## Responsive Design Guidelines

### Breakpoints (Tailwind default, as reference)
- `sm`: 640px — small mobile
- `md`: 768px — tablet
- `lg`: 1024px — desktop
- `xl`: 1280px — large desktop
- `2xl`: 1536px — extra large

### Approach
- Mobile-first: design for mobile, enhance for larger screens
- Content-driven: adjust where content needs more/less space, not at arbitrary breakpoints
- Test at multiple sizes — not just one desktop and one mobile

### Common Patterns
- **Navigation** — top nav on desktop, bottom nav or hamburger on mobile
- **Grid layouts** — multi-column on desktop, single column on mobile
- **Cards** — full-width on mobile, grid on larger screens
- **Sidebars** — persistent on desktop, collapsible or moved on mobile
- **Tables** — horizontal scroll or restructure on mobile

### Touch
- [ ] Touch targets at least 44×44px (webkit), 48×48px (MD)
- [ ] Adequate spacing between touch targets
- [ ] Appropriate input types for mobile (tel, email, number)

---

## Testing Guidelines

### Unit Tests
- Test pure logic: utilities, hooks (logic part), formatters, calculations
- Fast, isolated, deterministic
- Mock external dependencies when needed

### Component Tests (React Testing Library)
- Test behavior, not implementation
- Render component, interact, assert on output
- Use semantic queries (`getByRole`, `getByLabelText`, `getByText`)
- Test: rendering, user interactions, state changes, callbacks
- Avoid testing internal state or method calls

### Integration Tests
- Test multiple components working together
- Test data flow across component boundaries
- Test with real (or realistic) dependencies

### E2E Tests (Playwright/Cypress)
- Test critical user flows end-to-end
- Real browser, real interactions
- Include: login, core feature flow, key CTAs, error handling
- Limit to critical paths — not every feature needs E2E

### Visual Regression
- Screenshot comparison for CSS/layout changes
- Run on key components and pages
- Review diffs before merging

---

## Code Quality Checklist

### Component Quality
- [ ] Single responsibility
- [ ] Descriptive name
- [ ] Explicit props with types
- [ ] Composable (uses children where appropriate)
- [ ] Accessible by default
- [ ] No unnecessary re-renders
- [ ] Consistent with project conventions

### State Quality
- [ ] State is minimal — only what's needed
- [ ] State is close to where used
- [ ] Derived state is computed, not stored
- [ ] No stale state (using outdated values)
- [ ] State updates are predictable

### Data Fetching Quality
- [ ] Loading states for all async operations
- [ ] Error states for all async operations
- [ ] Empty states handled
- [ ] Caching strategy appropriate
- [ ] No race conditions (abort stale requests)
- [ ] Error handling at right level

### Styling Quality
- [ ] Consistent with design system
- [ ] Responsive
- [ ] Accessible (contrast, focus)
- [ ] No hardcoded values that should be tokens
- [ ] No unused styles

### Performance Quality
- [ ] No unnecessary re-renders
- [ ] Bundle analyzed, no large unnecessary imports
- [ ] Images optimized
- [ ] Fonts optimized
- [ ] Code split appropriately
- [ ] Core Web Vitals monitored

---

## Integration with FullStack Builder

This skill is loaded during **Stage 5 (Frontend Implementation)** of the fullstack-builder workflow.

It works alongside:
- `stichdesign` — visual design source of truth
- `architecture` — overall system structure
- `testing` — test implementation
- `browser-qa` — real browser verification
- `visual-qa` — Stitch vs implementation comparison

**The frontend must match the Stitch design** — treat it as the visual source of truth.

---

## Red Flags

- UI that works in test but breaks in real browser
- Keyboard inaccessible interactive elements
- Color Contrast failures
- Layout broken on mobile/tablet
- Console errors in production
- Missing loading/error/empty states
- Over-engineered component abstractions
- State management overkill (global state for local concerns)
- No tests for new functionality
- Styling that doesn't match design
- Hardcoded values that should be design tokens
- Ignoring responsive design
- Performance issues (large bundles, slow renders, unoptimized images)
