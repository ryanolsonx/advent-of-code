module Day05 exposing (..)

{-| Day 5: Binary Boarding

You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport control.

You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input); perhaps you can find your seat through process of elimination.

Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".

The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.

For example, consider just the first seven characters of FBFBBFFRLR:

    Start by considering the whole range, rows 0 through 127.
    F means to take the lower half, keeping rows 0 through 63.
    B means to take the upper half, keeping rows 32 through 63.
    F means to take the lower half, keeping rows 32 through 47.
    B means to take the upper half, keeping rows 40 through 47.
    B keeps rows 44 through 47.
    F keeps rows 44 through 45.
    The final F keeps the lower of the two, row 44.

The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.

For example, consider just the last 3 characters of FBFBBFFRLR:

    Start by considering the whole range, columns 0 through 7.
    R means to take the upper half, keeping columns 4 through 7.
    L means to take the lower half, keeping columns 4 through 5.
    The final R keeps the upper of the two, column 5.

So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 \* 8 + 5 = 357.

Here are some other boarding passes:

    BFFFBBFRRR: row 70, column 7, seat ID 567.
    FFFBBBFRRR: row 14, column 7, seat ID 119.
    BBFFBBFRLL: row 102, column 4, seat ID 820.

As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?

Your puzzle answer was 848.

--- Part Two ---

Ding! The "fasten seat belt" signs have turned on. Time to find your seat.

It's a completely full flight, so your seat should be the only missing boarding pass in your list. However, there's a catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing from your list as well.

Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.

What is the ID of your seat?

Your puzzle answer was 682.

-}

import Aoc


main =
    let
        input =
            getInput

        results =
            { day = 5
            , examplePart1 = Nothing
            , part1 = part1 input
            , examplePart2 = Nothing
            , part2 = Nothing
            }
    in
    Aoc.showResults results



-- MODEL


type alias RowAndColumnResult =
    { row : Int
    , column : Int
    }


type alias InstructionSet =
    { rowInsructions : List RowInstruction
    , columnInstructions : List ColumnInstruction
    }


type RowInstruction
    = Back
    | Front


type ColumnInstruction
    = Left
    | Right


type alias Range =
    ( Int, Int )



-- CODE


{-| Get the highest seat id
-}
part1 : List String -> Maybe Int
part1 input =
    getSeatIds input
        |> List.maximum


getSeatIds : List String -> List Int
getSeatIds input =
    input
        |> List.map toInstructions
        |> List.map getRowAndColumn
        |> List.map getSeatId


getSeatId : RowAndColumnResult -> Int
getSeatId { row, column } =
    (row * 8) + column


getRowAndColumn : InstructionSet -> RowAndColumnResult
getRowAndColumn instructionSet =
    { row = getRow instructionSet
    , column = getColumn instructionSet
    }


getRow : InstructionSet -> Int
getRow { rowInsructions } =
    getPosition ( 0, 127 ) getRowRange rowInsructions


getColumn : InstructionSet -> Int
getColumn { columnInstructions } =
    getPosition ( 0, 7 ) getColumnRange columnInstructions


{-| getPosition instructionSet.rowInstructions (1, 127) getRowRange
-}
getPosition : Range -> (Range -> a -> Range) -> List a -> Int
getPosition ( start, end ) getRangeFn instructions =
    if List.isEmpty instructions then
        start

    else
        let
            maybeInstruction =
                List.head instructions

            nextInstructions =
                Maybe.withDefault [] <| List.tail instructions
        in
        case maybeInstruction of
            Just instruction ->
                let
                    nextRange =
                        getRangeFn ( start, end ) instruction
                in
                getPosition nextRange getRangeFn nextInstructions

            Nothing ->
                start


getRowRange : Range -> RowInstruction -> Range
getRowRange range ins =
    (case ins of
        Back ->
            True

        Front ->
            False
    )
        |> getRange range


getColumnRange : Range -> ColumnInstruction -> Range
getColumnRange range ins =
    (case ins of
        Right ->
            True

        Left ->
            False
    )
        |> getRange range


getRange : Range -> Bool -> Range
getRange ( start, end ) takeFront =
    if takeFront then
        ( ((start + end) // 2) + 1, end )

    else
        ( start, ((end - start) // 2) + start )



-- TO MODEL


toInstructions : String -> InstructionSet
toInstructions input =
    { rowInsructions = toRowInstructions input
    , columnInstructions = toColumnInstructions input
    }


toRowInstructions : String -> List RowInstruction
toRowInstructions input =
    input |> String.toList |> List.filter isRowInstruction |> List.map toRowInstruction


isRowInstruction : Char -> Bool
isRowInstruction c =
    c == 'B' || c == 'F'


toRowInstruction : Char -> RowInstruction
toRowInstruction c =
    if c == 'B' then
        Back

    else
        Front


toColumnInstructions : String -> List ColumnInstruction
toColumnInstructions input =
    input |> String.toList |> List.filter isColumnInstruction |> List.map toColumnInstruction


isColumnInstruction : Char -> Bool
isColumnInstruction c =
    c == 'L' || c == 'R'


toColumnInstruction : Char -> ColumnInstruction
toColumnInstruction c =
    if c == 'L' then
        Left

    else
        Right



-- INPUT


getInput : List String
getInput =
    [ "FBFBFBFRRL"
    , "BFBBFFFRRL"
    , "FFBFFFFRLL"
    , "BFFFBBBRLL"
    , "BBFFBFBLLR"
    , "FFFFBBBRLR"
    , "FBBBBFFLRR"
    , "FBFFFBFRLL"
    , "FFFFBFFRRR"
    , "FFFBBFFRLR"
    , "BFBBBBFRLL"
    , "FBBFBFFLLL"
    , "FFFBFFBRRL"
    , "BFBFFBBLLL"
    , "FFBBFBBLLR"
    , "FFBFFBBRRL"
    , "BFBFBBBRRL"
    , "FFBFFBBLLL"
    , "BFFFBBBLRR"
    , "BFBFFBFRRR"
    , "BFFBFFBRRL"
    , "BFBFFFFLLR"
    , "FFFFBBBLRR"
    , "FFBBFBFRRR"
    , "BFFFBFBLLL"
    , "FBFFBBBRRL"
    , "FBBBBBBRRL"
    , "BBFBFFBLLL"
    , "BFFBFFFLLL"
    , "FBFFBBFLLR"
    , "FBFBFFBLRL"
    , "FFBFFFBRLR"
    , "FFBBBBFRLL"
    , "FBFBFFFLRL"
    , "FBBFBBFRLR"
    , "FFBBBBBLLL"
    , "FBFFBFBLLL"
    , "FBFFFBBRRR"
    , "BBFFBBFRRR"
    , "FBFFBFBRLL"
    , "FBBBFBBRRR"
    , "BFFFBFFRRL"
    , "FFBFBFBLLL"
    , "FBFBFFFRLR"
    , "FBBFBBBLLL"
    , "FFFBBBBLLL"
    , "FFFBFFBLLL"
    , "BFBFFBBLRR"
    , "FFBBFFFLLR"
    , "FFBBBBBLRR"
    , "BBFFFFBRLL"
    , "BFFFBBFLRR"
    , "BFBFFFBRRR"
    , "FBBFFFBLRR"
    , "BFBFBFFLLL"
    , "FBBFFBFRLL"
    , "FFBBBBFLRL"
    , "BFFFFBFLLR"
    , "FBFBBBFLLR"
    , "FFFBBFBRLL"
    , "FFBFFBBRLL"
    , "BFBBFFBRRR"
    , "FFFFBFBRLL"
    , "FBFFFBFRRL"
    , "FBBFFBBLLR"
    , "FFBBFFBRRL"
    , "FBBBFFBRRL"
    , "BFFFBBFLRL"
    , "FFBBBFBRRL"
    , "FFFFBFBRRL"
    , "BFBFFBFLLR"
    , "FBBBBBFLLR"
    , "BFFBFFFLRL"
    , "FFFBFBFRRL"
    , "FFFFBBBRLL"
    , "BFFFBFFRLL"
    , "BFFFBBBLLR"
    , "BBFFFFFRLR"
    , "BBFFFBFRLR"
    , "BFBBFBBLLL"
    , "FBFBBBFRLL"
    , "BFFBBFFRLR"
    , "BFFBFBBLRR"
    , "FFBFBBFRRR"
    , "BFBBBFFLRR"
    , "BFFBFBBRRR"
    , "BBFFFFFRRL"
    , "BBFFBFBLLL"
    , "BFBBFBFLRL"
    , "FBBFFBFLLL"
    , "FBBFBFFRLL"
    , "FBBBBFFLRL"
    , "FBBFBFFRRL"
    , "FFFBFBFLLL"
    , "FFBFFBFRLR"
    , "FBBFFFBLLR"
    , "FFFFBFBLRL"
    , "FFFBBFBLRR"
    , "FFBBBFFRLL"
    , "FBFBBBFRRR"
    , "BFBBBBFLLL"
    , "BBFFBFFLRL"
    , "FFFFBBBLLL"
    , "FFBFBBBLLL"
    , "BFBFBFFRRL"
    , "FBFFBBFRRR"
    , "FFFBBBBLRR"
    , "FBBBBFBLLL"
    , "FBBBBBBLRL"
    , "FFBFFFBLRR"
    , "BBFBFFBRRL"
    , "BFBBFFBLLL"
    , "BFFFFFFLRL"
    , "BFFFFBFRLR"
    , "FBFFFFFLLL"
    , "BFFBBFFRRL"
    , "BFBFBBFLLL"
    , "BFBFBFBRLL"
    , "FBFBFBBLLL"
    , "BFFFBFFLLR"
    , "FBBBFBBLLL"
    , "FFBFFFBRLL"
    , "FBBFFBBLRR"
    , "FFBFBFBRLL"
    , "BFFFBBBRLR"
    , "BBFFBFBLRL"
    , "BBFFBFBLRR"
    , "BBFFBBFRLL"
    , "BFFFFBBRRR"
    , "FBFBBFFLRR"
    , "FFBBBBBRRR"
    , "BFBBBFFRLL"
    , "BFBBFFFLRR"
    , "FBFBFFBRRR"
    , "FFBFFBFLRR"
    , "BFBBBBBLRL"
    , "FBFFFFBRRR"
    , "FFBFFFFLLR"
    , "BFFFFFBLRL"
    , "FFBBBBFLLL"
    , "FBFFFBBLRL"
    , "BBFFBFFLLR"
    , "FBBFFFBRLL"
    , "BBFFBBBRLR"
    , "FBFFFBFLRR"
    , "BFFBBFBRRL"
    , "FBBFFFFRLR"
    , "BFFBBBFLRR"
    , "FFBBFBBLRR"
    , "BFBBBBFRRL"
    , "FBFBBBBLLL"
    , "BBFFBFBRRR"
    , "FFFFBBFRLR"
    , "BFBBBBFRLR"
    , "FBBFFBFRLR"
    , "BFBFFFBRLL"
    , "FBFBFBBRRL"
    , "FBFBBFBRLR"
    , "BFBBBBBRRR"
    , "BBFBFFBRLR"
    , "FFBFFFBLRL"
    , "FBBFFBFLLR"
    , "BFFBFBFLLL"
    , "BFFFFFBLLL"
    , "BFBFFBBRLR"
    , "FBBBBFBRLR"
    , "BFBBBFBRLR"
    , "BFBBFBBRLL"
    , "BBFFFFBLLR"
    , "FBFBFBFRLL"
    , "FFFBBFBRRL"
    , "FBFFBBFRLR"
    , "FFFBBBBLLR"
    , "BBFFBFFLRR"
    , "FBBBFFFRRL"
    , "BBFFBBFLLL"
    , "BBFFFBFRLL"
    , "FFBFBBFLRR"
    , "BFBFFFBLRL"
    , "FFBFBBFLLR"
    , "FBBBBFFLLL"
    , "FFBBBBFLRR"
    , "FFFBFBBLRL"
    , "FFFBBFFLRR"
    , "FBBBFBBRLL"
    , "FFBFFFFLLL"
    , "FBBBFBFLRL"
    , "FBFBFBFRRR"
    , "FFBBFBFLRR"
    , "FFBFBBFRRL"
    , "FBFBBFFLRL"
    , "BFFFBBBRRL"
    , "BFBBBBFLLR"
    , "FFFBBFFRRR"
    , "BFBBFBBRRL"
    , "BBFFFBBLRL"
    , "BFBFBFFLRR"
    , "FFFFBFFLRL"
    , "BFBFFBFRLL"
    , "BFBFBBFRLR"
    , "BFFBFFFLRR"
    , "FBFFFFFLRR"
    , "BFFBFBFRLL"
    , "FBBFBFFLRR"
    , "FBFBBBBLRR"
    , "BFFFFFFRLR"
    , "FBBFBBBRRL"
    , "BFFBFBFRLR"
    , "FFFBFFFRRL"
    , "FFBFFFFRLR"
    , "BFFBFFBLLL"
    , "FFBFBBFLRL"
    , "BBFFFFFLRL"
    , "FFFBBFFRRL"
    , "FFBBBFFLRL"
    , "BFBBFFBLRR"
    , "FFBBFBFRLR"
    , "FFBFBFFRRR"
    , "FFFFBFFLRR"
    , "FBBBBFBRRL"
    , "BFBBFBBLRL"
    , "BFFBBFFLLR"
    , "FBFFFBFLLR"
    , "FBFBFFBLRR"
    , "FFBBFBBRLL"
    , "FBFFFFFRLR"
    , "FFBBBBFRRL"
    , "FBBFFBFRRR"
    , "FFFFBBFRRR"
    , "FBBBFFBLLL"
    , "FFBBFBBLLL"
    , "BFBFBFFRLL"
    , "BFFFBBFLLL"
    , "BFFBBFFRLL"
    , "FBFBBFFRRL"
    , "BBFBFFFLLR"
    , "BBFBFFBLRR"
    , "FBFFFFFRRR"
    , "FBFFBFFRRR"
    , "BFFBBFBRLR"
    , "FBFBFBFLLL"
    , "BFFBBBBLRR"
    , "BFBBFBBRLR"
    , "FFBBBFFLRR"
    , "FBFBBBBRRR"
    , "BFBBBBBRLL"
    , "BFBFFBBRRR"
    , "FBFBBFBRLL"
    , "FBFFBFBLRL"
    , "FBBFBBBRLL"
    , "FBFBBBBLRL"
    , "FBFFFBBLLR"
    , "BBFFFBFRRL"
    , "FBFBFBBRLL"
    , "BFBBBBBRLR"
    , "BFBFFFFRLR"
    , "FBFBBFBLRR"
    , "BFBBFBFRLR"
    , "BBFFBBBLLL"
    , "BFFFFFFRRR"
    , "BFBBBFBLRL"
    , "FBFBBFFLLR"
    , "FBFBBFFRLR"
    , "FFFBFBBLLR"
    , "FFBBFFFRLL"
    , "BFBFFFFLRR"
    , "FFFFBBBRRL"
    , "BFFFBFFRRR"
    , "BFFFBFBRLL"
    , "FFFFBFFRRL"
    , "BFFFBBFRRL"
    , "FFFBBFFLLL"
    , "BFBBFFBRRL"
    , "FBFBFFFRRR"
    , "FBFBFBFLRL"
    , "BFBFBFBLLL"
    , "FBBBFFBRLL"
    , "FBFFBBBLRL"
    , "BFBFFFFRRL"
    , "BFFBBFBLLL"
    , "FBFFFBBRLR"
    , "BBFBFFFRLL"
    , "FFBFBFFLRL"
    , "FBBFBBBLRL"
    , "BBFBFFFLRR"
    , "BBFBFFBRRR"
    , "BFFBFFBRLR"
    , "BBFFBBFRRL"
    , "FBFBBBFLRR"
    , "FBBFFFFLLL"
    , "BFFBBFBLRR"
    , "BFBFFFFLLL"
    , "BFFBBBBRLL"
    , "FFBFFBFLLL"
    , "FBBBBFBLLR"
    , "BBFFFBFLLR"
    , "BFBBBFBRLL"
    , "FBFFFFBRLR"
    , "FFBBBFFRRL"
    , "FFBFFFBRRR"
    , "BFFBFFFRLL"
    , "FFFBFBBLLL"
    , "FFFBBBFLLL"
    , "BFBBFBFRLL"
    , "BFBFFFBRLR"
    , "FBBFBBFRLL"
    , "FBBBFBFRRL"
    , "FFBFBFFRLR"
    , "BFBBFBBLLR"
    , "FBBFBFBRLR"
    , "BBFFFBBLLL"
    , "FBFBFFFLLL"
    , "BBFBFFFRRR"
    , "FBFBBFBLRL"
    , "FFBBBFBRLR"
    , "BFBBFFBRLR"
    , "FBFFBBBLRR"
    , "FFBBFFBRRR"
    , "BBFFBFBRRL"
    , "FFBBBFFRRR"
    , "BFBFFBFLRL"
    , "FBFFFFBLLL"
    , "BBFFFFBRRL"
    , "BBFFFFBLRR"
    , "FFBBFFBRLL"
    , "BFBBFFFLLL"
    , "FBBFBFBLLL"
    , "FBBBFFFLRL"
    , "FBFBBBBRRL"
    , "FFFBBBFRRR"
    , "FFBFFBBRRR"
    , "FBFFFFFLRL"
    , "BFFBFBFLRR"
    , "BBFFBBBRRR"
    , "FBFFFFFRRL"
    , "FBBFBFBLRR"
    , "BFFBBBBLLL"
    , "FBBBFFFLLR"
    , "BFFFFBFLLL"
    , "FFBFBFBLLR"
    , "FBFFFBBRLL"
    , "BFFFBFBRLR"
    , "FBBBFBFLLR"
    , "FBBBBFFLLR"
    , "BFFFFBBLLR"
    , "FFBBBBBRLR"
    , "BFFFBFBLRR"
    , "FBBBFFBLLR"
    , "FBFFBFBRRL"
    , "FBFBFBBRRR"
    , "FBBBBBBLRR"
    , "FFBBBBBRRL"
    , "FBFFFFBLLR"
    , "BBFBFFBRLL"
    , "FFFBBBFRLR"
    , "FBFFFBBLLL"
    , "FBFFBBBLLR"
    , "BFBFBBFRRL"
    , "BBFFBFBRLL"
    , "BFFFBBFRRR"
    , "BFFBBFBLRL"
    , "FBBBFBFLRR"
    , "FFFBFBFRRR"
    , "FFBBBFBLRR"
    , "BFBFBBFRRR"
    , "FFBBBFBRLL"
    , "BFFFBBBLLL"
    , "BFFFBFBRRL"
    , "BFFBFBBRLL"
    , "FBBFFFFLRL"
    , "FFFFBFFRLR"
    , "FFFBBBBRRL"
    , "BFFBFBFRRL"
    , "FFFBBFBRRR"
    , "FFBFBFBLRR"
    , "FFFFBBFLRL"
    , "BBFFFFBLRL"
    , "BFBBBBBRRL"
    , "FBBBBBFLLL"
    , "FBFFBFFLRL"
    , "FFBFBBBRRR"
    , "FBFBBBBRLL"
    , "BBFFFBBRRL"
    , "FFBBFBFRRL"
    , "FFBBBFFRLR"
    , "FFFBFBFRLL"
    , "FBBFBFBLLR"
    , "FFBBBBBLLR"
    , "FBFBFFBLLR"
    , "BFFFBBFRLR"
    , "FFBBFFFRRL"
    , "FFFFBBFLRR"
    , "BBFFFFFRRR"
    , "FFBBFFBLLR"
    , "FBFFFFBLRR"
    , "FFFFBFFRLL"
    , "BFBBFFFRLL"
    , "BFBBFFBRLL"
    , "BBFFFBBRLR"
    , "FFBFFFFRRR"
    , "BFBFBFBRRR"
    , "FFBBFBFLLR"
    , "BFFBBBFRLL"
    , "FBBBFFFRRR"
    , "BFBBBBBLLL"
    , "FFBFFFFLRR"
    , "FBFFFFBRLL"
    , "BFFFFBFRRL"
    , "FBBBBBBRRR"
    , "FFFFBBFLLL"
    , "FBFFBFFLRR"
    , "FFFBBBFRRL"
    , "FBBFFFBRRL"
    , "BFBFBBBRLL"
    , "BBFFFBFLRR"
    , "FBBFBFBRRL"
    , "FBBFFFFLRR"
    , "BFBBBFBLLL"
    , "BFFFFFBRRL"
    , "BBFFFBBLRR"
    , "BFFFFFBLRR"
    , "BFBBBBFLRL"
    , "FBFBFFBRRL"
    , "BBFFFFFLRR"
    , "FFFFBBBLLR"
    , "BFBBFBFLLL"
    , "FBBFFFBRRR"
    , "FFBBBFBRRR"
    , "FFBFBFFRLL"
    , "FFBBFBBLRL"
    , "FBBFFBFRRL"
    , "FFFBBFBLRL"
    , "FFBBFFBLRR"
    , "BFFFFBBLLL"
    , "FBBFBBFLRL"
    , "FFFBFFBLRL"
    , "FBBFFBBRRL"
    , "FBFFFBFRRR"
    , "BFBBBFFLRL"
    , "FFFFBFFLLL"
    , "FBFFFFFRLL"
    , "BFBFFFFRLL"
    , "FFBFBBBLRL"
    , "BFFBBBBLLR"
    , "BFFBBBFRRL"
    , "FFBBBBFLLR"
    , "FFFBFBFLRR"
    , "FBFFBFFRLR"
    , "BFBFBBBRLR"
    , "BFFBFFFLLR"
    , "FFFFBFBLLR"
    , "FBFFBFBLRR"
    , "BFFBFBFRRR"
    , "BFFBFFBLRL"
    , "FBBBBBFRRR"
    , "BFBBFFBLRL"
    , "FFBBFBBRRL"
    , "FBFFBFFRLL"
    , "FFBFFBFLLR"
    , "BFBBBBBLRR"
    , "BFFBBFFLRL"
    , "FBBBFBBRRL"
    , "BBFFBBBLRR"
    , "BBFFFBFRRR"
    , "FBFFBFBRLR"
    , "FBFBFFBRLR"
    , "BBFFFFBLLL"
    , "FBBFBFFRRR"
    , "FFBBFBFRLL"
    , "FFFFBFBLRR"
    , "FBFBFFFRRL"
    , "FBBFBBFRRL"
    , "FFBFFBFLRL"
    , "FFBFBFBRRR"
    , "FFFFBBFRRL"
    , "BFFBBBFRLR"
    , "FFBFBBBRRL"
    , "BFFBFBBLLL"
    , "FBBBBFFRRL"
    , "FFFBFBFRLR"
    , "FFBFFBBLRL"
    , "BFFBFFBLRR"
    , "FBBBFFFRLR"
    , "FBBBFFBRLR"
    , "FBBBBBBLLR"
    , "FBBFBFFLLR"
    , "BBFFBFFRRL"
    , "FBBBBBFRRL"
    , "FFFBBFFRLL"
    , "FFFBBFFLRL"
    , "FFBFFBBLRR"
    , "FBBFFFBLLL"
    , "FFFFBBFRLL"
    , "FFBFFBBLLR"
    , "BFFFBFFLLL"
    , "BFFBBFBRLL"
    , "FBBFFFBRLR"
    , "FFFBFBBLRR"
    , "BFBFFBBLRL"
    , "FBFFFBFRLR"
    , "BFBFFFFLRL"
    , "BFBBBBBLLR"
    , "FFFBBFFLLR"
    , "BFBFFFBLLR"
    , "FFFFBBFLLR"
    , "FBBFBBFLRR"
    , "FBBBFBBLLR"
    , "BFFFFFBRRR"
    , "FBFBFFFLLR"
    , "FBFBBBBRLR"
    , "FFFBFFBLLR"
    , "FFFBBFBLLL"
    , "BFFBFBBRRL"
    , "BFBFBBBLRL"
    , "BFFFBBFRLL"
    , "FBBFFBFLRL"
    , "BFBFBBBRRR"
    , "FFFBFFBRRR"
    , "BFFFBFFLRL"
    , "BBFFBBFRLR"
    , "FFFBBBBLRL"
    , "FBBFFFFRRL"
    , "FBFFBFFRRL"
    , "BFFFFFBRLL"
    , "FBFBBFBRRR"
    , "FBFBBBFLRL"
    , "FBFFBBBLLL"
    , "FFFFBBBRRR"
    , "FBBBFBBLRL"
    , "BFBFFBBRLL"
    , "FBFBBBFRLR"
    , "FFFBBBFLRR"
    , "BFFBFFFRLR"
    , "BFBFFBFRLR"
    , "BFBBFFFLLR"
    , "FBFFBBBRRR"
    , "FBBBFFBLRL"
    , "BFBFBBBLRR"
    , "FBBBBBFLRR"
    , "FBBBBBBRLR"
    , "BFBFFFFRRR"
    , "BFBBBBFLRR"
    , "BFBBFFFRRR"
    , "FFBFBFFLLL"
    , "FBFFFBFLRL"
    , "BFBBFBFLLR"
    , "BFFBBBFLLR"
    , "FBBFBFBRRR"
    , "FFBFFBFRLL"
    , "BFFFBFFLRR"
    , "FBFBBFFLLL"
    , "FFFBFBBRRR"
    , "FBBBFBBRLR"
    , "BFFFBBBRRR"
    , "FFFBFBFLLR"
    , "BFFBFBBLRL"
    , "FBFBBFFRLL"
    , "BFBBFBBLRR"
    , "FFFBBBBRLR"
    , "BFFFFFFLRR"
    , "FBFFBBFLRL"
    , "BFBFFFBRRL"
    , "BBFFBFFLLL"
    , "FFBBFBBRRR"
    , "BFBFFBFRRL"
    , "BFFFFBBLRL"
    , "BFBBFFFLRL"
    , "FBFFFBFLLL"
    , "FBBFFBBRLL"
    , "FFBBFFBRLR"
    , "FFFBFFBLRR"
    , "BFBFBFFLRL"
    , "FBBBBFBRRR"
    , "FBBFFBFLRR"
    , "BFFBBFBRRR"
    , "FFFBFFBRLL"
    , "FFBFBFFLRR"
    , "FFFBFFFLRL"
    , "BFBFBFBRRL"
    , "BFFFFBFRRR"
    , "FFBFBBBRLR"
    , "BFFBFFBRRR"
    , "FBBBFBFRRR"
    , "FBBBBBFRLL"
    , "BBFBFBFLLL"
    , "FBFFFBBRRL"
    , "FBBBBFBRLL"
    , "BBFFBFBRLR"
    , "FFFFBFBLLL"
    , "FFBFBBBLLR"
    , "FFFBBFBRLR"
    , "BFBFFBBRRL"
    , "FFBFBFBRRL"
    , "FFBFBFBRLR"
    , "FFFBBBFRLL"
    , "FFBFBBFRLL"
    , "FFFFBFBRRR"
    , "FFFFBFBRLR"
    , "BBFFFFFLLL"
    , "BFBFFFBLLL"
    , "BFBBBFFRRR"
    , "FBBBBBBLLL"
    , "FFBFBBBRLL"
    , "FBFBBBFLLL"
    , "FBBBFFBRRR"
    , "BFBBFBFLRR"
    , "FFFBBFBLLR"
    , "FFFBBBBRRR"
    , "FFBFBFBLRL"
    , "FFBBFFFLRR"
    , "FBBFBFBLRL"
    , "FBBFFBBRLR"
    , "FBBFFBBRRR"
    , "BFBFFBFLLL"
    , "FBFFFFBLRL"
    , "FFBBBBBRLL"
    , "FBFBFBBLRL"
    , "FBFFFFBRRL"
    , "BFBBBFBRRR"
    , "FFFBBBFLRL"
    , "FBFBFBFLRR"
    , "BFFBFFBLLR"
    , "BFBFBFBRLR"
    , "FBBFBBFRRR"
    , "BFBFFBBLLR"
    , "BFBFFFBLRR"
    , "FBBBBBFLRL"
    , "BFFFBFBLLR"
    , "BBFFFFBRLR"
    , "BBFBFFFRRL"
    , "BBFBFFBLRL"
    , "BBFFFBFLRL"
    , "FFBBFFFLRL"
    , "FBBBFBFRLL"
    , "BFFFFBFRLL"
    , "FBBBFFFLRR"
    , "FFBFFBFRRR"
    , "FBBBFBFRLR"
    , "FFBFBFFRRL"
    , "FBFBBFBLLL"
    , "FFBBBFBLRL"
    , "FFBBBBFRRR"
    , "FBFBFBBLLR"
    , "FBBBBFBLRL"
    , "FFBBBFFLLL"
    , "FBFFBBFLRR"
    , "FBFBFBBRLR"
    , "BBFFBBFLRR"
    , "FBFBBBFRRL"
    , "BFFBBFFRRR"
    , "BBFFFBBRRR"
    , "BFFBBBBRRL"
    , "BBFFFFFLLR"
    , "BFBBBFFLLR"
    , "BBFBFFFLLL"
    , "BFFBBBFLRL"
    , "BFBFFBFLRR"
    , "FBBFBFBRLL"
    , "BFFFFFBLLR"
    , "BFBFBBFRLL"
    , "FBBFBBBRRR"
    , "FFBFFFBRRL"
    , "BFBBBBFRRR"
    , "BFFFBBFLLR"
    , "FBBBFFFLLL"
    , "FBFFFFFLLR"
    , "FFBFFFFRRL"
    , "FFBBFFFRLR"
    , "FBFBFFFRLL"
    , "FFBBBBBLRL"
    , "FBFFBFBLLR"
    , "BFBFBBFLRL"
    , "BFFFBFFRLR"
    , "BBFFBBFLRL"
    , "BFFBFFBRLL"
    , "BFFFFBBLRR"
    , "BFBFBBBLLR"
    , "BFFBBBBRLR"
    , "FBBBBFFRRR"
    , "BBFFBBBLRL"
    , "FBBBFFFRLL"
    , "FBBFFFFRRR"
    , "FFBBBFFLLR"
    , "BBFFBBFLLR"
    , "BFFBBBBRRR"
    , "BFBBFFBLLR"
    , "BFBFBBBLLL"
    , "BFFBBFBLLR"
    , "BFBBFBFRRR"
    , "BFFFBFBRRR"
    , "BFBBBFFLLL"
    , "BBFFBFFRLL"
    , "FBBFFFBLRL"
    , "FFFBFFFLLL"
    , "BFBBBFBLRR"
    , "FFBBBBFRLR"
    , "BFFBFBFLRL"
    , "BFBFBFBLLR"
    , "BBFFFBBLLR"
    , "FBFBFFFLRR"
    , "FFBFBFFLLR"
    , "FFBBFFBLLL"
    , "BFBFBFFRRR"
    , "FBFBBBBLLR"
    , "BFBFBBFLLR"
    , "FBBFFBBLLL"
    , "FBFFBBBRLR"
    , "FBFFBBBRLL"
    , "FBFFBFFLLR"
    , "BFFBBBFRRR"
    , "BFFFFFFLLR"
    , "BFBBFBFRRL"
    , "FFBFFBBRLR"
    , "FBBBBFFRLR"
    , "BFFBFFFRRL"
    , "FFBFBBFLLL"
    , "FFFBFBBRLL"
    , "FFFBBBBRLL"
    , "FBBFBBBRLR"
    , "FFFBFBBRRL"
    , "FFBBFFFRRR"
    , "BFFFFFFRRL"
    , "FFBBFFBLRL"
    , "BFFFFFBRLR"
    , "BFFBBBFLLL"
    , "FBFFBFFLLL"
    , "FFBFFFFLRL"
    , "FFFFBBBLRL"
    , "FBFBBFFRRR"
    , "FBFFBBFRLL"
    , "BFFFFFFLLL"
    , "FFBFFFBLLL"
    , "BFBFBBFLRR"
    , "FBBFFFFLLR"
    , "BFBFBFFRLR"
    , "BFBBFFFRLR"
    , "BFBBBFFRLR"
    , "BFFBBFFLRR"
    , "BBFFBBBRLL"
    , "FBBFFFFRLL"
    , "BFFFFBBRRL"
    , "FBFBBFBRRL"
    , "BFFBFFFRRR"
    , "FFBFFBFRRL"
    , "BFFFFBBRLR"
    , "BFFFFBFLRL"
    , "BFBBBFFRRL"
    , "FBBBFBFLLL"
    , "BFFBFBBLLR"
    , "FBFBFBBLRR"
    , "FBBFBBBLRR"
    , "BFBFBFFLLR"
    , "BFFBBBBLRL"
    , "BFFFFFFRLL"
    , "FFFBFFFRLR"
    , "FFBBFBFLRL"
    , "FBFBFFBLLL"
    , "BBFFBFFRLR"
    , "FBBFBBFLLL"
    , "BFBBFBBRRR"
    , "FBBBBFFRLL"
    , "BFBBBFBLLR"
    , "FFBFFFBLLR"
    , "FFFBFFFLRR"
    , "FBFBFBFRLR"
    , "BBFFFFBRRR"
    , "FBBFBBBLLR"
    , "BFBBBFBRRL"
    , "BBFBFFBLLR"
    , "FFBFBBBLRR"
    , "FFBBBFBLLL"
    , "FBBBFFBLRR"
    , "FFFBFBFLRL"
    , "FBFFBBFRRL"
    , "FFFBBBFLLR"
    , "BFFFBBBLRL"
    , "BBFFFBBRLL"
    , "BBFFFBFLLL"
    , "FBBFBFFLRL"
    , "FFFBFBBRLR"
    , "FFBFBBFRLR"
    , "FBBBFBBLRR"
    , "FBFFBFBRRR"
    , "BFFBBFFLLL"
    , "FFBBFFFLLL"
    , "FFFBFFBRLR"
    , "FFBBFBFLLL"
    , "FBBFBBFLLR"
    , "FFFFBFFLLR"
    , "BFFBFBBRLR"
    , "FBFBFFBRLL"
    , "BBFFFFFRLL"
    , "BBFBFFFLRL"
    , "FFFBFFFRRR"
    , "BFFBFBFLLR"
    , "FFBBBFBLLR"
    , "FBFFBBFLLL"
    , "FBFFFBBLRR"
    , "BBFFBBBRRL"
    , "FBFBBFBLLR"
    , "FFFBFFFLLR"
    , "BBFFBFFRRR"
    , "FBBFFBBLRL"
    , "FBBFBFFRLR"
    , "BBFBFFFRLR"
    , "BFBFBFBLRR"
    , "FFBBFBBRLR"
    , "FFFBFFFRLL"
    , "BBFFBBBLLR"
    , "FBBBBFBLRR"
    , "FBFBFBFLLR"
    , "BFFFFBFLRR"
    , "BFFFFBBRLL"
    , "FBBBBBBRLL"
    , "FBBBBBFRLR"
    , "BFFFBFBLRL"
    ]
