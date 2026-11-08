include "Replay.dfy"

module F3_2Domain refines Domain {
  type Model = (bool, map<string, string>, map<string, set<string>>)

  datatype Action = Login(username: string) | Register(eventId: string) | Approve(eventId: string)

  ghost predicate Inv(m: Model) {
    var (loggedIn, users, events) := m;
    loggedIn ==> users != map[]
  }

  function Init(): Model {
    (false, map[], map[])
  }

  function Apply(m: Model, a: Action): Model {
    var (loggedIn, users, events) := m;
    match a
    case Login(username) =>
      (true, users + [username := "student"], events)
    case Register(eventId) =>
      if loggedIn then
        (loggedIn, users, events + [eventId := users.Keys()])
      else
        m
    case Approve(eventId) =>
      if loggedIn && eventId in events then
        (loggedIn, users, events - {eventId})
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

  lemma LoginEnsuresLoggedIn(m: Model, username: string)
    ensures (Apply(m, Login(username)).0)
  {
  }

  lemma RegisterEnsuresEventAdded(m: Model, eventId: string)
    ensures (if Apply(m, Register(eventId)).0 then eventId in Apply(m, Register(eventId)).2 else true)
  {
  }

  lemma ApproveEnsuresEventRemoved(m: Model, eventId: string)
    ensures (if Apply(m, Approve(eventId)).0 then eventId !in Apply(m, Approve(eventId)).2 else true)
  {
  }
}

module F3_2Kernel refines Kernel {
  import D = F3_2Domain
}