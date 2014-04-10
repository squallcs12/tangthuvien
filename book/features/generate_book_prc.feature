Feature: Book App :: Generate book prc

    Scenario: Create book prc
        Given there are "1" books exist in the system
        And some chapter was posted
        And after period of time
        Then a prc file was generated for this book
        And the prc file was listed in the list of attachments


    Scenario: Manually generate prc file
        Given I was a logged-in user
        And I have permission "can_generate_prc"
        And there are "1" books exist in the system
        When I read a book
        And I press generate prc button
        Then I see the generate prc process was shown
        When the process is done
        Then a prc file was generated for this book
        And the prc file was listed in the list of attachments