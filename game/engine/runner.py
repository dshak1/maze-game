"""
Safe code execution sandbox for user-provided code
"""
import ast
from typing import Dict, Any, List
from .agent import Agent

class SafeCodeRunner:
    """
    Executes user code safely by parsing AST and allowlisting nodes
    """
    
    ALLOWED_NODES = {
        ast.Module, ast.Expr, ast.Assign, ast.AnnAssign, ast.AugAssign,
        ast.For, ast.While, ast.If, ast.Compare, ast.Call, ast.Name, 
        ast.Constant, ast.FunctionDef, ast.Return, ast.Break, ast.Continue,
        ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.List, ast.Tuple, ast.Dict,
        ast.Subscript, ast.Slice, ast.Index, ast.Load, ast.Store,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Lt, ast.Gt,
        ast.LtE, ast.GtE, ast.Eq, ast.NotEq, ast.And, ast.Or, ast.Not,
        ast.arguments, ast.arg, ast.keyword,
        # F-string support
        ast.JoinedStr, ast.FormattedValue
    }
    
    FORBIDDEN_NAMES = {
        'eval', 'exec', 'compile', 'open', 'input', 'raw_input',
        '__import__', '__builtins__', 'globals', 'locals', 'vars',
        'dir', 'hasattr', 'getattr', 'setattr', 'delattr'
    }
    
    def __init__(self, agent: Agent):
        self.agent = agent
        self.execution_steps = []
        self.max_operations = 1000  # Prevent infinite loops
        self.operation_count = 0
        
        # API available to user code
        self.api = {
            "forward": self._safe_forward,
            "left": self._safe_left,
            "right": self._safe_right,
            "scan": self._safe_scan,
            "at_goal": self._safe_at_goal,
            "get_position": self._safe_get_position,
        }
    
    def _check_operation_limit(self):
        """Check if we've exceeded the operation limit"""
        self.operation_count += 1
        if self.operation_count > self.max_operations:
            raise RuntimeError(f"Too many operations (>{self.max_operations}). Possible infinite loop!")
    
    def _safe_forward(self, steps: int = 1) -> bool:
        """Safe wrapper for agent.forward()"""
        self._check_operation_limit()
        
        if not isinstance(steps, int) or steps < 0 or steps > 100:
            raise ValueError("forward() steps must be integer between 0 and 100")
        
        result = self.agent.forward(steps)
        self.execution_steps.append(f"forward({steps})")
        return result
    
    def _safe_left(self):
        """Safe wrapper for agent.left()"""
        self._check_operation_limit()
        self.agent.left()
        self.execution_steps.append("left()")
    
    def _safe_right(self):
        """Safe wrapper for agent.right()""" 
        self._check_operation_limit()
        self.agent.right()
        self.execution_steps.append("right()")
    
    def _safe_scan(self) -> str:
        """Safe wrapper for agent.scan()"""
        self._check_operation_limit()
        result = self.agent.scan()
        # Don't log every scan call - too verbose
        return result
    
    def _safe_at_goal(self) -> bool:
        """Safe wrapper for agent.at_goal()"""
        self._check_operation_limit()
        result = self.agent.at_goal()
        # Don't log every at_goal call - too verbose
        return result
    
    def _safe_get_position(self) -> tuple:
        """Safe wrapper for agent.get_position()"""
        self._check_operation_limit()
        result = self.agent.get_position()
        # Don't log every get_position call - too verbose
        return result
    
    def validate_code(self, code: str) -> tuple[bool, str]:
        """
        Validate code by parsing AST and checking for forbidden constructs
        Returns (is_valid, error_message)
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        
        # Check all nodes in the AST
        for node in ast.walk(tree):
            if type(node) not in self.ALLOWED_NODES:
                return False, f"Forbidden construct: {type(node).__name__}"
            
            # Check for forbidden function names
            if isinstance(node, ast.Name) and node.id in self.FORBIDDEN_NAMES:
                return False, f"Forbidden function: {node.id}"
            
            # Check for imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                return False, "Imports are not allowed"
            
            # Check for attribute access (prevent __builtins__ access)
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name) and node.value.id.startswith('__'):
                    return False, f"Access to {node.value.id} is forbidden"
        
        return True, ""
    
    def execute_code(self, code: str) -> tuple[bool, str, List[str]]:
        """
        Execute entire code block safely as one unit
        Returns (success, error_message, execution_steps)
        """
        print("🚀 Starting execution of complete code block...")
        self.execution_steps.clear()
        self.operation_count = 0  # Reset operation counter
        
        # Validate code first
        is_valid, error_msg = self.validate_code(code)
        if not is_valid:
            return False, error_msg, []
        
        # Remember starting position
        start_pos = self.agent.get_position()
        start_dir = self.agent.direction
        
        try:
            # Compile and execute with restricted environment
            tree = ast.parse(code)
            compiled = compile(tree, "<user_code>", "exec")
            
            # Create restricted execution environment
            exec_globals = {"__builtins__": {}}
            exec_locals = self.api.copy()
            
            # Execute the entire code block at once
            exec(compiled, exec_globals, exec_locals)
            
            # Log summary
            end_pos = self.agent.get_position()
            end_dir = self.agent.direction
            
            summary = f"Code block executed: {start_pos} → {end_pos}, {self.operation_count} operations"
            print(f"✅ {summary}")
            
            return True, "", self.execution_steps.copy()
            
        except Exception as e:
            error_msg = f"Execution error: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg, self.execution_steps.copy()
    
    def reset(self):
        """Reset execution state"""
        self.execution_steps.clear()
        self.operation_count = 0