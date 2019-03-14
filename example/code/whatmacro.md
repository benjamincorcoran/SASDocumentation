# whatmacro

## Libname(s):
| Name | Location |
| --- | --- |
| MacTemp | &workDir./MacroTemp |


## Include(s):
| Path |
| --- |
| &fname. |


## Macros(s):
### WhatMacro
*Macro to identify other macros with a name similar to macroName
	turn off logging and notes
	*

#### Argument(s):

| Name | Type | Default Value | About |
| --- | --- | --- | --- | --- |
| macroName | Required | None | No docstring provided for argument |
| Catalog | Optional | sasmac1 | No docstring provided for argument |
| HELP | Optional | NO | No docstring provided for argument |


## Full code:
~~~~
%macro WhatMacro(macroName,Catalog=sasmac1, HELP=NO) /des='Macro to search for other macros. Default assumes that the SAS macro catalog is work.sasmac1' ;
	/*Macro to identify other macros with a name similar to macroName*/
	/*turn off logging and notes*/
	%changeMLog(OFF);
	options nonotes;

	/*set local variables*/
	%local i j macroExist fname;

	/*help blurb*/
	%if %upcase(&help)= YES %then
		%do;
			%put;
			%put;
			%put Overview;
			%put --------;
			%put This macro searches the macro catalog and sasautos for macros whose name matches any part of the search;
			%put It will retunrn any macros with a similar name, and a description (if they have one);
			%put By default it searches for the SASMAC1 catalog. if it is erroring / not working, please do a proc contents on your work library.;
			%put Then, make sure that the catalog=option is set correctly.;
			%put;
			%put     Parameters;
			%put     ----------;
			%put;
			%put macroName - name of amcro to be searched for;
			%put;
			%put Catalog - name of SAS macro catalog. Default is sasmac1;
			%put If this code errors, this is probably the reason.;
			%put run a proc contents on the work library to identify the macro catalog if required;
			%put;
			%put help - put YES to call help;
			%put;
			%put     Example;
			%put     ----------;
			%put;
			%put %nrstr(%%)WhatMacro(macroname,Catalog=sasMac1,HELP=NO)%str(%;);
				%put ;
				%put ;
		%end;
	%else
		%do;
			/*assign a working library*/
			%let workDir = %sysfunc(getoption(work));
			options DLCREATEDIR=1;
			libname MacTemp "&workDir./MacroTemp";

			/*get list of sasauto macro locations*/
			data MacTemp.sasAutoLocs;
				string="&sasautos.";
				string1=substr(string,2,length(string)-2);
				i=1;

				do until (scan(string1,i,",","q")="");
					location=dequote(strip(scan(string1,i,",","q")));
					i=i+1;
					output;
				end;
			run;

			/*loop through list, and find possible matches*/
			proc sql;
				reset noprint;
				select count(*) into :numLocations from mactemp.sasAutoLocs;
			quit;

			%do i =1 %to &numLocations;

				data _null_;
					set mactemp.sasAutoLocs (firstobs= &i. obs=&i.);
					call symput ("LocNAME",strip(location));
				run;

				/*find any .sas files in a sas autocall location*/
				filename f1 pipe "dir ""&locName."" /b /s";

				data mactemp.filelist;
					infile f1;
					input;
					string=_infile_;

					if upcase(substr(string,length(string)-3)) = '.SAS';
				run;

				proc sql;
					reset noprint;
					select count(*) into :numfiles from mactemp.filelist;
				quit;

				/*loop through .sas files to look for likely macros with correct names*/
				%do j= 1 %to &numfiles;
					%let macroExist=0;

					data _null_;
						set mactemp.filelist (firstobs= &j. obs=&j.);
						call symput ("FNAME",strip(string));
					run;

					data _null_;
						infile "&fname.";
						input;
						string= _infile_;

						if find(upcase(string),"MACRO") > 0 and find(upcase(string),upcase("&macroName.")) > 0 then
							call symput ("macroExist","1");
					run;

					/*if .sas file gives a likely candidate, load it in so it is referenced in the SAS catalog*/
					%if  &macroExist %then
						%do;
							/*let users know macro is being loaded*/
							options notes;
							%put NOTE: loading &fname.;
							options nonotes;

							%include "&fname.";
				%end;
			%end;

			%let i= %eval(&i.+1);
		%end;

	/*interogate catalog for likely suspects, and output with description*/
	PROC CATALOG catalog=work.&catalog;
		Contents out=MacTemp.t1;
	Run;

	data _null_;
		set MacTemp.t1 (where =(Name ? upcase("&MacroName.")));
		options notes;

		if _n_=1 then
			put "NOTE: The following macros exist:";

		if desc='' then
			put Name=;
		else put name= desc=;

		if name ne '' then
			call symput("MacroExists","1");
	run;

	/*clear the libname, and turn logging back on*/
	libname MacTemp clear;
	;
		%end;

	%changeMLog(ON);
	options notes;
%mend;
~~~~