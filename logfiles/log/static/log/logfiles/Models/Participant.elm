module Models.Participant
    exposing
        ( Participant
        , decodeParticipant
        )


type Participant =
    Participant
    { id : Int
    , name : String
    , gender : String
    , notes : String
    , alts : List Participant
    }

decodeParticipant = "Not implemented"
