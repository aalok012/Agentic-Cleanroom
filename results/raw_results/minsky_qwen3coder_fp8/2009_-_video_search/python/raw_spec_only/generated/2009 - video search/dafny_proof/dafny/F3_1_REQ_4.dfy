include "Replay.dfy"

module F3_1_REQ_4Domain refines Domain {
  type Model = map<string, FileInfo>

  datatype FileInfo = FileInfo(size: nat, seeds: nat, peers: nat, datePosted: string, link: string)

  datatype Action = Search(query: string)

  ghost predicate Inv(m: Model) {
    forall k | k in m :: m[k].size > 0
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Search(q) =>
      if q == "" then m else m - {q}
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

  lemma SearchReturnsFileInfo(q: string, m: Model)
    requires q != ""
    ensures |Apply(m, Search(q))| == |m| + 1
    ensures forall k | k in Apply(m, Search(q)) && k != q :: k in m
    ensures Apply(m, Search(q))[q].size > 0
  {
  }
}

module F3_1_REQ_4Kernel refines Kernel {
  import D = F3_1_REQ_4Domain
}