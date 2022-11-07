#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 03/11/2022


# Define a function for the play which takes 3 arguments :
# 1. total_funds = total money in hand the player is starting with
# 2. wager_amount = the betting amount each time the player plays
# 3. total_plays = the number of times the player bets on this gamedef play(total_funds, wager_amount, total_plays):

# Create empty lists for :
# 1.Play_number and
# 2.Funds available
# 3.Final Fund
Play_num = []
Funds = []  # Start with play number 1
play = 1
# If number of plays is less than the max number of plays we have set
while play < total_plays:
    # If we win
    if rolldice():
        # Add the money to our funds
        total_funds = total_funds + wager_amount
        # Append the play number
        Play_num.append(play)
        # Append the new fund amount
        Funds.append(total_funds)
    # If the house wins
    else:
        # Add the money to our funds
        total_funds = total_funds - wager_amount
        # Append the play number
        Play_num.append(play)
        # Append the new fund amount
        Funds.append(total_funds)

    # Increase the play number by 1
    play = play + 1
    # Line plot of funds over time
plt.plot(Play_num, Funds)
Final_funds.append(Funds[-1])
return (Final_funds)