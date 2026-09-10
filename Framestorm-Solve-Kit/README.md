# Framestorm–Solve Kit

Portable copy of Sean's framestorming and solving method. No case background. Copy these three files into any project.

## Contents

| File | Goes to |
|---|---|
| `framestorm-and-solve.mdc` | `.cursor/rules/framestorm-and-solve.mdc` |
| `playbooks/Framestorming-Playbook.md` | `playbooks/Framestorming-Playbook.md` (project root) |
| `playbooks/Solving-Playbook.md` | `playbooks/Solving-Playbook.md` (project root) |

## Install

1. Copy `framestorm-and-solve.mdc` into the new project's `.cursor/rules/`.
2. Copy the `playbooks/` folder to the new project's root (so the paths in the rule resolve).
3. If you put the playbooks somewhere else, edit the two paths in the table at the top of the `.mdc` file.

Do not copy the drinkware canvases, memos, CSVs, or class notes with this kit. Those are worked examples from one practice case; this kit is the method only.

## What the rule does

- On framing prompts → agent reads `Framestorming-Playbook.md` first.
- On sizing / recommendation prompts → agent reads `Solving-Playbook.md` first.
- Enforces the non-negotiables and the solving pre-delivery gate.
