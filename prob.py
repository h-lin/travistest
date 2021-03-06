import we

from enum import Enum, unique, auto
from typing import Dict, List

from lenc import LengthConstraint
from regc import RegularConstraint
from we import WordEquation


@unique
class ValueType(Enum):
    bool = auto()
    int = auto()
    string = auto()
    unknown = auto()


class MultiDeclarationError(Exception):
    pass


class UnknownVariableError(Exception):
    pass


class UnsupportedConstructError(Exception):
    pass


class InvalidTypeError(Exception):
    pass


class InvalidConstructError(Exception):
    pass


class Problem:
    def __init__(self):
        self.variables: Dict[str, ValueType] = {}
        self.internal_var_count: int = 0
        self.word_equations: List[WordEquation] = []
        self.reg_constraints: List[RegularConstraint] = []
        self.len_constraints: List[LengthConstraint] = []

    def declare_variable(self, name: str, typ: ValueType):
        if name in self.variables:
            raise MultiDeclarationError(f'variable: {name}')
        self.variables[name] = typ
        if typ is ValueType.string:
            length_var_name = we.Variable(name).length().value
            self.declare_variable(length_var_name, ValueType.int)

    def new_variable(self, typ: ValueType) -> str:
        name = f'xxx_{typ.name}{self.internal_var_count}_'
        self.variables[name] = typ
        self.internal_var_count += 1
        return name

    def ensure_variable_known(self, var: str, typ: ValueType):
        if self.variables.get(var) is not typ:
            raise UnknownVariableError(f'variable: {var} type: {typ.name}')

    def add_word_equation(self, we: WordEquation):
        for var in we.variables():
            self.ensure_variable_known(var.value, ValueType.string)
        self.word_equations.append(we)

    def add_regular_constraint(self, constr: RegularConstraint):
        self.ensure_variable_known(constr.tgt_var.value, ValueType.string)
        self.reg_constraints.append(constr)

    def add_length_constraint(self, constr: LengthConstraint):
        for var in constr.variables():
            self.ensure_variable_known(var.value, ValueType.int)
        self.len_constraints.append(constr)
