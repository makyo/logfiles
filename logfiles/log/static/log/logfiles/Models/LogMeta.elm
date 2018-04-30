module Models.LogMeta
    exposing
        ( LogMeta
        , decodeLogList
        , decodeLogMeta
        , decodeLog
        )


type alias LogMeta =
    { id : Int
    , name : String
    , date : String
    , medium : String
    , complete : Bool
    , privacy : String
    , location : Tag
    }

decodeLogList = "Not implemented"

decodeLogMeta = "Not implemented"
