# ADR 0001: Modular monolith

## Status

Accepted

## Context

The reviewer is one deployable service, but API, domain, ports, and services should stay separable.

## Decision

Keep a single process and one package. Put boundaries in modules (`api`, `core`, `domain`, `contracts`, `ports`, `services`) instead of separate services.

## Consequences

One repo, one runtime, and clear import directions. A module can be extracted later if a boundary needs its own process.
