
Feature: Receipting speed

  Scenario: Receipt all loaded cases
    Given the sample file has been loaded
    And the sample has been fully ingested into action scheduler database
    When a receipt is sent for every case loaded
    And a case updated event is emitted with receipted true for every case