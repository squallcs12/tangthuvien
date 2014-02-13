Feature: Book App :: Upload book attachments
    As a converter / translator
    I want to upload the convert file to the book
    So that other user can download it

    Scenario: Normal user upload attachment
        Given I was a logged-in user
        When I read a book
        And I upload a attachment to the book
        Then I see the attachment listed when reading that book
        And the attachment can not be seen by other normal user
        When I reach the limited of uploading attachment
        Then I can not upload attachment anylonger

    Scenario: Super user upload attachment
        Given I was a logged-in super user
        When I read a book
        And I upload a attachment to the book
        Then I see the attachment listed when reading that book
        And the attachment can be seen by other normal user

    Scenario: Super user approve uploaded attachment
        Given I was a logged-in super user
        When I read a book has attachment uploaded by normal user
        And I approve that attachment
        Then the attachment can be seen by other normak user
        When I reach the limited of approving attachment
        Then I can not approve attachment anylonger

    Scenario: User download attachment
        Given I was a logged-in user
        When I read a book has approved attachment uploaded by normal user
        Then I can download the attachment
        After I reach the limited of downloading attachment
        Then I can not download attachment anylonger