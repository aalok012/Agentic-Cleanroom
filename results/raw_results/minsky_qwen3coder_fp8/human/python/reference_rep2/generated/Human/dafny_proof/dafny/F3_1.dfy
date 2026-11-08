include "Replay.dfy"

module F3_1Domain refines Domain {
  type Model = (string, map<string, string>, map<string, string>)

  datatype Action = EditEventDetails(details: map<string, string>, requirements: map<string, string>)

  ghost predicate Inv(m: Model) {
    var (event, details, requirements) := m;
    true
  }

  function Init(): Model {
    ("", map[], map[])
  }

  function Apply(m: Model, a: Action): Model {
    match a
    case EditEventDetails(newDetails, newRequirements) =>
      var (event, details, requirements) := m;
      (event, newDetails, newRequirements)
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

  lemma EditEventDetailsUpdates(m: Model, newDetails: map<string, string>, newRequirements: map<string, string>)
    ensures Apply(m, EditEventDetails(newDetails, newRequirements)) == (m.0, newDetails, newRequirements)
  {
  }
}

module F3_1Kernel refines Kernel {
  import D = F3_1Domain
}