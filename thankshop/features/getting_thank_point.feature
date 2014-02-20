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
		And I can not give any thank in a short time
		When I use all my thank points
		Then I can not thank anylonger

	Scenario: User buy thank points
		Given I was a logged-in user
		When I go to the buy thank points page
		Then I see a list of thank points packages
		When I buy a packages
		And I enter my paypal login information
		And I approve the buying process
		Then I receive an amount of thank points to spend