/*Model SAS Code*/

/*Date: 19/03/2019*/
/*Author: Benjamin Corcoran*/

/*This piece of code demonstrates the model layout for a .SAS file. This layout*/
/*can be easily read by SASAutoDocs to generate documentation about the entire */
/*script. If a whole project follows this layout, documentation can be generated*/
/*describing an entire work area.*/

%include "path-to-include";

libname LIB1 "path-to-library-one";
libname LIB2 "path-to-library-two";

%macro exampleMacro(arg1 /*This describes the argument*/,
					arg2= /*This describes the keyword argument*/,
					arg3=True /*This describes the keyword argument with a default value*/,
					help=False /*This describes the optional help argument*/)
					/des='This is an optional, short, descriptive sentence about the macro';
	
	/*This is the macros documentation string (DocString). This details the purpose*/
	/*of the macro. This should also include information on how to use the macro */
	/*and any considerations that should be made when using the macro. */

	%if &help ^= False %then %do;
		%put This is an optional structure which will print a series of ;
		%put strings into the log. These will detail how to use the macro;
		%put what arguments the macro takes, and the purpose of the macro;
		%put ;
		%put This will allow users to receive help directly from SASEG;
		%put ;
		%put These help statements will be parsed into documentation however;
		%put the DocString is considered complete documentation for the macro.;
	%end;

	data LIB1.dataset0;
	run;

%mend exampleMacro;


/*This describes the purpose of dataset1*/

data LIB1.dataset1;
	set LIB1.dataset0;
run;

/*This describes the purpose of dataset2 and dataset3*/

data LIB2.dataset2(where=(1=2)) LIB2.dataset3(where=(2=1));
	set LIB1.dataset1;
run;

/*This describes the purpose of the following procedure*/

proc sort data=LIB2.dataset3 out=LIB2.dataset4;
	by A B C;
run;

proc transpose data=LIB2.dataset4 out=dataset5;
	by a b c;
run;

proc summary data=dataset5 nway;
	class A B C;
	output out=dataset6;
run;

data dataset7;
	merge dataset6 LIB1.dataset2;
run;
