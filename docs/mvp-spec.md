# JSE Stock Tracker --- Project Scope & Implementation Plan

**Project type:** University web application\
**Market:** South African listed equities (JSE)\
**Status:** Working specification\
**Primary stack:** FastAPI, SQLAlchemy, SQLite locally, PostgreSQL in
Docker Compose, plain HTML/CSS/JavaScript\
**Deployment:** Docker, GitHub Actions, Render\
**Testing and observability:** pytest, optional Playwright end-to-end
test, JSON logs, Prometheus-format `/metrics`

------------------------------------------------------------------------

## 1. Project summary

Build a web application that helps beginner investors and students
learning about the stock market monitor South African shares, understand
price movements, configure price alerts, and explore potential
opportunities with clear explanations of both possible benefits and
risks.

The app is an **analysis and tracking tool, not a broker**. It should
not execute trades or present its opportunity scores as guaranteed
predictions. It should make the source and freshness of market data
clear and explain how its scores were calculated.

## 2. Users and problem

### Primary users

-   Beginner investors who want to monitor shares without using
    complicated trading tools.
-   Students learning about the stock market who want understandable
    charts, indicators, and company information.

### Problem to solve

Users need one simple place to find supported JSE-listed companies,
monitor current or most recently available prices, track selected
shares, set target-price alerts, and understand why a share may look
interesting or risky.

### Main user journey

1.  Visit the dashboard and browse popular supported JSE shares.
2.  Search for a company by name or ticker.
3.  Open a share's detail page to inspect its price, chart, indicators,
    and fundamentals.
4.  Review a rule-based opportunity score and an AI-generated
    explanation of the score, potential benefits, and risks.
5.  Add the share to a personal watchlist and optionally set a target
    price.
6.  Receive in-app and email notifications when the target is crossed.
7.  Return to the dashboard to review watchlist movements and triggered
    alerts.

## 3. Scope and features

### 3.1 Market dashboard

-   Show popular supported JSE shares.
-   Display latest available price, daily change amount, daily
    percentage change, and data timestamp.
-   Show watchlist movements and recent alerts for signed-in users.
-   Highlight shares that meet configured alert conditions.
-   Clearly label stale, delayed, cached, or unavailable data.
-   Provide loading, empty, and error states instead of silently showing
    misleading values.

### 3.2 Search and company discovery

-   Search supported shares by company name or ticker.
-   Provide a browsable list of popular supported JSE shares.
-   Use the data provider's actual coverage; do not imply every JSE
    listing is supported if it is not.
-   Show a useful message when a company cannot be found or the provider
    has no data for it.

### 3.3 Share detail page

Display: - Company name, ticker, and industry when available. - Latest
available price and the timestamp of that price. - Daily price change
amount and percentage. - Interactive or lightweight price-history
chart. - Chart ranges: 1 day, 1 week, 1 month, 3 months, and 1 year,
where the data source supports them. - Technical indicators: price
momentum, moving averages, and trading volume where available. - Company
fundamentals: earnings, debt, and profitability where reliable data is
available. - Opportunity score from 0--100, score breakdown, relevant
labels, and risk information. - A clear distinction between measured
market data, calculated indicators, and AI-generated narrative.

### 3.4 Watchlists and accounts

-   Allow visitors to browse shares without an account.
-   Require an account to save a personal watchlist and receive email
    alerts.
-   Support email-and-password registration, login, logout, and secure
    password hashing.
-   Persist users, watchlists, alert settings, and alert events in the
    database.
-   Protect private watchlists and alert settings so one user cannot
    access another user's data.
-   Use environment variables for secrets; never commit passwords, API
    keys, or email credentials.
-   Add email verification or password-reset workflows if supported by
    the selected implementation and time available; do not block core
    local operation if optional email configuration is missing.

### 3.5 Target-price alerts

-   Let users set a target price for a selected share.
-   Trigger an alert when the observed price crosses the configured
    target.
-   Support alerts on each new crossing, with a cooldown to prevent
    notification spam.
-   Provide in-app notifications.
-   Offer email delivery through a free or low-cost email provider
    configured with environment variables.
-   Let users choose between immediate email notifications and a daily
    summary.
-   Record alert events so the app can avoid repeatedly sending the same
    notification for the same crossing.
-   Show the target, observed price, crossing direction, and event
    timestamp.
-   Make it clear that delayed data can cause an alert to arrive after
    the market price has already moved.

### 3.6 Opportunity scoring

Use a transparent, deterministic scoring engine based on technical
indicators and company fundamentals. AI must not invent or silently
alter the numeric score.

Potential inputs: - Price momentum. - Position relative to moving
averages. - Trading volume or unusual volume, when available. - Earnings
and profitability indicators. - Debt-related measures, when reliable and
comparable.

Requirements: - Define the inputs, normalisation, weights, missing-data
handling, and label thresholds in code and documentation. - Keep the
scoring implementation testable independently of the API and AI
provider. - Require adequate technical data and fundamentals before
producing a full combined score, as requested. - If key data is missing,
show "Insufficient data to score" or a clearly marked partial analysis
instead of manufacturing a score. - Include a score label such as
"Strong opportunity," "Watch," or "High risk," based on documented
thresholds. - Explain that a high score is not a guarantee of returns
and does not mean a share is suitable for every user.

**Important product decision:** The exact formula and thresholds are not
yet defined. Treat initial weights and thresholds as documented,
configurable heuristics---not validated investment advice. Review them
with tests and sample cases before release.

### 3.7 AI explanations and risk information

-   Generate an explanation when a user opens a share's analysis, rather
    than automatically generating explanations for every share.
-   Explain why the share received its score and describe possible
    benefits and risks.
-   Use a configurable external AI provider selected during
    implementation.
-   Pass structured, sourced data to the model; do not ask it to guess
    missing prices or fundamentals.
-   Keep numeric scores calculated by the application, not by the
    language model.
-   Display the date/time of the data used for the explanation.
-   Handle provider errors and missing credentials gracefully, with a
    rule-based explanation fallback where practical.
-   Clearly label AI-generated content.
-   Avoid guaranteed predictions or definitive instructions to buy or
    sell. Use neutral language such as "indicators to investigate" and
    "potential opportunity," with risk context.

### 3.8 Data provider and refresh behaviour

-   Prefer a reliable, affordable data source that covers JSE-listed
    shares.
-   Target refresh intervals of 5--15 minutes, subject to provider
    limits and actual data availability.
-   Investigate provider coverage, rate limits, licensing,
    historical-data availability, and whether commercial or public
    display is permitted before committing to it.
-   Cache provider responses to control costs and rate limits.
-   When fresh data is unavailable, show the last available price with
    its timestamp.
-   If multiple providers are implemented, try the configured primary
    provider and then a fallback provider before using cached data.
-   Never label delayed or cached data as real time.
-   Keep provider-specific code behind a service interface so it can be
    replaced without rewriting the UI or scoring engine.
-   Use sample fixtures only for tests or explicitly labelled demo mode;
    do not present mock data as live market data.

### 3.9 Virtual portfolio and trading

-   A virtual portfolio was previously selected as a later feature, so
    it is **not part of the initial release** unless deliberately added
    after the core application is stable.
-   Real-money trading, brokerage integration, order execution,
    deposits, and withdrawals are not part of the initial release.
-   Keep the architecture open to a later virtual portfolio, but do not
    let it delay the core tracker.

## 4. Screens and user interface

### Screen 1: Dashboard

-   App navigation and login/account controls.
-   Search box and popular JSE shares.
-   Market overview cards or a table with ticker, price, daily change,
    timestamp, and status.
-   Opportunity/watch indicators with clear labels.
-   Signed-in user's watchlist summary and recent alerts.
-   Visible data freshness notice.

### Screen 2: Search/results

-   Search by company name or ticker.
-   Results list with ticker, company name, latest price, daily change,
    and data status.
-   Empty state for no matches.

### Screen 3: Share details

-   Company identity and current/last available quote.
-   Price chart with 1D, 1W, 1M, 3M, and 1Y controls where supported.
-   Technical indicators and company fundamentals.
-   Opportunity score and a readable breakdown of contributing factors.
-   AI explanation, potential benefits, risk warnings, and data
    timestamp.
-   Add/remove from watchlist and set/edit target-price alert controls.

### Screen 4: Watchlist

-   Saved shares and their latest available prices.
-   Target prices and alert status.
-   Quick links to detail pages and controls to remove items or edit
    alerts.

### Screen 5: Alerts

-   In-app alert history with share, target, observed price, crossing
    direction, and time.
-   Notification preferences for immediate emails versus daily
    summaries.
-   Clear empty and error states.

### Screen 6: Authentication

-   Register, login, and logout.
-   Validation and helpful errors.
-   No login required for public browsing.

### General UX requirements

-   Responsive layout that works on desktop and mobile.
-   Accessible labels, keyboard-friendly forms, readable contrast, and
    useful validation messages.
-   Currency and percentage formatting consistent across screens.
-   Explicit loading, stale-data, missing-data, and provider-error
    states.
-   Do not rely on colour alone to convey a price rise, drop, or risk
    label.

## 5. Technical architecture

### Backend

-   **FastAPI** serves HTML, static assets, and JSON API endpoints.
-   Use FastAPI's generated OpenAPI documentation for API exploration.
-   Separate route handlers from business logic, data providers,
    scoring, AI explanations, authentication, and notification delivery.
-   Validate request and response payloads with typed schemas.

### Database and persistence

-   **SQLAlchemy** for database access.
-   SQLite for simple local development if useful.
-   PostgreSQL through Docker Compose for the course-required database
    workflow and deployed environment.
-   Use migrations (preferably Alembic) so schema changes are
    repeatable.
-   Suggested core entities: User, WatchlistItem, PriceAlert,
    AlertEvent, CachedQuote, and AnalysisCache. Add price-history
    storage only if needed by the chosen provider and retention policy.

### Frontend

-   Plain HTML, CSS, and JavaScript served by FastAPI.
-   No frontend build step.
-   Use fetch calls to the API and render accessible dashboard, detail,
    watchlist, and alert views.

### External services

-   Market data provider behind a provider interface.
-   Configurable AI provider behind an explanation service.
-   Configurable email provider behind a notification service.
-   All API keys and credentials loaded from environment variables.

### Containers and deployment

-   Dockerfile for the application.
-   Docker Compose for app + PostgreSQL, with health checks and
    persistent database storage for local development.
-   Render deployment from the repository/Dockerfile, with production
    environment variables and a managed or otherwise supported
    persistent PostgreSQL database.
-   Do not assume a free hosting tier provides durable disk storage or
    unlimited runtime; verify current platform limits during deployment.

### CI/CD and observability

-   GitHub Actions runs linting where configured, unit tests, and
    integration tests on pushes and pull requests.
-   Add a small Playwright end-to-end test for a key browser journey if
    feasible.
-   Provide `/health` for service health and `/metrics` in Prometheus
    exposition format.
-   Use structured JSON logs, avoid logging credentials or sensitive
    data, and include useful error context.

## 6. API outline

Names can be adjusted to fit the implementation, but keep the API
consistent and documented.

-   `GET /api/stocks` --- list supported/popular stocks.
-   `GET /api/stocks/search?q=...` --- search supported companies.
-   `GET /api/stocks/{ticker}` --- quote and company details.
-   `GET /api/stocks/{ticker}/history?range=...` --- historical price
    series.
-   `GET /api/stocks/{ticker}/analysis` --- technical/fundamental
    metrics, score, and optionally generated explanation.
-   `GET /api/watchlist` --- current user's watchlist.
-   `POST /api/watchlist` --- add a stock.
-   `DELETE /api/watchlist/{ticker}` --- remove a stock.
-   `GET /api/alerts` --- current user's alert settings and event
    history.
-   `POST /api/alerts` --- create a target-price alert.
-   `PATCH /api/alerts/{id}` --- update target or notification settings.
-   `DELETE /api/alerts/{id}` --- delete/disable an alert.
-   Authentication endpoints for registration, login, and logout.
-   `GET /health` --- health check.
-   `GET /metrics` --- Prometheus-format metrics.

Protect user-specific endpoints with authentication and ownership
checks. Public market-data endpoints can remain accessible without
login.

## 7. Suggested data model

-   **User:** id, email, password_hash, created_at,
    notification_preferences.
-   **WatchlistItem:** id, user_id, ticker, created_at.
-   **PriceAlert:** id, user_id, ticker, target_price, direction/trigger
    rule, enabled, cooldown, notification mode, last_triggered_at.
-   **AlertEvent:** id, alert_id, observed_price, crossing direction,
    triggered_at, email_status.
-   **CachedQuote:** ticker, price, daily_change, daily_change_percent,
    source_timestamp, fetched_at, data_status.
-   **AnalysisCache:** ticker, score, score_inputs, fundamentals,
    explanation, source timestamps, generated_at, model/provider
    metadata.

Store only what is needed. Define unique constraints (for example, a
user should not have duplicate watchlist entries for the same ticker)
and indexes for common lookups.

## 8. Security, reliability, and responsible presentation

-   Hash passwords with a recognised password-hashing library; never
    store plaintext passwords.
-   Use secure session handling and CSRF protections appropriate to the
    chosen authentication approach.
-   Validate all user input, especially ticker symbols, target prices,
    and alert settings.
-   Add rate limiting or reasonable throttling to authentication and
    costly external API routes where practical.
-   Keep secrets out of source control and logs.
-   Enforce ownership checks for watchlists and alerts.
-   Handle API timeouts, provider rate limits, malformed responses, and
    AI/email service outages.
-   Show the source timestamp for quotes, fundamentals, charts, and
    analysis.
-   Clearly distinguish historical observations from estimates or
    generated explanations.
-   Explain that scores are heuristic indicators, not guarantees or
    personalised financial advice.

## 9. Acceptance criteria

The initial release is acceptable when the following can be
demonstrated:

### Market data

-   [ ] A visitor can browse popular supported JSE shares and search by
    ticker/company name.
-   [ ] A share detail page shows latest available quote, daily change,
    supported history ranges, and company identity.
-   [ ] Every quote shows its source timestamp and is not mislabelled as
    real time when delayed/cached.
-   [ ] Provider failure results in a useful stale-data or error state
    rather than fabricated live values.
-   [ ] Unsupported tickers and missing fundamentals are handled
    clearly.

### Analysis

-   [ ] Technical indicators are calculated by tested application code.
-   [ ] The opportunity score is deterministic for the same inputs and
    documented.
-   [ ] The combined score is not presented as complete when required
    technical or fundamental inputs are missing.
-   [ ] AI explanations are generated on demand and explain both score
    factors and possible risks.
-   [ ] AI-provider failure does not prevent the rest of the app from
    working.

### Accounts, watchlists, and alerts

-   [ ] A visitor can browse without signing in.
-   [ ] A user can register, log in, and log out.
-   [ ] A signed-in user can add/remove shares from a persistent
    watchlist.
-   [ ] A user can create, edit, disable, and delete target-price
    alerts.
-   [ ] Crossing an alert target produces one event per crossing,
    respecting the configured cooldown.
-   [ ] In-app alerts work and email delivery works when valid email
    credentials are configured.
-   [ ] Email can be configured for immediate notifications or daily
    summaries.
-   [ ] One user cannot access another user's watchlist or alerts.

### Engineering and delivery

-   [ ] Unit tests cover scoring, indicator calculations,
    alert-crossing/cooldown logic, and important validation.
-   [ ] Integration tests cover key API/database flows.
-   [ ] The browser-based end-to-end test covers at least a core
    journey, such as browsing/searching a stock and opening its detail
    page; extend it to authenticated flows where feasible.
-   [ ] Docker Compose starts the app and PostgreSQL successfully from
    documented instructions.
-   [ ] GitHub Actions runs the configured test suite.
-   [ ] Render deployment works with documented environment variables
    and persistent database configuration.
-   [ ] `/health`, `/metrics`, and JSON logs are available.
-   [ ] README explains setup, configuration, data-source limitations,
    test commands, deployment, and known limitations.

## 10. Implementation plan

Build in vertical slices: get one working path from database/provider
through API to the UI, then expand. Avoid building every layer in
isolation.

### Phase 1 --- Repository and running skeleton

1.  Inspect the existing repository and course requirements before
    changing files.
2.  Create a clear project structure for FastAPI routes, services,
    database models, schemas, static assets, and tests.
3.  Add configuration through environment variables and a safe
    `.env.example`.
4.  Add Dockerfile and Docker Compose with PostgreSQL and health checks.
5.  Add `/health` and a basic dashboard shell.
6.  Confirm the app starts locally before adding external integrations.

**Exit check:** local app and database start reliably.

### Phase 2 --- Database and market-data vertical slice

1.  Configure SQLAlchemy for SQLite development and PostgreSQL
    deployment.
2.  Add migrations and core models.
3.  Research and test candidate data providers for JSE coverage,
    free-tier limits, freshness, historical data, and terms of use.
4.  Implement a provider interface, caching, timestamps, and graceful
    fallbacks.
5.  Add stock list, search, quote, and history API routes.
6.  Render the dashboard and stock detail page using real provider
    responses where available.

**Exit check:** user can search for a supported stock and see a clearly
timestamped quote and history.

### Phase 3 --- Indicators, fundamentals, and scoring

1.  Implement and unit-test momentum, moving averages, and
    volume-derived indicators.
2.  Fetch fundamentals where supported and map fields into a normalised
    internal schema.
3.  Document scoring inputs, normalisation, weights, labels, and
    missing-data rules.
4.  Implement the deterministic score and expose the score breakdown in
    the API.
5.  Display indicators, fundamentals, and score on the detail page.

**Exit check:** the same input produces the same score, with explicit
handling of missing data.

### Phase 4 --- Authentication and watchlists

1.  Implement secure registration/login/logout and password hashing.
2.  Add protected watchlist APIs and ownership checks.
3.  Add watchlist UI and persist user selections.
4.  Add tests for authentication, validation, and cross-user access
    prevention.

**Exit check:** users can save and retrieve their own watchlists.

### Phase 5 --- Price alerts and email

1.  Implement target-price creation, editing, disabling, and deletion.
2.  Add a scheduled/polling process appropriate to the deployment
    environment to check prices at a provider-compliant cadence.
3.  Implement crossing detection, cooldowns, and persistent alert
    events.
4.  Add in-app alert history.
5.  Integrate a free/low-cost email provider through environment-based
    credentials.
6.  Implement immediate and daily-summary preferences, including safe
    retry/failure tracking.

**Exit check:** a test price crossing triggers one event, and configured
email delivery can be demonstrated.

### Phase 6 --- AI explanations and risk presentation

1.  Define a structured prompt using the calculated score, indicator
    values, fundamentals, and source timestamps.
2.  Select a provider and keep the API key in environment configuration.
3.  Generate explanations only when the user requests a stock's
    analysis.
4.  Instruct the model to explain score contributors, possible benefits,
    uncertainty, and risks without inventing facts or guaranteeing
    returns.
5.  Add timeouts, error handling, and a non-AI fallback.
6.  Test that the numeric score remains controlled by application code.

**Exit check:** an analysis explains the calculated result using
supplied data and remains usable when the AI provider is unavailable.

### Phase 7 --- Tests, CI, observability, and deployment

1.  Expand pytest unit and integration coverage.
2.  Add one Playwright browser test for a critical user journey.
3.  Configure GitHub Actions to run tests on push and pull request.
4.  Add JSON logging, `/metrics`, and health checks.
5.  Deploy the Dockerised app to Render and configure persistent
    PostgreSQL, secrets, and allowed external-service settings.
6.  Run smoke tests against the deployed URL and fix deployment-specific
    issues.
7.  Complete README setup, test, environment-variable, and deployment
    instructions.

**Exit check:** local Docker Compose, CI, browser test, and deployed
application all pass the documented checks.

### Phase 8 --- Polish and optional extensions

1.  Improve responsive layout, accessibility, and error messages.
2.  Add virtual portfolio simulation only after the required core
    features are stable.
3.  Consider additional indicators, richer fundamentals, or more
    providers after verifying data quality and cost.
4.  Do not add real-money trading or brokerage execution to the initial
    release.

## 11. Environment configuration

Create `.env.example` with placeholders only. Expected variables may
include:

-   `APP_ENV`
-   `DATABASE_URL`
-   `SECRET_KEY`
-   `STOCK_DATA_API_KEY` (if required by the selected provider)
-   `AI_PROVIDER`
-   `AI_API_KEY`
-   `EMAIL_PROVIDER`
-   `EMAIL_API_KEY` or SMTP configuration
-   `EMAIL_FROM`
-   `BASE_URL`

Document which variables are optional, required only for specific
features, and safe to omit in local development. Never commit a real
`.env` file.

## 12. Risks and decisions to resolve early

1.  **JSE data availability:** Some free providers may not offer
    reliable JSE coverage, 5--15-minute updates, fundamentals, or all
    chart ranges. Verify this before designing around a provider.
2.  **Provider licensing:** Confirm terms permit the intended display,
    caching, and educational use.
3.  **Email delivery:** Free tiers may require domain verification or
    impose sending limits.
4.  **Background work on hosting:** Alert polling and daily summaries
    need a reliable scheduler/worker. Verify what the chosen hosting
    plan supports; do not assume a web process can run indefinitely
    without interruption.
5.  **Score quality:** Technical and fundamental inputs have different
    scales and may be missing or stale. Document the heuristic and test
    edge cases; do not claim the score predicts returns.
6.  **AI reliability/cost:** Use structured input, bounded output,
    timeouts, and on-demand generation to control cost and reduce
    hallucinations.
7.  **Scope size:** Authentication, alerts, email, AI, data integration,
    deployment, and observability together form a substantial project.
    Deliver them in vertical slices and keep optional features behind
    graceful fallbacks rather than faking functionality.

## 13. Definition of done

The project is done when the acceptance criteria above are met, the main
flow works locally and on Render, the README allows another developer to
reproduce the setup, automated tests run in CI, and all data/AI
limitations are visible to users.

**Product principle:** Prefer honest, timestamped, explainable data over
a feature that looks complete but quietly uses unreliable or fabricated
information.
