module Models
    exposing
        ( LogMeta
        , Log
        , Line
        , Tag
        , Participant
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

type alias Log =
    { meta : LogMeta
    , lines : List Line
    }

type alias Line =
    { id : Int
    , log : LogMeta
    , line : String
    , num : Int
    , participant : Participant
    , moments : List Tag
    , topics : List Tag
    }

type alias Tag =
    { id : Int
    , tag : String
    , tag_type : String
    }

type alias TagRelation =
    { tag : Tag
    , log : Maybe LogMeta
    , particpant : Maybe Participant
    , topic : Maybe Line
    , moment : Maybe Line
    }

type Participant =
    Participant
    { id : Int
    , name : String
    , gender : String
    , notes : String
    , alts : List Participant
    }
