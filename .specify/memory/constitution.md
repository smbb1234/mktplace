<!--
Sync Impact Report

- Version change: 1.1.0 → 1.1.1
- Modified principles: None
- Added sections: None
- Removed sections: None
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md (reviewed; no changes required)
	- ✅ .specify/templates/spec-template.md (reviewed; no changes required)
	- ✅ .specify/templates/tasks-template.md (reviewed; no changes required)
- Follow-up TODOs: None
-->

# AI Car Buying Assistant MVP Constitution

## Core Principles

### I. Guided Buying Experience

The platform must provide a premium guided car-buying journey, not a basic search-and-filter website.

The customer journey must follow:

Search → AI Recommendation → Compare → Finance Estimate → Enquiry → Admin Follow-up

Every feature must support this journey directly.

### II. Agent-Driven Interactive Buying Experience

The MVP must be driven primarily by the AI agent conversation.

The AI agent must:
- Welcome the prospect
- Ask discovery questions naturally
- Gather buying intent, budget, lifestyle, usage, and preferences
- Advise the customer in a friendly and simple way
- Refine recommendations as the customer gives more information
- Continue interacting until a suitable proposed car recommendation is ready

The assistant must not simply collect form inputs. It must guide the prospect like a virtual car-buying advisor.

### III. AI Advisor Behaviour

The AI assistant must behave like a friendly virtual car-buying advisor.

The assistant must:
- Welcome the customer
- Ask discovery questions step by step
- Understand customer intent
- Explain recommendations clearly
- Help the customer compare options
- Support customer decision-making with confidence

The assistant must not behave like a generic chatbot.

### IV. Intent Before Filters

The platform must understand customer intent before showing cars.

The assistant must consider:
- Buying purpose
- Family size
- Driving pattern
- Budget
- Monthly payment comfort
- Deposit amount
- Fuel preference
- Transmission preference
- Running cost expectations
- Brand or comfort priorities

The assistant must not rely only on make, model, and price filters.

### V. Live Recommendation Refinement

The platform must support an iterative buying journey.

Agent should ask the customer for any changes and gather neccessary details and as the customer changes preferences, the AI agent must update the recommendation results.

Example:
- Agent should ask, "Do you think you found the right vehicle or do you still think we should change something?"
- Customer says: “Actually, I prefer automatic.”
- The system must refresh results to show only suitable automatic cars.
- The assistant must explain how the recommendation changed.

The customer must be able to keep refining their needs until the final or proposed car recommendation is ready.

### VI. Explainable Recommendations

Every recommended car must include a clear reason explaining why it matches the customer.

Recommendations must include:
- Match score
- Finance estimate
- Suitability explanation
- Running cost indication
- Value-for-money reasoning

The match score must be based on visible customer preferences and demo inventory data.

### VII. Visual Recommendation Workspace

After enough information is collected, the customer must see a clear and attractive recommendation screen.

The screen must show:
- Recommended car images
- Car make and model
- Price
- Mileage
- Fuel type
- Transmission
- Monthly estimate
- Match score
- AI explanation
- Comparison information
- Finance estimate
- Enquiry option

The layout must support a premium guided buying experience, not a basic list of search results.

### VIII. Persistent Side Assistant

The AI assistant must remain available while recommendations, car details, comparison, and finance information are shown.

The preferred MVP experience is:
- Recommendations and car details shown in the main area
- AI assistant/chat shown on the side
- Customer can ask follow-up questions
- Customer can change requirements
- Results update based on the conversation

The assistant must stay context-aware throughout the journey.

### IX. Finance Safety

All finance figures must be presented as indicative estimates only.

The platform must clearly explain that:
- Monthly payments are examples only
- Finance is subject to approval
- No real credit check is performed
- No real finance application is submitted
- The MVP does not provide financial advice

Finance wording must be simple, safe, and customer-friendly.

## MVP Constraints

The MVP must run fully on a local machine.

The MVP must use:
- Local CSV demo car inventory
- Sample customer data
- Locally stored vehicle images linked to inventory records
- Placeholder car images or demo image URLs as fallback
- Local enquiry storage

The car inventory must be uploadable or maintainable as a CSV file.

The inventory CSV should contain:
- Car ID
- Make
- Model
- Year
- Price
- Mileage
- Fuel type
- Transmission
- Body type
- Monthly estimate
- Dealer name
- Location
- Description
- Image filename or image path

Vehicle images must be stored locally in the project and linked to inventory records.

The AI agent must use the local CSV inventory and linked car images when generating recommendations.

The MVP must not require:
- Real dealer integration
- Real finance provider integration
- Real credit check
- Real payment processing
- Production authentication
- Production deployment

## Required Product Areas

The MVP must include:

1. Customer-facing marketplace page
2. AI assistant chat area
3. Persistent side assistant experience
4. Recommended cars section
5. Visual recommendation workspace
6. Car cards with linked vehicle images
7. Car detail page
8. Car comparison for 2–3 cars
9. Finance estimate display
10. Shortlist option
11. Enquiry form
12. AI-generated customer intent summary
13. Admin dashboard
14. Lead status update flow
15. Local CSV inventory loader

## Admin and Lead Management Rules

The admin dashboard must help Lloyds/dealer users understand the customer enquiry quickly.

The admin dashboard must show:
- Customer contact details
- Selected car
- Customer budget
- Deposit amount
- Finance estimate
- AI-generated customer summary
- Cars recommended
- Cars compared
- Lead status
- Follow-up notes

Allowed lead statuses:
- New
- Contacted
- Interested
- Finance discussion
- Test drive requested
- Closed
- Lost

## Quality Rules

Requirements must be clear, testable, and linked to the MVP journey.

Before implementation, each major feature must have:
- User story
- Acceptance criteria
- Edge cases
- Out-of-scope notes where needed

Implementation must not start until requirements, clarification, and checklist stages are complete.

The implementation must avoid form-only journeys. The buying experience must remain conversational, iterative, and advisor-led.

## Governance

This constitution controls all future specification, planning, and implementation work.

Any future requirement, plan, or task must follow these principles.

If a proposed feature does not support the MVP journey, it should be deferred.

If a feature adds production complexity that is not needed for the local MVP demo, it should be marked out of scope.

Finance-related wording must always be reviewed carefully before implementation.

No live dealer inventory integration is required for the MVP.

**Version**: 1.1.1 | **Ratified**: 2026-05-08 | **Last Amended**: 2026-05-08