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
    VARREF;
    LITERAL_STRING;
    LITERAL_INT;
    LITERAL_REGEXP;
    LITERAL_SQL;
    REQUEST;
    REQUEST_PATH;
    REQUEST_PATH_PARAM;
    STATEMENT_VALIDATE;
    STATEMENT_OUTPUT;
    FUNCTION_CALL;
    EXTERNAL;
    CACHE;
    DURATION_DAYS;
}

/* Main parts */
declaration
    :   service config? external* request*;
service :   'service' IDENTIFIER STATEMENT_END -> ^(SERVICE IDENTIFIER);
config  :   'config' '{' (configVariableDefinition STATEMENT_END)* '}' -> ^(CONFIG configVariableDefinition*);
request :   HTTP_METHOD requestPath '{' requestBody '}' -> ^(REQUEST HTTP_METHOD requestPath requestBody);
external
    :   'external:' IDENTIFIER StringLiteral STATEMENT_END -> ^(EXTERNAL IDENTIFIER StringLiteral);

/* Configuration */
configVariableDefinition
    :   variableType IDENTIFIER -> ^(VARIABLE variableType IDENTIFIER)
    |   variableDefinition
    ;
variableDefinition
    :   variableType variableCache? IDENTIFIER '=' literal -> ^(VARIABLE variableType variableCache? IDENTIFIER literal)
    |   variableType variableCache? IDENTIFIER '=' functionCall -> ^(VARIABLE variableType variableCache? IDENTIFIER functionCall)
    ;
variableType
    :   IDENTIFIER -> ^(VARTYPE IDENTIFIER);

/* Caching of variables */
variableCache
    : 'cached<' duration '>'  -> ^(CACHE duration);
duration
    : durationDay;
durationDay
    : IntLiteral 'day'  -> ^(DURATION_DAYS IntLiteral);

/* Literals */
literal
    :   StringLiteral -> ^(LITERAL_STRING StringLiteral)
    |   IntLiteral -> ^(LITERAL_INT IntLiteral)
    |   RegexpLiteral -> ^(LITERAL_REGEXP RegexpLiteral)
    |   SqlLiteral -> ^(LITERAL_SQL SqlLiteral)
    ;
StringLiteral
    :  '"' ~'"'* '"';
IntLiteral
    :  DIGIT+;
RegexpLiteral
    :  '/' ~'/'* '/';
SqlLiteral
    :  'SELECT' ~(STATEMENT_END)*;
functionCall
    :  IDENTIFIER '(' functionArgs? ')' -> ^(FUNCTION_CALL functionArgs)
    |  IDENTIFIER functionArgs          -> ^(FUNCTION_CALL functionArgs)
    ;
functionArgs
    :  functionArg (','! functionArg)*;
functionArg
    :   literal
    |   IDENTIFIER  -> ^(VARREF IDENTIFIER);

/* Request */
HTTP_METHOD
    :   'GET' | 'POST' | 'PUT';

requestPath
    : StringLiteral -> ^(REQUEST_PATH StringLiteral);

requestBody
    :   requestRule*;
requestRule
    : functionCall STATEMENT_END!
    | variableDefinition STATEMENT_END!
    | outputDefinition
    ;

/* Output of a service */
outputDefinition
    :   'output.' outputType '{' outputStatement* '}' -> ^(STATEMENT_OUTPUT outputType outputStatement*);
outputType
    :   'xml' | 'csv';
outputStatement
    :   literal
    |   variableReference;
variableReference
    :   '{' IDENTIFIER '}' -> ^(VARREF IDENTIFIER);

/* Primitives */
IDENTIFIER
    :   (ALPHANUM | '_')+;

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
