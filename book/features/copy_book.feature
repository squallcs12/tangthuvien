Feature: Book App :: Copy book
    As user, I want to copy a book from live site to dev site
    So that I can read it on dev site

    Scenario: Copy book
        Given I was a logged-in user
        And there are categories exist in the system:
            | category   |
            | category-0 |
            | category-1 |
            | category-2 |
            | category-3 |
        When I visit book index page
        And I click on link "Copy book"
        Then I see the copy book form
        When I fill in book title "Copy book title"
        And I fill in book description
        And I select image for book cover
        And I select book author
        And I select book categories
        And I select languages
        And I fill in book source thread page "http://www.tangthuvien.vn/forum/showthread.php?t=50129"
        And I submit the publish form
        Then I see the copying was processed
        When the process is finished
        Then I see the whole book was copied
        When I visit book index page
        And I click on link "Copy book"
        Then I see the copy book form
        When I fill in book title "Copy book title 2"
        And I fill in book description
        And I select image for book cover
        And I select book author
        And I select book categories
        And I select languages
        And I fill in book source thread page "http://www.tangthuvien.vn/forum/showthread.php?t=50129"
        And I submit the publish form
        Then I see the text "The book is already copied to this site."
        When I visit the copied book
        Then I can sync the new posted chapter from main-site of this book
        When I sync the new posted chapter
        Then I see the copying was processed
        When the process is finished
        Then I see only new posted chapter was copied
        When I visit the redirect page for copied thread id
        Then I was redirected to the reading page of copied book
