# servicegen

servicegen is a small domain specific language to specify web services.
The idea is to lower the barrier for creating a new service.

The simple service description will abstract a few common tasks:

  - Getting input parameters and validate them.
  - Get data from other web services or a database.
  - Configuration handling for deployments.
  - Logging.
  - Caching using e.g. memcached.
  - Correct handling of HTTP caching.

A few features can be provided based on the input format:

   - Create service in various programming languages and frameworks. I can
     imagine creating output for [web.py][], [Okapi][], [Spring][], etc.
     This would allow to easily switch deployment platform depending on
     current requirements.
   - Create documentation for the service in a consistent format.
   - Maybe even create clients for various programming languages.


## Status

Started on May 26, 2008 by [Patrice Neff][] during a local.ch-internal
hack day. Currently doesn't do much. There is:

  - An ANTLR grammar for a basic service description.
  - A generator in Python which gives some output based on what it parsed.
  - An extensive grammar documentation showing what's the intention.
  - An output target to create a basic web.py application.
  - An output target to create a basic HTML documentation.


## Usage

On a shell execute gen.py like this:

    $ ./gen.py docs/meteo-service.txt


## Design Choices

  - Variables can't change their value once the value is defined.
    This way on assignment of each variable it can be determined
    whether the variable can be read from a cache or not depending
    on the keyword "cached".

## TODO

  - Specified but to implement:
    - Missing functions in web.py target:
      - log.*
      - etag
      - expires
    - Correct output format for exceptions (XML, CSV, ...)
    - Caching
    - Caching of output blocks
  - Inherent documentation for web.py target at /__docs or similar
  - Language improvements:
    - Re-use output blocks


[web.py]:       http://webpy.org/
[Okapi]:        http://okapi.liip.ch/
[Spring]:       http://www.springframework.org/
[Patrice Neff]: http://weblog.patrice.ch/
