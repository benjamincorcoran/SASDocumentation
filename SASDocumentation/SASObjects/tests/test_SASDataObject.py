# Unit tests for the SASDataObject Class

import pytest
from ..SASDataObject import SASDataObject


baseDataObjectsTestPlan = {
    'test':[dict(library='test',dataset='test',condition=''),dict(library='test',dataset='test',condition='')]
}

testIds = []
testScenarios = []

for id, scenario in baseDataObjectsTestPlan.items():
    testIds.append(id)
    testScenarios.append(scenario)

@pytest.mark.parametrize("input,expected",testScenarios,ids=testIds)
def test_SASDataObject(input,expected):
    testDataObject = SASDataObject(input['library'],input['dataset'],input['condition'])
    assert testDataObject.library == expected['library']
    assert testDataObject.dataset == expected['dataset']
    assert testDataObject.condition == expected['condition']