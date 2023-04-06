# App name: group_by_name
Author: Xuhang Fan  
GitHub: https://github.com/Fanisting

## Description
this app shows how to let participants to select their partner in a 2-agent group.

## Pages:
1. Name: get each player's own name
2. Partner: get their expected partner's name
3. Wait: wait for all groups, prepare for group match
4. NotMatch: test whether some one is double-selected, if yes, the match should restart
5. MatchPage: group match here
6. Results: show the matching results

## Note:
1. All of the nams are restricted, and should be found in the '_rooms/econ101.txt'
2. Designed for PLAYERS_PER_GROUP = 2, modify the code to make it more flexible
3. Now the group will be changed in every round, disable several pages to make the only for the first round 
4. According to the existing 'econ101.txt', the available names for test are: Alice, Bob, Claire, and Dana
5. Have fun!
