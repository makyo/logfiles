module Models
    exposing
        ( Line
        , decodeLine
        )

import Models.LogMeta exposing (LogMeta, decodeLogMeta)
import Models.Participant exposing (Participant, decodeParticipant)
import Models.Tag exposing (Tag, decodeTag)


type alias Line =
    { id : Int
    , log : LogMeta
    , line : String
    , num : Int
    , participant : Participant
    , moments : List Tag
    , topics : List Tag
    }

decodeLine = "Not implemented"
