# Overview

model the card game <b>Thirty-One</b> and simulate hands to identify scenarios where one should knock on the initial hand

# TL;DR

If you want to survive your knock <b>60%</b> of the time, knock if you have the following minimum scores. Note that the minimum score required depends on the number of players in the game and your position following the dealer (where 0 = first player to act after the dealer):

| # of players | position after dealer | minimum score to knock | probability of surviving |
|:------------:|:---------------------:|:----------------------:|:------------------------:|
|       2      |           0           |           18           |            66%           |
|       2      |           1           |           20           |            71%           |
|       3      |           0           |           14           |            65%           |
|       3      |           1           |           15           |            63%           |
|       3      |           2           |           17           |            64%           |
|       4      |           0           |           13           |            68%           |
|       4      |           1           |           13           |            63%           |
|       4      |           2           |           14           |            65%           |
|       4      |           3           |           15           |            62%           |
|       5      |           0           |           11           |            62%           |
|       5      |           1           |           12           |            62%           |
|       5      |           2           |           13           |            72%           |
|       5      |           3           |           13           |            63%           |
|       5      |           4           |           15           |            76%           |
|       6      |           0           |           11           |            67%           |
|       6      |           1           |           11           |            64%           |
|       6      |           2           |           12           |            67%           |
|       6      |           3           |           12           |            64%           |
|       6      |           4           |           13           |            72%           |
|       6      |           5           |           13           |            62%           |

# Basic Strategy

<b>Knock early.</b> The minimum score required to have a greater probability of not losing compared to losing depends on the number of players in the game and your position after the dealer:
* As the number of players increase, the minimum score required decreases because the likelihood of a another player having a lower score increases.
* The further one sits from the dealer, the more opportunities other players have to increase their hands' scores.

# Methodology

For a given number of players, n, deal n hands. Simulate this deal of the cards where the first player knocks. Repeat for every other player in the game for a total of n games of this deal of the cards. For example, a 3-player game will be simulated 3 times: once where the first player knocks, the second where the second player knocks, and a third where the third player knocks.

Repeat that process for 2-, 3-, 4-, 5-, and 6-player games. Repeat for 10,000 deals for each n-player set of games for a total of 200,000 games simulated where 200,000 = 2 x 10,000 + 3 x 10,000 + ... + 6 x 10,000.

# Why?

* implement basic Monte Carlo simulation
* model a card game (incl. cards, stacks of cards, hands, games, etc.)

# Resources

* Thirty-One Rules<br>
https://en.wikipedia.org/wiki/Thirty-one_(card_game)#Object