import matplotlib.pyplot as plt

# Example data: Number of colors and expanded nodes for each heuristic
colors = [1, 2, 3]  # This is the same for all heuristics

# Lists for the number of expanded nodes for different heuristics
expanded_nodes_heuristic_1 = [10, 20, 30]
expanded_nodes_heuristic_2 = [5, 15, 25]
expanded_nodes_heuristic_3 = [12, 22, 35]

# Plotting each heuristic on the same graph
plt.plot(colors, expanded_nodes_heuristic_1, label='Heuristic 1', marker='o')
plt.plot(colors, expanded_nodes_heuristic_2, label='Heuristic 2', marker='s')
plt.plot(colors, expanded_nodes_heuristic_3, label='Heuristic 3', marker='^')

# Adding titles and labels
plt.title('Number of Expanded Nodes vs Number of Colors')
plt.xlabel('Number of Colors')
plt.ylabel('Number of Expanded Nodes')

# Displaying the legend
plt.legend()

# Show the plot
plt.show()
