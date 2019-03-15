

@echo off
pushd %~dp0

pip install sphinx recommonmark sphinx-markdown-tables

call sphinx-quickstart -q --project=%1 --author=%username% --batchfile --template=sphinxTemplate %1/docs
python SASParser.py %1

xcopy sphinxStatic %1\docs\_static\ /s/e/y

%1/docs/make.bat html


:end
popd

