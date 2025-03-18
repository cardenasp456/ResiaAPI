import json

class PlanModel:
    def get_plan_estudio(self):
        with open('plans/plan_estudio.json', encoding='utf-8') as f:
            plan_estudio = json.load(f)
        return plan_estudio