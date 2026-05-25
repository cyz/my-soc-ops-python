# Accessibility audit report (main flow)

## Findings
- Main flow buttons had no explicit keyboard focus style in CSS.
- The bingo modal had no dialog ARIA semantics (`role`, `aria-modal`, labels/descriptions).
- Some key controls in the flow were missing explicit accessible labels.
- Modal title color (`text-amber-500` on white) had low text contrast.

## Fixes applied
- Added visible `button:focus-visible` outline style in `app/static/css/app.css`.
- Added `aria-label` to start and back buttons.
- Added board semantics with `role="grid"` and `aria-label`.
- Added modal semantics: `role="dialog"`, `aria-modal`, `aria-labelledby`, `aria-describedby`, and initial button `autofocus`.
- Increased modal title contrast (`text-amber-800`).
- Added tests covering new ARIA attributes in main flow responses.
