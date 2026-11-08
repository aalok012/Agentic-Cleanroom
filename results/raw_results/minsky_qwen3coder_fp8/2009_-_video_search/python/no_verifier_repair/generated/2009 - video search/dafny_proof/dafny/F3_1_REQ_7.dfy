include "Replay.dfy"

module F3_1_REQ_7Domain refines Domain {
  type Model = (string, int, map<int, seq<string>>)

  datatype Action = PageClick(page: int)

  ghost predicate Inv(m: Model) {
    var (query, currentPage, results) := m;
    currentPage >= 1 &&
    currentPage <= |results| &&
    forall p | p in results && p >= 1 && p <= |results| :: results[p] != []
  }

  function Init(): Model {
    ("", 1, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case PageClick(page) =>
      var (query, currentPage, results) := m;
      if page in results && page >= 1 && page <= |results| then
        (query, page, results)
      else
        m
  }

  function Normalize(m: Model): Model {
    var (query, currentPage, results) := m;
    if currentPage < 1 then
      (query, 1, results)
    else if currentPage > |results| && |results| > 0 then
      (query, |results|, results)
    else
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

  lemma PageClickPreservesConsistency(m: Model, page: int)
    ensures
      match Apply(m, PageClick(page))
      case (query, newPage, results) =>
        newPage == page && 
        (page in results ==> results[page] != []) &&
        query == m.0
    case _ => true
  {
  }
}

module F3_1_REQ_7Kernel refines Kernel {
  import D = F3_1_REQ_7Domain
}