# Editor windows and custom drawing

## Assembly boundary

Put editor implementation in an editor-only assembly. Keep custom attribute declarations runtime-safe when applied to runtime classes. Verify asmdef references against the installed package; do not guess assembly names. Unity editor API calls inside callbacks still require an editor boundary.

## OdinEditorWindow

The [window tutorial](https://odininspector.com/tutorials/custom-editor-windows/how-to-make-an-odineditorwindow) uses `OdinEditorWindow` to draw members with attributes. Do not override `OnGUI` casually: the tutorial recommends `DrawEditors` or `OnInspectorGUI` for custom GUI integration. Verify the installed override signature and base lifecycle calls before customizing.

Original example, saved in an editor assembly as `AssetReviewWindow.cs`:

```csharp
using Sirenix.OdinInspector;
using Sirenix.OdinInspector.Editor;
using UnityEditor;
using UnityEngine;

public sealed class AssetReviewWindow : OdinEditorWindow
{
    [MenuItem("Tools/Asset Review")]
    private static void Open() => GetWindow<AssetReviewWindow>().Show();

    [ShowInInspector, InlineEditor]
    private ScriptableObject inspectedAsset;
}
```

This window is an inspection surface, not a persistence system for its own selection. For menu-based navigation, selectors and `OdinEditor`, see [menu-windows.md](menu-windows.md). Window ownership must not silently create or delete user assets.

## Choose the drawer type

- Use [`OdinValueDrawer<T>`](https://odininspector.com/tutorials/how-to-create-custom-drawers-using-odin/how-to-create-a-custom-value-drawer) for a value type's custom presentation. Override `DrawPropertyLayout(GUIContent label)`, accept a null label, and use `ValueEntry.SmartValue` for the normal value-entry path. For structs, modify a local copy and assign it back. Do not claim advanced multi-selection works without testing it.
- Use [`OdinAttributeDrawer<TAttribute>`](https://odininspector.com/documentation/sirenix.odininspector.editor.odinattributedrawer-1) for attribute-driven behavior; use the typed variant when constraining value types. A decorating drawer should continue the drawer chain with `CallNextDrawer(label)`. A terminal value drawer typically supplies the final control instead.
- Verify registration and priority against the installed Odin version. Online API remarks and tutorial examples can differ; do not mechanically add an obsolete registration attribute.

- Use [`OdinGroupDrawer<TGroupAttribute>`](https://odininspector.com/tutorials/how-to-create-custom-drawers-using-odin/how-to-make-a-custom-group) for a custom group. The attribute subclasses `PropertyGroupAttribute` (constructor passes the group path to `base(path)`) and overrides `CombineValuesWith(PropertyGroupAttribute other)` to merge settings declared on several members. The drawer draws its children with `this.Property.Children[i].Draw()`; persist foldout state with `this.GetPersistentValue<bool>(key, default)` (a `LocalPersistentContext<bool>`).
- To draw a class's whole inspector differently, a value drawer for that type is usually enough; see the official [struct](https://odininspector.com/tutorials/how-to-create-custom-drawers-using-odin/odin-value-drawers-for-structs) and [class](https://odininspector.com/tutorials/how-to-create-custom-drawers-using-odin/odin-value-drawers-for-classes) drawer tutorials.

## Drawer matching and ordering

- [Generic constraints](https://odininspector.com/tutorials/how-to-create-custom-drawers-using-odin/understanding-generic-constraints-on-odin-drawers): `OdinValueDrawer<Item>` matches only `Item`; use `class ItemDrawer<T> : OdinValueDrawer<T> where T : Item` for derived types. Interfaces and abstract types require the generic-constraint form. Multi-parameter constraints (`where TList : IList<TElement>`) are supported.
- `CanDrawTypeFilter(Type)` and `CanDrawAttributeProperty` / `CanDrawProperty(InspectorProperty)` refine matching; constraints are cheaper than runtime checks.
- `[DrawerPriority(super, wrapper, value)]` orders drawers; wrappers (decorators) run before value drawers. Use `[ShowDrawerChain]` to debug the chain. `SkipWhenDrawing` lets a drawer step aside at runtime (verify).
- Drawers are discovered automatically; there is no registration step in current versions.

## IMGUI helpers

`Sirenix.Utilities.Editor` provides `SirenixEditorGUI` (boxes, headers, foldouts, fade groups, toolbars, info/error boxes, `BeginHorizontalToolbar`, `ToolbarButton`), `SirenixEditorFields` (Odin-styled fields with rect and layout overloads), `GUIHelper` (`PushColor`/`PopColor`, `PushGUIEnabled`, `PushLabelWidth`, `RequestRepaint`) and `SirenixGUIStyles`. Rect extensions (`AlignRight`, `SubXMax`, `Split`, etc.) simplify rect math. The official [tips page](https://odininspector.com/tutorials/how-to-create-custom-drawers-using-odin/tips-tricks-and-best-practices) recommends rect-based drawing over layout for performance, and `EditorGUI.BeginChangeCheck` around conversions. Every Push must have a matching Pop.

## Common GUI rules

Restore any GUI state you change, preferably with `try/finally`. Balance layout scopes even when errors occur. Avoid recursive redraws, repeated reflection, asset queries and allocations on every repaint. Route edits through Odin's property/value system rather than bypassing it through unrelated reflection writes.

## Resolvers

The [value resolver tutorial](https://odininspector.com/tutorials/value-and-action-resolvers/using-value-resolvers) creates resolvers in `Initialize()` and reads their values during drawing. Check the exact `ValueResolver` API and error-reporting method for the installed version. Surface resolver errors visibly and avoid executing an invalid resolver. Do not build a new expression evaluator. Action resolvers, named values and property states are covered in [processors-resolvers.md](processors-resolvers.md). Recreate cached state when its property/target context changes.

## PropertyTree ownership

The official [`PropertyTree` API](https://odininspector.com/documentation/sirenix.odininspector.editor.propertytree) offers creation, drawing and disposal. Cache a tree for its targets, dispose owned trees when the host closes or targets change, and recreate when needed. Do not dispose a tree owned by Odin's host. `Draw` handles the normal Undo/dirty workflow; custom drawing paths require their own lifecycle review. Do not recreate a tree every repaint or treat property paths as interchangeable with Unity SerializedProperty paths.
