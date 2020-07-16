## JSON API Errors
See [the JSON API error spec](https://jsonapi.org/format/#errors), and
[examples](https://jsonapi.org/examples/#error-objects).

### Installation
TBA

### Deviations
LeafLink API errors deviate from JSON API errors in two ways:

1. LeafLink APIs do not wrap request bodies in the `data` top level key. Thus, error `source.pointer` properties will
never begin with `/data/`, they will begin with `/`.
2. Error responses will return a `Content-Type` of `application/json`, not `application/vnd.api+json`. This is because
we do not strictly meet the JSON API error spec.

### Remarks
Error `title` properties should _always_ be the same for the same error type. Example:

```javascript
// No
{
    "errors": [
        {
            ...,
            "title": "Product #123 not found."
        },
        {
            ...,
            "title": "Order #456 not found."
        }
    ]
}

// Yes
{
    "errors": [
        {
            ...,
            "title": "Not found.",
            "detail": "Product #123 could not be found."
        },
        {
            ...,
            "title": "Not found.",
            "detail": "Order #456 could not be found."
        }
    ]
}
```


## Development
See the project's [GitHub page](https://github.com/LeafLink/pyll-json-errors) for development information.
