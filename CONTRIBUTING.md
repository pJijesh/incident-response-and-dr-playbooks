# Contributing

Thank you for helping to make these playbooks more useful. The aim is practical material that a small IT team can adopt, so clarity beats completeness.

## Ground rules

1. **Keep it generic.** No employer, client or real-person information, no real incident data, no real credentials. Examples use the fictional Fernhill Freight Ltd or are unnamed.
2. **No invented facts.** Do not add statistics, breach figures, fines or case studies unless you cite a source. Add every source to [docs/references.md](docs/references.md) with its status (read, search only, not retrieved) and the date you checked it.
3. **Not legal advice.** Describe what guidance says and link to it. Do not tell readers what the law requires beyond what the cited source states.
4. **Style.** British English. Calm, professional tone. Short sentences. No hype, no em-dashes (use commas, colons or hyphens), no emoji.
5. **Placeholders.** Templates use `{{field}}`. Playbooks must not contain TODO, FIXME or TBD markers.

## Playbook structure

Every file in `playbooks/` (other than the index) must have:

- An H1 starting with `Playbook:` and a metadata table with Version, Owner and Last reviewed (ISO date).
- These H2 sections, in this order: Purpose, Triggers, Severity matrix, Roles, First 15 minutes, Containment, Eradication, Recovery, Evidence handling, Communications, Regulatory and contractual notifications, Decision points, Post-incident actions, Quick-reference checklist.
- A quick-reference checklist that fits one page (at least 8 tick boxes, no more than 45 lines).

Section numbers in headings are optional for the checker but the existing playbooks use them, so please keep them for consistency.

## Before you open a pull request

```bash
python tools/check_playbooks.py --all-links
python -m unittest discover -s tests -v
```

Both must pass. If you change the dependency map, re-render the image and commit both files:

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i dr/dependency-map.mmd -o docs/dependency-map.png -w 1800 -b white
```

The tests check that the Mermaid block in `dr/dependency-map.md` matches `dr/dependency-map.mmd`.

## Reporting a problem

Open an issue describing what is wrong, where, and what source supports the correction. For anything that looks like a security issue in the tooling, please say so in the issue title and avoid posting sensitive details.

## Licence

By contributing you agree that your contribution is licensed under the [MIT licence](LICENSE).
