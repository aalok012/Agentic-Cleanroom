include "Replay.dfy"

module F3_1_REQ_4Domain refines Domain {
  type Model = map<string, TorrentResult>

  datatype Action = Search(query: string)

  datatype TorrentResult = TorrentResult(
    seeds: int,
    peers: int,
    fileSize: int,
    datePosted: string,
    url: string
  )

  ghost predicate Inv(m: Model) {
    forall k | k in m :: 
      0 <= m[k].seeds && 
      0 <= m[k].peers && 
      0 <= m[k].fileSize &&
      m[k].datePosted != "" &&
      m[k].url != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Search(query) => 
      if query == "" then m
      else 
        // Simulate search results by creating dummy entries
        // In a real system, this would query a torrent database
        m + [query := TorrentResult(5, 3, 1024, "2023-01-01", "http://example.com")]
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

  lemma SearchResultContainsMetadata(query: string)
    requires query != ""
    ensures forall k :: k in Apply(Init(), Search(query)) && 
      Apply(Init(), Search(query))[k].seeds >= 0 &&
      Apply(Init(), Search(query))[k].peers >= 0 &&
      Apply(Init(), Search(query))[k].fileSize >= 0 &&
      Apply(Init(), Search(query))[k].datePosted != "" &&
      Apply(Init(), Search(query))[k].url != ""
  {
  }
}

module F3_1_REQ_4Kernel refines Kernel {
  import D = F3_1_REQ_4Domain
}