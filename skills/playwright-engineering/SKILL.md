---
name: playwright-engineering
description: "Use when writing Playwright tests or browser automation."
version: 1.0.0
author: Jarvis & Mahesh
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: software-development
    tags: [playwright, e2e-testing, ui-testing, browser-automation, testing, qa, visual-testing, debugging]
    related_skills: [browser-qa, visual-qa, testing, fullstack-builder]
---

# Playwright Engineering

Comprehensive guidance for browser automation, end-to-end testing, UI verification, debugging, and production-quality browser workflows using Playwright.

## Core Objective

Use Playwright whenever browser-level interaction, UI verification, end-to-end testing, or browser automation is the appropriate solution.

## When to Activate

Activate this skill when asked to:
- write Playwright tests / create E2E tests
- test a website or web application
- automate a browser / verify a UI
- debug a browser issue / reproduce a frontend bug
- test login/signup, checkout flows, or forms
- test responsive layouts / take screenshots
- inspect browser behavior / create regression tests
- validate a website after implementation / run browser-based acceptance testing

---

## 1. First Inspect the Project

Before creating tests, inspect the existing project:
- Framework, frontend architecture, and package manager
- Existing Playwright configuration, test directory, and conventions
- Existing authentication setup, environment config, and scripts
- Base URL, CI configuration, fixtures, page objects, and utilities

Never assume the project uses a particular structure. Respect the existing architecture.

---

## 2. Test Design Philosophy & Locators

- **User Behavior over Internals:** Write tests around user behavior (action → application behavior → expected user-visible result) rather than React component internals or private state.
- **Resilient Locators (Priority Order):**
  1. `getByRole`
  2. `getByLabel`
  3. `getByPlaceholder`
  4. `getByText` (when appropriate)
  5. `data-testid` (for stable test hooks)
  6. CSS selectors only when necessary
  7. XPath as a last resort
- **Avoid brittle selectors:** Avoid `div:nth-child(3)`, library-generated CSS classes, or absolute XPath.

---

## 3. Assertions & Synchronization

- Use Playwright web-first assertions (`await expect(locator).toBeVisible()`) so tests wait for expected states instead of arbitrary sleeps.
- Never use `await page.waitForTimeout()` unless specifically justified.
- Test meaningful behaviors (URL changes, error messages, confirmation displays, state updates).

---

## 4. Test Structure & Organization

- Organize tests around meaningful user journeys (`tests/auth/`, `tests/dashboard/`, `tests/payments/`, etc.).
- **Authentication:** Use Playwright's reusable authentication state (`storageState`) to avoid logging in through the UI before every test when possible, while keeping dedicated tests for the login flow itself.
- **Fixtures & Page Objects:** Use fixtures for reusable test setup (authenticated user, seeded data). Use Page Objects only when workflows are reused or pages are complex.

---

## 5. API + UI Testing & Network Inspection

- Use Playwright's API capabilities for fast test setup before opening the browser for UI interactions.
- Inspect network requests, responses, status codes, and payloads when debugging. Test important HTTP error states (400, 401, 403, 404, 500) without mocking everything.

---

## 6. Debugging Failures

When a test fails:
1. Read the assertion error.
2. Inspect trace viewer, screenshots, console errors, and network logs.
3. Reproduce and determine root cause (app bug, test bug, selector, timing, environment).
4. Fix application or test accordingly. Do not hide real bugs by weakening assertions.

---

## 7. Responsive, Accessibility & Visual Testing

- Test realistic viewport sizes (desktop, tablet, mobile) for responsive behavior.
- Use Playwright to check accessible roles, names, keyboard focus, and form labels.
- Use visual screenshot comparisons sparingly and deterministically, avoiding dynamic timestamps or flaky animations.

---

## 8. Test Data & Database Safety

- Use deterministic, isolated test data. Clean up after tests.
- **Database Safety:** Clearly distinguish local, test, staging, and production environments. Never run destructive operations against production.

---

## 9. Avoiding Flakiness

Treat flaky tests as engineering problems. Investigate race conditions, unstable selectors, asynchronous UI, timing assumptions, or shared state. Do not fix flakiness by blindly adding retries or sleeps.

---

## 10. AI Application Testing

When testing AI-powered apps:
- Test chat inputs, streaming responses, loading states, tool execution indicators, error states, retries, markdown rendering, code blocks, citations, file uploads, and conversation history.
- Prefer behavioral assertions over exact LLM string matching unless output is strictly deterministic.

---

## 11. Browser Automation & Scraping Boundaries

- Respect authentication, authorization, terms, rate limits, and robots policies.
- Do not bypass CAPTCHAs, authentication controls, or anti-abuse mechanisms.
- Prefer simpler HTTP/API extraction when sufficient; use Playwright only when JavaScript rendering or user interaction is required.

---

## 12. Learning Mode & Explanation

After meaningful Playwright work, explain:
1. What was tested and why E2E testing was appropriate.
2. How Playwright interacted with the application.
3. Important selectors and synchronization decisions.
4. Failures, root causes, fixes, and verification.
