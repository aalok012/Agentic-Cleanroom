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
      m[k].seeds >= 0 && 
      m[k].peers >= 0 && 
      m[k].fileSize >= 0 &&
      m[k].datePosted != "" &&
      m[k].url != ""
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case Search(query) => 
      // Simulate search results by creating mock data
      // In a real system, this would query a torrent database
      if query == "test" then
        m["test_torrent"] := TorrentResult(10, 5, 1024, "2023-01-01", "http://example.com/test")
      else if query == "movie" then
        m["movie_torrent"] := TorrentResult(100, 25, 1024000, "2023-01-02", "http://example.com/movie")
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

  lemma SearchEnsuresCorrectMetadata(m: Model, query: string)
    ensures (forall k | k in Apply(m, Search(query)) :: 
      Apply(m, Search(query))[k].seeds >= 0 &&
      Apply(m, Search(query))[k].peers >= 0 &&
      Apply(m, Search(query))[k].fileSize >= 0 &&
      Apply(m, Search(query))[k].datePosted != "" &&
      Apply(m, Search(query))[k].url != "")
  {
  }
}

module F3_1_REQ_4Kernel refines Kernel {
  import D = F3_1_REQ_4Domain
}