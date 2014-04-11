Feature: Book App :: Post new chapter

    Scenario: User post new chapter
        Given I was a logged-in user
        And there are "1" books exist in the system
        When I am reading a book
        And I click on "Add Chapter"
        Then I see the post new chapter form
        When I fill title for this chapter "New chapter 1"
        And I fill the next chapter number for this chapter
        And I enter chapter content "New chapter content 1"
        And I select language for this chapter
        And I click on "Post chapter"
        Then I see the notification "New chapter was posted successfully."
        And I see new chapter was posted
        And new chapter title is "New chapter 1"
        And new chapter content is "New chapter content 1"
        And other people can read this chapter
        And my posted chapter was increased

    Scenario: User edit chapter
        Given I was a logged-in user
        And there are "1" books exist in the system
        When I am reading a book
        And I edit that chapter
        Then I see that chapter was edited
