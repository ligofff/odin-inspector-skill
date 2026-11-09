# Resolvers, named values, property states and processors

Editor-only APIs (`Sirenix.OdinInspector.Editor`, `.ValueResolvers`, `.ActionResolvers`). Sources: [Resolving Strings to Stuff](https://odininspector.com/tutorials/value-and-action-resolvers/resolving-strings-to-stuff), [Using Value Resolvers](https://odininspector.com/tutorials/value-and-action-resolvers/using-value-resolvers), [Using Action Resolvers](https://odininspector.com/tutorials/value-and-action-resolvers/using-action-resolvers), [Named Values](https://odininspector.com/tutorials/value-and-action-resolvers/named-values), [Property States](https://odininspector.com/tutorials/using-attributes/property-states), [Using Custom Attribute Processors](https://odininspector.com/tutorials/using-property-resolvers-and-attribute-processors/using-custom-attribute-processors), [Custom Property Processors](https://odininspector.com/tutorials/using-property-resolvers-and-attribute-processors/custom-property-processors).

## Value resolvers

Turn an attribute string into a value: a member name, a `$member` reference or an `@` expression.

- Create in `Initialize()`: `ValueResolver.Get<T>(this.Property, this.Attribute.SomeString)`; strings meant to be either literal text or a reference use `ValueResolver.GetForString(this.Property, str)`. Some overloads take a fallback value; verify.
- In `DrawPropertyLayout`: if `resolver.HasError`, call `resolver.DrawError()` (singular in the official tutorial) and avoid using the value; otherwise read `resolver.GetValue()`. With multi-selection, `GetValue(selectionIndex)` reads per target (verify).
- Resolvers report errors instead of throwing; surface them, do not swallow.

## Action resolvers

Run an attribute string as an action: method name or `@` expression (e.g. `@UnityEngine.Debug.Log($value)`).

- `ActionResolver.Get(this.Property, this.Attribute.Action)` in `Initialize()`.
- On trigger: `resolver.DoActionForAllSelectionIndices()` (or `DoAction(index)`); draw errors with `resolver.DrawError()`.
- Built-in attributes using actions include `OnValueChanged`, `OnCollectionChanged`, `InlineButton`, `OnInspectorInit`, `OnInspectorDispose`, `OnStateUpdate`.

## Named values

Values exposed to expressions with `$name` and to referenced methods as parameters.

- Defaults: `property` (`InspectorProperty`) and `value` (the property's value, only when the property has one).
- Attribute-specific extras: e.g. `ValidateInput` adds `ref string message` and `ref InfoMessageType? messageType`, so a validator can be `bool Validate(string value, ref string message, ref InfoMessageType? messageType)`. Check each attribute page for its named values.
- Custom named values: pass `new NamedValue[] { new NamedValue("hour", typeof(int)) }` when creating the resolver and update with `resolver.Context.NamedValues.Set("hour", h)` before evaluating.
- Advanced: build a `ValueResolverContext` (`ValueResolverContext.CreateDefault<T>(...)`), set flags such as `SyncRefParametersWithNamedValues` before `ValueResolver.GetFromContext<T>(ref context)`; changing it afterwards throws.
- In expressions, `$property.Parent`, `$property.Path` and `$root` (root object; verify availability) give context. Prefer named methods over long expressions.

## Property states

`InspectorProperty.State` (since 3.0) holds `Visible`, `Enabled` and `Expanded` (persistent). `Enabled = false` can disable GUI but cannot re-enable GUI disabled by a parent. Custom states: `State.Create<T>(name, persistent, default)` once, then `State.Get<T>(name)` / `State.Set(name, v)` (verify signatures). Groups are addressed with `#`: in expressions `#(member)` targets a sibling property and `#(#Tabs)` a group named `Tabs`; `TabGroup` exposes `CurrentTabIndex`, `CurrentTabName`, `TabCount`. Typical use: `[OnStateUpdate("@#(details).State.Expanded = $value")]`.

## Attribute processors

Add, remove or change inspector attributes without editing the target type (third-party types, generated code, bulk policies).

```csharp
// Editor assembly. Original example; verify against the installed API.
using System;
using System.Collections.Generic;
using System.Reflection;
using Sirenix.OdinInspector;
using Sirenix.OdinInspector.Editor;

public sealed class SpawnPointProcessor : OdinAttributeProcessor<SpawnPoint>
{
    public override void ProcessSelfAttributes(InspectorProperty property, List<Attribute> attributes)
    {
        attributes.Add(new InlinePropertyAttribute());
    }

    public override void ProcessChildMemberAttributes(InspectorProperty parentProperty, MemberInfo member, List<Attribute> attributes)
    {
        if (member.Name == nameof(SpawnPoint.Radius))
            attributes.Add(new MinValueAttribute(0));
    }
}
```

- `ProcessSelfAttributes` affects properties whose value type matches; `ProcessChildMemberAttributes` affects each direct child member. `CanProcessSelfAttributes` / `CanProcessChildMemberAttributes` overrides narrow applicability (verify).
- Generic constraints behave like drawer constraints (`OdinAttributeProcessor<T> where T : IFoo`). Processors are discovered automatically.
- Processors change inspector attributes only. Serialization attributes (`SerializeField`, `OdinSerialize`) are read from members directly and cannot be added this way.

## Property processors

`OdinPropertyProcessor<TValue>` (and `<TValue, TAttribute>`) override `ProcessMemberProperties(List<InspectorPropertyInfo> propertyInfos)` to add, remove or reorder the child members Odin shows: e.g. add a virtual button or computed value, or hide a member. Helpers in the installed API include `propertyInfos.AddValue(...)`, `AddDelegate(...)`, `Remove(...)` / `RemoveAt` and `InspectorPropertyInfo.CreateValue(...)`; confirm exact overloads before use. Added members are inspector-only and never serialized.

## Property resolvers

`OdinPropertyResolver` subclasses decide how a value's children are produced (how lists, dictionaries and custom collections are expanded). Writing one is rare; use `[ShowPropertyResolver]` to debug which resolver is in effect before writing one.
