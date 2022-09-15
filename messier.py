from dataclasses import dataclass
from pathlib import Path
import random
import re
from typing import List, Tuple

@dataclass
class MessierObject:
    number: int
    constellation: str
    difficulty: int

class MessierTrainer:

    # By default the difficulty ranges from 1-5; this controls their probability of appearing
    difficulty_to_weight = [6, 5, 4, 3, 1]

    current_difficulty = len(difficulty_to_weight)
    score, total = 0, 0

    def __init__(self):
        fpath = Path(__file__).parent / "messier.csv"
        with open(fpath, 'r') as ff:
            self.all_data = [self.parse(x) for x in ff.readlines()]
            self.all_weights = self.generate_weights(self.all_data)

        # Include all difficulties by default
        self.data = self.all_data
        self.weights = self.all_weights

    @classmethod
    def generate_weights(cls, obj: List[MessierObject]) -> List[int]:
        return [cls.difficulty_to_weight[x.difficulty-1] for x in obj]

    def parse(self, data: str) -> Tuple[MessierObject]:
        # Messier number, constellation, weight (1 - 5)
        parts = data.split(',')
        return MessierObject(int(parts[0]), parts[1], int(parts[2]))

    def print_score(self):
        print(f"{self.score}/{self.total}: {self.score/self.total*100 if self.total != 0 else '-'}")

    def update_difficulty(self, new_difficulty: int):
        self.current_difficulty = new_difficulty
        print(f"Set new difficulty to {self.current_difficulty}")
        
        self.data = list(filter(lambda x: x.difficulty <= self.current_difficulty, self.all_data))
        self.weights = self.generate_weights(self.data)

    def run(self):
        
        prev_obj, next_obj = None, None
        while True:
            # No identical object back to back
            next_obj = prev_obj
            while next_obj == prev_obj:
                [next_obj] = random.choices(population=self.data, weights=self.weights, k=1)
            
            answer = input(f"[{next_obj.difficulty}] M{next_obj.number} > ").strip()
            
            if answer == 'exit':
                self.print_score()
                exit()
            elif answer == 'score':
                self.print_score()
            elif re.match(r'diff [1-5]', answer):
                self.print_score()
                self.score, self.total = 0, 0
                print("=" * 20)
                self.update_difficulty(int(answer.split()[1]))
            else:
                self.total += 1
                if answer.lower() == next_obj.constellation.lower():
                    self.score += 1
                    print("Correct!")
                else:
                    print(f"Wrong: {next_obj.constellation}")
            
            prev_obj = next_obj


if __name__ == "__main__":
    MessierTrainer().run()