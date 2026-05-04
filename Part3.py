import matplotlib.pyplot as plt

# x-axis must be integers 1 to N
x = range(1, len(daily) + 1)

# create line graph
plt.plot(x, daily.values)

# required title and labels
plt.title("V Closing Price")
plt.xlabel("Trading Day")
plt.ylabel("Closing Price")

# save graph as image for LaTeX report
plt.savefig("V_closing_price_graph.png", dpi=300, bbox_inches="tight")

# show graph
plt.show()
