include "Replay.dfy"

module F3_1_REQ_6Domain refines Domain {
  type Model = (map<string, string>, list<string>)

  datatype Action = SortBySize | SortByDate | SortByAlpha

  ghost predicate Inv(m: Model) {
    var (torrents, order) := m;
    |order| == |torrents| &&
    forall i | 0 <= i < |order| :: order[i] in torrents
  }

  function Init(): Model {
    (map[], [])
  }

  function Apply(m: Model, a: Action): Model {
    var (torrents, order) := m;
    match a
    case SortBySize =>
      var sorted := SortBySizeHelper(torrents);
      (torrents, sorted)
    case SortByDate =>
      var sorted := SortByDateHelper(torrents);
      (torrents, sorted)
    case SortByAlpha =>
      var sorted := SortByAlphaHelper(torrents);
      (torrents, sorted)
  }

  function Normalize(m: Model): Model {
    m
  }

  function SortBySizeHelper(torrents: map<string, string>): list<string> {
    var keys := set k | k in torrents :: k;
    var sortedKeys := SortStringList(keys);
    sortedKeys
  }

  function SortByDateHelper(torrents: map<string, string>): list<string> {
    var keys := set k | k in torrents :: k;
    var sortedKeys := SortStringList(keys);
    sortedKeys
  }

  function SortByAlphaHelper(torrents: map<string, string>): list<string> {
    var keys := set k | k in torrents :: k;
    var sortedKeys := SortStringList(keys);
    sortedKeys
  }

  function SortStringList(s: set<string>): list<string> {
    if s == {} then [] else
      var min := MinString(s);
      [min] + SortStringList(s - {min})
  }

  function MinString(s: set<string>): string {
    s.Choose()
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }

  lemma SortResultsReflectsCriteria(m: Model, a: Action)
    ensures match a
      case SortBySize => 
        var (torrents, order) := Apply(m, a);
        forall i, j | 0 <= i < j < |order| :: 
          GetSize(torrents, order[i]) <= GetSize(torrents, order[j])
      case SortByDate => 
        var (torrents, order) := Apply(m, a);
        forall i, j | 0 <= i < j < |order| :: 
          GetDate(torrents, order[i]) <= GetDate(torrents, order[j])
      case SortByAlpha => 
        var (torrents, order) := Apply(m, a);
        forall i, j | 0 <= i < j < |order| :: 
          order[i] <= order[j]
    {
  }

  function GetSize(torrents: map<string, string>, name: string): int {
    var sizeStr := torrents[name];
    var size := int.TryParse(sizeStr);
    size
  }

  function GetDate(torrents: map<string, string>, name: string): int {
    var dateStr := torrents[name];
    var date := int.TryParse(dateStr);
    date
  }
}

module F3_1_REQ_6Kernel refines Kernel {
  import D = F3_1_REQ_6Domain
}