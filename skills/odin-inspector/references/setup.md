# Installation, project setup and team workflow

Sources: [Installing Odin Inspector](https://odininspector.com/tutorials/getting-started/installing-odin-inspector), [Install as a Unity package](https://odininspector.com/tutorials/getting-started/install-odin-inspector-as-a-unity-package), [Using Odin With Source Control](https://odininspector.com/tutorials/getting-started/using-odin-with-source-control), [Editor Only Mode](https://odininspector.com/tutorials/getting-started/editor-only-mode), [Odin Modules](https://odininspector.com/tutorials/getting-started/odin-modules), [Visual Designer](https://odininspector.com/tutorials/visual-designer/getting-started-with-the-visual-designer), [Odin Static Inspector](https://odininspector.com/tutorials/getting-started/odin-static-inspector).

## Detect the installation

- Default location `Assets/Plugins/Sirenix/` (Assembly folder with DLLs, `Odin Inspector/Config`, `Demos`). It may also be a package under `Packages/` or a moved folder. Search for `Sirenix.OdinInspector.Attributes.dll` or `Sirenix.OdinInspector.Editor` references.
- Version: Odin's About/Preferences window, release notes in the installation, or the assembly version. Do not infer from the website.
- Asset Store installs are updated by re-importing the package, not through `manifest.json`. Do not upgrade, downgrade or reinstall Odin unless the user asks.
- License/DRM activation, organization licenses and keys are the user's responsibility. Never add, read out or commit license keys.

## Assemblies and asmdefs

- Runtime code that uses attributes references the Odin attribute assembly; editor code references the editor assemblies. Precompiled DLLs are referenced automatically unless an asmdef sets `overrideReferences`; then add the Sirenix DLLs explicitly by checking the actual DLL names in the installation.
- Keep `Sirenix.OdinInspector.Editor`, `Sirenix.Utilities.Editor` and `UnityEditor` usage in editor-only assemblies or `#if UNITY_EDITOR` blocks.

## Editor Only mode

Keeps almost all Odin code out of builds (only attribute definitions ship). Runtime Odin serialization is unavailable in players in this mode. Check Preferences > Editor Only Mode before writing runtime code that depends on `Serialized*` types or `SerializationUtility`.

## Source control

- Commit Odin's config assets that the team should share (`Odin Inspector/Config` contents), unless the project has a policy.
- Ignore generated AOT assemblies (`Assets/Plugins/Sirenix/Assemblies/AOT/*`) and unpacked demos (`Assets/Plugins/Sirenix/Demos/*`, keeping `*.unitypackage`); adjust paths if Odin was moved.
- Odin `Nodes` format keeps Odin data in assets text-mergeable when Unity uses Force Text serialization.

## Modules

Since 3.0, optional integration modules (e.g. for Unity packages such as Mathematics, Entities, Localization, Addressables; check the actual list in Preferences > Modules) can be toggled. Module toggling and updating default to "Ask"; experimental modules are always opt-in. Enable a module only when the project uses that package and the user agrees.

## Visual Designer

A tool for applying Odin attributes visually without editing code, storing designs in designer files; custom attributes can be registered. Prefer code attributes when the project already uses them; do not mix both for the same members without asking.

## Global settings

Preferences (Tools > Odin Inspector > Preferences) are `GlobalConfig` assets such as `GeneralDrawerConfig`, `InspectorConfig` (which types Odin draws, Unity vs Odin per type) and serialization/AOT config. These are project-wide team settings: change only on request and report the change.
