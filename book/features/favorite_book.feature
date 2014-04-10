Feature: Book App :: Favorite book
    As user, I want to mark some favorite book
    So that I can easily to read it for later

    Scenario: Manage favorite book
        Given I was a logged-in user
        And there are "1" books exist in the system
        When I read a book
        Then I see the mark-as-favorite button
        When I click on mark-as-favorite button
        Then the book was mark as my favorite book
        When I visit favorite-books manager page
        Then I see the book was listed there
        When I read the last chapter of the book
        Then I see the book was marked as favorite
        When a new chapter was posted to the book
        Then I see that book marked as unread on favorite list
        When I remove the book from favorite list
        Then I see the book was not marked as favorite
