module Models.Tag
    exposing
        ( Tag
        , decodeTag
        )


type alias Tag =
    { id : Int
    , tag : String
    , tag_type : String
    }

decodeTag = "Not implemented"
