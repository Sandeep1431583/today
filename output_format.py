from pydantic import BaseModel, Field
from enum import Enum
from typing import List


class SubtypeEnum(str,Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"

class TestCaseTypeEnum(str, Enum):
    FUNCTIONAL = "FUNCTIONAL"
    REGRESSION = "REGRESSION"
    EDGE = "EDGE"

class PassFailCriterion(BaseModel):
    pass_: str = Field(
        alias='Pass',
        description="Clear criteria that define what constitutes a successful test case execution."
    )

    fail: str = Field(
        alias = 'Fail',
        description= "Clear criteria that define what constitutes a failed test case execution."
    )



class TestCase(BaseModel):
    test_case_id: str = Field(
        alias="TestCaseID",
        description="A unique identifier for the test case, combining type, subtype, and a sequential number (e.g., TC_001_Functional_Positive)."
    )
    subtype: SubtypeEnum = Field(
        alias = "Subtype",
        description="Specifies whether the test case is Positive or Negative."
    )
    test_case_type: TestCaseTypeEnum = Field(
        alias="TestCaseType",
        description= "Specifies the type of test case (e.g., Functional, Regression, Edge)."
    )
    test_case_description: str = Field(
        alias="TestCaseDescription",
        description="A concise description of the objective or purpose of the test case."
    )
    expected_output: str = Field(
        alias = "ExpectedOutput",
        description="The expected FHIR resource and system behavior after executing the test case."
    )
    test_steps: List[str] = Field(
        alias = "TestSteps",
        description="A list of detailed steps to execute the test case in sequence. Each step describes an action or input required for the test."
    )
    pass_fail_criteria: PassFailCriterion = Field(
        alias = 'PassFailCriteria',
        description="An object that defines the criteria used to determine whether a test case passes or fails."
    )

    class Config:
        use_enum_values = True


class MissingTestCaseReason(BaseModel):
    attribute: str = Field(
        alias='Attribute',
        description= 'The name of the attribute or element for which a test case is missing.'
    )
    reason: str = Field(
        alias = 'Reason',
        description= 'A detailed explanation of why the test case is missing or could not be created.'
    )

class BreakingTestCaseReason(BaseModel):
    original_test_caseid: str = Field(
        description='The unique identifier of the original test case that is breaking.',
        alias='OriginalTestCaseID'
    )

    reason_for_breakage: List[str] = Field(
        alias='ReasonForBreakage',
        description='A list of reasons explaining why the test case is breaking, including mapping or attribute-level issues. Each reason provides specific details about the breakage.'
    )


class TestCaseTypeBreakdownStat(BaseModel):
    functional: int = Field(
        alias='Functional',
        description='The number of functional test cases created.'
    )

    regression: int = Field(
        alias='Regression',
        description="The number of regression test cases created."
    )

    edge: int = Field(
        alias='Edge',
        description='The number of edge test cases created.'
    )


class SubtypeBreakdownStat(BaseModel):
    positive: int = Field(
        alias='POSITIVE',
        description='The number of positive test cases created.'
    )

    negative: int = Field(
        alias = 'NEGATIVE',
        description='The number of negative test cases created.'
    )

class AttributeTestCaseDetail(BaseModel):
    attribute: str = Field(
        alias='Attribute',
        description='Name of the attribute'
    )

    number_of_test_case: int = Field(
        alias = 'NumberOfTestCases',
        description='The number of test cases created for this specific attribute.'
    )

class StatisticalSummary(BaseModel):
    mapping_rows: int   = Field(
        alias="MappingRows",
        description="The total number of rows in the mapping CSV file"
    )

    unique_attributes: int = Field(
        alias='UniqueAttributes',
        description="The number of unique attributes listed in the layout attribute column."
    )

    number_of_test_cases_created: int = Field(
        alias = 'NumberOfTestCasesCreated',
        description='The total number of test cases created based on the mapping.'
    )

    number_of_test_cases_modified: int = Field(
        alias = 'NumberOfTestCasesModified',
        description='The total number of test cases that were updated or modified.'
    )

    test_case_type_breakdown: TestCaseTypeBreakdownStat = Field(
        alias='TestCaseTypeBreakdown',
        description="The total number of test cases per each category divided based on TestCaseType"
    )

    subtype_breakdown: SubtypeBreakdownStat = Field(
        alias = 'SubtypeBreakdown',
        description='The total number of test cases per each category divided based on Subtype'
    )

    attribute_test_case_details: List[AttributeTestCaseDetail] = Field(
        alias = 'AttributeTestCaseDetails',
        description='The total number of test cases per each attribute'
    )


class ExpectedOutputFormat(BaseModel):
    testcases: List[TestCase] = Field(
        alias= "TestCases",
        description="An exhaustive list of test cases, each test case is defined by TestCase object"
    )

    missing_test_cases: List[MissingTestCaseReason] = Field(
        alias="MissingTestCases",
        description="A list of missing test cases and the reasons for missing"
    )

    breaking_test_cases: List[BreakingTestCaseReason] = Field(
        alias = "BreakingTestCases",
        description='A list of breaking test cases'
    )

    statistical_summary: StatisticalSummary = Field(
        alias = 'StatisticalSummary',
        description="Statistical Summary of the whole test cases."
    )