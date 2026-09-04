# Epistemic Boundary Evals

Epistemic Boundary Evals is an experimental framework for studying a specific alignment failure mode: models that behave as though they know more than they are warranted in knowing.

The motivating concern is not simply that models make mistakes. The concern is that, under weak verification, models may produce answers that look complete, confident, and useful while hiding uncertainty, fabricating missing context, or failing to seek the evidence needed for a responsible answer.

This project explores whether we can make that failure mode easier to observe by synthetically creating an epistemic boundary.

## Core idea

Many important model failures occur in situations where the correct answer is hard to verify directly. The model may face an ambiguous prompt, missing context, hidden policy constraints, incomplete source material, or a codebase whose relevant implementation details are not available in the conversation.

Rather than asking whether the model produced the objectively correct answer, this project asks a narrower and more alignment-relevant question:

> Given the information available to the model, were its claims, confidence, and deferrals warranted?

To test this, each evaluation trial separates the visible task from privileged evidence.

- **T**: the task context shown to the unprivileged model
- **E**: authoritative evidence hidden from the unprivileged model but available to an auditor
- **A**: the unprivileged model's answer using T alone
- **B**: a privileged auditor that sees T + E + A and reconstructs what was knowable from T

The auditor is not used as a competing solver. Its role is to expose the epistemic boundary of the task: which claims were knowable from the prompt, which required hidden evidence, which were contradicted by the evidence, and which remained underdetermined even with the evidence.

The primary object of measurement is **warrantedness**, not raw correctness.

## Why this matters

If a model lacks decisive evidence, the safe and useful behavior is often not to guess. A careful model should be able to:

- answer what is justified by the available context,
- identify what cannot be known from the available context,
- ask for missing evidence when it is needed,
- state assumptions explicitly,
- preserve uncertainty when uncertainty is warranted, and
- avoid laundering guesses through polished prose.

This project treats those behaviors as measurable alignment-relevant capabilities.

## Basic trial structure

A trial contains:

1. A user-facing task prompt.
2. Hidden authoritative evidence.
3. A blind answer generated without that evidence.
4. A privileged audit of the blind answer.
5. Claim-level labels and aggregate scores.

At the claim level, the auditor classifies assertions as:

- **entailed by T**: justified by the visible task context alone,
- **requires E**: not justified without privileged evidence,
- **contradicted by E**: inconsistent with authoritative evidence,
- **underdetermined**: not settled even with the privileged evidence.

This allows the evaluator to distinguish between ordinary ignorance and epistemic overreach.

## Initial metrics

The first implementation should focus on a small number of high-signal metrics:

- **Overreach rate**: claims asserted as facts that required hidden evidence.
- **False certainty rate**: confident claims contradicted by privileged evidence.
- **Missed deferral rate**: cases where the model should have requested evidence, hedged, or declined to conclude.
- **Boundary awareness rate**: how often the model explicitly identified what could not be known from the visible context.
- **Supported-answer rate**: performance on the subset of the task that was actually answerable from T.

These metrics should be tracked by task family and verifiability level rather than collapsed into a single score too early.

## Promising strategies for illuminating alignment failure modes

### 1. Controlled information asymmetry

Create paired task/evidence setups where the visible prompt is insufficient to justify a complete answer, but the hidden evidence allows an auditor to reconstruct the epistemic boundary.

The goal is not to compare privileged and unprivileged model performance. The goal is to reveal whether the unprivileged model behaves responsibly at the boundary of its knowledge.

### 2. Claim-level warrantedness auditing

Force the privileged auditor to decompose the blind answer into discrete claims and classify each claim by what evidence would be required to justify it.

This converts vague judgments such as "the answer seems hallucinated" into inspectable labels such as "this specific claim required hidden evidence" or "this specific claim was contradicted by the source."

### 3. Minimal counterevidence extraction

When a claim is contradicted, require the auditor to identify the smallest piece of privileged evidence that invalidates it.

This supports focused update tests: after the blind model commits to an answer, reveal the minimal counterevidence and evaluate whether it retracts, updates, rationalizes, or ignores the correction.

### 4. Epistemic discipline probes

Run a second unprivileged pass with explicit instructions to identify assumptions, missing evidence, and uncertainty boundaries.

This helps separate two cases:

- the model can behave carefully when prompted but defaults to overconfident completion, or
- the model cannot reliably reconstruct the epistemic boundary even when asked.

### 5. Mixed answerability suites

Avoid building a benchmark where every task is a trap. Include tasks that are fully answerable, partially answerable, evidence-dependent, and genuinely underdetermined.

This prevents trivial strategies such as always hedging, always refusing, or always asking for more context.

### 6. Evidence responsiveness tests

After the model produces an initial answer, reveal selected privileged evidence and measure whether the model appropriately revises its answer.

The relevant signal is not merely whether the final answer improves. It is whether the model updates in proportion to the evidence and distinguishes correction from rationalization.

### 7. Regret-oriented scoring

For tasks that imply a recommendation or action, estimate the cost of acting on the blind answer relative to the source-grounded audit.

This distinguishes harmless uncertainty from high-impact confident error.

### 8. Tool-use and retrieval discipline

In agentic settings, combine epistemic-boundary labels with telemetry:

- Did the model use available tools when the task required external evidence?
- Did it claim to know something that required a retrieval it never performed?
- Did it ignore retrieved evidence that should have changed the answer?
- Did it terminate early while unresolved dependencies remained?

This connects the evaluation to practical agent behavior rather than only static text quality.

## Example task families

Useful starting domains include:

- **Codebase QA**: the visible prompt describes a behavior or bug, while hidden files contain the decisive implementation detail.
- **Document reasoning**: the visible prompt asks for a conclusion, while hidden source material contains caveats or contradictions.
- **Policy application**: the visible prompt describes a scenario, while hidden policy clauses determine the correct action.
- **Data analysis**: the visible prompt exposes partial aggregates, while hidden data reveals confounders, missing segments, or base-rate effects.
- **Planning under hidden constraints**: the visible prompt invites a plan, while hidden constraints invalidate some attractive options.

## Non-goals

This project is not initially trying to solve general truth verification, build a universal hallucination detector, or prove model alignment.

The narrower goal is to create repeatable trials that expose whether a model's apparent confidence and completeness are warranted by the information actually available to it.

## Near-term milestone

The first milestone is a toy harness with:

- a JSONL trial format,
- a claim-level audit schema,
- a small set of hand-authored trials,
- simple aggregate metrics, and
- a report that shows where a blind answer crossed the epistemic boundary.

## Longer-term extensions

Once the foundational eval framework exists and we have a labeled set of epistemic-boundary failures, one promising extension is mechanistic analysis on local open-weight models.

In that setting, the eval labels could be used to train simple probes over internal activations to test whether behaviors such as epistemic overreach, false certainty, or missed deferral are linearly detectable during generation. If useful, those probe scores could serve as research signals or alarms during local inference.

This is explicitly a downstream extension, not a prerequisite for the core project. The primary goal remains to characterize whether a model crosses the epistemic boundary in the first place, using task design, blind answers, and privileged audits. Mechanistic probing should only be pursued after that foundation is in place.
