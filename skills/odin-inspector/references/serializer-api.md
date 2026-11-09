# Odin Serializer: API, refactoring and AOT

Read [serialization.md](serialization.md) first for ownership decisions. Sources: [Features And Limitations](https://odininspector.com/tutorials/serialize-anything/features-and-limitations), [Serializing Without Serialized Base Classes](https://odininspector.com/tutorials/serialize-anything/serializing-without-serialized-base-classes), [Making Save Games](https://odininspector.com/tutorials/serialize-anything/making-save-games-with-the-odin-serializer), [External Reference Resolver](https://odininspector.com/tutorials/serialize-anything/external-reference-resolver), [Refactoring](https://odininspector.com/tutorials/serialize-anything/refactoring), [AOT Serialization](https://odininspector.com/tutorials/serialize-anything/aot-serialization), [Best Practices](https://odininspector.com/tutorials/serialize-anything/best-practices), [Serializing Dictionaries](https://odininspector.com/tutorials/serialize-anything/serializing-dictionaries), [Avoiding Unity's Infinite Depth Warning](https://odininspector.com/tutorials/serialize-anything/avoiding-unity-s-infinite-depth-warning), [Serialization Debugger](https://odininspector.com/tutorials/serialize-anything/serialization-debugger), [Editor Only Mode](https://odininspector.com/tutorials/getting-started/editor-only-mode).

## Unity object integration

- Base classes that opt in: `SerializedMonoBehaviour`, `SerializedScriptableObject`, `SerializedBehaviour`, `SerializedComponent`, `SerializedStateMachineBehaviour`, `SerializedNetworkBehaviour`, `SerializedUnityObject`. With a required other base class, implement `ISerializationCallbackReceiver` per the integration tutorial.
- What Odin serializes on these: public fields and `[SerializeField]` private fields that Unity would not serialize, plus anything marked `[OdinSerialize]` (fields and auto-properties). Fields Unity can serialize stay Unity's.
- `[NonSerialized, OdinSerialize]` forces Odin ownership of a field Unity could serialize; also the fix for Unity's infinite-depth warning on self-referencing types.
- Odin runs after Unity's pass and stores its data inside the Unity object, so it is always slower than Unity alone. Use Unity serialization where it suffices.
- Prefab modifications on Odin-serialized members are stored differently from Unity's and may display or merge unexpectedly; test prefab overrides explicitly.
- Formats: `Binary` (default in builds and play mode), `Nodes` (default for editor assets outside play mode; text-friendly for version control), `JSON` (never default; slow; Odin JSON contains `$`-prefixed metadata and is not plain JSON).

## Serializing arbitrary data

Namespace `Sirenix.Serialization`.

```csharp
// Original example. Requires Odin runtime serialization in builds (not Editor Only mode).
using System.Collections.Generic;
using System.IO;
using Sirenix.Serialization;

public static class SaveSystem
{
    public static void Save(string path, PlayerState state)
    {
        byte[] bytes = SerializationUtility.SerializeValue(state, DataFormat.Binary);
        File.WriteAllBytes(path, bytes);
    }

    public static PlayerState Load(string path)
    {
        byte[] bytes = File.ReadAllBytes(path);
        return SerializationUtility.DeserializeValue<PlayerState>(bytes, DataFormat.Binary);
    }
}
```

- Overloads take a `SerializationContext` / `DeserializationContext`, or an `out List<UnityEngine.Object>` on serialize and the same list on deserialize so Unity object references become indices.
- At runtime, Odin cannot save Unity object references or their contents to a file. Keep save data in plain C# state classes and store IDs for assets.
- External references: implement `IExternalStringReferenceResolver` or `IExternalGuidReferenceResolver` (chainable via `NextResolver`) or `IExternalIndexReferenceResolver` (not chainable; same list both ways) and set them on the context (`StringReferenceResolver`, `GuidReferenceResolver`, `IndexReferenceResolver`). The tutorial's sample code is illustrative and contains inconsistencies; write against installed signatures.
- Version save files yourself; renamed or removed types break old saves unless bound (below).
- Security: do not deserialize files or network data from untrusted sources with polymorphic type information. Constrain allowed types with a custom `TwoWaySerializationBinder` or switch to a format without type metadata. Confirm the binder API in the installed version.
- Custom formatters (`MinimalBaseFormatter<T>`, `BaseFormatter<T>`, registered with `[assembly: RegisterFormatter(typeof(...))]`) handle types the default reflection formatter cannot. Verify base classes and registration in the installed API before writing one.

## Refactoring serialized data

- Rename a field: Unity's `[FormerlySerializedAs("old")]` works for Odin data too and is preferred; Odin's `[PreviouslySerializedAs("old")]` exists mainly for serialized properties.
- Rename/move a type or namespace in Odin data: `[assembly: BindTypeNameToType("Old.Namespace.OldName", typeof(New.Namespace.NewName))]`.
- Neither moves data between Unity and Odin ownership. To migrate, keep the old field (`[HideInInspector]`), add the new Odin field, copy in `OnAfterDeserialize`, reserialize assets (`AssetDatabase.ForceReserializeAssets`), verify, then remove the old field.
- Always back up representative assets before migration.

## AOT (IL2CPP and other AOT platforms)

- Odin serialization works on all platforms except UWP non-IL2CPP builds. AOT platforms need generated code so stripping does not remove required generic variants.
- Preferred: Tools > Odin Inspector > Preferences > Serialization > AOT Generation, enable automation for AOT platforms. Odin scans, generates a DLL for the build and cleans up.
- Manual: Scan Project, review the type list (custom additions persist across scans), Generate DLL, then build. Repeat before every AOT build. Generated DLLs live under `Assets/Plugins/Sirenix/Assemblies/AOT` by default; ignore them in source control.
- Types created only at runtime (not present in scanned assets) must be added to the list manually. Validate with a real player build on the target platform.

## Editor Only mode

Tools > Odin Inspector > Preferences > Editor Only Mode (or the Editor Only build) keeps almost all Odin code out of builds; only the small attributes assembly ships. The serializer still runs in the editor, but runtime Odin serialization (`Serialized*` base classes' data, `SerializationUtility`) is not available in players. Check this mode before proposing Odin-serialized runtime data.

## Diagnostics

Use the Serialization Debugger (Tools > Odin > Serialization Debugger, or the button on a Serialized* inspector) to see, per member, whether Unity, Odin or nobody serializes it. Use it before and after any ownership change.
