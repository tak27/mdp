
class MDP:
    def __init__(self,stateset,actionset,gamma=.9):
        self.stateset=stateset
        self.actionset=actionset
        self.gamma=gamma

    def R(self,state):
        """
        R(state) gives the reward which is given to the agent at the given state.
        """
        raise NotImplementedError

    def T(self,state,action):
        """
        T(state,action) gives a list of tuples of probability and state at which and to which the agent will move from the given state after taking the given action.
        """
        raise NotImplementedError

    def actions(self,state):
        """
        actions(state) gives a list of actions which the agent can take at the given state or [None] in case that there is no action available there.
        """
        return self.actionset

    def value_iteration(self,epsilon=.001):
        U={s:0 for s in self.stateset}
        R,T,gamma=self.R,self.T,self.gamma
        while True:
            U_=U.copy()
            delta=0
            for s in self.stateset:
                U[s]=R(s)+gamma*max([sum([p*U_[s_] for (p,s_) in T(s,a)]) for a in self.actions(s)])
                delta=max(delta,abs(U[s]-U_[s]))
            # print(U)
            if delta < epsilon*(1-gamma)/gamma:
                return U

    def best_policy(self,U):
        pi={}
        for s in self.stateset:
            pi[s]=max(self.actions(s),key=lambda a: expected_utility(a,s,U,self))
        return pi

def expected_utility(a,s,U,mdp):
    return sum([p*U[s_] for (p,s_) in mdp.T(s,a)])
