# API

## POST /bet

POST body example:

    {
        "title": "The coin will come up a head",
        "confidence": 0.8
    }

Response:

    {
        "id": 1
    }

## GET /bet

Response:

    [
        {
            "id": 1,
            "title": "The coin will come up a head",
            "confidence": 0.8
        },
        {
            "id": 2,
            "title": "Another prediction",
            "confidence": 0.8
        }
    ]

## GET /bet/1

Response:

    {
        "title": "The coin will come up a head",
        "confidence": 0.8
    }
