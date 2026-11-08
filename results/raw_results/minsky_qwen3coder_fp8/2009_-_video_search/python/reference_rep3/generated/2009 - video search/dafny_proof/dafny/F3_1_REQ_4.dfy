include "Replay.dfy"

module F3_1_REQ_4Domain refines Domain {
  type Model = map<string, TorrentInfo>

  datatype Action = Search(query: string)

  datatype TorrentInfo = TorrentInfo(
    seeders: int,
    leechers: int,
    fileSize: int,
    postDate: string,
    url: string
  )

  ghost predicate Inv(m: Model) {
    forall k | k in m :: 
      m[k].seeders >= 0 && 
      m[k].leechers >= 0 && 
      m[k].fileSize >= 0 &&
      m[k].url != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Search(q) => 
      if q in m then m else m[q := TorrentInfo(0, 0, 0, "", "")]
  }

  function Normalize(m: Model): Model {
    map k | k in m :: 
      TorrentInfo(
        if m[k].seeders < 0 then 0 else m[k].seeders,
        if m[k].leechers < 0 then 0 else m[k].leechers,
        if m[k].fileSize < 0 then 0 else m[k].fileSize,
        m[k].postDate,
        m[k].url
      )
  }

  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }

  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
    assert forall k | k in Apply(m, a) :: 
      (Apply(m, a))[k].seeders >= 0 && 
      (Apply(m, a))[k].leechers >= 0 && 
      (Apply(m, a))[k].fileSize >= 0 &&
      (Apply(m, a))[k].url != "";
  }

  lemma SearchResponseAccurate(q: string, m: Model)
    ensures 
      (q in Apply(m, Search(q))) ==> 
        (m[q].seeders >= 0 && m[q].leechers >= 0 && m[q].fileSize >= 0 && m[q].url != "")
  {
    assert true;
  }
}

module F3_1_REQ_4Kernel refines Kernel {
  import D = F3_1_REQ_4Domain
}