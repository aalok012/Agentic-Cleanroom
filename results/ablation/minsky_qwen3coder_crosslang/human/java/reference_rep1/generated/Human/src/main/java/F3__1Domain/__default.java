// Class __default
// Dafny class __default compiled into Java
package F3__1Domain;

@SuppressWarnings({"unchecked", "deprecation"})
public class __default {
  public __default() {
  }
  public static dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>> Init() {
    return dafny.Tuple3.<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>create(dafny.DafnySequence.asUnicodeString(""), dafny.DafnyMap.fromElements((dafny.Tuple2<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnySequence<? extends dafny.CodePoint>>[])new dafny.Tuple2[]{ }), dafny.DafnyMap.fromElements((dafny.Tuple2<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnySequence<? extends dafny.CodePoint>>[])new dafny.Tuple2[]{ }));
  }
  public static dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>> Apply(dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>> m, Action a)
  {
    Action _source0 = a;
    dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> _0___mcc_h0 = ((F3__1Domain.Action)_source0)._details;
    dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> _1___mcc_h1 = ((F3__1Domain.Action)_source0)._requirements;
    dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> _2_newRequirements = _1___mcc_h1;
    dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> _3_newDetails = _0___mcc_h0;
    dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>> _let_tmp_rhs0 = m;
    dafny.DafnySequence<? extends dafny.CodePoint> _4_event = ((dafny.DafnySequence<? extends dafny.CodePoint>)(java.lang.Object)(((dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>)_let_tmp_rhs0).dtor__0()));
    dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> _5_details = ((dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>)(java.lang.Object)(((dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>)_let_tmp_rhs0).dtor__1()));
    dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>> _6_requirements = ((dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>)(java.lang.Object)(((dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>)_let_tmp_rhs0).dtor__2()));
    return dafny.Tuple3.<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>>create(_4_event, _3_newDetails, _2_newRequirements);
  }
  public static dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>> Normalize(dafny.Tuple3<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>, dafny.DafnyMap<? extends dafny.DafnySequence<? extends dafny.CodePoint>, ? extends dafny.DafnySequence<? extends dafny.CodePoint>>> m) {
    return m;
  }
  @Override
  public java.lang.String toString() {
    return "F3_1Domain._default";
  }
}
