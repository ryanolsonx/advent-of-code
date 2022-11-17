module Day05Tests exposing (..)

import Day05 exposing (..)
import Debug exposing (..)
import Expect exposing (Expectation)
import Fuzz exposing (Fuzzer, int, intRange, list, string)
import Parser exposing (DeadEnd, Problem(..), run)
import Test exposing (..)


suite =
    [ toInstructionsTests
    , getRowRangeTests
    , getColumnRangeTests
    , getRowTests
    , getRowAndColumnTests
    , getSeatIdTests
    , part1Tests
    ]


toInstructionsTests =
    describe "toInstructions"
        [ test "BFFFBBFRRR" <|
            \_ ->
                toInstructions "BFFFBBFRRR"
                    |> Expect.equal
                        { rowInsructions = [ Back, Front, Front, Front, Back, Back, Front ]
                        , columnInstructions = [ Right, Right, Right ]
                        }
        , test "BBFFBBFRLL" <|
            \_ ->
                toInstructions "BBFFBBFRLL"
                    |> Expect.equal
                        { rowInsructions = [ Back, Back, Front, Front, Back, Back, Front ]
                        , columnInstructions = [ Right, Left, Left ]
                        }
        ]


getRowRangeTests =
    describe "getRowRange"
        [ test "0 127 Front" <|
            \_ ->
                getRowRange ( 0, 127 ) Front
                    |> Expect.equal ( 0, 63 )
        , test "0 63 Back" <|
            \_ ->
                getRowRange ( 0, 63 ) Back
                    |> Expect.equal ( 32, 63 )
        , test "32, 63 Front" <|
            \_ ->
                getRowRange ( 32, 63 ) Front
                    |> Expect.equal ( 32, 47 )
        , test "32, 47 Back" <|
            \_ ->
                getRowRange ( 32, 47 ) Back
                    |> Expect.equal ( 40, 47 )
        , test "40, 47 Back" <|
            \_ ->
                getRowRange ( 40, 47 ) Back
                    |> Expect.equal ( 44, 47 )
        , test "44, 47 Front" <|
            \_ ->
                getRowRange ( 44, 47 ) Front
                    |> Expect.equal ( 44, 45 )
        , test "44, 45 Front" <|
            \_ ->
                getRowRange ( 44, 45 ) Front
                    |> Expect.equal ( 44, 44 )
        , test "44, 45 Back -- alt" <|
            \_ ->
                getRowRange ( 44, 45 ) Back
                    |> Expect.equal ( 45, 45 )
        ]


getColumnRangeTests =
    describe "getColumnRange"
        [ test "0 7 Right" <|
            \_ ->
                getColumnRange ( 0, 7 ) Right
                    |> Expect.equal ( 4, 7 )
        , test "4 7 Left" <|
            \_ ->
                getColumnRange ( 4, 7 ) Left
                    |> Expect.equal ( 4, 5 )
        , test "4 5 Right" <|
            \_ ->
                getColumnRange ( 4, 5 ) Right
                    |> Expect.equal ( 5, 5 )
        ]


getRowTests =
    describe "getRow"
        [ test "FBFBBFFRLR" <|
            \_ ->
                toInstructions "FBFBBFFRLR"
                    |> getRow
                    |> Expect.equal 44
        , test "BFFFBBFRRR" <|
            \_ ->
                toInstructions "BFFFBBFRRR"
                    |> getRow
                    |> Expect.equal 70
        , test "FFFBBBFRRR" <|
            \_ ->
                toInstructions "FFFBBBFRRR"
                    |> getRow
                    |> Expect.equal 14
        , test "BBFFBBFRLL" <|
            \_ ->
                toInstructions "BBFFBBFRLL"
                    |> getRow
                    |> Expect.equal 102
        ]


getColumnTests =
    describe "getColumn"
        [ test "FBFBBFFRLR" <|
            \_ ->
                toInstructions "FBFBBFFRLR"
                    |> getColumn
                    |> Expect.equal 5
        , test "BFFFBBFRRR" <|
            \_ ->
                toInstructions "BFFFBBFRRR"
                    |> getColumn
                    |> Expect.equal 7
        , test "FFFBBBFRRR" <|
            \_ ->
                toInstructions "FFFBBBFRRR"
                    |> getColumn
                    |> Expect.equal 7
        , test "BBFFBBFRLL" <|
            \_ ->
                toInstructions "BBFFBBFRLL"
                    |> getColumn
                    |> Expect.equal 4
        ]


getRowAndColumnTests =
    describe "getRowAndColumn"
        [ test "BFFFBBFRRR" <|
            \_ ->
                toInstructions "BFFFBBFRRR"
                    |> getRowAndColumn
                    |> Expect.equal { row = 70, column = 7 }
        ]


getSeatIdTests =
    describe "getSeatId"
        [ test "BFFFBBFRRR" <|
            \_ ->
                toInstructions "BFFFBBFRRR"
                    |> getRowAndColumn
                    |> getSeatId
                    |> Expect.equal 567
        ]


getSeatIdsTests =
    describe "getSeatIds"
        [ test "multiple" <|
            \_ ->
                [ "BFFFBBFRRR", "FFFBBBFRRR", "BBFFBBFRLL" ]
                    |> getSeatIds
                    |> Expect.equal [ 567, 119, 820 ]
        ]


part1Tests =
    describe "part1"
        [ test "part1 with result" <|
            \_ ->
                [ "BFFFBBFRRR", "FFFBBBFRRR", "BBFFBBFRLL" ]
                    |> part1
                    |> Expect.equal (Just 820)
        , test "part1 no result" <|
            \_ ->
                []
                    |> part1
                    |> Expect.equal Nothing
        ]
