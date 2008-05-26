grammar servicegen;

options {
    language=Python;
    output=AST;
}

tokens {
    SERVICE;
    CONFIG;
    VARIABLE;
    VARTYPE;
    LITERAL_STRING;
    REQUEST;
    REQUEST_PATH;
}

/* Main parts */
declaration
    :   service config? request*;
service :   'service' IDENTIFIER STATEMENT_END -> ^(SERVICE IDENTIFIER);
config  :   'config' '{' variableDefinition* '}' -> ^(CONFIG variableDefinition*);
request :   HTTP_METHOD requestPath '{' requestBody '}' -> ^(REQUEST HTTP_METHOD requestPath requestBody);

/* Configuration */
variableDefinition
    :   variableType IDENTIFIER STATEMENT_END -> ^(VARIABLE variableType IDENTIFIER)
    |   variableType IDENTIFIER '=' literal STATEMENT_END -> ^(VARIABLE variableType IDENTIFIER literal) 
    ;
variableType
    :   IDENTIFIER -> ^(VARTYPE IDENTIFIER);
literal
    :   StringLiteral -> ^(LITERAL_STRING StringLiteral)
    ;
StringLiteral
    :  '"' ~'"'* '"'
    ;

/* Request */
requestPath: path -> ^(REQUEST_PATH path);

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

HTTP_METHOD
    :   'GET' | 'POST' | 'PUT';

/* Primitives */
IDENTIFIER
    :   ALPHANUM+;

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

/* Ignore */
WS  :  (' '|'\r'|'\t'|'\u000C'|'\n') {$channel=HIDDEN;};
LINE_COMMENT
    : '#' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;};
COMMENT
    :   '/*' ( options {greedy=false;} : . )* '*/' {$channel=HIDDEN;}
    ;
