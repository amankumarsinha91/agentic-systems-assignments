Q1. Why did the plain ChatGPT-style chatbot give wrong answers?
The plain ChatGPT-style chatbot failed because it had no access to ShopEase’s internal support documents. It was answering questions based only on its general training, not on ShopEase’s actual policies. For example, ShopEase updated its refund timeline last quarter, but the model could not “see” that change, so it relied on patterns it had seen elsewhere. This is a static knowledge problem: the model does not know ShopEase-specific rules unless they are explicitly provided.
When the model lacks real information, it often hallucinates—meaning it confidently generates answers that sound reasonable but are made up. Hallucination happens because the LLM is designed to always produce an answer, even when it doesn’t have facts to rely on.
A concrete case from the pilot: a customer asked, “When will my refund be processed?” The chatbot replied, “Refunds are processed within 3 days.” In reality, ShopEase’s Refund Policy clearly states that refunds take 7 working days after the returned item passes inspection.

Q2. What should the new assistant “read from” to give correct answers?

Returns & Replacements Policy — answers questions about return windows, damaged items, eligibility, and replacement rules.
Refunds & Payment Timelines Policy — answers questions about refund processing time, original payment methods, and bank delays.
Shipping & Delivery Guidelines — answers questions about delivery timelines, courier partners, delays, and tracking issues.
Warranty & After-Sales Support Policy — answers questions about warranty duration, eligible products, and service-center escalation.
ShopEase Support Playbook (Internal) — answers agent-style questions about edge cases, approvals, and escalation paths.


Q3. 4-step RAG flow for a real ShopEase customer question
Customer question (Query)
“I received a damaged mixer-grinder 5 days ago. Can I still get a replacement?”
Retrieve
The assistant searches ShopEase’s knowledge base and pulls relevant sections from the Returns & Replacements Policy. A retrieved chunk looks like:

“Customers may request a replacement for damaged or defective products within 7 calendar days of delivery. The item must include original packaging and accessories. Replacement is subject to inspection approval.”

Context
This retrieved policy text is placed directly into the prompt along with the customer’s question. The LLM now sees both:

the user’s exact situation (damaged mixer-grinder, 5 days since delivery), and
the official rule stating a 7-day replacement window for damaged products.

Because the policy text is explicitly provided, the model does not need to guess or rely on generic e-commerce behavior.
Generate
Using the retrieved policy, the assistant produces a grounded answer:
“Yes, you are still eligible for a replacement. ShopEase allows replacements for damaged products within 7 calendar days of delivery. Since your mixer-grinder was delivered 5 days ago, you can request a replacement through the ‘My Orders’ section. Please ensure the item includes its original packaging and accessories, as it will be inspected before approval.”
This answer is built directly from the retrieved policy, not from the LLM’s assumptions.