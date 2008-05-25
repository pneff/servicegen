grammar servicegen;

/* Main parts */
declaration
    :   service config? request*;
service :   'service' identifier ';';
config  :   'config' '{' variableDefinition* '}';
request :   HTTP_METHOD path '{' requestBody '}';

/* Service body */
variableDefinition
    :   variableType identifier ';';
variableType
    :   'database';

requestBody
    :   requestRule*;
requestRule
    :   validation | variableDefinition | outputDefinition;

/* Validation */
validation
    :   'validate' identifier validationRule ';';
validationRule
    :   regexpValidationRule;
regexpValidationRule
    :   '/' regexp '/';
regexp  :   ~('/');

/* Output of a service */
outputDefinition
    :   'output.' outputType '{' outputStatement* '}';
outputType
    :   'xml' | 'csv';
outputStatement
    :   variableReference | xmlTag;
variableReference
    :   '{' identifier '}';
xmlTag
    :   '<' identifier '/>'
    |   '<' identifier '>' xmlTag* '</' identifier '>';

/* Path as taken from RFC 2396 */
path    :   '/' path_segments;
path_segments
    :   path_segment ('/' path_segment)*;
path_segment
    :   path_char* (';' path_param)*;
path_param
    :   path_char*;
path_char
    :   ALPHANUM | path_escaped
    |   ':' | '@' | '&' | '='
    |   '+' | '$' | ',' | '-'
    |   '_' | '.' | '!' | '~'
    |   '*' | '\'' | '(' | ')';
path_escaped
    :   '%' HEX HEX;

/* Primitives */
identifier
    :   ALPHANUM+;
HEX :   DIGIT | 'a'..'f' | 'A'..'F';
ALPHANUM:   LETTER | DIGIT;
LETTER  :   'a'..'z' | 'A'..'Z';
DIGIT   :   '0'..'9';
HTTP_METHOD
    :   'GET' | 'POST' | 'PUT';
