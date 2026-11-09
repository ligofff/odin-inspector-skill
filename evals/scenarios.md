# Manual behavior scenarios

Give the prompt and skill to an agent without the expected outcomes. Evaluate its output afterward. These are manual regression cases, not evidence of Unity execution.

| Prompt | Expected behavior |
| --- | --- |
| Add tabs and a conditional delay field to my existing MonoBehaviour. | Retains base class and backend; uses attributes; checks installed API. |
| My ShowInInspector dictionary disappears after restart. | Separates display and persistence; investigates serializer opt-in; does not promise an attribute-only fix. |
| Add OdinSerialize to all public fields to make saving reliable. | Explains duplicate-ownership risk and chooses a targeted fix. |
| This component must inherit from our networking base class. Add dictionary persistence. | Preserves base class; investigates existing serialization and official integration before coding. |
| Make an Odin window with a custom OnGUI override. | Reviews Odin lifecycle and uses a supported integration point. |
| Create a struct drawer for two values. | Handles null label, modifies a copy, writes it back; checks multi-selection. |
| Build an IL2CPP player using Odin-serialized polymorphic objects. | Checks installed runtime setup and official AOT guidance; requests actual target validation. |
| I have no Unity installed here. Is this guaranteed to compile? | Clearly states compilation is unverified. |
| Build an editor window listing all ItemDefinition assets with a create button. | Uses OdinMenuEditorWindow/BuildMenuTree, editor assembly, rebuilds tree after creation, asks before deletes. |
| Show a "Damage per second" value computed from two fields. | ShowInInspector with ReadOnly or DisplayAsString on a property; does not serialize it. |
| Add Odin attributes to a third-party class I cannot edit. | Proposes an OdinAttributeProcessor in an editor assembly; notes it cannot change serialization. |
| Save player progress to a file with Odin. | Uses SerializationUtility with a plain state class; avoids Unity object references; checks Editor Only mode, AOT and untrusted-data risk. |
| Rename a class whose instances are stored in Odin-serialized assets. | Uses BindTypeNameToType; backs up assets; verifies with Serialization Debugger. |
| Fail our CI build when any item asset has an empty Id. | Checks Odin Validator is installed; writes a registered RootObjectValidator and a ValidationSession entry point. |
| Group these 12 fields into tabs with a foldout inside one tab. | Uses consistent slash group paths; no conflicting group types at one path. |
| Make my custom drawer apply to all classes implementing IDamageable. | Uses a generic drawer with a `where T : IDamageable` constraint, not `OdinValueDrawer<IDamageable>`. |
