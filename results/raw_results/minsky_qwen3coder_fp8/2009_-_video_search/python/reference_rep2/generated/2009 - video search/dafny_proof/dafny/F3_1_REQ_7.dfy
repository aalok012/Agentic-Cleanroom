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
        (query, totalResults, map i | i in results && 0 <= i < 10 :: results[i])
      else
        m
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
    ensures 
      if page >= 0 && page * 10 < m.1 then
        let newModel := Apply(m, PageClick(page)) in
        let (query, totalResults, results) := newModel in
        |results| == 10 && forall i | 0 <= i < 10 :: results[i] != ""
      else
        true
  {
  }
}

module F3_1_REQ_7Kernel refines Kernel {
  import D = F3_1_REQ_7Domain
}