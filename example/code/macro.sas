
libname test 'thisisatest';
libname test2 "thisisanothertest";

%include 'path-to-a-test';

/*MacroName doctstring*/
%macro macro1(
    argument1 /*argument 1 docstring*/,
    argument2 /*argument 2 docstring*/
    );

    

%mend;
    

    
    %macro macro3(
    argument1 /*argument 1 docstring*/,
    argument2 /*argument 2 docstring*/
    );

    /*MacroName doctstring*/

%mend;
    