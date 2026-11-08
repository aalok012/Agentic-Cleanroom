// Class Action
// Dafny class Action compiled into Java
package F3__1Domain;

@SuppressWarnings({"unchecked", "deprecation"})
public class Action {
  public dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> _details;
  public dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> _requirements;
  public Action (dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> details, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> requirements) {
    this._details = details;
    this._requirements = requirements;
  }

  @Override
  public boolean equals(Object other) {
    if (this == other) return true;
    if (other == null) return false;
    if (getClass() != other.getClass()) return false;
    Action o = (Action)other;
    return true && java.util.Objects.equals(this._details, o._details) && java.util.Objects.equals(this._requirements, o._requirements);
  }
  @Override
  public int hashCode() {
    long hash = 5381;
    hash = ((hash << 5) + hash) + 0;
    hash = ((hash << 5) + hash) + java.util.Objects.hashCode(this._details);
    hash = ((hash << 5) + hash) + java.util.Objects.hashCode(this._requirements);
    return (int)hash;
  }

  @Override
  public String toString() {
    StringBuilder s = new StringBuilder();
    s.append("F3_1Domain.Action.EditEventDetails");
    s.append("(");
    s.append(dafny.Helpers.toString(this._details));
    s.append(", ");
    s.append(dafny.Helpers.toString(this._requirements));
    s.append(")");
    return s.toString();
  }
  private static final dafny.TypeDescriptor<Action> _TYPE = dafny.TypeDescriptor.<Action>referenceWithInitializer(Action.class, () -> Action.Default());
  public static dafny.TypeDescriptor<Action> _typeDescriptor() {
    return (dafny.TypeDescriptor<Action>) (dafny.TypeDescriptor<?>) _TYPE;
  }

  private static final Action theDefault = Action.create(dafny.DafnyMap.<dafny.DafnySequence<? extends dafny.CodePoint>,dafny.DafnySequence<? extends dafny.CodePoint>> empty(), dafny.DafnyMap.<dafny.DafnySequence<? extends dafny.CodePoint>,dafny.DafnySequence<? extends dafny.CodePoint>> empty());
  public static Action Default() {
    return theDefault;
  }
  public static Action create(dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> details, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> requirements) {
    return new Action(details, requirements);
  }
  public static Action create_EditEventDetails(dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> details, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> requirements) {
    return create(details, requirements);
  }
  public boolean is_EditEventDetails() { return true; }
  public dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> dtor_details() {
    return this._details;
  }
  public dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> dtor_requirements() {
    return this._requirements;
  }
}
