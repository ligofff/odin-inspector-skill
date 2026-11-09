# Verification and troubleshooting

These checks are author recommendations. Run only those relevant to the change. They are not claims that the repository has been tested in every Unity/Odin version.

## Before code

- Record installed versions and compilation context. Read local signatures for APIs used by custom tooling.
- Confirm whether persistence changes are needed at all.
- Read the closest official page in sources.md. Follow its current links for advanced features; do not invent URL slugs or rely on release dates from memory.
- If browsing is unavailable, use installed documentation. Mark unresolved API assumptions explicitly.

## After code

1. Compile runtime and editor assemblies in the actual Unity project.
2. Inspect visible, hidden, disabled, null and empty states. Confirm group layout and callback resolution.
3. For mutating operations, exercise Undo/Redo and dirty state; test multiple selected objects and prefab overrides where supported.
4. For persistence changes, save and reload representative data. Confirm references and polymorphic types survive.
5. For custom trees/windows, reopen, switch targets and reload scripts; watch for leaked trees, exceptions and unbalanced GUI state.
6. For runtime serializer changes, follow current Sirenix AOT guidance and validate a target player build.

## Diagnose by symptom

| Symptom | Investigation |
| --- | --- |
| Field visible but lost after reload | Check ShowInInspector-only exposure, backend opt-in and Serialization Debugger |
| Attribute does nothing | Check supported member/type, existing custom editor and attribute arguments |
| Missing callback or expression error | Check name/signature, member context and supported expression syntax |
| Player build references editor APIs | Inspect asmdefs, editor folders and conditional compilation |
| Value edits fail in a struct drawer | Confirm modified struct is assigned back through value entry |
| Excessive repaint cost | Look for asset scans, allocations, reflection and tree recreation |
| Custom drawer hides other attributes | Inspect drawer chain and CallNextDrawer use |
| Data changes after backend migration | Stop further migration and compare backed-up assets and serializer ownership |

## Report honestly

Distinguish source review, static checks, Unity compilation, editor interaction and player tests. State exactly which happened. Do not claim compatibility from Markdown validation. Do not install or upgrade Odin, change its license settings, or migrate user data merely to make an example compile.
