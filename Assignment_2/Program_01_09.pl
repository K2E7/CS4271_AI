%%% Problem 1 %%%
% Base case: Duplicating an empty list results in an empty list
duplicate([], _, []).

% Duplicate the elements of the list N times
duplicate([H|T], N, Result) :-
    duplicate_element(H, N, Duplicated),
    duplicate(T, N, RestDuplicated),
    append(Duplicated, RestDuplicated, Result).

% Helper predicate to duplicate a single element N times
duplicate_element(_, 0, []).
duplicate_element(X, N, [X|Rest]) :-
    N > 0,
    N1 is N - 1,
    duplicate_element(X, N1, Rest).

%%% Problem 2 %%%
% Base case: An empty list is always a sublist
is_sublist([], _).

% Predicate to check if L1 is a sublist of L2
is_sublist([X|Xs], [X|Ys]) :- % Match the first element
    is_sublist(Xs, Ys). % Check the rest

is_sublist(L, [_|Ys]) :- % Skip the first element of the second list
    is_sublist(L, Ys).

%%% Problem 3 %%%
% Helper predicate to check if an element is a member of a list
my_member(X, [X|_]).
my_member(X, [_|T]) :-
    my_member(X, T).

% Intersection of two sets
intersection_set([], _, []).
intersection_set([X|Set1], Set2, Intersection) :-
    my_member(X, Set2),
    intersection_set(Set1, Set2, RestIntersection),
    Intersection = [X|RestIntersection].
intersection_set([_|Set1], Set2, Intersection) :-
    intersection_set(Set1, Set2, Intersection).

% Union of two sets
% Helper predicate to remove duplicates from a list
remove_duplicates([], []).
remove_duplicates([X|Xs], Result) :-
    member(X, Xs),
    remove_duplicates(Xs, Result).
remove_duplicates([X|Xs], [X|Result]) :-
    \+ member(X, Xs),
    remove_duplicates(Xs, Result).

% Union of two sets
union_set(Set1, Set2, Union) :-
    append(Set1, Set2, CombinedSet),
    remove_duplicates(CombinedSet, Union).

% Difference of two sets
difference_set([], _, []).
difference_set([X|Set1], Set2, Difference) :-
    \+ my_member(X, Set2),
    difference_set(Set1, Set2, RestDifference),
    Difference = [X|RestDifference].
difference_set([_|Set1], Set2, Difference) :-
    difference_set(Set1, Set2, Difference).

% Symmetric difference of two sets
symmetric_difference_set(Set1, Set2, SymmetricDifference) :-
    difference_set(Set1, Set2, Difference1),
    difference_set(Set2, Set1, Difference2),
    append(Difference1, Difference2, SymmetricDifference).

%%% Problem 4 %%%
% Helper predicate to create pairs from corresponding elements of two lists
pair_elements(X, Y, (X, Y)).

% Transpose lists L1 and L2 into a list of pairs L
transpose_lists(L1, L2, L) :-
    maplist(pair_elements, L1, L2, L).

%%% Problem 5 %%%
% Helper predicate to split a list into two parts
split_helper(0, L, [], L).
split_helper(N, [X|Rest], [X|L1], L2) :-
    N > 0,
    N1 is N - 1,
    split_helper(N1, Rest, L1, L2).

split(List, N, L1, L2) :-
    length(List, Len),
    between(0, Len, N),
    split_helper(N, List, L1, L2).

%%% Problem 6 %%%
slice([X|_],1,1,[X]). 

slice([X|Xs],1,K,[X|Ys]) :- 
    K > 1, 
    K1 is K - 1, 
    slice(Xs,1,K1,Ys). 
    
slice([_|Xs],I,K,Ys) :- 
    I > 1, I1 is I - 1, 
    K1 is K - 1, 
    slice(Xs,I1,K1,Ys).

%%% Problem 7 %%%
% Helper predicate to select K elements from a list
selectK(0, _, []).
selectK(K, [X|Xs], [X|Ys]) :-
    K > 0,
    K1 is K - 1,
    selectK(K1, Xs, Ys).
selectK(K, [_|Xs], Ys) :-
    K > 0,
    selectK(K, Xs, Ys).

% Main predicate to generate combinations
combinations(K, List, Result) :-
    selectK(K, List, Result).

%%% Problem 8 %%%
% Bubble Sort %
% Helper predicate to swap two elements in a list
swap([X, Y|Rest], [Y, X|Rest]) :- X > Y.
swap([Z|Rest1], [Z|Rest2]) :- swap(Rest1, Rest2).

% Base case: An already sorted list
bubble_sort(List, List) :- \+ (swap(List, NewList), List \= NewList).

% Recursive case: Continue sorting
bubble_sort(List, Sorted) :- swap(List, Swapped), bubble_sort(Swapped, Sorted).

% Insertion Sort %
% Helper predicate to insert an element into a sorted list
insert(X, [], [X]).
insert(X, [Y|Rest], [X,Y|Rest]) :- X =< Y.
insert(X, [Y|Rest1], [Y|Rest2]) :- X > Y, insert(X, Rest1, Rest2).

% Base case: An empty list is already sorted
insertion_sort([], []).

% Recursive case: Insert the head into the sorted tail
insertion_sort([H|T], Sorted) :- insertion_sort(T, SortedTail), insert(H, SortedTail, Sorted).

% Merge Sort %
% Helper predicate to merge two sorted lists
merge([], L, L).
merge(L, [], L).
merge([X|Xs], [Y|Ys], [X|Z]) :- X =< Y, merge(Xs, [Y|Ys], Z).
merge([X|Xs], [Y|Ys], [Y|Z]) :- X > Y, merge([X|Xs], Ys, Z).

% Base case: An empty list or a single-element list is already sorted
merge_sort([], []).
merge_sort([X], [X]).

% Recursive case: Split the list into two, sort each part, and merge them
merge_sort(List, Sorted) :-
    length(List, Len),
    Len > 1,
    HalfLen is Len // 2,
    length(Left, HalfLen),
    append(Left, Right, List),
    merge_sort(Left, SortedLeft),
    merge_sort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).

%%% Problem 9 %%%
% Helper predicate for 'pack/2'
pack_helper([], []).
pack_helper([X], [[X]]).
pack_helper([X, X | T], [[X | Rest] | RestPacked]) :-
    pack_helper([X | T], [Rest | RestPacked]).
pack_helper([X, Y | T], [[X] | Packed]) :-
    \+ X = Y,
    pack_helper([Y | T], Packed).

% Predicate to pack consecutive duplicates into sublists
pack(List, PackedList) :-
    pack_helper(List, PackedList).

% Helper predicate for 'encode/2'
encode_helper([], []).
encode_helper([X], [[1, X]]).
encode_helper([X, X | T], [[N, X] | RestEncoded]) :-
    encode_helper([X | T], [[M, X] | RestEncoded]),
    N is M + 1.
encode_helper([X, Y | T], [[1, X] | Encoded]) :-
    \+ X = Y,
    encode_helper([Y | T], Encoded).

% Predicate to encode consecutive duplicates as terms [N, E]
encode(List, EncodedList) :-
    encode_helper(List, EncodedList).
