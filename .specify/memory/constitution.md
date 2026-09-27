<!--
Sync Impact Report
Version change: 1.0.0 → 1.1.0 (material expansion to define the Zigbee plug access-control scope).
Modified principles: I. Integration-First → I. Integration-First;
II. Native Home Assistant APIs → II. Native Home Assistant and Zigbee APIs;
III. Verified Behavior → V. Parent Auditability and Verified Behavior;
IV. Secure Handling → IV. Secure Handling and Child Privacy;
V. Minimal and Maintainable → VI. Minimal and Maintainable.
Added principle: III. Parent-Controlled Authorization and Quotas.
Added sections: none.
Removed sections: none.
Deferred items: integration domain; supported keypad, plug, and Zigbee stack combinations;
quota unit and time-zone/day-boundary rules; exact GitHub release update mechanism.
-->

# Home Assistant Custom Integration Constitution

## Core Principles

### I. Integration-First
This project develops a custom Home Assistant integration to control a Zigbee electrical plug
using a compatible Zigbee keypad. Integration code MUST follow Home Assistant's packaging
conventions and be installable under `custom_components/<domain>`. Integration behavior MUST NOT
require modifying or forking Home Assistant Core. Parents MUST be able to manage the integration
through Home Assistant, and children MUST be able to request plug activation by entering their
assigned personal code on the keypad.

### II. Native Home Assistant and Zigbee APIs
Integrations MUST use supported Home Assistant APIs and follow its current developer
documentation and Core patterns. I/O MUST be asynchronous where supported and MUST NOT block
Home Assistant's event loop. Config flows, entity lifecycles, services, and diagnostics MUST
follow Home Assistant conventions when applicable. Zigbee devices MUST be accessed through a
supported Home Assistant Zigbee stack and its supported interfaces; direct coordinator access
requires explicit justification in the feature specification.

### III. Parent-Controlled Authorization and Quotas
Parents MUST be able to configure allowed usage periods in a Home Assistant calendar interface
and set a daily usage quota for each child. A keypad request MUST be associated with a child and
MUST pass code verification, the active schedule, and remaining quota checks before the plug is
energized. When an allowed period ends or the child's quota is exhausted, the integration MUST
stop that child's authorized usage. Rejected or indeterminate authorization MUST leave the plug
off; a Home Assistant restart or device reconnection MUST NOT energize it without a new valid
request.

### IV. Secure Handling and Child Privacy
Personal codes and usage records MUST be protected as sensitive data. Raw codes MUST NOT be
written to logs, diagnostics, tracked files, or unredacted test fixtures. Persisted credentials
MUST use the safest supported representation and Home Assistant storage mechanisms. Code entry
MUST have protections against repeated guessing, and code changes or recovery MUST remain under
parent control. The integration MUST collect and expose only the child and usage data needed to
enforce policies and provide the parent activity view.

### V. Parent Auditability and Verified Behavior
Parents MUST be able to review per-child usage details, including the identity used, activation
and stop times, duration, and whether a request was allowed or rejected. Usage totals MUST be
consistent with quota enforcement. Every behavior change MUST have automated coverage for its
normal and error paths. Bug fixes MUST include regression coverage. Tests MUST use supported
Home Assistant test helpers and exercise config-entry, policy, keypad, and entity interactions
when relevant.

### VI. Minimal and Maintainable
Changes MUST stay focused, reuse Home Assistant and Python capabilities, and add dependencies
only when they solve a demonstrated need. Code MUST follow the project's type-checking and lint
conventions. Each release MUST state its supported Home Assistant versions and requirements.
Development and validation MUST initially use the official Home Assistant Container image
`ghcr.io/home-assistant/home-assistant:stable` with Apple's native `container` CLI.

## Architecture and Runtime Constraints
The development runtime exposes port `8123` for the local UI and mounts integration source under
`/config/custom_components`. Runtime state and credentials MUST remain outside tracked source.
Supervisor-only features and add-ons are out of scope unless a feature specification explicitly
adds them. The project MUST publish versioned releases from its GitHub repository and provide an
automatic update path based on those releases. Updates MUST preserve Home Assistant configuration
and usage history, and MUST NOT install arbitrary unversioned branch contents.

## Development Workflow
Feature work MUST begin with a Spec Kit specification, followed by a plan and actionable tasks
before implementation. Plans and implementation MUST identify which principles apply. Changes
MUST be checked with the relevant automated tests and project quality tools before they are
considered complete. Any exception to this constitution MUST be justified in the feature
specification and reviewed before implementation. Feature specifications MUST settle supported
Zigbee device models and stacks, quota units and day/time-zone boundaries, and the GitHub release
update mechanism before implementation begins.

## Governance
This constitution governs project decisions and takes precedence over conflicting local
conventions. Amendments MUST update this document and its version metadata. Use semantic
versioning: MAJOR for incompatible principle changes, MINOR for new or materially expanded
principles or sections, and PATCH for clarifications that do not change policy. Feature specs,
plans, and reviews MUST check compliance; an exception requires a written rationale in the
relevant specification. Keep the Sync Impact Report for review and remove it before committing
the constitution.

**Version**: 1.1.0 | **Ratified**: 2026-09-26 | **Last Amended**: 2026-09-26
