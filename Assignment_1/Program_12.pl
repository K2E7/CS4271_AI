% Facts representing parent-child relationships
parent(john, ann).
parent(jim, john).
parent(jim, keith).
parent(mary, ann).
parent(mary, sylvia).
parent(brian, sylvia).

% Facts representing gender information
male(john).
male(jim).
male(keith).
male(brian).
female(ann).
female(mary).                                                                                                                                                                                                                                                                                                    %%% K2E7: MADE BY SRIPARNO GANGULY 2020CSB004 %%%
last_element(X, [X]).
female(sylvia).

% Predicate to check if two people share at least one parent
halfsister(X, Y) :-
    parent(Z, X),  % Z is the common parent
    parent(Z, Y),
    X \= Y,        % X and Y are different individuals                                                                                                                                                                                                                              
    X \= Y,        % X and Y are different individuals                                                                                                                                                                                                                              
    \+ sibling(X, Y).  % X and Y are not full siblings
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    %%% K2E7: MADE BY SRIPARNO GANGULY 2020CSB004 %%%
% Predicate to check if two people are full siblings
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y,
    male(P).  % P is the shared parent and must be male for half-sister relationship


% Rules for defining grandparents
grandparent(GP, GC) :-
    parent(GP, Parent),                                                                                                                                                                                                                                                                                      %%% K2E7: MADE BY SRIPARNO GANGULY 2020CSB004 %%%
    parent(Parent, GC).

% Rules for defining aunts and uncles
aunt(Aunt, NieceNephew) :-
    parent(Parent, NieceNephew),
    sibling(Aunt, Parent),
    female(Aunt).

uncle(Uncle, NieceNephew) :-
    parent(Parent, NieceNephew),
    sibling(Uncle, Parent),
    male(Uncle).                                                                                                                                                                                                                                                                                                                                                                                                        %%% K2E7: MADE BY SRIPARNO GANGULY 2020CSB004 %%%
