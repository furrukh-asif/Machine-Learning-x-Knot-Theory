from board import Board, GameResult
from agent import Agent 
from human import HumanPlayer

# p1 = Agent("p1")
# p2 = Agent("p2")

# st = Board(p1, p2)
# print("training...")
# st.simulation(50000)

# p1.savePolicy()
# p2.savePolicy()


p1 = Agent("computer", q_init=0)
p1.loadPolicy("policy_p1")

p2 = HumanPlayer("human")

st = Board(p1, p2)
st.play2()