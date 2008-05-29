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
    DURATION_SECONDS;
    DURATION_MINUTES;
    DURATION_HOURS;
    DURATION_DAYS;
    DURATION_MONTHS;
    DURATION_YEARS;
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
    :   variableType caching? IDENTIFIER '=' literal -> ^(VARIABLE variableType caching? IDENTIFIER literal)
    |   variableType caching? IDENTIFIER '=' functionCall -> ^(VARIABLE variableType caching? IDENTIFIER functionCall)
    ;
variableType
    :   IDENTIFIER -> ^(VARTYPE IDENTIFIER);

/* Caching of variables */
caching
    : 'cached<' duration '>'  -> ^(CACHE duration);
duration
    : IntLiteral 'second'  -> ^(DURATION_SECONDS IntLiteral)
    | IntLiteral 'seconds' -> ^(DURATION_SECONDS IntLiteral)
    | IntLiteral 'minute'  -> ^(DURATION_MINUTES IntLiteral)
    | IntLiteral 'minutes' -> ^(DURATION_MINUTES IntLiteral)
    | IntLiteral 'hour'    -> ^(DURATION_HOURS IntLiteral)
    | IntLiteral 'hours'   -> ^(DURATION_HOURS IntLiteral)
    | IntLiteral 'day'     -> ^(DURATION_DAYS IntLiteral)
    | IntLiteral 'days'    -> ^(DURATION_DAYS IntLiteral)
    | IntLiteral 'month'   -> ^(DURATION_MONTHS IntLiteral)
    | IntLiteral 'months'  -> ^(DURATION_MONTHS IntLiteral)
    | IntLiteral 'year'    -> ^(DURATION_YEARS IntLiteral)
    | IntLiteral 'years'   -> ^(DURATION_YEARS IntLiteral)
    ;

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
