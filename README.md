# Transformation from NFA to DFA plus DFA minimization
The input form is:
1. Number of states of automata
2. The labels for the states (anything separated by space)
3. Number of transitions
4. For the following ... lines the transitions of the automata are put like this: `start-state`  `end-state`  `letter`. For the lambda/epsilon NFA the letter is 'lambda', but can easily be changed in code to something simpler. 
5. The label of the start state
6. Number of final states
7. The labels for the final states (separated by space)

In "date.out" are displayed the steps: first how the DFA transformed from the input looks (the states that were combined are easily spotted with a dash in betweeen them) with the inital state and the final states. Then the minimized version with the states renamed.

In "verificare.txt" the transformed version is displayed in the input form with the states renamed, same for the minimized automaton.
