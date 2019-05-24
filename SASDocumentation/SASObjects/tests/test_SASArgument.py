# Unit tests for the SASArguement Class

import pytest
from ..SASArgument import SASArgument

scenarios = [
    ('A',dict(testId='Argument',name='A',type='Required',defaultValue='Not set',docString='No description provided')),
    ('A=',dict(testId='OptionalArgument',name='A',type='Optional',defaultValue='Not set',docString='No description provided')),
    ('A=B',dict(testId='DefaultArgument',name='A',type='Optional',defaultValue='B',docString='No description provided')),
    ('A/*This is A\'s docstring.*/',dict(testId='ArgumentWDocstring',name='A',type='Required',defaultValue='Not set',docString='This is A\'s docstring.')),
    ('A=/*This is A\'s docstring.*/',dict(testId='OptionalArgumentWDocstring',name='A',type='Optional',defaultValue='Not set',docString='This is A\'s docstring.')),
    ('A=B/*This is A\'s docstring.*/',dict(testId='DefaultArgumentWDocstring',name='A',type='Optional',defaultValue='B',docString='This is A\'s docstring.'))
]  

testIds = []
for scenario in scenarios:
    testIds.append(scenario[1]['testId'])

@pytest.mark.parametrize("rawStr,expected",scenarios,ids=testIds)
def test_SASArguementParseName(rawStr,expected):
    testArguement = SASArgument(rawStr)
    assert testArguement.name == expected['name']

@pytest.mark.parametrize("rawStr,expected",scenarios,ids=testIds)
def test_SASArguementParseType(rawStr,expected):
    testArguement = SASArgument(rawStr)
    assert testArguement.type == expected['type']

@pytest.mark.parametrize("rawStr,expected",scenarios,ids=testIds)
def test_SASArguementParseDefaultValue(rawStr,expected):
    testArguement = SASArgument(rawStr)
    assert testArguement.defaultValue == expected['defaultValue']

@pytest.mark.parametrize("rawStr,expected",scenarios,ids=testIds)
def test_SASArguementParseDocString(rawStr,expected):
    testArguement = SASArgument(rawStr)
    assert testArguement.docString == expected['docString']




