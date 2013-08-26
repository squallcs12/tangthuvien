Feature: Accounts App :: Social login
    As a member
    I want to be able to login with my social account
    
    Scenario: Facebook login
        Given I was a non-logged-in user
        When I login using my facebook account
        Then I was asked to update my account password
        And I update my account password
        When I login using my twitter account
        Then my account was associated with both facebook and twitter
        When I login using my google account
        Then my account was associated with facebook, twitter and google
        