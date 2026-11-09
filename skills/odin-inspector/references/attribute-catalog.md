# Attribute catalog

Every attribute listed in the [official catalog](https://odininspector.com/attributes), grouped by the site's categories (an attribute may appear in several). One-line purposes and common arguments are original summaries for choosing an attribute. Constructor overloads and optional named parameters vary by version: confirm them on the attribute's page (`https://odininspector.com/attributes/<kebab-name>-attribute`, e.g. `show-if-attribute`) or in the installed XML docs before using anything beyond the basics shown here. All attributes live in `Sirenix.OdinInspector` unless noted.

## Shared conventions

- **Member references.** Most string parameters that name a condition, label, title, color, list source or action accept a member name (use `nameof`) or an `@` expression. Many label/title/message parameters also accept `"$memberName"` to pull a string from a member. See [processors-resolvers.md](processors-resolvers.md) for resolver rules and named values (`$value`, `$property`, plus attribute-specific ones).
- **Conditionals compare values.** `ShowIf("mode", Mode.Advanced)` compares a member to a value; `ShowIf("@mode == Mode.Advanced")` uses an expression; `ShowIf(nameof(IsAdvanced))` uses a bool member.
- **Group paths.** Groups are identified by slash-separated paths: `[TabGroup("Main/Tabs", "Stats")]` nests a tab group inside group `Main`. Members using the same path share the group. Do not declare different group types at the same path. Optional group settings (width, order, labels) only need to be set once per group; conflicting values on the same path are merged by the group attribute. `PropertyOrder` and group `Order` control ordering.
- **Methods.** `Button`, `OnInspectorGUI` and `ShowInInspector` on methods/properties draw non-field members. Buttons with parameters render inline argument fields.

## Essentials

| Attribute | Purpose / common use |
| --- | --- |
| AssetsOnly | Object field accepts only project assets, not scene objects. |
| CustomValueDrawer | `[CustomValueDrawer(nameof(Draw))]` draws the value with a method `T Draw(T value, GUIContent label)`; editor-only method body (`#if UNITY_EDITOR`). |
| DelayedProperty | Applies edits only after the field loses focus/Enter (like Unity `Delayed`, for any property). |
| DetailedInfoBox | Info box with a short message that expands to details. |
| EnableGUI | Re-enables GUI for a member that would otherwise be disabled (e.g. get-only property shown with ShowInInspector). |
| GUIColor | Tints the member: `GUIColor(r, g, b)` or a color member/expression string. |
| HideLabel | Draws the value without its label. |
| PropertyOrder | Sort order among siblings (lower first; default 0). |
| PropertySpace | Vertical space before/after (`SpaceBefore`, `SpaceAfter`). |
| ReadOnly | Draws the member disabled in the inspector only. |
| Required | Error message when an object reference/string is null or empty. |
| RequiredIn | Required only in given prefab kinds (`PrefabKind` flags). |
| Searchable | Adds a search field to a class, list or member tree. |
| ShowInInspector | Draws a non-serialized field, property or static member. Does not serialize. |
| Title | Bold title with optional subtitle and line above a member. |
| TypeFilter | Restricts selectable types for a polymorphic field to a member returning `IEnumerable<Type>`. |
| TypeInfoBox | Info box shown at the top of a type's inspector (applied to a class). |
| ValidateInput | Calls a validation member; message and message type; supports dynamic message via `ref string message`. |
| ValueDropdown | Dropdown from a member returning values or `ValueDropdownList<T>` / `ValueDropdownItem<T>`; options like `IsUniqueList`, `ExcludeExistingValuesInList`, `DrawDropdownForListElements`. |

## Groups

| Attribute | Purpose |
| --- | --- |
| BoxGroup | Box with optional header around members. |
| FoldoutGroup | Collapsible group; `Expanded` default. |
| TabGroup | Tabs: `TabGroup("group", "Tab name")` or `TabGroup("Tab name")`. Exposes states `CurrentTabIndex`, `CurrentTabName`, `TabCount`. |
| HorizontalGroup | Side-by-side members; `Width`, `MinWidth`, `MaxWidth`, `LabelWidth`, margins. |
| VerticalGroup | Vertical stack, usually inside a HorizontalGroup column. |
| ToggleGroup | Group enabled by a bool member, drawn as a toggle header. |
| TitleGroup | Group with a Title-style header. |
| ShowIfGroup / HideIfGroup | Conditionally visible group; condition from the path or a member/expression. |
| ButtonGroup | Lays out several `[Button]` methods in one row. |
| ResponsiveButtonGroup | Button group that wraps to available width. |
| Button | Also counts as a group member when placed in groups. |

Custom groups: subclass `PropertyGroupAttribute` and write an `OdinGroupDrawer<T>`; see [editor-tools.md](editor-tools.md).

## Buttons

| Attribute | Purpose |
| --- | --- |
| Button | Draws a method as a button. Size via `ButtonSizes` or pixel height; `ButtonStyle` controls parameter display; `Expanded`, `DirtyOnClick`, `DisplayParameters`, `Icon` (version-dependent). |
| ButtonGroup / ResponsiveButtonGroup | Row of buttons (see Groups). |
| InlineButton | Small button next to a field invoking an action (`InlineButton(nameof(Reset), "Reset")`). Uses action resolvers. |
| EnumPaging | Previous/next buttons to step an enum. |
| EnumToggleButtons | Draws an enum (including flags) as toggle buttons. |

Button side effects are not automatically undoable; record Undo for Unity objects you mutate and mark them dirty.

## Collections

| Attribute | Purpose |
| --- | --- |
| ListDrawerSettings | List options: `ShowIndexLabels`, `ShowPaging`, `NumberOfItemsPerPage`, `DraggableItems`, `HideAddButton`, `HideRemoveButton`, `CustomAddFunction`, `CustomRemoveElementFunction`, `OnBeginListElementGUI`, `ListElementLabelName`, `DefaultExpandedState`, `ShowFoldout`. Names changed across versions (e.g. older `Expanded`, `IsReadOnly`); verify. |
| TableList | Draws a list of classes/structs as a table; `ShowIndexLabels`, `AlwaysExpanded`, `IsReadOnly`, paging. |
| TableColumnWidth | Column width for a member inside a TableList element (`TableColumnWidth(60, resizable: false)`). |
| TableMatrix | Draws a 2D array as a grid; custom cell drawers via `DrawElementMethod`. |
| DictionaryDrawerSettings | Dictionary display: `KeyLabel`, `ValueLabel`, `DisplayMode` (`DictionaryDisplayOptions`), `IsReadOnly`. Drawing only; persistence needs an Odin- or custom-serialized dictionary. Page URL has no `-attribute` suffix. |
| ValueDropdown | Also used for list elements (see Essentials). |

## Conditionals

| Attribute | Purpose |
| --- | --- |
| ShowIf / HideIf | Show/hide by member, value comparison or expression; `Animate` option. |
| EnableIf / DisableIf | Enable/disable editing by condition. |
| ShowIfGroup / HideIfGroup | Conditional groups. |
| ShowIn / HideIn / EnableIn / DisableIn | Condition on prefab context via `PrefabKind` flags (e.g. `PrefabKind.InstanceInScene`, `PrefabKind.PrefabAsset`). |
| DisableInEditorMode / DisableInPlayMode | Disable outside / inside play mode. |
| HideInEditorMode / HideInPlayMode | Hide outside / inside play mode. |
| DisableInInlineEditors / ShowInInlineEditors | Behavior when drawn inside an InlineEditor. |

## Misc

| Attribute | Purpose |
| --- | --- |
| CustomContextMenu | Adds a right-click menu item calling a method. |
| DisableContextMenu | Removes Odin context menus (optionally for children). |
| DrawWithUnity | Forces Unity's own drawer for this member (use for Unity PropertyDrawers that conflict with Odin). |
| HideDuplicateReferenceBox | Hides the "duplicate reference" notice for shared references. |
| Indent | Indents the member by levels. |
| InfoBox | Message box above the member; `InfoMessageType`; optional visibility condition. |
| InlineProperty | Draws a class/struct's members inline instead of in a foldout; `LabelWidth`. |
| LabelText | Custom label; supports `$member` and expressions; optional `SdfIconType` icon in newer versions. |
| LabelWidth | Label width for this member. |
| OnCollectionChanged | Calls a method before/after a collection changes, receiving `CollectionChangeInfo`. |
| OnInspectorDispose | Calls an action when the inspector property is disposed. |
| OnInspectorGUI | Draws custom IMGUI from a method, before/after the member, or as a standalone member on a method. |
| OnInspectorInit | Calls an action when the inspector property initializes. |
| OnStateUpdate | Runs an action every inspector update, typically to set property states (`@#(member).State.Visible = ...`). |
| OnValueChanged | Calls a method/action after the value changes via the inspector; `IncludeChildren`, `InvokeOnUndoRedo`, `InvokeOnInitialize`. Not called for changes from code. |
| PropertyTooltip | Tooltip; supports `$member`. |
| SuffixLabel | Text after the field (e.g. units); `Overlay` draws inside the field. |
| TypeSelectorSettings | Controls the polymorphic type selector (filter, show categories, `ShowNoneItem`). |
| TypeRegistryItem | Applied to a type: display name, icon, category in type selectors. |

## Numbers

| Attribute | Purpose |
| --- | --- |
| MinValue / MaxValue | Clamp a number (or vector components) to a constant or resolved value. |
| PropertyRange | Slider whose min/max may come from members/expressions. |
| MinMaxSlider | Two-handle slider for `Vector2`/`Vector2Int`; `ShowFields`. |
| ProgressBar | Draws a number as a progress bar; min/max/color can be resolved. Editable by dragging. |
| Unit | Shows and converts units (`Units.Meter`, display unit vs base unit); see the Unit Attributes tutorial. |
| Wrap | Wraps a value into a range (e.g. angles 0-360). |

## Type specifics

| Attribute | Purpose |
| --- | --- |
| AssetList | Draws a list/field as a checklist of matching project assets (`Path`, `AutoPopulate`, `Tags`, `LayerNames`, `AssetNamePrefix`, `CustomFilterMethod`). |
| AssetSelector | Adds a searchable asset picker button (`Paths`, `Filter`, `FlattenTreeView`). |
| ChildGameObjectsOnly | Object field accepts only children of the owning GameObject; `IncludeSelf`. |
| SceneObjectsOnly | Accepts only scene objects. |
| ColorPalette | Pick a color from a named palette (palettes edited in Odin preferences). |
| DisplayAsString | Draws a value as a non-editable label. |
| EnumPaging / EnumToggleButtons | See Buttons. |
| FilePath / FolderPath | String field with browse button; `ParentFolder`, `Extensions`, `AbsolutePath`, `RequireExistingPath`, `UseBackslashes`. |
| HideInInlineEditors / HideInTables | Hide in those contexts. |
| HideMonoScript | Hides the Script field on a component/ScriptableObject. |
| HideNetworkBehaviourFields | Hides networking base fields on network behaviours. |
| HideReferenceObjectPicker | Hides the polymorphic object picker for non-Unity references. |
| InlineEditor | Draws a referenced Unity object's inspector inline; `InlineEditorModes`, `InlineEditorObjectFieldModes`, `Expanded`, preview sizes. |
| MultiLineProperty | Multi-line text area for any string member (including properties). |
| PreviewField | Thumbnail object field; `Height`, `Alignment`, `ObjectFieldAlignment`. |
| PolymorphicDrawerSettings | Polymorphic field options (e.g. `ShowBaseType`, `ReadOnlyIfNotNullReference`, `CreateInstanceFunction`). Newer API; verify. |
| TypeDrawerSettings | Options for `System.Type` fields (base type filter, filter flags). Newer API; verify. |
| TableList / TableMatrix | See Collections. |
| Toggle | Draws a class/struct with a bool member as a toggleable foldout (`Toggle(nameof(Enabled))`). |
| ToggleLeft | Draws a bool with the checkbox left of the label. |

## Validation

AssetsOnly, ChildGameObjectsOnly, DisallowModificationsIn (blocks edits in given `PrefabKind` contexts), FilePath / FolderPath (`RequireExistingPath`), MaxValue, MinValue, MinMaxSlider, PropertyRange, Range, Required, RequiredIn, RequiredListLength (exact or min/max element count), SceneObjectsOnly, ValidateInput. Their errors appear in the inspector, and the Odin Validator product reports them project-wide (see [validator.md](validator.md)).

## Unity (Unity's own attributes, drawn by Odin)

Multiline, Range, Space, TextArea, plus `Header`, `Tooltip`, `HideInInspector`, `SerializeField`, `SerializeReference` which Odin respects. Prefer Odin equivalents only when you need their extra features.

## Debug

| Attribute | Purpose |
| --- | --- |
| ShowDrawerChain | Lists the drawers applied to a member, in order; use when a drawer is missing or overridden. |
| ShowPropertyResolver | Shows which property resolver produced a member's children. |

Remove debug attributes before finishing a task.

## Meta

| Attribute | Purpose |
| --- | --- |
| SuppressInvalidAttributeError | Silences Odin's "attribute is not valid on this member type" error. Fix the cause first. |
| IncludeMyAttributes | Put on a custom attribute class to bundle the Odin attributes declared on that class: applying the custom attribute applies them all (composite attributes). Confirm on the installed API page. |

## Choosing quickly

| Need | Prefer |
| --- | --- |
| Compact related settings | HorizontalGroup + LabelWidth, or BoxGroup/FoldoutGroup |
| Mode-dependent fields | ShowIf/HideIf on an enum, or ShowIfGroup |
| Pick one of known values | ValueDropdown, EnumToggleButtons |
| Pick assets | AssetSelector, AssetList, AssetsOnly, FolderPath/FilePath |
| Show a computed value | ShowInInspector + ReadOnly or DisplayAsString |
| Edit a referenced ScriptableObject in place | InlineEditor |
| List of rows | TableList |
| React to edits | OnValueChanged, OnCollectionChanged (editor feedback only) |
| Authoring errors | Required, ValidateInput, ISelfValidator |
| Reuse a bundle of attributes | IncludeMyAttributes composite |
