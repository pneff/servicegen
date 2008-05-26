require 'rake/clean'
# Cleanup
CLEAN.include('**/*.pyc')
CLEAN.include('parser/servicegenLexer.py')
CLEAN.include('parser/servicegenParser.py')
CLEAN.include('parser/servicegen.tokens')
CLEAN.include('parser/servicegen__.g')

task :default => 'test'

task :test => 'parser/servicegenLexer.py' do
  sh "python tests.py"
end

file 'parser/servicegenLexer.py' => 'parser/servicegen.g' do |t|
  sh "java org.antlr.Tool parser/servicegen.g"
end

