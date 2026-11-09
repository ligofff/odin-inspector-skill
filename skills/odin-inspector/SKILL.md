---
name: odin-inspector
description: Implement and debug Unity C# inspectors, editor tooling and data serialization with Sirenix Odin Inspector, Odin Serializer and Odin Validator. Use for any Odin attribute (groups, conditionals, buttons, dropdowns, tables, asset pickers, validation), SerializedMonoBehaviour/SerializedScriptableObject, Odin serialization and save data, AOT/IL2CPP setup, OdinEditorWindow and OdinMenuEditorWindow tools, custom value/attribute/group drawers, PropertyTree, value and action resolvers, attribute and property processors, custom validators and validation pipelines. Ground API decisions in official Sirenix documentation and the project's installed version. Not for the Odin programming language.
---

# Odin Inspector for Unity

Build the smallest maintainable solution that fits the project's installed Odin and Unity versions. These are community-authored instructions based on official Sirenix sources, not an official Sirenix product.

## Establish project facts

1. Read project instructions and nearby C# code. Inspect `ProjectSettings/ProjectVersion.txt`, package manifests, Sirenix installation metadata and assembly definitions. Odin may be under Assets or Packages; do not assume a fixed installation path. See [setup.md](references/setup.md).
2. Determine the installed Unity and Odin versions, whether Editor Only mode is on, whether Odin Validator is installed, serializer choice, target platforms and existing custom editors. Ask only for facts that block the task. Without project access, state assumptions and provide a conditional implementation.
3. Keep existing base classes and serialized field names unless a migration is explicitly needed. Do not switch serialization backends just to improve appearance.
4. Consult the relevant reference below. For every unfamiliar constructor, named parameter, callback signature or version-sensitive API, check installed source/XML docs or the linked official page before writing it. If online docs and installed signatures disagree, use installed signatures and explain the discrepancy. Never invent overloads, symbols, assembly names or version guarantees.

## Route the work

| Task | Read |
| --- | --- |
| Pick attributes; full catalog by category | [attribute-catalog.md](references/attribute-catalog.md) |
| Layout patterns, expressions, validation and dropdown details | [attributes.md](references/attributes.md) |
| Values disappear, dictionaries, polymorphism, ownership | [serialization.md](references/serialization.md) |
| SerializationUtility, save files, refactoring, AOT, Editor Only mode | [serializer-api.md](references/serializer-api.md) |
| Custom drawers, groups, PropertyTree, IMGUI helpers | [editor-tools.md](references/editor-tools.md) |
| OdinEditorWindow, OdinMenuEditorWindow, selectors, OdinEditor | [menu-windows.md](references/menu-windows.md) |
| Resolvers, named values, property states, attribute/property processors | [processors-resolvers.md](references/processors-resolvers.md) |
| ISelfValidator, Odin Validator, custom validators, CI | [validator.md](references/validator.md) |
| Installation, asmdefs, modules, source control, preferences | [setup.md](references/setup.md) |
| Regressions, final verification, unknown API | [verification.md](references/verification.md) |
| Official source URLs and coverage | [sources.md](references/sources.md) |

## Implementation rules

- Prefer built-in attributes before processors, and processors or attributes before custom drawers. Use `nameof` for member callbacks when that parameter accepts a member name. Keep expressions simple and free of side effects.
- Separate display, validation and persistence. `ShowInInspector` exposes a member; it does not make it persistent. `ReadOnly` is an editor UI affordance, not runtime protection.
- Use `Sirenix.OdinInspector` for inspector attributes and `Sirenix.Serialization` when explicitly using serializer APIs such as `OdinSerialize`. Keep `UnityEditor`, `Sirenix.OdinInspector.Editor` and `Sirenix.Utilities.Editor` dependencies in editor-only code and assemblies. An Editor folder alone is not a substitute for checking existing asmdef boundaries.
- Enable Odin serialization deliberately. Do not add `OdinSerialize` indiscriminately or claim that the attribute alone enables serialization on a plain MonoBehaviour. Never rely on Odin runtime serialization when Editor Only mode is enabled.
- Do not make gameplay correctness depend on inspector callbacks or validation. Keep runtime invariants in runtime logic.
- Preserve Undo, prefab modifications and multi-object behavior. Side effects invoked by buttons need explicit review; do not assume a button automatically records arbitrary mutations.
- Do not deserialize untrusted data with Odin's polymorphic formats without restricting types.
- Do not change Odin preferences, modules, licenses or installation unless asked. Do not ship Sirenix binaries, license keys, or copied documentation with generated work.

## Complete the task

Implement the change, then follow the relevant checks in verification.md. Remove debug attributes such as `ShowDrawerChain`. Report modified files, important behavior and checks actually run. If Unity or Odin is unavailable, say that compilation and editor behavior remain unverified; never substitute a text check for a Unity test. Link official sources for non-obvious API or serialization choices. Respond in the user's language.
