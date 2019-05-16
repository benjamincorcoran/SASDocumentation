# Unit tests for the SASBaseObject Class

import pytest
from ..SASBaseObject import SASBaseObject

testSASBaseObject = SASBaseObject()

# Split Data Objects

splitDataObjectsTestPlan = {
    'singleDataItem':('dataItem',[['','dataItem']]),
    'macroDataItem':('&dataItem.',[['','&dataItem.']]),
    'partialMacroDataItem':('&data.Item',[['','&data.Item']]),
    'parenthDataItem':('dataItem()',[['','dataItem()']]),
    'parenthConditionDataItem':('dataItem(where=() keep=test test)',[['','dataItem(where=() keep=test test)']]),
    'parenthMacroDataItem':('&data.Item(where=())',[['','&data.Item(where=())']]),
   
    'singleLibDataItem':('library.dataItem',[['library','dataItem']]),
    'macroLibDataItem':('library.&dataItem.',[['library','&dataItem.']]),
    'partialLibMacroDataItem':('library.&data.Item',[['library','&data.Item']]),
    'parenthLibDataItem':('library.dataItem()',[['library','dataItem()']]),
    'parenthConditionLibDataItem':('library.dataItem(where=() keep=test test)',[['library','dataItem(where=() keep=test test)']]),
    'parenthLibMacroDataItem':('library.&data.Item(where=())',[['library','&data.Item(where=())']]),

    'macroLibSingleDataItem':('&library..dataItem',[['&library.','dataItem']]),
    'macroLibMacroDataItem':('&library..&dataItem.',[['&library.','&dataItem.']]),
    'macroLibPartialMacroDataItem':('&library..&data.Item',[['&library.','&data.Item']]),
    'parenthMacroLibDataItem':('&library..dataItem()',[['&library.','dataItem()']]),
    'parenthConditionMacroLibDataItem':('&library..dataItem(where=() keep=test test)',[['&library.','dataItem(where=() keep=test test)']]),
    'parenthMacroLibPartialMacroDataItem':('&library..&data.Item(where=())',[['&library.','&data.Item(where=())']]),

    'partialMacroLibDataItem':('li&bra.ry.dataItem',[['li&bra.ry','dataItem']]),
    'partialMacroLibMacroDataItem':('li&bra.ry.&dataItem.',[['li&bra.ry','&dataItem.']]),
    'partialMacroLibPartialMacroDataItem':('li&bra.ry.&data.Item',[['li&bra.ry','&data.Item']]),
    'parenthPartialMacroLibDataItem':('li&bra.ry.dataItem()',[['li&bra.ry','dataItem()']]),
    'parenthConditionPartialMacroLibDataItem':('li&bra.ry.dataItem(where=() keep=test test)',[['li&bra.ry','dataItem(where=() keep=test test)']]),
    'parenthPartialMacroLibPartialMacroDataItem':('li&bra.ry.&data.Item(where=())',[['li&bra.ry','&data.Item(where=())']])
}


baseTestIds = []
baseScenarios = []
for id, scenario in splitDataObjectsTestPlan.items():
    baseTestIds.append(id)
    baseScenarios.append(scenario)

@pytest.mark.parametrize("str,expected",baseScenarios,ids=baseTestIds)
def test_SASBaseObjectSplitSingleDataObject(str,expected):
    assert testSASBaseObject.splitDataObjects(str) == expected

dynamicSplitDataObjectsTestPlan = {}

for firstId, firstTest in splitDataObjectsTestPlan.items():
    for secondId, secondTest in splitDataObjectsTestPlan.items():
        dynamicSplitDataObjectsTestPlan['{} & {}'.format(firstId,secondId)] = ('{} {}'.format(firstTest[0],secondTest[0]),[firstTest[1][0],secondTest[1][0]])

dynamicTestIds = []
dynamicScenarios = []
for id, scenario in dynamicSplitDataObjectsTestPlan.items():
    dynamicTestIds.append(id)
    dynamicScenarios.append(scenario)

@pytest.mark.parametrize("str,expected",dynamicScenarios,ids=dynamicTestIds)
def test_SASBaseObjectSplitMultipleDataObject(str,expected):
    assert testSASBaseObject.splitDataObjects(str) == expected

# Validate Split Data Objects

# validateSplitDataObjectsTestPlan = {
#     'space'
# }

