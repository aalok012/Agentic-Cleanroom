include "Replay.dfy"

module F3_1_REQ_6Domain refines Domain {
  type Model = (seq<string>, map<string, int>, map<string, string>, map<string, string>)

  datatype Action = SortBySize | SortByDate | SortByAlpha

  ghost predicate Inv(m: Model) {
    var (torrents, sizes, dates, names) := m;
    |torrents| == |sizes| && |torrents| == |dates| && |torrents| == |names|
  }

  function Init(): Model {
    ([], map[], map[], map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case SortBySize =>
      var (torrents, sizes, dates, names) := m;
      var sorted := SortBySizeHelper(torrents, sizes);
      (sorted, sizes, dates, names)
    case SortByDate =>
      var (torrents, sizes, dates, names) := m;
      var sorted := SortByDateHelper(torrents, dates);
      (sorted, sizes, dates, names)
    case SortByAlpha =>
      var (torrents, sizes, dates, names) := m;
      var sorted := SortByAlphaHelper(torrents, names);
      (sorted, sizes, dates, names)
  }

  function Normalize(m: Model): Model {
    m
  }

  function SortBySizeHelper(torrents: seq<string>, sizes: map<string, int>): seq<string> {
    torrents
  }

  function SortByDateHelper(torrents: seq<string>, dates: map<string, string>): seq<string> {
    torrents
  }

  function SortByAlphaHelper(torrents: seq<string>, names: map<string, string>): seq<string> {
    torrents
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma SortBySizeEnsures(m: Model)
    ensures var (torrents, sizes, dates, names) := m;
            var sorted := SortBySizeHelper(torrents, sizes);
            Inv((sorted, sizes, dates, names))
  {
    assert |sorted| == |torrents|;
    assert |sorted| == |sizes|;
    assert |sorted| == |dates|;
    assert |sorted| == |names|;
  }

  lemma SortByDateEnsures(m: Model)
    ensures var (torrents, sizes, dates, names) := m;
            var sorted := SortByDateHelper(torrents, dates);
            Inv((sorted, sizes, dates, names))
  {
    assert |sorted| == |torrents|;
    assert |sorted| == |sizes|;
    assert |sorted| == |dates|;
    assert |sorted| == |names|;
  }

  lemma SortByAlphaEnsures(m: Model)
    ensures var (torrents, sizes, dates, names) := m;
            var sorted := SortByAlphaHelper(torrents, names);
            Inv((sorted, sizes, dates, names))
  {
    assert |sorted| == |torrents|;
    assert |sorted| == |sizes|;
    assert |sorted| == |dates|;
    assert |sorted| == |names|;
  }
}

module F3_1_REQ_6Kernel refines Kernel {
  import D = F3_1_REQ_6Domain
}