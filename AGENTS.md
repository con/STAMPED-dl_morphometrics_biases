# Repository instructions

Read `docs/conversion-plan.md` before making changes. Treat it and the applicable repository-local skills as project policy; stop and resolve any conflict among them before implementation.

For any work that creates, migrates, executes, debugs, audits, or releases the neuroimaging research object, read and follow `skills/stamped-neuroimaging-analysis/SKILL.md` completely.

When creating or adapting a project-authored BIDS App, also read and follow `skills/bids-app-builder/SKILL.md` and its referenced resources completely.

Do not import historical scientific code until the repository, environment/image registry, and toy BABS campaign have passed the gates that precede Phase 4.

## Commit co-authorship

Every commit authored by Codex MUST include a `Co-Authored-By` trailer identifying the tool name and version and the underlying model identifier reported by the active session.

Format:

```text
Co-Authored-By: <tool name> <tool version> / <reported model identifier> <codex@openai.com>
```

Discover the tool version from the tool itself, commonly with `codex --version` or `/Applications/Codex.app/Contents/Resources/codex --version`. Use the active model identifier reported by the Codex session or configuration. Reasoning or effort levels such as `Light` and `Ultra` are execution settings, not model versions, and MUST NOT be included in the trailer. Do not infer a model version from an effort level and do not guess the model identifier; if either the tool version or model identifier cannot be discovered, ask before committing.
