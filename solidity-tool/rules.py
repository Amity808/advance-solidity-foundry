# rules.py
from solidity_parser import parser

class Rule:
    def check(self, tree, source_lines):
        pass

class MissingVisibilityRule(Rule):
    def check(self, tree, source_lines):
        issues = []
        # Traverse the AST for function definitions
        def visit_node(node):
            if isinstance(node, dict) and node.get('type') == 'FunctionDefinition':
                if not node.get('visibility'):
                    name = node.get('name', '<anonymous>')
                    line = node.get('src', '').split(':')[1] or 'unknown'
                    issues.append(f"Function '{name}' at line {line} missing visibility specifier")
            for child in node.get('children', []):
                visit_node(child)
        
        visit_node(tree)
        return issues

class DeprecatedThrowRule(Rule):
    def check(self, tree, source_lines):
        issues = []
        # Check for 'throw' statements
        def visit_node(node):
            if isinstance(node, dict) and node.get('type') == 'ThrowStatement':
                line = node.get('src', '').split(':')[1] or 'unknown'
                issues.append(f"Deprecated 'throw' statement used at line {line}")
            for child in node.get('children', []):
                visit_node(child)
        
        visit_node(tree)
        return issues

class LongFunctionRule(Rule):
    def check(self, tree, source_lines):
        issues = []
        def visit_node(node):
            if isinstance(node, dict) and node.get('type') == 'FunctionDefinition':
                body = node.get('body', {})
                if body and 'src' in body:
                    src = body['src'].split(':')
                    start_line = int(src[1])
                    end_line = start_line + int(src[2])
                    line_count = end_line - start_line
                    if line_count > 20:  # Arbitrary threshold
                        name = node.get('name', '<anonymous>')
                        issues.append(f"Function '{name}' at line {start_line} is too long ({line_count} lines)")
            for child in node.get('children', []):
                visit_node(child)
        
        visit_node(tree)
        return issues