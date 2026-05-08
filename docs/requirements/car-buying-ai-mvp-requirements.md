# AI Car Buying Assistant MVP Requirements

## 1. Product Goal

Build a local MVP demo of an AI-powered car-buying platform that guides customers through a premium, conversational buying journey.

The journey is:

Search → AI Recommendation → Compare → Finance Estimate → Enquiry → Admin Follow-up

## 2. Target Users

### Customer
A person looking to buy a used or demo car but unsure which car best fits their lifestyle, budget, and finance expectations.

### Dealer / Lloyds Admin User
A dealer or internal user who reviews customer enquiries, AI summaries, finance estimates, and follow-up status.

## 3. Core Experience

The platform must feel like a guided car-buying advisor, not a basic search-and-filter website.

The assistant must:
- Welcome the customer
- Ask discovery questions step by step
- Understand customer intent
- Recommend cars
- Explain recommendations
- Compare cars
- Explain finance estimates
- Capture enquiry details
- Generate admin summary

## 4. Customer Discovery Requirements

The assistant must ask personalised questions before showing cars.

Example questions:
- Are you buying this car for family use, commuting, business, or weekend driving?
- What is more important to you: lower monthly payments, comfort, reliability, brand, or fuel economy?
- How many people will usually travel in the car?
- Do you need good boot space?
- Do you prefer petrol, diesel, hybrid, electric, or are you open to suggestions?
- What monthly payment would feel comfortable for you?
- Do you already have a deposit amount in mind?

## 5. Intent Understanding Requirements

The assistant must understand customer intent, not just filters.

Example intents:
- I need a reliable family car.
- I want something cheap to run.
- I drive mostly on motorways.
- I need a car for school runs.
- I want a premium car but within monthly budget.
- I am not sure whether I should choose petrol, hybrid, or electric.

## 6. Recommendation Requirements

The platform must recommend cars based on:
- Customer intent
- Budget
- Lifestyle
- Driving pattern
- Fuel preference
- Transmission preference
- Family size
- Mileage preference
- Running cost expectation

Each recommendation must show:
- Car details
- Match score
- AI explanation
- Finance estimate

## 7. Match Score Requirements

Each recommended car must have a match score.

The score should consider:
- Budget fit
- Monthly payment fit
- Usage fit
- Fuel preference
- Transmission preference
- Family size
- Mileage preference
- Running cost expectation

Example:
Match Score: 87%

## 8. Comparison Requirements

The customer must be able to compare 2–3 cars side by side.

Comparison must include:
- Price
- Monthly finance estimate
- Mileage
- Fuel type
- Transmission
- Body type
- Suitability for customer need
- Running cost indication
- Value-for-money explanation

## 9. Finance Estimate Requirements

Each car must include a simple finance estimate.

Finance estimate should include:
- Vehicle price
- Deposit amount
- Loan/finance term
- Example interest rate
- Estimated monthly payment

The assistant must explain that figures are indicative and subject to approval.

## 10. Shortlist and Enquiry Requirements

The customer must be able to:
- Shortlist cars
- Select one preferred car
- Continue to enquiry
- Submit lead details

Lead capture fields:
- Full name
- Email address
- Phone number
- Preferred contact method
- Preferred contact time
- Selected car
- Monthly budget
- Deposit amount
- Buying timeframe

## 11. AI Customer Summary Requirements

After enquiry submission, the system must generate an AI summary containing:
- Customer buying purpose
- Budget range
- Monthly payment expectation
- Preferred fuel type
- Preferred transmission
- Key concerns
- Cars viewed
- Selected car
- Customer readiness level

## 12. Admin Dashboard Requirements

The admin dashboard must show:
- New customer enquiries
- Customer contact details
- Selected car
- Customer budget
- Finance estimate
- AI-generated customer summary
- Cars recommended
- Cars compared
- Lead status
- Follow-up notes

Admin must be able to update enquiry status:
- New
- Contacted
- Interested
- Finance discussion
- Test drive requested
- Closed
- Lost

## 13. Demo Inventory Requirements

The MVP must use local sample/demo inventory data.

Inventory fields:
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
- Short description
- Image URL or placeholder image

## 14. Customer Pages

The customer-facing marketplace page must include:
- AI assistant chat area
- Recommended cars section
- Car cards
- Compare option
- Finance estimate
- Enquiry button

The car detail page must include:
- Car image
- Make and model
- Price
- Mileage
- Fuel type
- Transmission
- Key features
- AI explanation
- Finance estimate
- Compare button
- Enquiry button

## 15. MVP Constraint

The MVP must run fully on a local machine using demo data.

No real finance approval.
No real credit check.
No real dealer integration.
No production payment or lending workflow.

## 16. Non-Functional Requirements

The platform must:
- Be simple enough for MVP demo
- Have a premium guided buying feel
- Use friendly customer-facing language
- Avoid overloading the customer with filters
- Keep the assistant behaviour focused on car-buying advice
- Provide clear finance disclaimer wording