# Editor windows, menu trees and selectors

All types here are editor-only (`Sirenix.OdinInspector.Editor`, helpers in `Sirenix.Utilities.Editor`). Put them in an editor assembly or Editor folder and check asmdef references. Sources: [Odin Editor Windows](https://odininspector.com/tutorials/custom-editor-windows/odin-editor-windows), [How To Make An OdinEditorWindow](https://odininspector.com/tutorials/custom-editor-windows/how-to-make-an-odineditorwindow), API pages for [OdinMenuEditorWindow](https://odininspector.com/documentation/sirenix.odininspector.editor.odinmenueditorwindow) and [OdinMenuTree](https://odininspector.com/documentation/sirenix.odininspector.editor.odinmenutree).

## OdinEditorWindow

- Subclass `OdinEditorWindow`; open it from a `[MenuItem]` with `GetWindow<T>().Show()`. Members of the window itself are drawn with Odin attributes (groups, buttons, tables, `AssetsOnly`, etc.).
- Override `protected override object GetTarget()` to inspect another object instead of the window (for example `Selection.activeObject`). The target need not be a serializable Unity object. Overriding `GetTargets()` supports several targets (verify in installed API).
- Override `protected override void Initialize()` for setup such as `WindowPadding = Vector4.zero`.
- Do not override `OnGUI`. Customize with `DrawEditors()` (call `base.DrawEditors()` where appropriate), `OnBeginDrawEditors()` / `OnEndDrawEditors()` (verify availability), or `[OnInspectorGUI]` methods. If `OnGUI` must be overridden, call `base.OnGUI()`.
- `OdinEditorWindow.InspectObject(obj)` opens a temporary window inspecting any object (verify signature and return value in the installed version).
- The window instance is a ScriptableObject: serialized window fields persist across domain reloads but are not project assets. Do not store authoring data there.

## OdinMenuEditorWindow

A two-pane window: a searchable menu tree on the left, the selected item's inspector on the right.

```csharp
// Editor assembly. Original example; verify against the installed API.
using System.Linq;
using Sirenix.OdinInspector.Editor;
using Sirenix.Utilities.Editor;
using UnityEditor;
using UnityEngine;

public sealed class ItemDatabaseWindow : OdinMenuEditorWindow
{
    [MenuItem("Tools/Item Database")]
    private static void Open() => GetWindow<ItemDatabaseWindow>().Show();

    protected override OdinMenuTree BuildMenuTree()
    {
        var tree = new OdinMenuTree(supportsMultiSelect: false);
        tree.Config.DrawSearchToolbar = true;
        tree.AddAllAssetsAtPath("Items", "Assets/Data/Items", typeof(ScriptableObject), includeSubDirectories: true);
        tree.EnumerateTree().AddThumbnailIcons();
        tree.SortMenuItemsByName();
        return tree;
    }

    protected override void OnBeginDrawEditors()
    {
        var selected = MenuTree?.Selection.SelectedValue as Object;
        SirenixEditorGUI.BeginHorizontalToolbar();
        GUILayout.FlexibleSpace();
        if (selected != null && SirenixEditorGUI.ToolbarButton("Ping"))
            EditorGUIUtility.PingObject(selected);
        SirenixEditorGUI.EndHorizontalToolbar();
    }
}
```

Key APIs (names confirmed on official pages; parameter lists vary, so check overloads):

| API | Use |
| --- | --- |
| `BuildMenuTree()` | Required override returning a new `OdinMenuTree`. Called on open and on `ForceMenuTreeRebuild()`. |
| `tree.Add(path, instance)` | Add any object (asset, plain class, config singleton) at a menu path. Returns created items. |
| `tree.AddAssetAtPath(menuPath, assetPath)` | Add one asset. |
| `tree.AddAllAssetsAtPath(menuPath, folder, type, includeSubDirectories, flattenSubDirectories)` | Add assets found under a folder. |
| `tree.EnumerateTree()` | Enumerate items; extension methods such as `AddThumbnailIcons()`, `AddIcons(...)`, `SortMenuItemsByName()` live in `OdinMenuTreeExtensions`. |
| `tree.Selection` | `OdinMenuTreeSelection`: `SupportsMultiSelect`, `SelectedValue`, `SelectionChanged` event. |
| `tree.DefaultMenuStyle` / `OdinMenuStyle.TreeViewStyle` | Visual style of items. |
| `tree.Config` | Drawing config such as `DrawSearchToolbar`, `AutoScrollOnSelectionChanged` (verify names). |
| `MenuTree` (window property) | Current tree; `TrySelectMenuItemWithObject(obj)` selects an item (verify). |
| `ForceMenuTreeRebuild()` | Rebuild after creating/deleting assets. |

Practices:
- Build the tree from asset queries once per rebuild, not in `OnGUI`. Rebuild explicitly after create/delete operations.
- Asset creation buttons should use `AssetDatabase.CreateAsset`, `Undo.RegisterCreatedObjectUndo` where useful, then rebuild and select the new item. Ask before deleting assets; prefer `AssetDatabase.MoveAssetToTrash`.
- Menu paths use `/` for nesting; escape or sanitize asset names containing slashes.

## OdinEditor (custom inspectors)

Odin already draws every inspector it is enabled for. Write a custom `OdinEditor` subclass (`[CustomEditor(typeof(MyComponent))] public class MyEditor : OdinEditor`) only when you need inspector-level behavior such as scene GUI or a header; call `base.OnInspectorGUI()` to keep Odin drawing. Prefer attributes and drawers first. An existing Unity `Editor` for a type overrides Odin's for that type; check before blaming attributes.

## Selectors

- `OdinSelector<T>` is the base for searchable popup pickers. `GenericSelector<T>` builds one from a collection: create it, subscribe to `SelectionConfirmed` (receives `IEnumerable<T>`), then `ShowInPopup(...)`. Check the installed overloads of the constructor and `ShowInPopup`.
- `TypeSelector` (verify in installed version) lists types for polymorphic choices.
- Use selectors from buttons, custom drawers or `ValueDropdown` alternatives when the list is large or needs search/tree structure.

## Static Inspector and preferences

- The Static Inspector window (Tools > Odin menu; `StaticInspectorWindow`) shows static members of any type for debugging. Not for authoring.
- Odin preferences live under Tools > Odin Inspector > Preferences. Settings are `GlobalConfig<T>` assets (e.g. `GeneralDrawerConfig.Instance`). Change project-wide preferences only when the user asks; they affect the whole team.
