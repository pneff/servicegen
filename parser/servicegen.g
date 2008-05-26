grammar servicegen;

options {
    language=Python;
    output=AST;
}

/* Main parts */
declaration
    :   service config? request*;
service :   'service' IDENTIFIER STATEMENT_END;
config  :   'config' '{' variableDefinition* '}';
request :   HTTP_METHOD path '{' requestBody '}';

/* Service body */
variableDefinition
    :   variableType IDENTIFIER STATEMENT_END;
variableType
    :   'database';

requestBody
    :   requestRule*;
requestRule
    :   validation | variableDefinition | outputDefinition;

/* Validation */
validation
    :   'validate' IDENTIFIER validationRule STATEMENT_END;
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
    :   '{' IDENTIFIER '}';
xmlTag
    :   '<' IDENTIFIER '/>'
    |   '<' IDENTIFIER '>' xmlTag* '</' IDENTIFIER '>';

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
IDENTIFIER
    :   ALPHANUM+;

HTTP_METHOD
    :   'GET' | 'POST' | 'PUT';

fragment
HEX :   DIGIT | 'a'..'f' | 'A'..'F';
fragment
ALPHANUM:   LETTER | DIGIT;
fragment
LETTER  :   'a'..'z' | 'A'..'Z';
fragment
DIGIT   :   '0'..'9';

STATEMENT_END
    :   ';';

WS  :  (' '|'\r'|'\t'|'\u000C'|'\n') {$channel=HIDDEN;};
