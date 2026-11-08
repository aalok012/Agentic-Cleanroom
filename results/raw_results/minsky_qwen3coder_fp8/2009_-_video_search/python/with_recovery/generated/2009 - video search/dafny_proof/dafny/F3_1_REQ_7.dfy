include "Replay.dfy"

module F3_1_REQ_7Domain refines Domain {
  type Model = (string, int, map<int, seq<string>>)

  datatype Action = PageClick(page: int)

  ghost predicate Inv(m: Model) {
    var (query, currentPage, results) := m;
    currentPage >= 1 && currentPage <= TotalPages(query, results)
  }

  function Init(): Model {
    ("", 1, map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case PageClick(page) =>
      var (query, currentPage, results) := m;
      if page > 0 && page <= TotalPages(query, results) then
        (query, page, results)
      else
        m
  }

  function Normalize(m: Model): Model {
    var (query, currentPage, results) := m;
    var totalPages := TotalPages(query, results);
    if currentPage < 1 then
      (query, 1, results)
    else if currentPage > totalPages then
      (query, totalPages, results)
    else
      m
  }

  function TotalPages(query: string, results: map<int, seq<string>>): int {
    if query == "" then 1 else if results == map[] then 1 else |results|
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
    assert Inv(("", 1, map[]));
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    var (query, currentPage, results) := m;
    match a
    case PageClick(page) =>
      var newPage := if page > 0 && page <= TotalPages(query, results) then page else currentPage;
      var normalizedPage := if newPage < 1 then 1 else if newPage > TotalPages(query, results) then TotalPages(query, results) else newPage;
      assert Inv((query, normalizedPage, results));
  }

  lemma PageClickDisplaysCorrectResults(m: Model, a: Action)
    requires Inv(m)
    ensures (match a 
             case PageClick(page) => 
               currentPage == page && page > 0 && page <= TotalPages(query, results)
             case _ => true)
    where var (query, currentPage, results) := m
  {
  }
}

module F3_1_REQ_7Kernel refines Kernel {
  import D = F3_1_REQ_7Domain
}