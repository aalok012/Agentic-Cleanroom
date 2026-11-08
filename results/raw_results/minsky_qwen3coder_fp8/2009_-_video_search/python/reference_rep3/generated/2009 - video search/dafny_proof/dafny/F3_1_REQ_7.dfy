include "Replay.dfy"

module F3_1_REQ_7Domain refines Domain {
  type Model = (string, int, map<int, string>)

  datatype Action = PageClick(page: int)

  ghost predicate Inv(m: Model) {
    var (query, totalResults, results) := m;
    totalResults >= 0 &&
    forall i | i in results && 0 <= i < totalResults :: results[i] != ""
  }

  function Init(): Model {
    ("", 0, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case PageClick(page) =>
      var (query, totalResults, results) := m;
      if page >= 0 && page * 10 < totalResults then
        (query, totalResults, map i | i in results && page * 10 <= i < (page + 1) * 10 :: results[i])
      else
        (query, totalResults, map[])
  }

  function Normalize(m: Model): Model {
    m
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma PageClickPostcondition(m: Model, page: int)
    ensures match Apply(m, PageClick(page))
      case (_, _, results) => 
        forall i | i in results :: results[i] != ""
    ensures match Apply(m, PageClick(page))
      case (query, totalResults, results) =>
        totalResults >= 0 && 
        (page >= 0 && page * 10 < totalResults ==> |results| <= 10)
  {
  }
}

module F3_1_REQ_7Kernel refines Kernel {
  import D = F3_1_REQ_7Domain
}