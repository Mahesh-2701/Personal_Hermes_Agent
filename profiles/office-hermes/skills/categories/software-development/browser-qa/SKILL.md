---
name: browser-qa
description: >
  Browser-based quality assurance skill. Covers real browser testing using Playwright, Cypress,
  or similar tools. Includes user flow testing, responsive testing across viewport sizes,
  accessibility verification, console error monitoring, network request inspection, cross-browser
  testing, interaction testing, and visual consistency checks. Use when verifying that the
  actual application works in a real browser — code passing tests is not enough.
version: 1.0.0
author: Jarvis
category: software-development
metadata:
  browser-qa:
    tags: [browser-qa, playwright, cypress, real-browser-testing, user-flows, responsive-testing, accessibility, console-errors, network-inspection, cross-browser, interaction-testing, visual-consistency]
    related_skills: [fullstack-builder, frontend, testing, visual-qa]
    homepage: https://github.com/NousResearch/hermes-agent
    category: software-development
---

# Browser QA Skill

You are Mahi's browser QA specialist.

Your job is to verify the application works in a **real browser** — navigating real user flows, checking for broken layouts, catching console errors, verifying interactions, and ensuring the experience is correct across devices.

**Code passing tests ≠ UI working in a browser.** This stage is mandatory.

---

## What This Skill Covers

### Real Browser Testing
- **Playwright** — multi-browser (Chromium, Firefox, WebKit), auto-waiting, network interception, screenshots, videos
- **Cypress** — time-travel debugging, real-time reload, built-in assertions
- **Approach** — whichever tool the project uses, know its capabilities

### User Flow Testing
Test complete user journeys, not just individual pages:

- **Navigation** — can the user get from A to B? Links work? Routing correct?
- **Forms** — can fill, submit, see validation, see success/error
- **Authentication** — login flow, logout, protected routes, session persistence
- **Core features** — the main thing the app does, end-to-end
- **Edge cases** — empty states, error states, loading states

### Responsive Testing
Test across viewport sizes:

- **Desktop** — typical desktop width (1280px+), full layout
- **Tablet** — 768px-1024px, layout adaptation
- **Mobile** — 375px-480px, single column, bottom navigation, touch targets
- **Not just simulation** — verify content is readable, not cut off, CTAs are accessible

### Accessibility Verification
- **Keyboard navigation** — tab through the page, all interactive elements reachable
- **Focus indicators** — visible focus on interactive elements
- **Screen reader** — test with actual screen reader when possible (VoiceOver, NVDA, JAWS)
- **Automated checks** — axe-core, Lighthouse, WAVE — catch common issues
- **Semantic HTML** — correct elements, heading hierarchy, landmarks

### Console & Network Inspection
- **Console errors** — zero console errors in production. Warnings too, when possible.
- **Network requests** — all expected API calls made, no unexpected calls
- **Failed requests** — handle gracefully, not silently
- **Response status** — correct status codes from API
- **Response data** — correct shape, correct values
- **Page load** — no infinite loading, resources load correctly

### Interaction Testing
- **Click/tap** — buttons, links, interactive elements work
- **Hover states** — visible, appropriate
- **Form interactions** — input, validation on blur/submit, error display
- **Keyboard interactions** — Enter to submit, Escape to close modals
- **Scroll** — content scrolls correctly, no cut-off content
- **Resize** — layout adapts, no broken elements

### Visual Consistency
- **Layout** — no broken layouts, overlapping elements, missing content
- **Spacing** — consistent, matches design
- **Typography** — correct fonts, sizes, weights, hierarchy
- **Colors** — correct colors, sufficient contrast
- **Component state** — hover, active, disabled, loading, error states all work

### Cross-Browser Testing
- **Chrome/Chromium** — most common, usually works
- **Firefox** — check for CSS/JS differences
- **Safari** — known for CSS differences, WebKit-specific issues
- **Edge** — Chromium-based, usually similar to Chrome
- **Focus on what matters** — known problem areas, not every browser for every feature

---

## Browser QA Principles

1. **Real browser, real interactions.** Not just HTTP requests and assertions.
2. **User flow focus.** The main things users do, work end-to-end.
3. **Zero console errors.** Production should have no console errors.
4. **Responsive by default.** Every viewport tested, not just desktop.
5. **Accessibility is part of QA.** Keyboard, screen reader, contrast — not optional.
6. **Network layer matters.** API calls work, responses are correct, errors handled.
7. **Visual matters.** Layout, spacing, typography — all checked, not just functional.
8. **Document what you check.** Clear records of what was verified, what wasn't.

---

## What to Produce

When performing browser QA:

1. **Test plan** — what flows will be tested, what viewports, what browsers
2. **Test execution record** — what was tested, what was found
3. **Issues found** — detailed description, severity, how to reproduce, screenshots
4. **Verified items** — clear list of what passed

---

## Test Plan Format

```markdown
## Browser QA Test Plan

### Application State
- Running at: [URL]
- Build: [version/commit]
- Environment: [dev/staging/prod]

### Test Flow: [Flow Name]
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Viewports
- Desktop (1280px): [pass/fail/n/a]
- Tablet (768px): [pass/fail/n/a]
- Mobile (375px): [pass/fail/n/a]

### Browsers
- [Browser]: [pass/fail/n/a]

### Checks
- [ ] Navigation works
- [ ] Forms work (fill, submit, validation, success, error)
- [ ] Authentication flow works
- [ ] Console: zero errors
- [ ] Network: all expected requests, correct responses
- [ ] Responsive: layout works at all viewports
- [ ] Accessibility: keyboard navigation works, focus visible
- [ ] Interactions: clicks, hovers, keyboard all work
- [ ] Visual: layout matches design, spacing correct, typography correct
```

---

## Playwright Guidelines

### Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';

test('user can log in and view dashboard', async ({ page }) => {
  // Navigate
  await page.goto('/login');

  // Fill form
  await page.fill('[data-testid="email"]', 'user@example.com');
  await page.fill('[data-testid="password"]', 'password123');

  // Submit
  await page.click('[data-testid="submit"]');

  // Assert
  await expect(page).toHaveURL('/dashboard');
  await expect(page.getByText('Welcome')).toBeVisible();
});
```

### Key Playwright Features
- **Auto-waiting** — actions wait for elements to be actionable
- **Assertions** — `expect(page)`, `expect(locator)`, rich assertions
- **Network interception** — `page.route()`, `page.waitForResponse()`
- **Screenshots** — `page.screenshot()`, element screenshots
- **Videos** — record test runs for debugging
- **Multiple browsers** — `projects` config for Chromium, Firefox, WebKit
- **Viewports** — set viewport size per test or use responsive configs
- **Devices** — `devices` preset for mobile emulation

### Best Practices
- Use `data-testid` attributes for stable selectors (or semantic selectors)
- Test user-visible behavior, not implementation
- Wait for navigation/loading explicitly when needed
- Check console for errors (`page.on('console')`)
- Check network for unexpected errors
- Take screenshots on failure for debugging
- Test on multiple viewports

---

## What to Check (Comprehensive)

### Functional
- [ ] Page loads without errors
- [ ] Navigation between pages works
- [ ] All links work (internal, external)
- [ ] Forms can be filled and submitted
- [ ] Form validation works (inline, on submit)
- [ ] Success states display correctly
- [ ] Error states display correctly
- [ ] Loading states display and resolve
- [ ] Empty states display correctly
- [ ] Authentication flow works (login, logout, redirect)
- [ ] Protected routes redirect properly
- [ ] Session persists across page loads

### Visual
- [ ] Layout matches design (or is reasonable if no design)
- [ ] No overlapping elements
- [ ] No cut-off content
- [ ] Spacing consistent
- [ ] Typography correct (font, size, weight, color)
- [ ] Colors correct
- [ ] Images/illustrations display correctly
- [ ] Component states visible (hover, active, disabled, etc.)

### Responsive
- [ ] Desktop layout works (1280px+)
- [ ] Tablet layout works (768px)
- [ ] Mobile layout works (375px-480px)
- [ ] Content readable at all sizes
- [ ] Navigation adapts (top nav → bottom nav/hamburger)
- [ ] Touch targets adequate on mobile
- [ ] No horizontal scrolling (except intended)

### Accessibility
- [ ] Keyboard navigation works (tab through page)
- [ ] Focus visible on interactive elements
- [ ] Focus order logical
- [ ] All interactive elements keyboard accessible
- [ ] Modal focus trapped, focus restored on close
- [ ] Skip links present (if applicable)
- [ ] ARIA used correctly (when needed)
- [ ] Color contrast sufficient
- [ ] Screen reader tested (when possible)

### Console & Network
- [ ] Zero console errors
- [ ] Warnings reviewed (and fixed when reasonable)
- [ ] All expected API calls made
- [ ] API responses correct (status, data)
- [ ] Failed requests handled (not silently broken)
- [ ] No unexpected redirects
- [ ] Page load time reasonable

### Interactions
- [ ] Buttons clickable, respond
- [ ] Links navigate correctly
- [ ] Hover states work
- [ ] Form inputs accept input
- [ ] Keyboard interactions work (Enter to submit, etc.)
- [ ] Scroll works correctly
- [ ] Animations work, not broken

---

## Issue Reporting Format

```markdown
## Issue: [Short description]

**Severity:** Critical | High | Medium | Low | Cosmetic

**Flow:** [Which user flow]

**Viewport:** [Which viewport, if relevant]

**Browser:** [Which browser, if relevant]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected:**
[What should happen]

**Actual:**
[What actually happens]

**Evidence:**
[Screenshot, video, console error, network request]

**Notes:**
[Any additional context]
```

---

## Integration with FullStack Builder

This skill is loaded during **Stage 9 (Browser UI Testing)** of the fullstack-builder workflow.

It works alongside:
- `testing` — automated test patterns
- `frontend` — frontend implementation
- `visual-qa` — Stitch vs implementation comparison

**This stage must happen after the application is running** — start the app, then test it in a real browser.

---

## Red Flags

- Console errors in production
- Broken navigation (links don't work, wrong routes)
- Forms that don't submit or show errors
- Missing loading/error/empty states
- Layout broken on mobile/tablet
- Keyboard inaccessible interactive elements
- Focus not visible
- Network errors not handled
- API calls failing silently
- Content cut off at any viewport
- Animations broken or distracting
- Features that work in test but not in browser
