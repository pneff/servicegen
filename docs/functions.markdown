# Built-in Functions

There are a number of functions which are defined by the servicegen language.
They are designed to work well with HTTP.

## validate

    validate(value, comparison)

The `validate` function takes two parameters. A value to validate and a value
to validate against. Usually you'll use this function at the beginning of the
request block to make sure the incoming values conform to the specification.

If the value does not validate, an exception is thrown. This means that the
service outputs a valid answer for the current request type (an XML structure
if the client is requesting an XML document, a text output for text output,
etc.). Additionally the HTTP response code 400 (Bad Request) is sent.

If you pass in a regexp literal, the value must match exactly against that
expression. So passing in `/[0-9]{4}/` is the same as passing in
`/^[0-9]{4}$/`. If any other literal is passed in as comparison value, the
value must match exactly.


## log.*

    log.trace(message, params...)
    log.debug(message, params...)
    log.info(message, params...)
    log.warn(message, params...)
    log.error(message, params...)
    log.fatal(message, params...)

Logs the message with the level defined by the function name. Logging levels
and destinations can be set at deployment. So a developer will usually set the
level to 'debug' but may track down a problem with 'trace'. In production
environments the level will usually be set to 'error'.

The generated code by servicegen also uses the same logging framework,
especially the 'trace' method to make sure that code flow can easily be
debugged.

`message` can contain very simple format specifiers (inspired by C's printf).
In the servicegen framework only the '%s' modifier is used and supported. It's
used to easily add the given params at the correct place in the output.


## etag

    etag(hash)

Calling the etag function allows you to implement a very easy HTTP cache
handling. You call it with the hash you want to assign to the current request.
If you pass in any non-string data type, servicegen will calculate a hash out
of the variable's content.

If the client has sent a "If-None-Match" HTTP header containing exactly that
hash, then the request is immediately aborted and the response code 304 (Not
Modified) is sent. If the client sets the "no-cache" option in its
"Cache-Control" header, this behaviour is turned off.

In the case that the request continues, the "ETag" response header is set.


## expires

  expires(duration)

Specifies how long the response is to be cached by clients. The input must be
of the duration variable type. For any other value the function will return
and log an error.

The function sets the two HTTP headers "Expires" and "Cache-Control"
correctly. Expires is for HTTP/1.0 implementations, Cache-Control for 1.1. The
effect is that the client knows that it can (but doesn't have to) cache the
response for the duration period.

