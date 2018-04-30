module Models.Log
    exposing
        ( Log
        , decodeLog
        )

import Models.Line exposing (Line, decodeLine)
import Models.LogMeta exposing (LogMeta, decodeLogMeta)


type alias Log =
    { meta : LogMeta
    , lines : List Line
    }

decodeLog = "Not implemented"
