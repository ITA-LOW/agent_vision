import motion
from agent_core import get_plan_for_goal  # Importa a versão compilada

class PlanLibrary:
    def __init__(self):
        self.plans = {}

    def set_plan_library(self, planlb):
        """Define a biblioteca de planos corretamente."""
        self.plans = {}
        for plan in planlb:
            goal, context_plan = plan
            if goal not in self.plans:
                self.plans[goal] = []
            self.plans[goal].append(context_plan)

    def add_plan(self, goal, prec, plan):
        """Adiciona um novo plano."""
        if goal not in self.plans:
            self.plans[goal] = []
        self.plans[goal].append({"context": prec, "plan": plan})

    def get_plan(self, goal, bb):
        """Retorna o primeiro plano adequado para o objetivo com base nos beliefs."""
        print("DEBUG - Beliefs atuais:", bb)
        print("DEBUG - Buscando plano para:", goal)

        if goal not in self.plans:
            print("DEBUG - Nenhum plano encontrado para esse objetivo.")
            return None

        plan = get_plan_for_goal(self.plans[goal], bb)
        if plan:
            print("DEBUG - Plano encontrado:", plan)
            return plan

        print("DEBUG - Nenhum plano compatível encontrado.")
        return None

class Action:
    def look_at_position(self, position):
        print(f"###> Looking at position {position} <### ")
        motion.look_at(position)

class Agent:
    def __init__(self):
        self.beliefs = {}
        self.desires = []
        self.intention = []
        self.plan_library = PlanLibrary()

    def get_desires(self):
        return self.desires.pop() if self.desires else None

    def add_desires(self, desire):
        self.desires.append(desire)

    def add_beliefs(self, beliefs):
        self.beliefs.update(beliefs)

    def set_plan_library(self, pl):
        self.plan_library.set_plan_library(pl)

    def update_intention(self, goal):
        plan = self.plan_library.get_plan(goal, self.beliefs)
        if plan:
            self.intention.extend(plan)
        else:
            print("Nenhum plano encontrado para a intenção:", goal)

    def execute_intention(self):
        while self.intention:
            next_action = self.intention.pop(0)
            print("Executando ação:", next_action)

            if self.plan_library.get_plan(next_action, self.beliefs) is None:
                action_instance = Action()
                action_instance.look_at_position(self.beliefs.get("position"))
            else:
                self.intention.extend(self.plan_library.get_plan(next_action, self.beliefs))
