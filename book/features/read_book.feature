Feature: Book App :: Book reading page

    Scenario: Read book as guest
        Given I was a non-logged-in user
        When I visit book index page
        And I click on a book
        Then I see the book rating box
        And I see the book rating result
        And I see rating book button
        And I can not rate for the book
        And I see the "Start reading" button
        When I click on the "Start reading" button
        Then I see the first chapter
        When I go to next chapter
        Then I see the second chapter
        When I choose a random chapter from selection box
        Then I see a random chapter
        When I go to last chapter
        Then I see the last chapter
        And I see chapter thank count
        And I can not thank the poster

    Scenario: Read book as user
        Given I was a logged-in user
        When I visit book index page
        And I click on a book
        Then I see the book rating box
        And I see the book rating result
        And I see rating book button
        And I can rate for the book
        And I see the book rating count is 0
        When I rate 5 star for the book
        Then I see the book rating is 5.00
        And I see the book rating count is 1
        And I can not rate for the book anylonger
        And I see the button "Start reading"
        When I click on "Start reading"
        And I choose a random chapter from selection box
        And I visit book index page
        And I click on the previous book
        And I click on "Continue reading"
        And I see the last random chapter
        And I see chapter thank count
        And I can thank the poster for this chapter
        When I thank the poster for this chapter
        Then I see the chapter thank was increased
        And I can not thank the poster anymore
        When I reload the page
        Then I still see thank number not change after increasing
        And I can not thank the poster
        And I see the book rating is 5.00
        And I see the book rating count is 1
        And I can not rate for the book anylonger

    Scenario: Configurate reading section
        Given I was a logged-in user
        When I read a book
        And I change the reading section font face and font size
        Then I see the configuration of readind section is applied
        When I go to next chapter
        Then I see the configuration of readind section is applied
        When I read another book
        Then I see the configuration of readind section is applied

    Scenario: Select language while reading
        Given I was a logged-in user
        And a book exists in "4" languages
        And that book contain chapters:
            | number | title                | language   |
            | 1      | chapter 1 language 0 | language-0 |
            | 1      | chapter 1 language 1 | language-1 |
            | 1      | chapter 1 language 2 | language-2 |
            | 1      | chapter 1 language 3 | language-3 |
            | 2      | chapter 2 language 0 | language-0 |
            | 2      | chapter 2 language 1 | language-1 |
            | 2      | chapter 2 language 2 | language-2 |
            | 3      | chapter 3 language 0 | language-0 |
            | 3      | chapter 4 language 1 | language-1 |
            | 4      | chapter 1 language 0 | language-0 |
        When I visit this book introduction page
        Then I see a languages prefer contain "language-0,language-1,language-2,language-3"
        When I choose "language-2" as prefer language
        And I click on "Start reading"
        Then I see chapter title is "chapter 1 language 2"
        When I go to chapter "2"
        Then I see chapter title is "chapter 2 language 2"
        And I see a list of languages contain "language-0,language-1,language-2"
        When I choose language "language-1"
        Then I see chapter title is "chapter 2 language 1"
        When I go to chapter "1"
        Then I see chapter title is "chapter 1 language 1"
        When I go to chapter "4"
        Then I see chapter title is "chapter 4 language 0"
        When I go to chapter "3"
        Then I see chapter title is "chapter 3 language 0"
        When I setting my language prefer to "language-1,language-0,language-2,language-3"
        And I visit this book introduction page
        And I click on "Continue reading"
        Then I see chapter title is "chapter 3 language 1"
        When I go to chapter "1"
        Then I see chapter title is "chapter 1 language 2"