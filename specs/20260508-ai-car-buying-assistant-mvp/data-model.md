# Data Model: AI Car Buying Assistant MVP

## InventoryVehicle

Purpose: normalized representation of a recommendable vehicle parsed from CSV inventory.

| Field | Type | Notes |
|------|------|-------|
| vehicle_id | string | From `car_id`; primary external identifier |
| make | string | Required |
| model | string | Required |
| variant | string | Optional trim/variant |
| registration_year | integer | Required for display and tie-breakers |
| body_type | string | Required for recommendation filters |
| fuel_type | string | Required for recommendation filters |
| transmission | string | Required for recommendation filters |
| mileage | integer | Required for scoring/tie-breakers |
| colour | string | Optional display field |
| seats | integer | Optional but used for family fit |
| doors | integer | Optional display field |
| location | string | Used for recommendation context and admin visibility |
| stock_status | string | `Available`, `In Preparation`, etc. |
| is_featured | boolean | Optional merchandising hint |
| description | string | Derived from CSV if available, else synthesized deterministically from attributes |
| image_path | string | Local asset path or placeholder |
| is_placeholder_image | boolean | Required for UI fallback handling |
| created_at | datetime | Derived from `added_date` when available |

Validation rules:

- `vehicle_id`, `make`, `model`, `fuel_type`, `transmission`, and `stock_status` are mandatory.
- Vehicles without pricing records cannot appear in recommendations.
- `stock_status != Available` may still render in details/comparison but should be flagged and generally excluded from top recommendations.

## VehiclePricing

Purpose: normalized finance and list-price data associated with an inventory vehicle.

| Field | Type | Notes |
|------|------|-------|
| price_id | string | Primary identifier from pricing blob |
| vehicle_id | string | FK to InventoryVehicle |
| list_price_gbp | decimal | Required |
| monthly_from_gbp | decimal | Default monthly estimate |
| deposit_gbp | decimal | Default deposit |
| apr_percent | decimal | Example APR only |
| term_months | integer | Default finance term |
| annual_mileage_limit | integer | Optional finance display field |
| admin_fee_gbp | decimal | Optional |
| delivery_fee_gbp | decimal | Optional |
| discount_gbp | decimal | Optional |
| vat_included | boolean | Optional display flag |
| price_updated_at | datetime | Optional |

## CustomerSession

Purpose: canonical journey state for a single customer interaction.

| Field | Type | Notes |
|------|------|-------|
| session_id | UUID | Primary key |
| stage | enum | `discovery`, `recommended`, `comparing`, `finance_review`, `enquiry_started`, `submitted` |
| created_at | datetime | Required |
| updated_at | datetime | Required |
| last_recommendation_at | datetime | Optional |
| selected_vehicle_id | string nullable | Optional current focus vehicle |
| readiness_level | enum nullable | `exploring`, `shortlisting`, `ready_to_enquire` |

State transitions:

- `discovery -> recommended` when minimum inputs are satisfied.
- `recommended -> comparing` when 2–3 vehicles are actively compared.
- `recommended|comparing -> finance_review` when finance estimate is opened.
- Any active stage -> `enquiry_started` when contact form begins.
- `enquiry_started -> submitted` on successful lead submission.

## SessionPreference

Purpose: normalized extracted customer intent and constraints for a session.

| Field | Type | Notes |
|------|------|-------|
| session_id | UUID | FK to CustomerSession |
| buying_intent | string nullable | e.g. family car, commuter, first car |
| monthly_budget_gbp | decimal nullable | Minimum required for recommendations |
| deposit_gbp | decimal nullable | Optional until finance stage |
| buying_timeframe | string nullable | Optional enquiry/admin field |
| family_size | integer nullable | Optional |
| fuel_preference | string nullable | Optional |
| transmission_preference | string nullable | Optional |
| body_type_preference | string nullable | Optional |
| running_cost_priority | string nullable | Optional qualitative field |
| mileage_preference | string nullable | Optional qualitative field |
| brand_preferences | jsonb nullable | Optional list |
| lifestyle_notes | jsonb nullable | Optional structured notes |
| concerns | jsonb nullable | Optional list of objections or questions |
| extraction_confidence | decimal nullable | Aggregate confidence from AI extraction |

## SessionMessage

Purpose: persisted chat transcript for customer and assistant interactions.

| Field | Type | Notes |
|------|------|-------|
| message_id | UUID | Primary key |
| session_id | UUID | FK to CustomerSession |
| role | enum | `user`, `assistant`, `system`, `tool` |
| content | text | Required |
| tool_name | string nullable | Present for tool events |
| metadata | jsonb nullable | Structured UI directives, extraction outputs |
| created_at | datetime | Required |

## SessionShortlistItem

Purpose: persisted shortlist membership per session.

| Field | Type | Notes |
|------|------|-------|
| session_id | UUID | FK |
| vehicle_id | string | FK to inventory identifier |
| added_at | datetime | Required |
| flagged_no_longer_fits | boolean | Required default false |
| no_longer_fits_reason | string nullable | e.g. `exceeds budget` |

## SessionComparison

Purpose: tracks the current 2–3 car comparison set.

| Field | Type | Notes |
|------|------|-------|
| comparison_id | UUID | Primary key |
| session_id | UUID | FK |
| vehicle_ids | jsonb | Ordered array of 2–3 IDs |
| created_at | datetime | Required |
| updated_at | datetime | Required |

Validation rules:

- Must contain 2 or 3 distinct vehicle IDs.
- Compared vehicles must exist in normalized inventory.

## FinanceEstimate

Purpose: snapshot of an indicative finance calculation shown to the user.

| Field | Type | Notes |
|------|------|-------|
| estimate_id | UUID | Primary key |
| session_id | UUID | FK |
| vehicle_id | string | FK to inventory identifier |
| list_price_gbp | decimal | Required |
| deposit_gbp | decimal | Required |
| term_months | integer | Required |
| apr_percent | decimal | Required |
| estimated_monthly_gbp | decimal | Required |
| disclaimer_text | text | Required, canonical constant |
| created_at | datetime | Required |

## Enquiry

Purpose: customer lead captured from the buying journey.

| Field | Type | Notes |
|------|------|-------|
| enquiry_id | UUID | Primary key |
| session_id | UUID | FK |
| vehicle_id | string | Required selected or focal vehicle |
| full_name | string | Required |
| email | string | Required |
| phone | string | Required |
| preferred_contact_method | enum | `email`, `phone`, `sms`, `whatsapp` |
| preferred_contact_time | string nullable | Optional |
| monthly_budget_gbp | decimal nullable | Copied from preferences |
| deposit_gbp | decimal nullable | Copied from preferences/user input |
| buying_timeframe | string nullable | Required by spec if provided |
| status | enum | Default `New` |
| created_at | datetime | Required |

## LeadStatusHistory

Purpose: append-only audit log of admin lead status transitions.

| Field | Type | Notes |
|------|------|-------|
| history_id | UUID | Primary key |
| enquiry_id | UUID | FK |
| old_status | enum nullable | Null on creation |
| new_status | enum | One of allowed statuses |
| changed_at | datetime | Required |
| changed_by | string | `system` or local admin identifier |

Allowed statuses:

- `New`
- `Contacted`
- `Interested`
- `Finance discussion`
- `Test drive requested`
- `Closed`
- `Lost`

## LeadNote

Purpose: freeform admin follow-up notes.

| Field | Type | Notes |
|------|------|-------|
| note_id | UUID | Primary key |
| enquiry_id | UUID | FK |
| note_text | text | Required |
| created_at | datetime | Required |
| created_by | string | Local admin identifier |

## AICustomerSummary

Purpose: structured summary for admin review and follow-up.

| Field | Type | Notes |
|------|------|-------|
| summary_id | UUID | Primary key |
| session_id | UUID | FK |
| enquiry_id | UUID nullable | Optional if generated pre-enquiry |
| purpose | string | Required |
| budget_summary | jsonb | Monthly/deposit summary |
| fuel_preference | string nullable | Optional |
| transmission_preference | string nullable | Optional |
| key_concerns | jsonb | List |
| cars_viewed | jsonb | Ordered list of vehicle IDs |
| cars_compared | jsonb | Ordered list of vehicle IDs |
| selected_vehicle_id | string nullable | Optional |
| readiness_level | string nullable | Required if inferable |
| missing_information | jsonb | Gaps for follow-up |
| rendered_summary_text | text | Human-readable admin summary |
| created_at | datetime | Required |