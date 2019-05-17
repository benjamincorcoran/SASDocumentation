# Unit tests for the SASBaseObject Class

import pytest
from ..SASBaseObject import SASBaseObject

testSASBaseObject = SASBaseObject()

# Split Data Objects

baseDataObjectsTestPlan = {
    'singleDataItem':('dataItem',[['','dataItem']]),
    'macroDataItem':('&dataItem.',[['','&dataItem.']]),
    'partialMacroDataItem':('&data.Item',[['','&data.Item']]),
    'parenthDataItem':('dataItem()',[['','dataItem()']]),
    'parenthConditionDataItem':('dataItem(where=() keep=test test)',[['','dataItem(where=() keep=test test)']]),
    'parenthMacroDataItem':('&data.Item(where=())',[['','&data.Item(where=())']]),   
}

splitDataObjectsTestPlan = {}

for id, test in baseDataObjectsTestPlan.items():
    splitDataObjectsTestPlan[id]=test
    splitDataObjectsTestPlan['{}Lib'.format(id)]=('library.{}'.format(test[0]),[['library',test[1][0][1]]])
    splitDataObjectsTestPlan['{}MacroLib'.format(id)]=('&library..{}'.format(test[0]),[['&library.',test[1][0][1]]])
    splitDataObjectsTestPlan['{}MacroPartialLib'.format(id)]=('li&bra.ry.{}'.format(test[0]),[['li&bra.ry',test[1][0][1]]])


singleTestIds = []
singleScenarios = []
for id, scenario in splitDataObjectsTestPlan.items():
    singleTestIds.append(id)
    singleScenarios.append(scenario)

@pytest.mark.parametrize("str,expected",singleScenarios,ids=singleTestIds)
def test_SASBaseObjectSplitSingleDataObject(str,expected):
    assert testSASBaseObject.splitDataObjects(str) == expected

multipleSplitDataObjectsTestPlan = {}

for firstId, firstTest in splitDataObjectsTestPlan.items():
    for secondId, secondTest in splitDataObjectsTestPlan.items():
        multipleSplitDataObjectsTestPlan['{} & {}'.format(firstId,secondId)] = ('{} {}'.format(firstTest[0],secondTest[0]),[firstTest[1][0],secondTest[1][0]])

multipleTestIds = []
multipleScenarios = []
for id, scenario in multipleSplitDataObjectsTestPlan.items():
    multipleTestIds.append(id)
    multipleScenarios.append(scenario)

@pytest.mark.parametrize("str,expected",multipleScenarios,ids=multipleTestIds)
def test_SASBaseObjectSplitMultipleDataObject(str,expected):
    assert testSASBaseObject.splitDataObjects(str) == expected

# Validate Split Data Objects

# validateSplitDataObjectsTestPlan = {
#     'space'
# }

