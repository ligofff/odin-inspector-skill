# Inspector attributes

## Choose a minimal surface

Use the [official attribute catalog](https://odininspector.com/attributes) to choose attributes and verify constructor arguments. Useful starting points:

| Intent | Candidates to inspect |
| --- | --- |
| Related fields | BoxGroup, FoldoutGroup, TabGroup |
| Horizontal/vertical arrangement | HorizontalGroup, VerticalGroup |
| Ordering and labels | PropertyOrder, LabelText, Title |
| Conditional visibility/editing | ShowIf, HideIf, EnableIf, DisableIf |
| Read-only diagnostics | ShowInInspector, ReadOnly |
| Actions | Button, InlineButton |
| Lists and tables | ListDrawerSettings, TableList |
| Inline object editing | InlineEditor, InlineProperty |
| Constraints and diagnostics | Required, ValidateInput, MinValue |

This is a navigation list; the complete list by category is in [attribute-catalog.md](attribute-catalog.md). Check exact attribute pages before using optional settings. Use consistent group paths; avoid conflicting group types at the same path.

## Member callbacks and expressions

[Attribute expressions](https://odininspector.com/tutorials/using-attributes/attribute-expressions) start with `@` where supported. Do not assume every string parameter accepts expressions. Named values such as `$value` and `$property` depend on the resolver context. Prefer a named predicate for complex conditions so refactoring and unit testing remain straightforward. Do not perform asset scans or mutations from a frequently evaluated UI getter.

## Validation

[ValidateInput](https://odininspector.com/attributes/validate-input-attribute) can call a method returning a boolean and can provide a message. Match the inspected value's type and check overloads before using dynamic messages. Make validators deterministic and null-safe. Treat them as authoring feedback; runtime input needs its own validation. For `ISelfValidator`, custom validators and project-wide Odin Validator workflows see [validator.md](validator.md).

## Dropdowns

[ValueDropdown](https://odininspector.com/attributes/value-dropdown-attribute) obtains options from a named member. Match option types to the field. Use `ValueDropdownList<T>` when display names should differ from stored values. Empty results and missing references must be handled. Cache expensive discovery outside repaint and expose an explicit refresh when appropriate.

## Original example: Unity-serialized authoring data

Save as `LaunchSettings.cs`. This example intentionally retains ordinary Unity serialization; Odin changes presentation. Compile against the installed Odin version before adopting it.

```csharp
using Sirenix.OdinInspector;
using UnityEngine;

[CreateAssetMenu(menuName = "Tools/Launch Settings")]
public sealed class LaunchSettings : ScriptableObject
{
    [SerializeField, BoxGroup("Launch")]
    private bool useDelay;

    [SerializeField, BoxGroup("Launch"), ShowIf(nameof(useDelay))]
    [ValidateInput(nameof(IsDelayValid), "Delay must be non-negative.")]
    private float delaySeconds;

    [SerializeField, ValueDropdown(nameof(AllowedCounts))]
    private int launchCount = 2;

    private static readonly int[] AllowedCounts = { 2, 4, 8 };
    private bool IsDelayValid(float value) => value >= 0f;

    [ShowInInspector, ReadOnly]
    private float EffectiveDelay => useDelay ? delaySeconds : 0f;
}
```

The computed diagnostic property is intentionally not persisted. Validation feedback does not clamp negative values or provide a runtime guarantee.
