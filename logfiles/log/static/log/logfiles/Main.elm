module Main exposing (main)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Models
import Navigation



main =
    Navigation.program UrlChange
    { init = init
    , view = view
    , update = update
    , subscriptions = (\_ -> Sub.none)
    }



-- MODEL


type alias Model =
    { history : List Navigation.Location
    }


init : Navigation.Location -> ( Model, Cmd Msg )
init location =
    ( Model [ location ]
    , Cmd.none
    )



-- UPDATE


type Msg =
    UrlChange Navigation.Location
    | LogsLoaded


type Page =
    ListLogs
    -- | ViewLog
    -- | LogMeta
    -- | TagMeta



update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    (model, Cmd.none)





-- VIEW


view : Model -> Html msg
view model =
    div []
    [ h1 [] [ text "Logfiles" ]
    , a [ href ("#logs") ] [ text "All Logs"]
    ]


viewLink : String -> Html msg
viewLink name =
    li [] [ a [ href ("#" ++ name) ] [ text name ] ]


viewLocation : Navigation.Location -> Html msg
viewLocation location =
    li [] [ text (location.pathname ++ location.hash) ]
