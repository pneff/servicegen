task :default => 'servicegenLexer.py'

file 'parser/servicegenLexer.py' => 'parser/servicegen.g' do |t|
  sh "java org.antlr.Tool parser/servicegen.g"
end

task :clean do
  generated = ['parser/servicegenLexer.py', 'parser/servicegen.tokens',
               'parser/servicegen__.g', 'parser/servicegenParser.py']
  rm_f generated
end
