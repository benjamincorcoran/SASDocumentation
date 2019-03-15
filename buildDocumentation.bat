
@echo off
pushd %~dp0



call sphinx-quickstart -q --project=%1 --author=%username% --batchfile --template=sphinxTemplate %1/docs
python SASParser.py %1
%1/docs/make.bat html
:end
popd
