# Architecture

This service is a modular monolith. HTTP handlers live in `app/api` and speak only through `app/contracts`. They call `app/services`, which use `app/domain` types. External IO is hidden behind `app/ports` so GitHub, storage, and knowledge sources can be swapped without changing the review flow.

Reviews are read-only. The API records a request and returns a summary. It does not post comments, push commits, or merge pull requests.
