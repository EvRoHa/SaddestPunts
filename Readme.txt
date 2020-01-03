This is based on the work of Jon Bois. See this link to the timestamp of his video for an explanation: https://www.youtube.com/watch?v=F9H9LwGmc-0&time=20m

The basic formula is Surrender_Index = Field_Position * First_Down_Distance * Score_of_Game * Clock

Each of these components are calculated as follows:

Field_Position is a piecewise discrete function composed of a linear section and two exponential sections. If x in the line of scrimmage (indexed as 0-100) then FP(x) is:
FP(x) = 1 if x <= 40, 1.1^(x-40) if 40 < x <= 50 else 2.59*1.2^(x-50)

First_Down_Distance is a simple categorical function. If x is the distance to go on 4th down then FDD(x) is:
FDD(x) = 1 if x<=1, 0.8 if 2<=x<=3, 0.6 if 4 <= x <= 6, 0.4 if 7 <= x <= 9, 0.2 if 10 <= x

Score_of_Game is a simple categorical function as well. The score differential (offense score - defense score) is categorized as winning, tied, trailing by one score, or trailing by more than one score. If x is the score differential (offense score - defense score) then SOG(x) is:
SOG(x) = 1 if 0 < x, 2 if x == 0, 4 if -8 <= x < 0, 3 if x <-8

Finally, the time remaining in the game is used. If the team is tied or trailing, and the game is in the second half, we apply a modifier. Assuming those conditions are met, the clock modifier is given by:

C(x) = ((x*0.001)^3) + 1

where x is the number of seconds elapsed since halftime. If those conditions aren't met, C(x)=1.