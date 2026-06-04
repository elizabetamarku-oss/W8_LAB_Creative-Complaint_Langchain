# Lab Summary — NormalObjects Creative Complaint Handler

Across three complaints the agent made 8 tool calls, favouring `consult_demogorgon` and
`check_hawkins_records` equally (3 calls each), followed by `gather_party_wisdom` (2 calls),
while `cast_interdimensional_spell` was never called at all — suggesting the LLM gravitated
toward evidence and perspective over pure invention. 

The agent chained 2–3 tools per complaint
in a pattern that was partly logical and partly surprising: 

### for creature and psychic complaints
it consistently opened with the Demogorgon's perspective before grounding the answer in
records, which makes intuitive sense, but 

### for the portal complaint 
it reversed that order, checking records first — a small difference that would be impossible to predict in advance.

## This unpredictability is the defining trade-off of the freeform LangChain approach: 

the agent is free to sequence tools however it judges best, which suits open-ended creative tasks where variety adds value and no single "correct" order exists. 

A structured LangGraph workflow would: 
- enforce a fixed sequence — records, then party wisdom, then creature perspective — making the
logic transparent, repeatable, and easy to debug, but at the cost of that flexibility. 
- The
right choice comes down to the task: use a freeform agent when exploration and creativity
matter more than consistency; use LangGraph when the workflow has clear stages, auditability
is required, or downstream steps depend on the specific output of earlier ones.
