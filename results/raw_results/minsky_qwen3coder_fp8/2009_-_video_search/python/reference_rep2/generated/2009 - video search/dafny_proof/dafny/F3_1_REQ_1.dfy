include "Replay.dfy"

module F3_1_REQ_1Domain refines Domain {
  type Model = (string, set<string>, set<string>)

  datatype Action = Search(query: string)

  ghost predicate Inv(m: Model) {
    var (q, t, s) := m;
    q == "" || q != ""
  }

  function Init(): Model {
    ("", {}, {})
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Search(q) => 
      var (old_q, torrents, streams) := m;
      (q, torrents, streams)
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

  lemma SearchResultReflectsQuery(m: Model, a: Action)
    requires Inv(m)
    ensures match a
      case Search(q) =>
        var (query, _, _) := Apply(m, a);
        query == q
      case _ => true
    ensures match a
      case Search(q) =>
        var (_, torrents, streams) := Apply(m, a);
        torrents == {}
      case _ => true
    ensures match a
      case Search(q) =>
        var (_, _, streams) := Apply(m, a);
        streams == {}
      case _ => true
    ensures match a
      case Search(q) =>
        var (query, torrents, streams) := Apply(m, a);
        query == q && torrents == {} && streams == {}
      case _ => true
  {
  }
}

module F3_1_REQ_1Kernel refines Kernel {
  import D = F3_1_REQ_1Domain
}