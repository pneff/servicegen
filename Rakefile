task :default => 'servicegenLexer.py'

file 'servicegenLexer.py' => 'servicegen.g' do |t|
  sh "java org.antlr.Tool servicegen.g"
end

task :clean do
  generated = ['servicegenLexer.py', 'servicegen.tokens',
               'servicegen__.g', 'servicegenParser.py']
  rm_f generated
end
