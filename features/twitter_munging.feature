Feature: Add entries to page
    As a PyCon attendee
    In order to let people contact me via Twitter
    I want to enter my Twitter ID in various ways and have it work

    Scenario Outline: Handling various forms of Twitter ID
        Given I am at the PyCon AU meetup page
        When I enter "Benno Rice" as my name
        And I select "DJ 1320" as my flight
        And I select "Friday" as my arrival day
        And I enter "<twitter_id>" as my Twitter ID
        And I click "Add me!"
        Then my flight should appear in the flights table
        And my name should appear next to my flight
        And my name should link to my Twitter profile

        Examples:
            | twitter_id                   |
            | jeamland                     |
            | @jeamland                    |
            | http://twitter.com/jeamland  |
            | https://twitter.com/jeamland |
