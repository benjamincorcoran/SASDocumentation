@echo off

pushd %~dp0

if [%2] == [] (
	set out=%1\docs
) else (
    set out=%2\docs
)


call pip install sphinx recommonmark sphinx-markdown-tables matplotlib numpy networkx

call sphinx-quickstart -q --project=%1 --author=%username% --batchfile --template=sphinxTemplate %out%
python SASParser.py %1 %out%

xcopy sphinxStatic %out%\_static\ /s/e/y

%out%\make.bat html


:end
popd

