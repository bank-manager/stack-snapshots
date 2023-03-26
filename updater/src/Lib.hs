module Lib
    ( someFunc
    , loadSnapshot
    ) where

import           Data.Yaml                      ( decodeFileEither
                                                , parseEither
                                                , parseJSON
                                                )
import           Pantry                         ( RawSnapshotLayer(..) )
import           Pantry.Internal.AesonExtended  ( WithJSONWarnings(..) )
import           Pantry.Types                   ( Unresolved )
someFunc :: IO ()
someFunc = putStrLn "someFunc"



-- warningsParserHelper
--     :: SnapshotLocation -> Value -> Maybe (Path Abs Dir) -> IO RawSnapshotLayer
-- warningsParserHelper sl val mdir = case parseEither parseJSON val of
--     Left e -> throwIO $ "Couldn't ParseSnapshot" (toRawSL sl) e
--     Right (WithJSONWarnings x ws) -> do
--         unless (null ws) $ do
--             logWarn
--                 $  Utf8Builder "Warnings when parsing snapshot "
--                 <> display sl
--         for_ ws $ logWarn

loadSnapshot :: FilePath -> IO RawSnapshotLayer
loadSnapshot fp = do
    eValue <- decodeFileEither fp
    case eValue of
        Left  e     -> error "error"
        Right value -> case parseEither parseJSON value of
            Left  e -> error e
            Right (WithJSONWarnings (Unresolved x) _) -> return x
