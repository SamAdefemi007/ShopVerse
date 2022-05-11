Feature: Confirming that product catalog can be selected by the users

    Scenario: Selecting the appropriate category
     Given I navigate to the homepage
      When I select the shop now icon
      Then I should be able to see products in that category


    Scenario: Viewing product detail
     Given I navigate to the products page
      When I click the view product detail icon
      Then I should be able to see the details of the products


