// Class History
// Dafny class History compiled into Java
package F3__1Kernel;

@SuppressWarnings({"unchecked", "deprecation"})
public class History {
  public dafny.DafnySequence<? extends dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> _past;
  public dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>> _present;
  public dafny.DafnySequence<? extends dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> _future;
  public History (dafny.DafnySequence<? extends dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> past, dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>> present, dafny.DafnySequence<? extends dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> future) {
    this._past = past;
    this._present = present;
    this._future = future;
  }

  @Override
  public boolean equals(Object other) {
    if (this == other) return true;
    if (other == null) return false;
    if (getClass() != other.getClass()) return false;
    History o = (History)other;
    return true && java.util.Objects.equals(this._past, o._past) && java.util.Objects.equals(this._present, o._present) && java.util.Objects.equals(this._future, o._future);
  }
  @Override
  public int hashCode() {
    long hash = 5381;
    hash = ((hash << 5) + hash) + 0;
    hash = ((hash << 5) + hash) + java.util.Objects.hashCode(this._past);
    hash = ((hash << 5) + hash) + java.util.Objects.hashCode(this._present);
    hash = ((hash << 5) + hash) + java.util.Objects.hashCode(this._future);
    return (int)hash;
  }

  @Override
  public String toString() {
    StringBuilder s = new StringBuilder();
    s.append("F3_1Kernel.History.History");
    s.append("(");
    s.append(dafny.Helpers.toString(this._past));
    s.append(", ");
    s.append(dafny.Helpers.toString(this._present));
    s.append(", ");
    s.append(dafny.Helpers.toString(this._future));
    s.append(")");
    return s.toString();
  }
  private static final dafny.TypeDescriptor<History> _TYPE = dafny.TypeDescriptor.<History>referenceWithInitializer(History.class, () -> History.Default());
  public static dafny.TypeDescriptor<History> _typeDescriptor() {
    return (dafny.TypeDescriptor<History>) (dafny.TypeDescriptor<?>) _TYPE;
  }

  private static final History theDefault = History.create(dafny.DafnySequence.<dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> empty(dafny.Tuple3.<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>_typeDescriptor(dafny.DafnySequence.<dafny.CodePoint>_typeDescriptor(dafny.TypeDescriptor.UNICODE_CHAR), dafny.DafnyMap.<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnySequence<? extends dafny.CodePoint>>_typeDescriptor(dafny.DafnySequence.<dafny.CodePoint>_typeDescriptor(dafny.TypeDescriptor.UNICODE_CHAR), dafny.DafnySequence.<dafny.CodePoint>_typeDescriptor(dafny.TypeDescriptor.UNICODE_CHAR)), dafny.DafnyMap.<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnySequence<? extends dafny.CodePoint>>_typeDescriptor(dafny.DafnySequence.<dafny.CodePoint>_typeDescriptor(dafny.TypeDescriptor.UNICODE_CHAR), dafny.DafnySequence.<dafny.CodePoint>_typeDescriptor(dafny.TypeDescriptor.UNICODE_CHAR)))), dafny.Tuple3.<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>Default(dafny.DafnySequence.<dafny.CodePoint> empty(dafny.TypeDescriptor.UNICODE_CHAR), dafny.DafnyMap.<dafny.DafnySequence<? extends dafny.CodePoint>,dafny.DafnySequence<? extends dafny.CodePoint>> empty(), dafny.DafnyMap.<dafny.DafnySequence<? extends dafny.CodePoint>,dafny.DafnySequence<? extends dafny.CodePoint>> empty()), dafny.DafnySequence.<dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> empty(dafny.Tuple3.<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>_typeDescriptor(dafny.DafnySequence.<dafny.CodePoint>_typeDescriptor(dafny.TypeDescriptor.UNICODE_CHAR), dafny.DafnyMap.<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnySequence<? extends dafny.CodePoint>>_typeDescriptor(dafny.DafnySequence.<dafny.CodePoint>_typeDescriptor(dafny.TypeDescriptor.UNICODE_CHAR), dafny.DafnySequence.<dafny.CodePoint>_typeDescriptor(dafny.TypeDescriptor.UNICODE_CHAR)), dafny.DafnyMap.<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnySequence<? extends dafny.CodePoint>>_typeDescriptor(dafny.DafnySequence.<dafny.CodePoint>_typeDescriptor(dafny.TypeDescriptor.UNICODE_CHAR), dafny.DafnySequence.<dafny.CodePoint>_typeDescriptor(dafny.TypeDescriptor.UNICODE_CHAR)))));
  public static History Default() {
    return theDefault;
  }
  public static History create(dafny.DafnySequence<? extends dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> past, dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>> present, dafny.DafnySequence<? extends dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> future) {
    return new History(past, present, future);
  }
  public static History create_History(dafny.DafnySequence<? extends dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> past, dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>> present, dafny.DafnySequence<? extends dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> future) {
    return create(past, present, future);
  }
  public boolean is_History() { return true; }
  public dafny.DafnySequence<? extends dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> dtor_past() {
    return this._past;
  }
  public dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>> dtor_present() {
    return this._present;
  }
  public dafny.DafnySequence<? extends dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>> dtor_future() {
    return this._future;
  }
}
