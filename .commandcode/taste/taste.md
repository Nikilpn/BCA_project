# backend
- Form-input date strings must be parsed to proper Python `date` objects (via `strptime`) before being used in comparisons, filters, or database storage — raw string comparison leads to broken validation and overlap detection. Confidence: 0.85
- Booking/date constraints should be validated redundantly: on the frontend (HTML `min` attribute on date inputs) and in the backend (check-in must be today or later, check-out must be after check-in) to ensure correctness regardless of browser support. Confidence: 0.80

# communication
- Prefers mixed Malayalam-English (Manglish) for conversation when working on projects. Confidence: 0.80
- Expects project-wide, systematic auditing for errors (checking all models, views, URLs, settings, admin, templates etc.) rather than fixing issues only as they're reported one-by-one — wants a comprehensive sweep of the entire codebase. Confidence: 0.85
- Expects the assistant to proactively verify and confirm the correctness/correctness of generated outputs (e.g., diagrams, document structure) before finalizing. Confidence: 0.75
- Meticulously reviews generated diagrams (e.g., ER diagram arrows, entity connections) themselves — catches visual misplacements and incorrect element targeting even after the assistant claims correctness. Confidence: 0.75

# forms-and-ux
- Computed/system-derived values (e.g., room price, total amount) in user-facing forms should be marked `readonly` to prevent manual editing — the price should come from the backend, not user input. Confidence: 0.85

# security

- Prefers that static assets (images, files) served on admin/protected pages are gated behind the same authentication/authorization as the pages themselves — they should not be publicly accessible via the static file handler. Confidence: 0.85
- Passwords must be hashed (not stored in plain text), and authentication logic must use password verification functions (e.g., `check_password`) instead of raw string comparison. Confidence: 0.90

# report-generation
See [report-generation/taste.md](report-generation/taste.md)
