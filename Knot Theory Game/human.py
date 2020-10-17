class HumanPlayer:
    def __init__(self, name):
        self.name = name 
    
    def chooseAction(self, positions):
        while True:
            crossing_idx = int(input("Which crossing will you play on?"))
            change_input = input("Will you change or keep the crossing? (Enter "Yes" or "No"))
            if change_input == "Yes":
                change = True
            elif change_input == "No":
                change = False
            action = (crossing_idx, change)
            if action[0] in positions:
                return action