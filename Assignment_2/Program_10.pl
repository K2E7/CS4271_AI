store(best_smoothies, [alan,john,mary], 
    [ smoothie(berry, [orange, blueberry, strawberry], 2),  
      smoothie(tropical, [orange, banana, mango, guava], 3),  
      smoothie(blue, [banana, blueberry], 3) ]). 

store(all_smoothies, [keith,mary], 
    [ smoothie(pinacolada, [orange, pineapple, coconut], 2),  
      smoothie(green, [orange, banana, kiwi], 5), 
      smoothie(purple, [orange, blueberry, strawberry], 2),  
      smoothie(smooth, [orange, banana, mango],1) ]). 

store(smoothies_galore, [heath,john,michelle], 
    [ smoothie(combo1, [strawberry, orange, banana], 2),  
      smoothie(combo2, [banana, orange], 5), 
      smoothie(combo3, [orange, peach, banana], 2), 
      smoothie(combo4, [guava, mango, papaya, orange],1),  
      smoothie(combo5, [grapefruit, banana, pear],1) ]). 

%% Sub-Problem-a %%
more_than_four(X) :-
    store(X, _, Smoothies),
    length(Smoothies, N),
    N >= 4.

%% Sub-Problem-b %%
exists(X) :-
    store(_, _, Smoothies),
    member(smoothie(X, _, _), Smoothies).

%% Sub-Problem-c %%
% Helper predicate to calculate the ratio
calculate_ratio(Store, Ratio) :-
    store(Store, Employees, Smoothies),
    length(Employees, NumEmployees),
    length(Smoothies, NumSmoothies),
    NumSmoothies > 0, % Avoid division by zero
    Ratio is NumEmployees / NumSmoothies.

% Main ratio predicate
ratio(X, R) :-
    calculate_ratio(X, R).

%% Sub-Problem-d %%
% Helper predicate to calculate the total price of a list of smoothies
calculate_total_price([], 0).
calculate_total_price([smoothie(_, _, Price) | Rest], Total) :-
    calculate_total_price(Rest, RemainingTotal),
    Total is RemainingTotal + Price.

% Helper predicate to calculate the number of smoothies in a list
calculate_num_smoothies([], 0).
calculate_num_smoothies([_|Rest], Num) :-
    calculate_num_smoothies(Rest, RemainingNum),
    Num is RemainingNum + 1.

% Main average predicate
average(X, A) :-
    store(X, _, Smoothies),
    calculate_total_price(Smoothies, TotalPrice),
    calculate_num_smoothies(Smoothies, NumSmoothies),
    NumSmoothies > 0, % Avoid division by zero
    A is TotalPrice / NumSmoothies.

%% Sub-Problem-e %%
% Helper predicate to extract smoothie names from a list of smoothies
extract_smoothie_names([], []).
extract_smoothie_names([smoothie(Name, _, _) | Rest], [Name | Names]) :-
    extract_smoothie_names(Rest, Names).

% Main smoothies_in_store predicate
smoothies_in_store(X, L) :-
    store(X, _, Smoothies),
    extract_smoothie_names(Smoothies, L).

%% Sub-Problem-f %%
% Helper predicate to check if a fruit is an ingredient of a given smoothie
fruit_in_smoothie(Fruit, smoothie(_, Ingredients, _)) :-
    member(Fruit, Ingredients).

% Helper predicate to check if a fruit is present in all smoothies of a store
fruit_in_all_smoothies_helper(_, []).
fruit_in_all_smoothies_helper(Fruit, [Smoothie | RestSmoothies]) :-
    fruit_in_smoothie(Fruit, Smoothie),
    fruit_in_all_smoothies_helper(Fruit, RestSmoothies).

% Main predicate to check if a fruit is an ingredient in all smoothies of a store
fruit_in_all_smoothies(Store, Fruit) :-
    store(Store, _, Smoothies),
    fruit_in_all_smoothies_helper(Fruit, Smoothies).
