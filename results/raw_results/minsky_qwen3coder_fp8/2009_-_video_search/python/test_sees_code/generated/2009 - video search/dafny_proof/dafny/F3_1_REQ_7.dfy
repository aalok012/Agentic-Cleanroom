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
    if query == "" then 1 else |results|
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma PageClickPreservesQuery(m: Model, page: int)
    ensures var (query, _, _) := Normalize(Apply(m, PageClick(page))); query == m.0
  {
  }
}

module F3_1_REQ_7Kernel refines Kernel {
  import D = F3_1_REQ_7Domain
}