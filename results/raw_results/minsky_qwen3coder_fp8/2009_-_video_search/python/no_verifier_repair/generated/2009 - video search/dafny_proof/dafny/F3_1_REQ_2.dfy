include "Replay.dfy"

module F3_1_REQ_2Domain refines Domain {
  type Model = map<string, (string, int)>
  
  datatype Action = UpdateDB
  
  ghost predicate Inv(m: Model) {
    forall k | k in m :: 
      m[k].1 >= 0 && m[k].1 <= 1000
  }
  
  function Init(): Model {
    map[]
  }
  
  function Apply(m: Model, a: Action): Model {
    match a
    case UpdateDB => 
      // Simulate updating database with new torrent site info
      // In a real system, this would fetch from internet
      m
  }
  
  function Normalize(m: Model): Model {
    // Ensure all weights are within bounds
    map k | k in m :: 
      (m[k].0, if m[k].1 < 0 then 0 else if m[k].1 > 1000 then 1000 else m[k].1)
  }
  
  lemma InitSatisfiesInv()
    ensures Inv(Init())
  {
  }
  
  lemma StepPreservesInv(m: Model, a: Action)
    ensures Inv(Normalize(Apply(m, a)))
  {
  }
  
  lemma UpdateDBPreservesState(m: Model)
    ensures Inv(Normalize(Apply(m, UpdateDB)))
  {
  }
}

module F3_1_REQ_2Kernel refines Kernel {
  import D = F3_1_REQ_2Domain
}