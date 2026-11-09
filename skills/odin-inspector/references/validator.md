# Validation and Odin Validator

Inspector validation attributes (`Required`, `ValidateInput`, `MinValue`, `RequiredListLength`, etc.) and `ISelfValidator` show errors in the inspector. The Odin Validator product scans the whole project, scenes and assets and adds custom validators, rules, fixes and pipeline use. Confirm whether the project has Odin Validator (look for `Sirenix.OdinValidator.Editor` and the Validator window) before writing validator classes or pipeline code. Sources: [Getting Started With Odin Validator](https://odininspector.com/tutorials/odin-validator/getting-started-with-odin-validator), [Validator Types Overview](https://odininspector.com/tutorials/odin-validator/validator-types-overview), [Validators vs Validation Rules](https://odininspector.com/tutorials/odin-validator/validators-vs-validation-rules), [Creating Custom Fixes](https://odininspector.com/tutorials/odin-validator/creating-custom-fixes), [Custom Pipeline](https://odininspector.com/tutorials/odin-validator/using-the-validator-in-your-custom-pipeline), [Migrating Validators to 3.1](https://odininspector.com/tutorials/odin-validator/migrating-2.1-and-3.0-validators-to-3.1).

## Choose a validator type

| Type | Base | Validates |
| --- | --- | --- |
| Value validator | `ValueValidator<T>` | Every value of type `T` anywhere (fields, list elements). |
| Root object validator | `RootObjectValidator<T>` | Root Unity objects (assets, components) of type `T`. |
| Attribute validator | `AttributeValidator<TAttribute, TValue>` | Members carrying a custom attribute; read `this.Attribute`. |
| Scene validator | `SceneValidator` | A scene as a whole (e.g. exactly one AudioListener). |
| Self validator | `ISelfValidator` (`Sirenix.OdinInspector`, runtime namespace) | The type validates itself with private access. |

Base classes and `ValidationResult` are in `Sirenix.OdinInspector.Editor.Validation` and belong in editor code.

## Writing validators

```csharp
// Editor assembly. Original example; verify against the installed API.
using Sirenix.OdinInspector.Editor.Validation;

[assembly: RegisterValidator(typeof(NonEmptyIdValidator))]

public sealed class NonEmptyIdValidator : RootObjectValidator<ItemDefinition>
{
    protected override void Validate(ValidationResult result)
    {
        if (string.IsNullOrWhiteSpace(this.Value.Id))
            result.AddError("Item has no Id.")
                  .WithFix(() => this.Value.Id = System.Guid.NewGuid().ToString("N"));
    }
}
```

- Register every validator except `ISelfValidator` with `[assembly: RegisterValidator(typeof(X))]`, or `[assembly: RegisterValidationRule(typeof(X))]` when it should appear in the Rules tab with an enable toggle and serialized configuration (e.g. a `ValidatorSeverity` field used via `result.Add(severity, msg)`).
- Result API: `AddError`, `AddWarning`, `Add(severity, msg)`, chained with `.WithFix(...)`, `.WithButton(...)`, `.WithContextClick(...)`, `.WithSceneGUI(...)`, `.WithSelectionObject(...)`, `.WithMetaData(...)`, `.EnableRichText()`.
- Fixes with arguments: `.WithFix<FixArgs>(args => ...)` where `FixArgs` is a non-abstract class with a public parameterless constructor whose fields are drawn in the fix UI (verify generic form).
- Fixes that change Unity objects must keep Undo/dirty state correct; prefer modifying `this.Value` through the provided path.
- Validators must be fast, deterministic and side-effect free; they run often.

`ISelfValidator` example (runtime type):

```csharp
using Sirenix.OdinInspector;
using UnityEngine;

public sealed class Spawner : MonoBehaviour, ISelfValidator
{
    [SerializeField] private GameObject prefab;
    [SerializeField] private int count = 1;

    public void Validate(SelfValidationResult result)
    {
        if (prefab == null) result.AddError("Prefab is missing.");
        if (count <= 0) result.AddWarning("Count should be positive.");
    }
}
```

## Pipeline / CI

```csharp
// Editor code, Odin Validator required. Verify namespaces in the installed version.
using (var session = new ValidationSession(ValidationProfile.MainValidationProfile))
{
    foreach (var result in session.ValidateEverythingEnumerator(openClosedScenes: true, showProgressBar: false))
    {
        if (result.ResultType == ValidationResultType.Error) { /* fail the build */ }
    }
}
```

Custom profiles are assets loaded with `AssetDatabase.LoadAssetAtPath<ValidationProfile>(...)`. Sessions can export `ToJson()` / `ToHtml()` reports. Hook into a build preprocess step or a batchmode `-executeMethod` entry point; make failures explicit.

## Version notes

Validator 3.1 changed the validator API. Code written for 2.1/3.0 (e.g. old `Validator` signatures) needs the official migration guide. Check the installed version before copying older examples.
