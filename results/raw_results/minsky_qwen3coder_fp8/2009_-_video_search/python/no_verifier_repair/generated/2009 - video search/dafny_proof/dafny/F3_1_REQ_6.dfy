include "Replay.dfy"

module F3_1_REQ_6Domain refines Domain {
  type Model = map<string, Torrent>

  datatype Action = SortBySize | SortByDate | SortByAlpha

  ghost predicate Inv(m: Model) {
    true
  }

  function Init(): Model {
    map[]
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case SortBySize => m
    case SortByDate => m
    case SortByAlpha => m
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

  datatype Torrent = Torrent(name: string, size: int, date: int)

  function SortTorrentsByName(torrents: seq<Torrent>): seq<Torrent> {
    torrents
  }

  function SortTorrentsBySize(torrents: seq<Torrent>): seq<Torrent> {
    torrents
  }

  function SortTorrentsByDate(torrents: seq<Torrent>): seq<Torrent> {
    torrents
  }

  lemma SortByNamePreservesOrdering(t: seq<Torrent>)
    ensures |SortTorrentsByName(t)| == |t|
    ensures forall i, j | 0 <= i < j < |t| :: SortTorrentsByName(t)[i].name <= SortTorrentsByName(t)[j].name
  {
  }

  lemma SortBySizePreservesOrdering(t: seq<Torrent>)
    ensures |SortTorrentsBySize(t)| == |t|
    ensures forall i, j | 0 <= i < j < |t| :: SortTorrentsBySize(t)[i].size <= SortTorrentsBySize(t)[j].size
  {
  }

  lemma SortByDatePreservesOrdering(t: seq<Torrent>)
    ensures |SortTorrentsByDate(t)| == |t|
    ensures forall i, j | 0 <= i < j < |t| :: SortTorrentsByDate(t)[i].date <= SortTorrentsByDate(t)[j].date
  {
  }
}

module F3_1_REQ_6Kernel refines Kernel {
  import D = F3_1_REQ_6Domain
}