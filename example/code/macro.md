# macro

## Libname(s):
| Name | Location |
| --- | --- |
| test | [thisisatest](thisisatest) |
| test2 | [thisisanothertest](thisisanothertest) |


## Include(s):
| Path |
| --- |
| [path-to-a-test](path-to-a-test) |


## Macros(s):
### macro1
*No doc string*

#### Argument(s):

| Name | Type | Default Value | About |
| --- | --- | --- | --- |
| argument1 | Required | None | argument 1 docstring |
| argument2 | Required | None | argument 2 docstring |


### macro3
*MacroName doctstring

*

#### Argument(s):

| Name | Type | Default Value | About |
| --- | --- | --- | --- |
| argument1 | Required | None | argument 1 docstring |
| argument2 | Required | None | argument 2 docstring |


## Full code:
~~~~.sas

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
    
~~~~