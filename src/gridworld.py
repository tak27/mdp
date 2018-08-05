from mdp import MDP

class GridWorld(MDP):
    def __init__(self,rows,cols,definitiveness,initstate,terminals,obstacles,gamma=.9):
        self.rows=rows
        self.cols=cols
        self.definitiveness=definitiveness
        self.initstate=initstate
        self.terminals=terminals
        self.obstacles=obstacles
        stateset=set()
        for y in range(1,self.cols+1):
            for x in range(1,self.rows+1):
                stateset.add((x,y))
        actionset={'up','down','right','left'}
        MDP.__init__(self,stateset,actionset,gamma)

    def T(self,state,action):
        if action is None:
            return [(1.0,state)]
        else:
            return [(self.definitiveness,self.move(state,action)),
                    ((1-self.definitiveness)/2,self.move(state,turn_right(action))),
                    ((1-self.definitiveness)/2,self.move(state,turn_left(action)))]
    
    def R(self,state):
        if state in self.terminals:
            return 1
        elif state in self.obstacles:
            return -1
        else:
            return 0

    def actions(self,state):
        if state in self.terminals:
            return [None]
        else:
            return self.actionset

    def move(self,state,action):
        dic={'up':(-1,0),'down':(1,0),'right':(0,1),'left':(0,-1)}
        tostate=tuple([a+b for (a,b) in zip(state,dic[action])])
        if tostate in self.stateset:
            return tostate
        else:
            return state

def turn_right(action):
    dic={'up':'right','down':'left','right':'down','left':'up'}
    return dic[action]

def turn_left(action):
    dic={'up':'left','down':'right','right':'up','left':'down'}
    return dic[action]

if __name__=='__main__':
    gridworld=GridWorld(4,4,.8,(1,1),[(4,4)],[(3,3),(3,2)])
    # print(gridworld.T((3,2),'up'))
    # print(gridworld.move((4,4),'right'))
    U=gridworld.value_iteration()
    # print(U)
    policy=gridworld.best_policy(U)
    print(policy)

    # rewards={}
    # for s in gridworld.stateset:
    #     rewards[s]=gridworld.R(s)
    # print(rewards)