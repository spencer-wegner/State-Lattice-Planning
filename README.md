# State Lattice Planning
Artificial Intelligence Practicum - University of Colorado Boulder  
Mark Ivlev and Spencer Wegner  
December 2018  

## Methods
&nbsp;&nbsp;&nbsp;&nbsp;State Lattice Planning is a method of state space navigation that uses A* search to get an agent from a start state to a goal state. Similarly to Pivtoraiko, Knepper and Kelly, the goal for this project is finding a path between two states vehicle considering its heading and wheel angle and in the presence of arbitrary obstacles. The state lattice itself is “a particular discretization of robot state space” (Pivtoraiko, Knepper, Kelly 1). Discretization of the state space drastically reduces the overall computational complexity of motion plan- ning. Initially, the agent does not have any knowledge about the state space except how it is structured, so it makes an initial plan to go straight to the goal, using A*. This means that the agent “sees” its own version of the state space that initially, as far as the agent knows, is completely free of any obstacles. As the agent moves along its initial A* route, it updates its knowledge of the state space by “perceiving” the space around it. If the agent perceives that there is an obstacle obstructing its path, it will re-plan using A*. At any given point along a path, the agent has only “seen” a certain amount of the actual state lattice, and so it will plan according to what it knows. Furthermore, throughout navigation, the agent is aware of the direction of its wheels (center, left or right) and its heading (North, South, East or West). Because of these added parameters, the agent is a more realistic representation of an an actual robot. This implementation is similar to that of others such as Pivtoraiko, Knepper and Kelly in multiple published papers, as well as McNaughton, Urmson, Dolan and Lee.

&nbsp;&nbsp;&nbsp;&nbsp;The methods we implemented for this project were building a randomized state lattice, and modifying A* search to work with the additional parameters of heading and wheel angle. Both the heading and wheel angle are discrete sets of options, rather than continuous. Each time the program is run, the size of the state lattice may be changed, as well as the amount of “vision” the agent has (how far ahead it can see when updating its knowledge), the start and goal positions of the agent, and the probability distribution for the obstacles in the state lattice. Each position in the state lattice is a tuple in the form of (X, Y, Heading, Wheel Angle). X and Y are integers that form a coordinate position. Heading takes one of four options: north, south, east or west, and wheel angle takes one of three options: center, left or right. The probability distribution represents the probability that any given space in the state lattice will have an obstacle in it. For example, a probability distribution of [0.8,0.2] would give an 80% chance that any given space will be open and a 20% chance that a space will have an obstacle in it. Upon running the program, the agent will attempt to make its way through the randomized state space. If it successfully navigates to the goal state, the path that the agent took will be printed, as well as the total number of A* plans, path cost and number of nodes expanded. If the agent is unable to reach the goal state, that means that there is no possible path to the goal state in the state space. The program will still print all of the information about path, plans, cost, and expansion relevant to the point at which the agent figured out that there was no available path.

&nbsp;&nbsp;&nbsp;&nbsp;While our implementation of state lattice planning did include most of the necessary methods, there were some methods that we did not implement, or did not fully implement. Pivtoraiko, Knepper and Kelly have published several papers on state lattice planning ad- dressing the methods that were not fully implemented in our project, such as better represen- tations of wheel angle, heading, and the state lattice itself. Additionally, our implementation would need some adapting in order to be used with an actual robot, as it stands right now it is only a simulation.

## Results
&nbsp;&nbsp;&nbsp;&nbsp;Here are a few outcomes of our state lattice planning agent with different parameters. In all of the following examples we set the start state to (0, 0, south, center) and the goal state to (9, 9, south, center), and worked with a 10x10 grid in order to show differences in the probability distribution of availability of nodes and the vision of the agent.

&nbsp;&nbsp;&nbsp;&nbsp;In this first example the agent vision is 1 unit and the probability of a node being blocked is 10%. The agent made two A* plans, incurred a path cost of 31 and expanded 954 nodes.

![Figure1](https://github.com/spencer-wegner/State-Lattice-Planning/blob/master/images/Figure_1.png)

&nbsp;&nbsp;&nbsp;&nbsp;The agent vision remains 1 unit for this second example but the probability of a node being blocked is now 30%. As the probability of blockages increases, the agent usually has to make more A* plans to find its way through the state space. Here, the agent made four A* plans, incurred a cost of 66, and expanded 1,740 nodes in the process.

![Figure3](https://github.com/spencer-wegner/State-Lattice-Planning/blob/master/images/Figure_3.png)

&nbsp;&nbsp;&nbsp;&nbsp;Now we have increased the agent vision to 5 units. The probability of a node being blocked is still 30%. As the agent vision increases, the average number of A* plans that the agent has to make decreases because the agent can take in more information and apply more information to each plan. In this case the agent only needed two A* plans, incurred a cost of 35, and expanded 640 nodes. Because of the randomization of the state space, the comparisons are not direct, but it is natural to see that if the agent has less vision, the cost would have been higher and the agent most likely would have needed to make more A* plans.

![Figure5](https://github.com/spencer-wegner/State-Lattice-Planning/blob/master/images/Figure_5.png)

&nbsp;&nbsp;&nbsp;&nbsp;In this example, the agent vision is 4 units and the probability of a node being blocked is 30%. The agent agent expanded 1,376 nodes with a cost of 66 but did not find a path to the goal. As the probability of blockages increase, the probability of not finding a path to the goal increases. As is seen through the A* plans however, the agent continues to make A* plans as it makes its way through the state space until the A* planner returns None based on the agent’s current knowledge.

![Figure4](https://github.com/spencer-wegner/State-Lattice-Planning/blob/master/images/Figure_4.png)

&nbsp;&nbsp;&nbsp;&nbsp;Things get a little more interesting (and take much longer to compute) when we expand the search space to a size of 25x25. Here there is a 10% chance of each node being blocked. The agent made seven A* plans, incurred a cost of 231 and expanded 23,464 nodes.

![Figure2](https://github.com/spencer-wegner/State-Lattice-Planning/blob/master/images/Figure_2.png)

## Discussion and Conclusion
&nbsp;&nbsp;&nbsp;&nbsp;State Lattice Planning has clear real world application, especially for fields such as self- navigating robots and self-driving cars. These fields of computer science are among the most relevant and important areas of technological advancement today, which lent a sense of significance to this project. Overall, this project was an enlightening foray into these greater possibilities of State Lattice Planning, and A* search in real world application. It is clear that if the features of this project were further developed and expanded, that it would be able to be used in real world environments in a useful way. Things like making the wheel angle and heading continuous, and updating knowledge of a state space using actual sensor data would be some of the obvious next steps if this project were to be further developed. Additional modifications and improvements would need to be made in order for this implementation to work with an actual robot or vehicle. Even as a simulation, this implementation shows how powerful even basic state lattice planning can be when used to solve the seemingly daunting task of motion planning.

## Bibliography
[Pivtoraiko, Knepper, Kelly - Differentially Constrained Mobile Robot Motion Planning in State Lattices](https://people.csail.mit.edu/rak/www/sites/default/files/pubs/PivKneKel09.pdf) \\ \\

    \href{https://www.inf.fu-berlin.de/inst/ag-ki/rojas_home/documents/Betreute_Arbeiten/Diss-Shuiying.pdf}{Wang - State Lattice-based Motion Planning for Autonomous On-Road Driving} \\ \\

    \href{http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.225.4980&rep=rep1&type=pdf}{McNaughton, Urmson, Dolan, Lee - Motion Planning for Autonomous Driving with a Conformal Spatiotemporal Lattice} \\ \\

    \href{https://www.researchgate.net/publication/221064731_High_Performance_State_Lattice_Planning_Using_Heuristic_Look-Up_Tables}{Knepper, Kelley - High Performance State Lattice Planning Using Heuristic Look-Up Tables} \\ \\

    \href{https://www.ri.cmu.edu/publications/efficient-constrained-path-planning-via-search-in-state-lattices/}{Pivtoraiko, Kelley - Efficient Constrained Path Planning via Search in State Lattices}
