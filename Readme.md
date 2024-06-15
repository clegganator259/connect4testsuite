# Connect 4 Testing Harness

## Description

This is a specification, and a matching testing harness. The idea is to provide
a standard project for use when learning new languages for web development.

## Running

Requirements:
- `Python3`
- `Pipenv`

To install run `make`
To run the test suites run `make test`

## Specification

This is a webapp that allows users to play games of connect 4 against
eachother. It will track the games, and record the moves taken and will store
results against the game when it is complete.

### Players

There are two players:
- Red (`R`)
- Yellow (`Y`)

### Board

The board is represented as 6x7 Element arrays with `""` represents an empty
cell, `"R"` represents a cell that is filled by a red token and `"Y"`
represents a cell that is filled by a yellow token.

#### Examples:

An empty board:
```
[
    [ "", "", "", "", "", ""],
    [ "", "", "", "", "", ""],
    [ "", "", "", "", "", ""],
    [ "", "", "", "", "", ""],
    [ "", "", "", "", "", ""],
    [ "", "", "", "", "", ""]
    [ "", "", "", "", "", ""]
]
```
A board with a single red entry in the middle
```
[
    [ "", "", "", "", "", ""],
    [ "", "", "", "", "", ""],
    [ "", "", "", "", "", ""],
    ["R", "", "", "", "", ""],
    [ "", "", "", "", "", ""],
    [ "", "", "", "", "", ""]
    [ "", "", "", "", "", ""]
]
```
A game in which yellow has won after a series of turns
```
[
    [ "", "", "", "", "", ""],
    [ "", "", "", "", "", ""],
    ["Y", "", "", "", "", ""],
    ["R","Y", "", "", "", ""],
    ["R","R","Y", "", "", ""],
    ["Y","R","R","Y", "", ""]
    [ "", "", "", "", "", ""]
]
```

Notice how the board appears "on it's side" This is so the indexing
`board[i][j]` makes sense on a board looking like this

```
5 [ ][ ][ ][ ][ ][ ][ ]
4 [ ][ ][ ][ ][ ][ ][ ]
3 [ ][ ][ ][ ][ ][ ][ ]
2 [ ][ ][ ][ ][ ][ ][ ]
1 [ ][ ][ ][ ][ ][ ][ ]
0 [ ][ ][ ][ ][ ][ ][ ]
   0  1  2  3  4  5  6
```

### Moves

A move is an object with two keys: "player" and "column" Where players is "R"
or "Y" and column is an integer from 0-6 corresponding to the game column. When
creating it in the API we will only send the column as the player will be
inferred from the authentication

#### Examples:

```
{
    "player": "R",
    "column": 3
}
```
### Game

```
{
    "id": <gameid matching : "game_[2-9A-HJ-NP-Za-km-z]{22}">,
    "players": {"R": <user_id>, "Y": <Optional user_id>},
    "board": <board defined above>,
    "moves": <list of moves defined above>,
    "status": <OPEN|IN_PLAY|COMPLETE>
    "victor": <None|R|Y|STALEMATE>
}
```

#### Statuses:
 - OPEN: The game has been created but only has 1 player
 - IN_PLAY: The game has two players and has not been completed
 - COMPLETE: The game has been finished

## Endpoints

<TODO> Full openapi 3 specs will be in api/connect4.yml

### Create user

`POST /users` - Create a users

Takes the following payload

```
{
    "username": <str>,
    "password": <str> # Plaintext
}
```
Responses:
200 OK:
```
{
    "id": <shortid matching : "user_[2-9A-HJ-NP-Za-km-z]{22}">
}
```
400 Bad Request:

When a badly formed request is sent
```
{"reason": "Bad request"}
```

### Get user
`GET /users/<shortid matching : "user_[2-9A-HJ-NP-Za-km-z]{22}">`
Responses:
200 OK:
```
{
    "id": <shortid matching : "user_[2-9A-HJ-NP-Za-km-z]{22}">
    "username": <str>
}
```

404 Not found:
```
# No content
```

### Login
/login

```
{
    "username": <str>,
    "password": <str> # Plaintext
}
```

Responses:
200 OK
```
{"token": <str auth_token>}
```
The token should be a JWT which includes some encoding of the user to enable
permission token

401 Unauthorised
```
{"reason": "invalid-credentials"}
```

### Start a connect 4 game
`POST /connect4/start`

200 OK
```
{
    id: <gameid matching : "user_[2-9A-HJ-NP-Za-km-z]{22}">
}
```

401 Unauthorised
```
{"reason": "invalid-credentials"}
```
Players must be logged in to play

### Join any existing game

`POST /connect4/<gameid matching : "game_[2-9A-HJ-NP-Za-km-z]{22}">/join`
Request:
```
# No content
```

200 OK
```
{
    Game object defined above
}
```

404 Not found
```
# No content
```
401 Unauthorised
```
{"reason": "invalid-credentials"}
```
403 Forbidden
```
{"reason": "game is full"}
```
400 Bad request
```
{"reason": "already in game"}
```

### Get an existing game
Can be polled for status - ie who's turn is it

`GET /connect4/<gameid matching : "game_[2-9A-HJ-NP-Za-km-z]{22}">`
200 OK
```
{
    Game object
}
```

404 Not found
```
# No content
```

401 Unauthorised
```
{"reason": "invalid-credentials"}
```

### Make move

`POST /connect4/<gameid matching : "game_[2-9A-HJ-NP-Za-km-z]{22}">/move`

Request:
```
{
    "column": <int>
}
```
200 OK
```
{
    Game object defined above with new state
}
```

404 Not found
```
# No content
```
401 Unauthorised
```
{"reason": "invalid-credentials"}
```
403 Forbidden
```
{"reason": "user is not in this game"}
```
400 Bad request
```
{"reason": "it is not your turn"}
```
