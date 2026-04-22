---
title: Agent-Friendly Design
tags: [agentic-ai, mcp, tool-design, api-design, ux]
created: 2026-04-08
updated: 2026-04-08
sources:
  - title: OpenAI Plans Launch of Desktop Superapp
    url: https://www.wsj.com/tech/openai-plans-launch-of-desktop-superapp-to-refocus-simplify-user-experience-9e19931d
---

# Agent-Friendly Design

A set of design principles for building software interfaces that can be reliably discovered, invoked, and composed by autonomous AI agents — as opposed to interfaces optimized primarily for direct human interaction.

## Overview

As agentic AI systems (running inside superapps or as standalone orchestrators) take on complex multi-step tasks, they must interact with external tools. Traditional software surfaces — web UIs, rich desktop apps, modal workflows — are difficult for agents to use reliably because they were designed around human perception and manual interaction.

Agent-friendly design reorients software toward machine legibility. The canonical implementation is an MCP (Model Context Protocol) server: a lightweight JSON-RPC service that exposes a tool's capabilities as a typed schema with clear input/output contracts. An agent can discover available tools at runtime, select the right one for a task, call it with structured parameters, and parse the result — all without human instruction.

Key properties of agent-friendly interfaces:
- **Schema-first**: every action is described by a machine-readable schema (name, description, parameters, return type)
- **Idempotent where possible**: agents retry on transient failures; non-idempotent operations must be clearly flagged
- **Descriptive error messages**: agents use error text to self-correct; vague errors block autonomous recovery
- **Minimal state assumptions**: agents may call tools in novel orders; interfaces should not assume prior UI state
- **Least-privilege scoping**: tools should expose narrow, composable actions rather than broad capabilities

## Key Ideas

- **MCP as the standard**: Anthropic's Model Context Protocol is the emerging standard for agent-callable tool interfaces
- **From UI to tool**: the product question shifts from "what should this screen look like?" to "what should this tool schema expose?"
- **Discoverability matters**: agents can only use tools they know about; tool descriptions must be precise enough for an LLM to select them correctly
- **Human fallback**: well-designed agent interfaces include a human-review step for irreversible or high-stakes actions

## Backlinks

- [Superapp Paradigm](superapp-paradigm.md) — superapps require agent-friendly tool surfaces
- [API to SuperAgent Transition](api-to-superagent.md) — describes the same shift from the API side
- [derived: OpenAI Plans Desktop Superapp](../derived/openai-superapp-superagent.md)
- [Constrained Decoding](constrained-decoding.md) — tool schemas are the agent-facing interface contract

## Related Concepts

- [Superapp Paradigm](superapp-paradigm.md)
- [API to SuperAgent Transition](api-to-superagent.md)
- [Agentic Harness](agentic-harness.md)

## References

- [OpenAI Plans Launch of Desktop Superapp](https://www.wsj.com/tech/openai-plans-launch-of-desktop-superapp-to-refocus-simplify-user-experience-9e19931d) — context for the shift toward agent-first product design
