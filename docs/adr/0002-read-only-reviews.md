# ADR 0002: Read-only reviews

## Status

Accepted

## Context

An automated reviewer that can comment, push, or merge can change a repository without a human in the loop.

## Decision

Reviews never post comments, push commits, or merge pull requests. The API returns a read-only result. A GitHub token, when set, is for reading only.

## Consequences

Callers must apply feedback themselves. The service cannot accidentally mutate a pull request.
