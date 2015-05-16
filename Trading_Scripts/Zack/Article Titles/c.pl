
parent(thing,person).
parent(person,man).
parent(person,woman).
parent(thing,vehicle).
parent(vehicle,tractor).
parent(vehicle,car).
parent(tractor,massey).
parent(thing,animal).
parent(thing,plant).
parent(thing,place).
parent(plant,flower).
parent(plant,vegetable).
parent(plant,tree).
parent(animal,dog).
parent(animal,cat).
parent(place,house).



property(exist,thing).
property(live,person).
property(live,animal).
property(live,plant).
property(think,person).
property(move,vehicle).
property(plough,tractor).
property(grow,plant).
property(eat,animal).
property(move,man).
property(move,woman).


property(X,Y) :- parent(Q,Y),
                 property(X,Q).

child(X,Y) :- parent(Y,X).

sibling(X,Y) :- parent(Z,X),
                parent(Z,Y),
                X \== Y.

ancestor(X,Y) :- parent(X,Y).
ancestor(X,Y) :- parent(X,Z),
                 ancestor(Z,Y).

cousin(X,Y) :- parent(P,X),
               parent(Q,Y),
               parent(R,Q),
               parent(R,P),
               P \== Q.