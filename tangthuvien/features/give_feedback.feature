Feature: Tangthuvien :: Give feedback
    As a user
    I want to leave some feedback to admin

    Scenario: User give feedback
        Given I was a visitor
        When I visit the homepage
        And I click on link "Feedback"
        Then I should see a modal show up
        When I fillin on modal field "Subject" text "Feedback subject"
        And I fillin on modal field "Content" text "Feedback content"
        And I click button on modal "Submit feedback"
        Then I should see the popup notification "Your feedback is sent. We will work on that as soon as possible."