from dataclasses import dataclass

@dataclass
class Cost:
    input_tokens: int = 0
    output_tokens: int = 0
    usd: float = 0.0

    def add(self, other: "Cost"):
        self.input_tokens += other.input_tokens
        self.output_tokens += other.output_tokens
        self.usd += other.usd
