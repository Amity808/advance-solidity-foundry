# analyzer.py
from solidity_parser import parser

def parse_code(file_path):
    try:
        with open(file_path, 'r') as file:
            source = file.read()
        tree = parser.parse(source)
        return tree
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None
    
    # analyzer.py
from rules import MissingVisibilityRule, DeprecatedThrowRule, LongFunctionRule

class SolidityAnalyzer:
    def __init__(self):
        self.rules = [
            MissingVisibilityRule(),
            DeprecatedThrowRule(),
            LongFunctionRule()
        ]

    def analyze(self, file_path):
        tree = parse_code(file_path)
        if tree is None:
            return []
        
        with open(file_path, 'r') as file:
            source_lines = file.readlines()

        issues = []
        for rule in self.rules:
            issues.extend(rule.check(tree, source_lines))
        
        return issues

def main():
    analyzer = SolidityAnalyzer()
    file_path = "tests/test_contract.sol"
    issues = analyzer.analyze(file_path)
    for issue in issues:
        print(issue)

if __name__ == "__main__":
    main()