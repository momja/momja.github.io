---
description: LLMs can be expensive, so lets talk about how to get to RCAs quickly
  without wasting money
publish_date: '2026-07-05'
title: Using LLMs to Investigate And Reproduce Complex Bugs
---

_This blog post is based on a presentation I recently gave to our engineering team at my day job. I wanted to share more broadly, so I used Gemini to do the slides → blog post translation, then I heavily edited it to make it my own voice and strip it of anything specific to my company. Much of this is specifically about Claude Code._

# Using LLMs to Investigate And Reproduce Complex Bugs With Reasonable Token Spend

Every engineer knows the feeling of staring down a cryptic stack trace buried deep within a complex application framework. Historically, resolving these issues meant hours of tracing nested logic and reading through the code. LLM agents have changed how I approach that work entirely.

I am convinced that one of the best places to start with agentic engineering is with RCAs and bug reproduction, because it's _verifiable_. If Claude Code can produce the exact same stack trace with a failing unit test, or it can hit our APIs with the magic request that triggers the same failing behavior, I can quickly RCA an issue and verify the cause against a production failure.

Despite it sometimes feeling like magic, it is vital to establish a core truth about LLMs right from the start: **an LLM agent is like a junkyard electromagnet.** If you are looking for a needle, it will find it for you. In fact, it makes the proverbial needle in the haystack ludicrously easy to find, but you are still the one who has to decide what to do with the needle once you pry it off that magnet. [Clankers](https://lucumr.pocoo.org/2026/5/26/clankers/) have no ability to make a decision, or exercise judgment. LLMs don't get blamed when the CI/CD pipeline fails or Prod goes down. Own your responsibility, and be happy you have a fancy new magnet, because at the end of the day, your job is still to [deliver code that works](https://simonwillison.net/2025/Dec/18/code-proven-to-work/).

LLMs may enhance your workflow, but they cannot replace your brain. My objective as an engineer is explicitly not to build "dark factories" where humans are entirely out of the loop. I don't believe every product can [loop its way to success](https://lucumr.pocoo.org/2026/6/23/the-coming-loop/), and I don't believe its the right way to frame the future of engineering work.

Let's boil this down to what I'm calling the **"Meathead" Rule**: You are [made out of meat](https://web.mit.edu/people/dpolicar/writing/prose/text/thinkingMeat.html). Digging through files, tracing call chains, grinding through reproduction attempts is the boring stuff that can be done by machine while your real job is to deeply contemplate how to solve a problem and determine what problems actually need solving. By utilizing tools like Claude Code, we can bypass the tedious work of digging through files, allowing us to focus our mental energy on delivering better Root Cause Analyses (RCAs) and superior architectural solutions. The greatest part of all of this is how much _better_ we can make our outputs. It should not be just about how _fast_ we can work.

---

## Working With the Available Models

To get the most value out of agentic engineering, you must match the specific model to the complexity of the problem at hand. The expensive models will always be able to handle the tasks of the cheaper models. But they are _expensive_. Getting more out of less will always be a valuable skill. And in case you haven't heard, token budgeting is [now in fashion](https://techcrunch.com/2026/06/05/the-token-bill-comes-due-inside-the-industry-scramble-to-manage-ais-runaway-costs/).

* **Claude Opus (The "Needle in the Haystack" Solver)\*:** Best reserved for high-complexity, logic-heavy reasoning where you must trace complex system behaviors across multiple layers.
* **Claude Sonnet (The Workhorse):** Faster and cheaper; it excels at executing clearly defined coding transformations once the core path is understood.
* **Claude Haiku (The Automator):** Ideal for well-constrained problems embedded within highly established, repetitive workflows.

_\* I wrote this before Fable came out. I have used Fable, and it's impressive. Given the cost, I'm uncertain how it will fit into my professional work or personal projects._

AI models evolve rapidly. If a task fails on Sonnet today, a future iteration of the model may solve it correctly tomorrow. Sometimes the right move is to wait, not to escalate to a bigger model forever. Don't be a [tokenmaxxer](https://en.wikipedia.org/wiki/Token_maxxing). The wasted resources I hear about are tremendous and it benefits no one (except I guess the stakeholders at the AI firms). Engineers should be as careful with resources in our dev work as we are with the products we build.

### Opus vs. Sonnet

I've established the habit of using Opus for everything that requires thinking or planning. If it's doing 'understanding' work, then I use Opus. I'll [hand off](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md) that work to Sonnet for implementation in a separate session.

Another approach if using plan mode: the `/model opusplan` configuration allows you to combine the strengths of sonnet/opus automatically:

1. **Opus** is deployed first to analyze the codebase, digest the context, and outline a robust, logical plan including fix verification.
2. **Sonnet** then steps in to transform that explicit plan into working, verifiable code.

---

## Provide Good Context, Minimize Token Burn

Dumping a raw, unorganized bug report directly into an agent without guidance is a major anti-pattern. Without direction, the agent will waste massive resources trying to guess systemic gaps, causing severe token burn. Not to mention, any gap it needs to fill is an opportunity for an LLM to introduce inaccuracy. I work in a very large repository, and I know what's relevant and what isn't. If you don't provide an idea of relevance, it's likely to go off the rails.

To achieve the results I'm looking for, I construct structured prompts using explicit section headers. Try formatting your inputs using distinct markers or XML style formatting:

> <bug_report>
> Provide the explicit ticket context or raw error behavior.
> </bug_report>
> 
> <related_documents>
> Point directly to architecture markdown files or relevant guides.
> </related_documents>
> 
> <relevant_files>
> Identify the exact classes, paths, or test files that the model should inspect.
> </relevant_files>
> 

This is as much assurance for myself that I provide the necessary context as it is about structuring the prompt. If you don't have relevant documentation, you should fix that. It doesn't need to be committed directly into your repo, but it helps.

---

## Two Bugs

Here are two recent bugs where an agent rapidly resolved issues that required complicated investigative work:

### Case Study 1: Navigating Deep Logic Chains

An application threw a nested `NullPointerException` buried deep within custom Java Comparator chains. The true failure occurred during the construction of the comparator, but the stack trace only pointed to its final usage point.

```
java.lang.NullPointerException: Cannot invoke "java.lang.Comparable.compareTo(Object)" because the return value of "java.util.function.Function.apply(Object)" is null
        at java.util.Comparator.lambda$comparing$77a9974f$1(Comparator.java:473) ~[?:?]
        at java.util.Comparator.lambda$thenComparing$36697e65$1(Comparator.java:221) ~[?:?]
        at java.util.Comparator.lambda$thenComparing$36697e65$1(Comparator.java:220) ~[?:?]
        at java.util.Comparator.lambda$thenComparing$36697e65$1(Comparator.java:220) ~[?:?]
        ...
        at java.util.Comparator.lambda$thenComparing$36697e65$1(Comparator.java:220) ~[?:?]
        at java.util.Comparator.lambda$thenComparing$36697e65$1(Comparator.java:220) ~[?:?]
        at java.util.Comparator.lambda$thenComparing$36697e65$1(Comparator.java:220) ~[?:?]
```

This trace is truncated — there were about 20 layers of `#thenComparing` in total.

Manually tracing this would have meant mapping numerous layers of logic. And the production logging did not include relevant record IDs. We didn't have logs of the records involved in the failure, so it would be a best guess effort to try and interpret the failure from the DB.

The general structure of my prompt was:

> Investigate this stack trace: @trace.txt. There are many layers of `#thenComparing` calls.
> This is built in `#x_function`.
> Understand how the comparator is instantiated, then reverse engineer the cause and pinpoint the issue by writing a failing unit test that reproduces the stack trace exactly.

By framing a structured prompt for the agent, it accurately decoded the stack trace and isolated the line where a sequence tiebreaker was added as a bare natural-ordering key with zero null handling. This was done in a two stage process. First, it traced the _entire_ stack of `#thenComparing` calls, cross referencing the usage of the comparator with the comparator builder to identify potential failure points. Second, it started writing unit tests to reproduce the _exact_ stack trace that was captured in production. This would allow it to demonstrate a plausible scenario where given a certain shape of data, we would encounter this failure.

Once the LLM was able to reproduce the trace, it proposed a root cause, which was able to be demonstrably proven as the issue based on a real environment.

The fix was trivial. Getting to the fix by demonstrating the root cause was not.

### Case Study 2: Testing Legacy States

One of our data models had recently changed, and the old behavior was quite different from the new behavior. Regardless, historical production audits must be supported forever. Even if the data model has changed for performance reasons, that should not cause any issues for audit. Early in development, we'd found the data model change was triggering a failure when trying to render and display the audit history to a user in our old test environments.

Instead of manually parsing thousands of rows of legacy data to reproduce a regression, I instructed an LLM agent to synthesize a localized unit test directly from a raw `.audit` file containing the failure. This unlocked rapid Red/Green Test-Driven Development (TDD) while allowing me to focus on the E2E reproduction steps. By the time the agent had reproduced the bug in unit testing and was able to specify a root cause, I had an environment configured to perform the end-to-end reproduction and verification of the fix. This allowed me to fulfill my job of delivering demonstrably working code.

---

## Trust but Verify: You Are the Arbiter

Your LLM electromagnet found the needle. It reproduced the trace, it wrote the failing test, it proposed the root cause. But none of that is a given. You have to set the magnet up properly and know how to adjust its power. Turn it on full blast and it will collect all sorts of stuff you weren't expecting, burning a lot of electricity doing it. And even when it's tuned right, the magnet doesn't make decisions. You're the one who pries the needle off, takes a look at it, and decides what to do with it.