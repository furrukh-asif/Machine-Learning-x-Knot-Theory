from knot import Knot, GameResult
from agent import Agent 


# p1 = Agent("Unknotter")
# p2 = Agent("knotter")

# # pd_code = [[1,4, 2, 5], [3, 8, 4, 9], [5, 10, 6, 1], [9, 6, 10, 7], [7, 2, 8, 3]]
# pd_code = [[1, 4, 2, 5], [3, 6, 4, 1], [5, 2, 6, 3]]
# st = Knot(p1, p2, pd_code)
# print("training...")
# print(st.knot)
# st.simulation(pd_code, 50000)

# p1.savePolicy()
# p2.savePolicy()


p1 = Agent("Unknotter")
p1.loadPolicy("policy_p1")
p2 = Agent("knotter")
p2.loadPolicy("policy_p2")

# pd_code = [[1,4, 2, 5], [3, 8, 4, 9], [5, 10, 6, 1], [9, 6, 10, 7], [7, 2, 8, 3]]
pd_code = [[1, 4, 2, 5], [3, 6, 4, 1], [5, 2, 6, 3]]
st = Knot(p1, p2, pd_code)
st.play2()