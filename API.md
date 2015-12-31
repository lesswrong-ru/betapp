# API

All URLs start with `/api`.

## POST /bets

Create a bet.

POST body example:

    {
        "title": "The coin will come up a head",
        "confidence": 0.8
    }

Response:

    {
        "id": 13,
        "title": "The coin will come up a head",
        "confidence": 0.8,
        "outcome": null
    }

## GET /bets

Get the list of all bets.

Response:

    [
        {
            "id": 1,
            "title": "The coin will come up a head",
            "confidence": 0.8,
            "outcome": null,
        },
        {
            "id": 2,
            "title": "Another prediction",
            "confidence": 0.8,
            "outcome": true
        }
    ]

## DELETE /bets/123

Remove a bet.

Response: HTTP 204 code, no content.

## PATCH /bets/123

Edit a bet data.

Response: HTTP 204 code on success, HTTP 400 bad request on failure.
