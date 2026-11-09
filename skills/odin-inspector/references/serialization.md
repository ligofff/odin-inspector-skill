# Serialization and persistence

## Separate visibility from persistence

[ShowInInspector](https://odininspector.com/attributes/show-in-inspector-attribute) does not serialize a field or property. For a missing value, first identify the member's serializer and owning Unity object. Use Odin's Serialization Debugger rather than inferring persistence from what appears in the inspector.

The [OdinSerialize/ShowInInspector tutorial](https://odininspector.com/tutorials/using-attributes/the-odinserialize-and-the-showininspector) also describes property restrictions. Do not assume arbitrary computed, virtual or interface-backed properties can be persisted. Prefer explicit backing fields when unclear.

## Choose a backend deliberately

The [integration tutorial](https://odininspector.com/tutorials/serialize-anything/implementing-the-odin-serializer) describes opting in through `SerializedMonoBehaviour` or `SerializedScriptableObject`. A class with a required existing base type needs explicit integration; do not discard its base class. Read the full official callback integration example and the installed API before implementing `ISerializationCallbackReceiver` with `UnitySerializationUtility` and `SerializationData`.

Odin [extends Unity serialization](https://odininspector.com/tutorials/serialize-anything/on-odins-serialization-procotol). Unity still saves the containing object's Odin data. Avoid forcing both serializers to own the same field: `[OdinSerialize]` on a public Unity-supported field can duplicate serialization. When forcing Odin ownership is justified, verify the documented `NonSerialized` plus `OdinSerialize` pattern against the installed backend. Do not prescribe this combination for every field.

## Dictionary and polymorphism decisions

Check the exact Unity/Odin combination and the project's existing data format. Do not make timeless claims about Unity dictionary or polymorphic support. UI attributes such as DictionaryDrawerSettings only configure drawing.

For a new asset explicitly opting into Odin serialization, this original minimal example illustrates a private dictionary forced to Odin ownership:

```csharp
using System.Collections.Generic;
using Sirenix.OdinInspector;
using Sirenix.Serialization;
using UnityEngine;

[CreateAssetMenu(menuName = "Tools/Cost Catalog")]
public sealed class CostCatalog : SerializedScriptableObject
{
    [OdinSerialize]
    private Dictionary<string, int> costs = new Dictionary<string, int>();
}
```

Do not use this pattern in an editor-only Odin setup without verifying runtime serializer availability. For polymorphic data, inspect existing `[SerializeReference]`, Unity object references and Odin-owned fields before choosing a representation. Avoid switching an existing representation without a tested migration.

Serializer API calls, save files, refactoring attributes, AOT and Editor Only mode are in [serializer-api.md](serializer-api.md).

## Persistence and build checks

[Features and limitations](https://odininspector.com/tutorials/serialize-anything/features-and-limitations) describes platform constraints and AOT requirements. Check the current linked AOT procedure for IL2CPP/AOT builds; do not assume editor success proves player compatibility.

For relevant changes: edit a value, save the scene/asset, deselect/reselect, reload the domain or restart Unity, and inspect the saved value. Exercise prefab instances and overrides if used. For runtime serialization, test a player build on the target backend. Preserve representative existing assets before changing base classes, member names or serialization ownership.
