# bitcoin arbitrage puzzle 

This code solves the puzzle to look for the optimal arbitrage pricing based on real time exchange rate data



The oringial post is found [here](http://priceonomics.com/jobs/puzzle/) 

# solution

- Download realtime data, and convert them into a 2x2 matrix for pricing lookup
- Create a Tree structure representing all the possible arbitrage paths that originates from a currency A to itself.
- A possible arbitrage path should not include any repeating currency except the oringinating currency
- The terminating node of the tree should be the same as the oringinating currency
- We don't want to use any repeating currency, other than the originating currency, because it will create a cycle within the tree/graph, and it will create an infinite path. 
- Also it makes sense that the cyclical reference should not be included becuase this same back reference path should have been considered as part of the other arbitrage path. If that path has a higher value, the path would have been chosen. Hence, there is no need to conside this back reference path 
- A stack is also used for ancestor look up so that no cyclic reference will be created

A full graph for the USD to USD arbitrage path is shown below

![Alt Text](https://s3-us-west-2.amazonaws.com/smarterme-assets/graph1.gif)

# more explanation

Why don't we want to consider a cyclical path?

Consider the following graph

![Alt Text](https://s3-us-west-2.amazonaws.com/smarterme-assets/graph2.gif)

If there is a path from EUR to BTC, it needs to go through the path BTC to JPY to EUR again so that it will get to the terminating node USD. And in this case, the only path that add to this cyclic path is the boost that EUR to BTC contributes. And if it indeed adds more, the EUR to BTC path on the left would have been considered. Hence, there is no need for this back reference path from EUR to BTC




