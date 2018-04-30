module Models
    exposing
        ( TagRelation
        )

import Models.Tag exposing (Tag)
import Models.LogMeta exposing (LogMeta)
import Models.Participant exposing (Participant)
import Models.Line exposing (Line)


type alias TagRelation =
    { tag : Tag
    , log : Maybe LogMeta
    , particpant : Maybe Participant
    , topic : Maybe Line
    , moment : Maybe Line
    }
