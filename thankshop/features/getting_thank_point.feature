Feature: As a user
	I can get thank points by login to the website daily
	And I can spend my thank points to thank other people

	Scenario: User get points by daily login
		Given I was a non-logged-in user
		When I log into the website for the first time in a day
		Then I receive a number of thank points
		When I re-login again
		Then I do not receive any thank points
		When I do not log into website in the next day
		Then I see my thank points was decreased

	Scenario: User give thank points to the poster
		Given I was a logged-in user
		When I thank a poster for a chapter
		Then I see my thank points was spent
		And poster thanked points was increased by half of those points
		When I thank a poster for a chapter
		Then I should see the popup notification "You can not thank in next"
		When I use all my thank points
		And I thank a poster for a chapter
		Then I should see the popup notification "You need at least"
		And I should see the popup notification "thank points to do thank"

	Scenario: User buy thank points
		Given I was a logged-in user
        And there is a list of thankpoint package:
        	| name      | price | points |
        	| package 1 | 100   | 100    |
        	| package 2 | 200   | 200    |
        	| package 3 | 300   | 300    |
        	| package 4 | 400   | 400    |
		When I go to the buy thank points page
		Then I see a list of thank points packages
		When I buy a package of "200" thank points
		Then I was redirected to paypal checkout
		When I enter my paypal login information
		And I approve the buying process
		Then I see the notification "200 thank points was added to your account"
		And I receive an amount of thank points to spend