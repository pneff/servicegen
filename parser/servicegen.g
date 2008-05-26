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
    LITERAL_REGEXP;
    LITERAL_SQL;
    REQUEST;
    REQUEST_PATH;
    REQUEST_PATH_PARAM;
    STATEMENT_VALIDATE;
    STATEMENT_OUTPUT;
    FUNCTION_CALL;
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
    |   variableType IDENTIFIER '=' functionCall STATEMENT_END -> ^(VARIABLE variableType IDENTIFIER functionCall)
    ;
variableType
    :   IDENTIFIER -> ^(VARTYPE IDENTIFIER);
literal
    :   StringLiteral -> ^(LITERAL_STRING StringLiteral)
    |   RegexpLiteral -> ^(LITERAL_REGEXP RegexpLiteral)
    |   SqlLiteral -> ^(LITERAL_SQL SqlLiteral)
    ;
StringLiteral
    :  '"' ~'"'* '"';
RegexpLiteral
    :  '/' ~'/'* '/';
SqlLiteral
    :  'SELECT' ~(STATEMENT_END)*;
functionCall
    :  IDENTIFIER '(' functionArgs? ')' -> ^(FUNCTION_CALL functionArgs);
functionArgs
    :  functionArg (functionArgAdditional)*;
functionArgAdditional
    :   ',' functionArg -> ^(functionArg);
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
    :   validation | variableDefinition | outputDefinition;

/* Validation */
validation
    :   'validate' IDENTIFIER literal STATEMENT_END -> ^(STATEMENT_VALIDATE IDENTIFIER literal);

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
xmlTag
    :   '<' IDENTIFIER '/>'
    |   '<' IDENTIFIER '>' xmlTag* '</' IDENTIFIER '>';

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
