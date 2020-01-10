Feature: RM produces all initial contact print files within a time window

  Scenario: Sample load through to initial contact print file production
    Given the sample file has been loaded
    And the sample has been fully ingested into action scheduler database
    When all initial contact action rules are scheduled for now
    Then all the initial contact print files are produced on the SFTP
    And they all have the correct line count
    And they are produced within the configured time limit

#  Scenario: 3.5 Million Sample load through to initial contact print file production
#    Given the sample file has been loaded from the bucket
#    And the sample has been fully ingested into action scheduler database
#    When all initial contact action rules are scheduled for now
#    Then all the initial contact print files are produced on the SFTP
#    And they all have the correct line count
#    And they are produced within the time limit 100 minutes
