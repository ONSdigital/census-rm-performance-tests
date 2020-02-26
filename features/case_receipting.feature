Feature: Case Processor receipts cases in an acceptable time

  @case-receipt-test
  Scenario: Case Processor receipting test
    Given the sample file '10000_sample_file.csv' is loaded and '11988' messages are queued on 'case.rh.uac'
    And we gather a list of QIDs
    Then case processor receipts at an acceptable rate