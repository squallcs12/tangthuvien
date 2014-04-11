Feature: Book App :: Cloned book notification
    As a book from main site was cloned to new site
    User should receive notification when reading that book

    Background:
        Given thread with id "10" was cloned to current site book id "11"
        And thread with id "11" was cloned to current site book id "12"

    Scenario: Cloned book notification
        When I read thread "10" on main site
        Then I should see a dialog show up
        And I should see on dialog "This story was cloned to new site."
        And I should see option on dialog "Keep reading on current site."
        And I should see option on dialog "Go to the new site."
        And I should see button on dialog "Go"
        And I should see checkbox on dialog "Remember my choice for all cloned books."

    Scenario: Move user to cloned book
        When I read thread "10" on main site
        And I click label on dialog "Go to the new site."
        And I click button on dialog "Go"
        Then I should be reading book id "11"

    Scenario: Save user selection
        When I read thread "10" on main site
        And I click label on dialog "Go to the new site."
        And I click label on dialog "Remember my choice for all cloned books."
        And I click button on dialog "Go"
        And I read thread "11" on main site
        Then I should be reading book id "12"

    Scenario: Save user selection 2
        When I read thread "10" on main site
        And I click label on dialog "Keep reading on current site."
        And I click label on dialog "Remember my choice for all cloned books."
        And I click button on dialog "Go"
        Then I should not see any dialog
        When I read thread "11" on main site
        Then I should not see any dialog