# Governance

This document describes the **proposed** governance baseline for the software-water-handbook.
It is intended to support a future move from Amadeus stewardship to a broader
community or Green Software Foundation project. It does not claim that a transfer
or GSF adoption has occurred.

## Project purpose

The handbook is a companion resource for implementing and evaluating the Green
Software Foundation's Software Water Intensity (SWI) work. It curates sources,
structures observations, records methodological limitations, and provides
reproducible derived tables. It is not itself the SWI specification.

## Roles

Until a receiving project is formally appointed:

- **Current maintainer:** Hongliu Cao (`@caohongliu`).
- **Reviewers:** maintainers or delegated subject-matter reviewers listed in
  `.github/CODEOWNERS`.
- **Contributors:** anyone who follows `CONTRIBUTING.md` and the applicable
  licensing and provenance requirements.

A future host should explicitly appoint maintainers, reviewers, an editor, and a
contact for conduct and security reports. Role changes should be recorded in a
pull request and reflected in `CODEOWNERS`.

## Decision-making

Routine corrections and editorial changes may be approved by a maintainer after
review. Changes to extraction schemas, attribution methodology, licensing,
repository ownership, or public claims require at least one maintainer review and
an explicit rationale in the pull request.

For a future GSF-hosted project, the receiving working group should confirm the
applicable review period, objection handling, approval threshold, and any required
Steering Committee ratification before the project is represented as an official
GSF deliverable. Until then, this repository should be described as a draft
companion resource.

## Contributions and review

Contributions are made through issues and pull requests. Reviewers should check:

1. provenance and source authority;
2. methodological scope and limitations;
3. reproducibility of derived outputs;
4. licensing and third-party reuse constraints; and
5. consistency with the repository's stated purpose.

The CI workflow must pass before merging changes that affect structured data or
validation tooling. Contributors should use DCO sign-off as described in
`CONTRIBUTING.md`.

## Releases and versioning

There is currently no formal release series. Until one is established, changes
are tracked through commits and pull requests. Before publishing a stable public
release, maintainers should define a release cadence, changelog practice, and
versioning policy. Version numbers must not imply that the handbook is an approved
SWI standard.

## Transfer checklist

Before a transfer or donation to another organization, confirm in a reviewed
pull request:

- receiving organization, working group, and named maintainers;
- repository-local Code of Conduct and security contacts;
- license and third-party data-rights approval;
- ownership of the GitHub repository and default branch;
- branch protection, required checks, dependency updates, and secret scanning;
- issue/PR templates and contributor communication channels; and
- public wording describing the project's status and relationship to SWI.
