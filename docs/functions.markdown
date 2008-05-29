# Built-in Functions

There are a number of functions which are defined by the servicegen language.
They are designed to work well with HTTP.

## validate

    validate(value, comparison)

The `validate` function takes two parameters. A value to validate and a value
to validate against. Usually you'll use that at the beginning of the request
block to make sure the incoming values conform to the specification.

If the value does not validate, an exception will be thrown. This means that
the service will output a valid answer for the current request type (an XML
structure if the client is requesting an XML document, a text output for text
output, etc.). Additionally the HTTP response code 400 (Bad Request) is sent.

If you pass in a regexp literal, the value must match exactly against that
expression. So passing in `/[0-9]{4}/` is the same as passing in
`/^[0-9]{4}$/`. If any other literal is passed in as comparison value, the
value must match exactly.
