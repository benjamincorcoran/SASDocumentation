@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation
if "%1" == "" goto end

call sphinx-quickstart -q --project=%1 --author=%username% --batchfile --template=sphinxTemplate %1/docs
python SASParser.py %1
%1/docs/make.bat html
:end
popd
