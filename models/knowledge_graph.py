import json
import os

class OpponentKnowledgeGraph:
    def __init__(self):
        graph_path = os.path.join(os.path.dirname(__file__), "..", "database", "opponent_knowledge_graph.json")
        with open(graph_path, "r") as f:
            self.graph = json.load(f)

    def get_weakness(self, driver):
        data = self.graph["drivers"].get(driver)
        if data:
            return data.get("weaknesses", {})
        return {}

    def best_attack_area(self, driver):
        weaknesses = self.get_weakness(driver)
        if not weaknesses:
            return None
        return max(weaknesses, key=weaknesses.get)

    def weakness_severity(self, driver):
        area = self.best_attack_area(driver)
        if area:
            return self.get_weakness(driver)[area]
        return 0.0
