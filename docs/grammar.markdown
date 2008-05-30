# servicegen Grammar

## Language syntax

A service file describes one REST web service. The basic components of
the language are

  - Commands. Each command ends with a semicolon and can span over as many
    lines as wished.
  - Blocks. A block is opened with the corresponding keyword(s) followed by a
    curly bracket '{'. It's closed with the closing curling bracket '}'.
  - Comments.
      - Single-line comments starting with a hash ('#')
      - Single-line comments starting with a double-slash ('//')
      - Multi-line comments starting with '/*' and ending with '*/'


## Service definition

Each service can consists of the following components:

  - service name
  - configuration block
  - external includes
  - request blocks


## Service name

The service name is mandatory. It's a one line command:

    service SERVICENAME;

This name is currently mainly used for documentation.


## Configuration block

One of the difficulties solved by servicegen is deployment. For that purpose
constants should be declared in a configuration block, where they can be
overwritten by some configuration files in deployment. This should include
database connections, references to externals files and any other value that
doesn't change through the request.

A configuration block looks like this:

    config {
        database meteo_db;
        int      version = 2;
    }

As you can see, there are two different ways to create configuration
variables. In the first variant you just declare the variable and leave
setting the value completely to external configuration. In the second case a
default value is set, which can be overwritten by the external configuration
but doesn't have to be.

How you overwrite the value depends on the deployment target.


## External includes

As servicegen is on purpose not a Turing-complete language, it relies on
"real" programming languages for implementing business logic. In an MVC
environment, servicegen only implements the controller and primitive view
facilities. So for the model it relies on external code.

To include such code, use the keyword 'external'. For example:

    external:php "service.php";
    external:java "service.java";

This declare two externals, one which is included in a PHP-deployment and the
other which is included only in Java-deployments. These files are supposed to
export functions that can then be called inside the request blocks.

The exact manner of how those functions are exported depends on the deployment
target.


## Request blocks

### Definition

A request block is defined by the a HTTP verb and path. The body of the
request block is executed if the verb/path combination matches the incoming
request. The path can contain variable definitions in curly brackets.

Example:

    GET "/{zip}" {
        # .....
    }

This declares a commend, which will match every GET request with one path
component. The path component is assigned to the variable called 'zip'.

A few example requests:

  - `GET /9000` - matches, zip=9000
  - `GET /foo` - matches, zip=foo
  - `GET /` - does not match, no argument given
  - `GET /foo/bar` - does not match, contains two path components


### Body

The body of the request block contains a list of function calls and variable
definitions, followed by output blocks.


### Variables

Variable definitions are the same as in the configuration block with the
exception, that each variable must be initialized at the moment of
declaration. It's not possible to re-assign a variable after it's been
declared to make it possible to cache each variable using the `cached`
keyword.

A few example variables:

  1. records weather = SELECT * FROM weather;
  2. hash info = getInfo(zip);
  3. hash cached<1 day> info2 = getInfo(zip);
  4. int foo = 3;

Explanations:

  1. Execute SQL against the first database defined in the config block.
  2. Call function getInfo() from external include.
  3. Result of the function is cached for 1 day.
  4. Assign a number to the variable.

### Caching

The caching strategy depends on the deployment target, but memcache is
favored. The caching time specified is the maximum cache time, thus it's
possible that the cache expires before that. Commonly this happens when
maximum cache size limits have been reached.

To determine the cache key, the service name, service version, variable name
and the full command (including function parameters, complete SQL
statement, etc.) are used as qualifiers.

So in the above example the cached value would only be used if the value of
'zip' is the same as an already cached version.


### Literals

There are several kind of literals that can be used as values.

  - String: Starts and ends with double quotes.
  - Int: Any number.
  - Regexp: Starts and ends with a slash.
  - SQL: Starts with 'SELECT' and runs until the end of the current statement
    (usually the semicolon).


### Variable types

The following variable types are currently in use:

  - `string`: Corresponds to String literal.
  - `int`: Corresponds to Int literal.
  - `regexp`: Corresponds to Regexp literal.
  - `sql`: Corresponds to SQL literal.
  - `database`: A database connection. Can currently only be defined in the
                config block.
  - `service`: A REST web service which can be queried. TODO: How to query a
               service?
  - `dom`: An XML document, opened using a DOM. Can for example be used as a
           cheap and dirty database. TODO: How to query?
  - `array`: Holds a list of other objects.
  - `hash`: Bolds key/value pairs.
  - `records`: Basically an array of hashes. Stores the result of a database
               query.

Variable types mainly define how the variable will be output to the client as you can see below in the segment "Transformations".


### Function calls

Functions can be called with and without brackets:

  - validate x, /[0-9]+/;
  - validate(x, /[0-9]+/);
  - myfunction;
  - myfunction();

There are a few built-in functions, which are documented in the separate document "functions".


### Output blocks

    output.xml {
        # ....
    }

The output blocks can be defined for different types of output. The output
type ('xml' in the above example) is matched against subtype parts of the
'Accept' headers of the incoming request. So for example if the client sends
in 'Accept: text/xml', the subtype is 'xml'.

Additionally (and with higher precedence), the given output block also matches
for that file extension. So in the given example, any request ending in '.xml'
will be answered by that output block. This is a compromise to allow easy
communication and debugging of services.

Inside the output blocks only literals and variable references are allowed.
Those will be printed to the client. A variable references is a valid variable
name inside curly brackets. Example `{info2}`.

Some transformations will happen automatically based on the variable type and output type.

### Transformations

#### Transformations in XML

For some transformations the variable name is important. In that case it's
referenced as 'varname' in the output specification.

- `string`: Output as is.
- `int`: Output as is.
- `regexp`: Output as is.
- `sql`: Executed and output the same way as `records`.
- `database`: Can't be output. Will be ignored, but a warning is logged.
- `service`: Can't be output. Will be ignored, but a warning is logged.
- `dom`: Output as XML.
- `array`: Creates one `<varname>value</varname>` tag for each element.
           The value output is itself transformed based on its type.
- `hash`: Creates a `<varname>` tag, inside that creates pairs of
          `<key>value</key>`.
- `records`: As it's an array of hashes, Creates one `<varname>` tag for each
             record and inside that `<key>value</key>` tags.
