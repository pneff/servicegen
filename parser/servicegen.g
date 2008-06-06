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
    LITERAL_DURATION;
    LITERAL_XML;
    REQUEST;
    REQUEST_NAME;
    REQUEST_PATH;
    REQUEST_BODY;
    REQUEST_OUTPUT;
    STATEMENT_VALIDATE;
    STATEMENT_OUTPUT;
    FUNCTION_CALL;
    FUNCTION_NAME_USER;
    FUNCTION_NAME_BUILTIN;
    EXTERNAL;
    CACHE;
    DURATION_SECONDS;
    DURATION_MINUTES;
    DURATION_HOURS;
    DURATION_DAYS;
    DURATION_MONTHS;
    DURATION_YEARS;
    DOC;
    DOC_FOR;
}

/* Main parts */
declaration
    :   service config? external* request*;
service :   docStatement* 'service' IDENTIFIER STATEMENT_END -> ^(SERVICE IDENTIFIER docStatement*);
config  :   'config' '{' (configVariableDefinition STATEMENT_END)* '}' -> ^(CONFIG configVariableDefinition*);
request :   docStatement* requestName? HTTP_METHOD requestPath '{' requestBody requestOutput '}'
            -> ^(REQUEST HTTP_METHOD requestPath requestBody requestOutput requestName? docStatement*);
external
    :   docStatement* 'external:' IDENTIFIER StringLiteral STATEMENT_END -> ^(EXTERNAL IDENTIFIER StringLiteral docStatement*);

/* Configuration */
configVariableDefinition
    :   docStatement* variableType IDENTIFIER -> ^(VARIABLE variableType IDENTIFIER docStatement*)
    |   variableDefinition
    ;
variableDefinition
    :   docStatement* variableType caching? IDENTIFIER '=' literal -> ^(VARIABLE variableType caching? IDENTIFIER literal docStatement*)
    |   docStatement* variableType caching? IDENTIFIER '=' functionCall -> ^(VARIABLE variableType caching? IDENTIFIER functionCall docStatement*)
    ;
variableType
    :   variableTypeIdentifier -> ^(VARTYPE variableTypeIdentifier);
variableTypeIdentifier
    :   'string' | 'int' | 'regexp' | 'duration'
    |   'database' | 'service' | 'dom' | 'array' | 'hash'
    |   'records'
    ;

/* Caching of variables */
caching
    : 'cached<' durationLiteral '>'  -> ^(CACHE durationLiteral);

/* Literals */
literal
    :   StringLiteral -> ^(LITERAL_STRING StringLiteral)
    |   IntLiteral -> ^(LITERAL_INT IntLiteral)
    |   RegexpLiteral -> ^(LITERAL_REGEXP RegexpLiteral)
    |   durationLiteral -> ^(LITERAL_DURATION durationLiteral)
    |   xmlLiteral -> ^(LITERAL_XML xmlLiteral)
    ;

StringLiteral
    :  '"' ( EscapeSequence | ~('\\'|'"') )* '"'
       { 
           str = self.getText()[1:-1]
           str = str.replace("\\b", "\b")
           str = str.replace("\\f", "\f")
           str = str.replace("\\n", "\n")
           str = str.replace("\\r", "\r")
           str = str.replace("\\t", "\t")
           str = str.replace("\\'", "'")
           str = str.replace("\\\"", "\"")
           str = str.replace("\\\\", "\\")
           self.setText(str)
       }
    ;

IntLiteral
    :  DIGIT+;
RegexpLiteral
    :  '/' ~'/'* '/';
durationLiteral
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
xmlLiteral
    : '<' ~'>'+ '>'
    | '</' ~'>'+ '>';

functionCall
    :  functionNameBuiltin functionArgs -> ^(FUNCTION_CALL ^(FUNCTION_NAME_BUILTIN functionNameBuiltin) functionArgs)
    |  functionNameBuiltin '(' functionArgs ')' -> ^(FUNCTION_CALL ^(FUNCTION_NAME_BUILTIN functionNameBuiltin) functionArgs)
    |  IDENTIFIER '(' functionArgs? ')' -> ^(FUNCTION_CALL ^(FUNCTION_NAME_USER IDENTIFIER) functionArgs)
    |  IDENTIFIER functionArgs?         -> ^(FUNCTION_CALL ^(FUNCTION_NAME_USER IDENTIFIER) functionArgs)
    ;
functionArgs
    :  functionArg (','! functionArg)*;
functionArg
    :   literal
    |   IDENTIFIER  -> ^(VARREF IDENTIFIER);
functionNameBuiltin
    :   'validate'
    |   'log.trace' | 'log.debug' | 'log.info' | 'log.warn'
    |   'log.error' | 'log.fatal'
    |   'etag' | 'expires'
    ;

/* Request */
HTTP_METHOD
    :   'OPTIONS' | 'GET' | 'HEAD' | 'POST' | 'PUT'
    |   'DELETE' | 'TRACE' | 'CONNECT';

requestPath
    : StringLiteral -> ^(REQUEST_PATH StringLiteral);
requestName
    : IDENTIFIER ':' -> ^(REQUEST_NAME IDENTIFIER);
requestBody
    :   statement* -> ^(REQUEST_BODY statement*);
requestOutput
    :   outputDefinition* -> ^(REQUEST_OUTPUT outputDefinition*);
statement
    : functionCall STATEMENT_END!
    | variableDefinition STATEMENT_END!
    ;

/* Output of a service */
outputDefinition
    :   docStatement* 'output.' outputType caching? '{' outputStatement* '}'
                    -> ^(STATEMENT_OUTPUT outputType caching? outputStatement* docStatement*);
outputType
    :   'xml' | 'csv';
outputStatement
    :   literal
    |   variableReference;
variableReference
    :   '{' IDENTIFIER '}' -> ^(VARREF IDENTIFIER);

/* Documentation */
docStatement
    :   '@' docName StringLiteral -> ^(DOC docName StringLiteral)
    |   '@param' IDENTIFIER StringLiteral -> ^(DOC_FOR IDENTIFIER StringLiteral)
    ;
docName
    :   'doc' | 'author' | 'version';

/* Primitives */
IDENTIFIER
    :   (ALPHANUM | '_')+;

fragment
ALPHANUM:   LETTER | DIGIT;
fragment
LETTER  :   'a'..'z' | 'A'..'Z';
fragment
DIGIT   :   '0'..'9';

fragment
EscapeSequence
    :   '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\');

STATEMENT_END
    :   ';';

/* Ignore */
WS  :  (' '|'\r'|'\t'|'\u000C'|'\n') {$channel=HIDDEN;};
LINE_COMMENT
    : '#' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;};
COMMENT
    :   '/*' ( options {greedy=false;} : . )* '*/' {$channel=HIDDEN;}
    ;
