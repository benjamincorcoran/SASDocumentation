# macro

## About
MacroName doctstring

## Libname(s)

| Name | Location |
| --- | --- |
| test | [thisisatest](thisisatest) |
| test2 | [thisisanothertest](thisisanothertest) |


## Include(s)

| Path |
| --- |
| [path-to-a-test](path-to-a-test) |


## Macro(s)
### macro1
#### About
MacroName doctstring


#### Argument(s)

| Name | Type | Default Value | About |
| --- | --- | --- | --- |
| argument1 | Required | Not set | argument 1 docstring |
| argument2 | Required | Not set | argument 2 docstring |


### macro3
#### About
MacroName doctstring



#### Argument(s)

| Name | Type | Default Value | About |
| --- | --- | --- | --- |
| argument1 | Required | Not set | argument 1 docstring |
| argument2 | Required | Not set | argument 2 docstring |


## Full code:

<details><summary>Show/Hide</summary>

~~~~sas


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

</details>

## Properties

| Meta | Property |
| --- | --- |
| **Author:** | |
| **Path:** | *W:\SASDocumentation\example\code\macro.sas* |
| **Last updated:** | *2019-03-14 10:33:11* |
