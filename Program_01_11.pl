% %%% To find last element of a list

% Base Case :
% Last element of a one element list is the element itself                                                                                                                                                                                                                                                                                                          %%% K2E7: MADE BY SRIPARNO GANGULY 2020CSB004 %%%
last_element(X, [X]).
% Recursive rule: 
% Remove the head of the list and find the last element in the tail.
last_element(X, [_|Tail]):-
    last_element(X, Tail).

% %%% To append two lists

% Base case: 
% Appending an empty list to another list results in the same list.
append_lists([], L, L).
% Recursive rule: 
% Append the head of the first list to the result of appending the rest.
append_lists([X|Xs], Y, [X|Z]) :-
    append_lists(Xs, Y, Z).

% %%% To reverse a list

% Base case: 
% Reversing an empty list results in an empty list.
reverse_list([], []).
% Recursive rule: 
% Reverse the tail of the list and append the head to the reversed tail.
reverse_list([X|Xs], Reversed) :-
    reverse_list(Xs, ReversedTail),
    append_lists(ReversedTail, [X], Reversed).

% %%% Check whether list is a palindrome

% Base case: An empty list is a palindrome.
palindrome([]).

% Base case: A list with a single element is a palindrome.
palindrome([_]).

% Recursive rule: Check if the first and last elements are the same,
% and recursively check if the remaining sublist is a palindrome.
palindrome([X|Xs]) :-
    append_lists(Inner, [X], Xs),  % Split the list into Inner and [X]                                                                                                                                                                                                                                                                                                                                                                                           %%% K2E7: MADE BY SRIPARNO GANGULY 2020CSB004 %%%
last_element(X, [X]).
    reverse_list(Inner, ReversedInner),
    append_lists([X], ReversedInner, [X|Xs]).

% %%% Kth element of a list

% Base case: 
% The kth element of a list is its head when k is 1.
element_at(X, [X|_], 1).

% Recursive rule: 
% Decrement k and check the rest of the list.
element_at(X, [_|Xs], K) :-
    K > 1,
    K1 is K - 1,
    element_at(X, Xs, K1).

% Base case: 
% sum and average of an empty list are 0.
sum_and_avg([], 0, 0).

% Recursive case: 
% calculate the sum and average of the tail of the list,
% and add the head to the sum.
sum_and_avg([H|T], Sum, Avg) :-
    sum_and_avg(T, TailSum, TailAvg),
    Sum is H + TailSum,
    Avg is Sum / (1 + TailAvg).

% %%% GCD of two numbers
                                                                                                                                                                                                                                                                                                                                                                                                 %%% K2E7: MADE BY SRIPARNO GANGULY 2020CSB004 %%%
last_element(X, [X]).
% Base case: 
% GCD of any number with 0 is the number itself.
gcd(X, 0, X).
gcd(0, Y, Y).

% Recursive rule: 
% GCD of X and Y is the same as GCD of Y and X mod Y.
gcd(X, Y, Result) :-
    Y > 0,
    Z is X mod Y,
    gcd(Y, Z, Result).


% %%% Prime or Not Prime

% Base case: 0 and 1 are not prime.
is_prime(0) :- false.
is_prime(1) :- false.

% Predicate to check if N is prime.
is_prime(N) :-
    N > 1,
    is_prime_helper(N, 2).

% Helper predicate to check if N is divisible by any number from Start to N.
is_prime_helper(N, Start) :-
    Start > sqrt(N), % Only need to check up to the square root of N.
    !.

is_prime_helper(N, Start) :-
    N mod Start =\= 0,
    Next is Start + 1,
    is_prime_helper(N, Next).


% %%% Prime Factors

% Define a predicate to find the prime factors of a number.
prime_factors(N, Factors) :-
    N > 0,
    prime_factors_helper(N, 2, Factors).

prime_factors_helper(1, _, []) :- !.

prime_factors_helper(N, Factor, [Factor | Rest]) :-
    N mod Factor =:= 0,
    Next is N // Factor,
    prime_factors_helper(Next, Factor, Rest).

prime_factors_helper(N, Factor, Factors) :-
    N mod Factor =\= 0,
    NextFactor is Factor + 1,
    prime_factors_helper(N, NextFactor, Factors).

% %%% Goldberg's Conjecture

% Predicate to find two prime numbers that sum up to a given even integer
goldbach(N, [P1, P2]) :-
    N > 2,
    N mod 2 =:= 0,
    goldbach_helper(N, 3, P1),
    P2 is N - P1,
    is_prime(P2).

goldbach_helper(N, P, P) :-
    P =< N // 2,
    is_prime(P).
goldbach_helper(N, P, Result) :-
    P < N // 2,
    next_prime(P, NextPrime),
    goldbach_helper(N, NextPrime, Result).

% Predicate to find the next prime number                                                                                                                                                                                                                                                                                                                                                                                                %%% K2E7: MADE BY SRIPARNO GANGULY 2020CSB004 %%%
last_element(X, [X]).
next_prime(P, NextPrime) :-
    P1 is P + 2,
    is_prime(P1),
    NextPrime is P1, !.
next_prime(P, NextPrime) :-
    P1 is P + 2,
    next_prime(P1, NextPrime).

% %%% Fibonacci Numbers

% Base case: The first Fibonacci number is 0.
fibonacci(0, 0).

% Base case: The second Fibonacci number is 1.
fibonacci(1, 1).

% Recursive rule: Calculate the Nth Fibonacci number.
fibonacci(N, Result) :-
    N > 1,
    N1 is N - 1,
    N2 is N - 2,
    fibonacci(N1, Fib1),
    fibonacci(N2, Fib2),
    Result is Fib1 + Fib2.
