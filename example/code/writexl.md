# writexl

## About:

Excel points

has to be a network drive
Has to be named range - can't be a cell reference
unable to expand if data below
Needs to be closed
Can't have blank headings, limited to 256 characters


## Include(s):
| Path |
| --- |
| [L:\home\StatData\Platform administration\ServerStartupMods\writexl.sas](L:\home\StatData\Platform%20administration\ServerStartupMods\writexl.sas) |


## Macro(s):
### writexl
#### About:

Excel points

has to be a network drive
Has to be named range - can't be a cell reference
unable to expand if data below
Needs to be closed
Can't have blank headings, limited to 256 characters






#### Help:


 Overview
 --------

 This macro produces excel outputs from SAS datasets.
 It can output direct, or use template files.
 A range (i.e. the macro variable range) must have a value.
 This macro uses the PCFILES libname option in order to output to excel. 
 To troubleshoot, googling common issues with this libname option may be useful.

 Parameters
 ----------

 dataset - dataset name to be exported
 template= (optional) - file reference of template file if template is being used
 outfile= - file reference of output file
 range= - This is CASE SENSITIVE, and MUST BE SPECIFIED. named range to export to in template file, or name of worksheet if exporting to workbook where range does not exist.
 var= (optional) - variable to be exported. If not specified, all variables will be exported
 start_row= (optional) - start row for outputting. If APPEND is specified it will add onto the end of the data in the workbook
 end_row= (optional) - to specify the end row if start row is specified
 dbLabel= (optional) - specify YES to use variable labels for column headers
 help = (optional) - specify YES to see help. Code will not execute to produce outputs if help documentation is called

 Example
 ----------

 Below example uses a template to populate two worksheets based on a template:
 %nrstr(%%)writexl(dataset=highcost,
         template =\\hefce\ASDPROJECTS\ASDTeams\DAMIT\Infrastructure\MacroHelpExamples\Toutput1819.xlsx
         outfile = \\folderReference\fileName.xlsx,
         range = Highcost,
         var =ukprn-instname-mission-homef-healthadj-m_d_adj-fteadj%nrstr(%&)yy.-fte%nrstr(%&)yy.-highcost%nrstr(%&)yy.-ughealthfte1718-hc%nrstr(%&)yy._health)
 
 
 %nrstr(%%)writexl(dataset=tas,
         outfile = \\folderReference\fileName.xlsx,
         range = TAS,
         var =ukprn-instname-mission-pgts_ta%nrstr(%&)yy.-accl_ta%nrstr(%&)yy.-int_ta%nrstr(%&)yy.-eras_ta%nrstr(%&)yy.-lond_ta%nrstr(%&)yy.-sci_ta%nrstr(%&)yy.-
         is_ta%nrstr(%&)yy.-ccpay_ta%nrstr(%&)yy.-sagp_ta%nrstr(%&)yy.-nhs_ta%nrstr(%&)yy.-HEALTH_TA%nrstr(%&)yy.-otarget%nrstr(%&)yy.-int_ta%nrstr(%&)yy._health-accl_ta%nrstr(%&)yy._health-lond_ta%nrstr(%&)yy._health)
 
 Below example outputs some datasets to the same workbook with different worksheet names
 %nrstr(%%)writexl(dataset=hesa15.campus, range=Campus15, outfile=\\folderRef\test.xlsx)
 %nrstr(%%)writexl(dataset=hesa16.campus, range=Campus16, outfile=\\folderRef\test.xlsx)

#### Argument(s):

| Name | Type | Default Value | About |
| --- | --- | --- | --- |
| dataset | Optional | Not set | Not set |
| template | Optional | NULL | Not set |
| outfile | Optional | Not set | Not set |
| range | Optional |   | CASE SENSITIVE!! |
| var | Optional | *  |  /*seperate with -  |
| start_row | Optional | NULL  | APPEND means add on to end |
| end_row | Optional | NULL  |  if you wish to replace contents of rows specify the end row |
| dbLabel | Optional | No  | specify yes for labels as headers |
| help | Optional | NO | Not set |


## Full code:
~~~~.sas
﻿

/*******************************
Excel points

has to be a network drive
Has to be named range - can't be a cell reference
unable to expand if data below
Needs to be closed
Can't have blank headings, limited to 256 characters
******************************/



%macro writexl(dataset=,template=NULL, outfile=, range= /*CASE SENSITIVE!!*/,var=* /*seperate with - */, start_row=NULL /*APPEND means add on to end*/ ,
end_row=NULL /* if you wish to replace contents of rows specify the end row*/, dbLabel=No /*specify yes for labels as headers*/
,help=NO) /des ='Exports a datset to an excel file and can use a template';
%changeMLog(OFF);
%if %upcase(&help)= YES %then
		%do;
		%put;
			%put;
			%put Overview;
			%put --------;
			%put;
%put This macro produces excel outputs from SAS datasets.;
%put It can output direct, or use template files.;
%put A range (i.e. the macro variable range) must have a value.;
%put This macro uses the PCFILES libname option in order to output to excel. ;
%put To troubleshoot, googling common issues with this libname option may be useful.;
			%put;
			%put     Parameters;
			%put     ----------;
			%put;
			

%put dataset - dataset name to be exported;
%put template= (optional) - file reference of template file if template is being used;
%put outfile= - file reference of output file;
%put range= - This is CASE SENSITIVE, and MUST BE SPECIFIED. named range to export to in template file, or name of worksheet if exporting to workbook where range does not exist.;
%put var= (optional) - variable to be exported. If not specified, all variables will be exported; 
 %put start_row= (optional) - start row for outputting. If APPEND is specified it will add onto the end of the data in the workbook; 
%put end_row= (optional) - to specify the end row if start row is specified; 
%put dbLabel= (optional) - specify YES to use variable labels for column headers;
%put help = (optional) - specify YES to see help. Code will not execute to produce outputs if help documentation is called;

					%put;
			%put     Example;
			%put     ----------;
			%put;
			%put  Below example uses a template to populate two worksheets based on a template:;
%put %nrstr(%%)writexl(dataset=highcost,;
%put         template =\\hefce\ASDPROJECTS\ASDTeams\DAMIT\Infrastructure\MacroHelpExamples\Toutput1819.xlsx;
%put         outfile = \\folderReference\fileName.xlsx,;
%put         range = Highcost,;
%put         var =ukprn-instname-mission-homef-healthadj-m_d_adj-fteadj%nrstr(%&)yy.-fte%nrstr(%&)yy.-highcost%nrstr(%&)yy.-ughealthfte1718-hc%nrstr(%&)yy._health);;
%put ;
%put ;
%put %nrstr(%%)writexl(dataset=tas,;
%put         outfile = \\folderReference\fileName.xlsx,;
%put         range = TAS,;
%put         var =ukprn-instname-mission-pgts_ta%nrstr(%&)yy.-accl_ta%nrstr(%&)yy.-int_ta%nrstr(%&)yy.-eras_ta%nrstr(%&)yy.-lond_ta%nrstr(%&)yy.-sci_ta%nrstr(%&)yy.-;
%put         is_ta%nrstr(%&)yy.-ccpay_ta%nrstr(%&)yy.-sagp_ta%nrstr(%&)yy.-nhs_ta%nrstr(%&)yy.-HEALTH_TA%nrstr(%&)yy.-otarget%nrstr(%&)yy.-int_ta%nrstr(%&)yy._health-accl_ta%nrstr(%&)yy._health-lond_ta%nrstr(%&)yy._health);;
%put ;
%put Below example outputs some datasets to the same workbook with different worksheet names;
%put %nrstr(%%)writexl(dataset=hesa15.campus, range=Campus15, outfile=\\folderRef\test.xlsx);
%put %nrstr(%%)writexl(dataset=hesa16.campus, range=Campus16, outfile=\\folderRef\test.xlsx);
			%put;;
			%put;
		%end;
	%else %do;

%Let colon=:;
%if not %sysfunc(exist(&dataset)) %then %do;
	%put ERROR&colon. Dataset does not exist!;
	%abort cancel;
	%end;
  %if &end_row ne NULL and %sysfunc(anyDigit(&end_row.)) eq 0 %then %do;
   %put ERROR&colon. End_row must be either numeric or not included;
   %abort cancel;
%end;


	/*link to excel file*/
%if "&template." = "NULL" and &start_row. = NULL %then %do;
	
	*pc file server writes new files as .xlsb, so working around to force .xlsx or .xls because that is what people expect;
	%Let xlExtension = Not found;
	%If %eval(%index(%upcase(&outFile.), .XLSX) > 0) %then %do; %Let xlExtension = .xlsx; %end;
	%Else %if %eval(%index(%upcase(&outFile.), .XLSB) > 0) %then %do; %Let xlExtension = .xlsb; %end;
	%Else %if %eval(%index(%upcase(&outFile.), .XLSM) > 0) %then %do; %Let xlExtension = .xlsm; %end;
	%Else %if (%index(%upcase(&outFile.), .XLS) > 0) %then %do; %Let xlExtension = .xls; %end;

	%If "&xlExtension." = "Not found" %then %do;
		%Put ERROR&colon. Could not determine excel extension.;
		%Abort Cancel;
	%End;
	%Else %Put NOTE&colon. Excel extension is &xlExtension.;;
	
	%If (&xlExtension. = .xls or &xlExtension. = .xlsx or &xlExtension. = .xlsm) 
		and %sysFunc(fileExist(&outFile.)) = 0 %then %do;
		%put NOTE&colon. Using blank template.;
	 
		sysTask command "copy ""\\hefce-sas\data\home\StatData\Platform administration\ServerStartupMods\AutoCompile\writexl&xlExtension."" ""&outfile"" /y" wait status=copyBlankTemplate;
		%If &copyBlankTemplate. ne 0 %then %do;
			%Put ERROR&colon. Return code for copyBlankTemplate=&copyBlankTemplate.;
			%Abort cancel;
		%End;
	%End;
%end;
%else %if "&template" ne "NULL" %then %do;
/*x copy "&template." "&outfile." /y;*/ *<< X command should not be used in new world, SAS does not wait - CG 25/02/16;
	sysTask command "copy ""&template."" ""&outfile"" /y" wait status=copyTemplate;
	%If &copyTemplate. ne 0 %then %do;
		%Put ERROR&colon. Return code for copyTemplate=&copyTemplate.;
		%Abort cancel;
	%End;
%end;

/*  libname _xltmp excel "&outfile." DBSASLABEL=COMPAT; Libname excel on the blink on SAS3 cg: 10/11/15*/
	
	*moving to pc file server for better functionality and to allow install of office on servers;
/*	libname _xltmp odbc required="Driver={Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)};dbq=&outfile.;ReadOnly=0;";*/

	libname _xltmp pcFiles path="&outFile.";


  /*order variables correctly*/
  proc sql;
    create table _xltmpIN as 
      select  %sysfunc(tranwrd(&var.,-,%str(,))) from &dataset;
  quit;

  proc contents data= _xltmpIN  noprint out= _xltmpINPC;
  run;


  /*IF output range exists then...*/
    %if %sysfunc(exist(_xltmp.&range.)) %then %do;
  /*identify column names*/
  proc contents data= _xltmp.&range. noprint out= _xltmpPC;
  run;



  /*place labels and column names into macro variables*/
  data _null_;
    set _xltmpPC end=eod;;
    retain num_col;
    call symput("VARNAMXL"||strip(varnum),Name);
    if Label='F'||strip(varnum) or label='' then 
      call symput("VARLABXL"||strip(varnum),"''");    
    else  
      call symput("VARLABXL"||strip(varnum),Label);

    if varnum > num_col then
      num_col=varnum;

    if eod then
      call symput("NUMCOLXL",num_col);
  run;

  data _null_;
    set _xltmpINPC end=eod;
    retain num_col;
    call symput("VARNAMIN"||strip(varnum),Name);
    if Label='' then 
      call symput("VARLABINXL"||strip(varnum),"''");    
    else  
      call symput("VARLABINXL"||strip(varnum),Label);

    if varnum > num_col then
      num_col=varnum;

    if eod then
      call symput("NUMCOLIN",num_col);
  run;

  /*ensure same number of both*/
  %if &numcolin ne &numcolxl %then
    %do;
      %put ERROR&colon. number of columns do not match;
	libname _xltmp clear;
      %abort cancel;
    %end;
	/*********************************************************/

  proc datasets NODETAILS NOLIST;
    modify _xltmpIN;
    rename
    %do
      i= 1 %to &numcolin.;
        &&VARNAMIN&i=%sysfunc(strip(&&VARNAMIN&i..))__1
      %end;
    ;
    rename

      %do
      i= 1 %to &numcolin.;
        %sysfunc(strip(&&VARNAMIN&i..))__1=&&VARNAMXL&i
      %end;
    ;
    label

      %do i= 1 %to &numcolin.;
        %if "&&VARLABXL&i" = "''" or "&&VARLABXL&i" = ""  %then %do ; %put VARLABINXL&i=&&VARLABINXL&i;
          %if "&&VARLABINXL&i" = "''" or "&&VARLABINXL&i" = "" %then %do ; %put VARNAMIN&i=&&VARNAMIN&i; &&VARNAMXL&i="%sysfunc(strip(&&VARNAMIN&i))" %end;
          %else %do;  %put VARLABINXL&i =&&VARLABINXL&i ; &&VARNAMXL&i="%sysfunc(strip(&&VARLABINXL&i))" %end;
        %end;
        %else %do ; &&VARNAMXL&i="%sysfunc(strip(&&VARLABXL&i))" %end;
      %end;
    ;
  run;

  quit;

  *determining the correct SAS reference for the range if named the same thing as the sheet;
  *______________________________________________________________;
	%If %sysFunc(exist(_xlTmp."&range.$"n)) %then %do;
		%Put NOTE&Colon. Potential $ range name detected;

		Proc Contents Data=_xlTmp.&range. Out=_nonDollarCols NoPrint;
		Quit;
		
		Proc Contents Data=_xlTmp."&range.$"n Out=_dollarCols NoPrint;
		Quit;

		Proc SQL noPrint;
			Select count(*)
			Into :nNonDollarCols
			From _nonDollarCols
			;

			Select count(*)
			Into :nDollarCols
			From _dollarCols
			;

			Select count(*)
			Into :nNonDollarRows
			From _xlTmp.&range.
			;

			Select count(*)
			Into :nDollarRows
			From _xlTmp."&range.$"n
			;
		Quit;
		
		%Let nonDollarCells = %eval(&nNonDollarCols. * &nNonDollarRows.);
		%Let dollarCells = %eval(&nDollarCols. * &nDollarRows.);

		%Put non$ = %sysFunc(strip(&nNonDollarCols.)) * %sysFunc(strip(&nNonDollarRows.)) = &nonDollarCells.;
		%Put $ = %sysFunc(strip(&nDollarCols.)) * %sysFunc(strip(&nDollarRows.)) = &dollarCells;

		%If %eval(&nonDollarCells. > &dollarCells.) %then %do;
			%Put NOTE&Colon. $ name has fewer cells than non$, choosing &range.$ as range name;
			%Let range = "&range."n;
		%End;
		%Else %if %eval(&dollarCells. > &nonDollarCells.) %then %do;
			%Put NOTE&Colon. non$ name has fewer cells than $, choosing &range. as range name;
			%Let range = &range.;
		%End;
		%Else %do;
			%Put WARNING&Colon. Range reference could not be determined, SAS determined the range and sheet have the same number of cells;
		%End;
	%End;
  *______________________________________________________________;

  /*if keeping original data */
  %if &start_row ne NULL %then
    %do;
  %if &end_row = NULL %then %let end_row=&start_row;
      data _xltmp1;
        set _xltmp.&range.;
      run;

      /*appending*/
      %if %sysfunc(anyDigit(&end_row.)) eq 0 %then %do;
      %if %upcase(&start_row) = APPEND %then
        %do;

          data _xltmpIN;
            set _xltmp1  _xltmpIN;
            ;
          run;

        %end;
        %end;

      /*inserting at random point*/
      %else
        %do;

          data _xltmpIN;
            set _xltmp1(obs=%eval(&start_row. - 1)) _xltmpIN _xltmp1(firstobs=&end_row);
          run;

          proc datasets NODETAILS NOLIST;
            delete _xltmp1;
          run;

          quit;

        %end;
    %end;

  proc datasets library= _xltmp NODETAILS NOLIST;
  	delete &range.;
  run;

  quit;
%end;

*write the data out;
data _xltmp.&range. (dbLabel=&dbLabel.);
	set _xltmpin ;
run;

/*proc SQL;*/
/*	create table _xlTmp."&range.$"n as*/
/*	Select * from _xlTmpIn*/
/*	;*/
/*Quit;*/
/**/
/*  proc datasets NODETAILS NOLIST;*/
/*    delete _xltmpin _xltmpPC _xltmpPCIN;*/
/*  run;*/

/*  quit;*/
libname _xltmp clear;
%end;
%changeMLog(ON);
%mend;
/*%include 'L:\home\StatData\Platform administration\ServerStartupMods\writexl.sas';*/
/*%writexl(dataset=t3 , /*dataset to be outputted*/ */
/*          outfile=N:\user\breezan\temp\Log2.xlsx,/*name of workbook. Has to exist!!*/*/
/*        range=BOOM , /*CASE SENSITIVE!! Range to output data to. Must included column headings*/ */
/*        var= * /*separate with - leave out if not needed*/, */
/*        row=NULL/*leave out or set as null if you wish to overwrite data. if you want to append to existing data, use APPEND.*/
/*                  If you wish to insert between rows, use the number of rows you wish to isnert at*/);*/
;

~~~~
| Meta | Property |
| --- | --- |
| **Author:** | |
| **Path:** | *W:\SASDocumentation\example\code\writexl.sas* |
| **Last updated:** | *2019-03-14 10:33:11* |
