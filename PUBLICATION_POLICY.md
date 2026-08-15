# Public Pages publishing policy

This repository publishes to a **public, unauthenticated** website. Treat every file under `site/` as readable forever by anyone who has its URL, search engines, repository forks, or archives.

## Never publish

- Names, usernames, email addresses, phone numbers, home/work addresses, dates of birth, account/order/claim numbers, location history, schedules, employer-specific details, photos with metadata, or private correspondence.
- Passwords, API keys, tokens, cookies, private keys, `.env` files, credentials in URLs, or backup exports containing private data.
- Personal preference profiles phrased as facts about a particular person (for example, “items already owned,” “what was watched,” or “what someone said”). Rewrite as general editorial context or keep it off the public site.
- Forms, analytics, trackers, ads, chat widgets, remote scripts, webhooks, databases, authentication flows, or user-submitted content without a separate security design and explicit approval.

## Required before every public deployment

1. Put deployable assets only in `site/`.
2. Run `python scripts/public_site_check.py`; it must pass.
3. Manually review the diff for context the scanner cannot infer: identity clues, personal routines, sensitive preferences, screenshots, and accidental copied text.
4. Keep the page static and client-only unless a new security/privacy review explicitly approves a backend.
5. Do not weaken the Content Security Policy, referrer policy, or the deployment workflow without an explicit review.

## What the automated check covers

It blocks common identifiers and credentials: emails, phone and SSN-shaped strings, local home paths, private keys, GitHub/AWS tokens, credential URLs, street-address patterns, and terms in `scripts/public-denylist.txt`.

Automation cannot prove that prose, images, or combinations of harmless facts are non-identifying. Manual review remains mandatory.

## Public hosting identity

The current `github.io` URL embeds the GitHub account name. Content can be anonymized, but this hostname cannot. A neutral account/organization or custom domain is required for an anonymous public-facing address.
