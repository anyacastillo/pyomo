from pyomo.core.kernel.constraint import constraint, constraint_dict
from pyomo.core.kernel.variable import variable, variable_dict
from pyomo.core.kernel.objective import objective
from pyomo.core.kernel.delayed_constructors import DelayedVarConstructor, DelayedConstraintConstructor
from pyomo.core.kernel.block import block


def Set(initialize, ordered=True):
    return initialize


def Constraint(index_over=None, rule=None, expr=None):
        if expr is not None:
            assert index_over is None
            assert rule is None
            return constraint(expr=expr)
        else:
            return DelayedConstraintConstructor(index_over, rule, constraint_dict, constraint)


def Var(index_over=None, initialize=None, bounds=None):
    if index_over is None:
        if type(bounds) is tuple:
            lb = bounds[0]
            ub = bounds[1]
        else:
            assert bounds is None
            lb = None
            ub = None
        return variable(lb=lb, ub=ub, value=initialize)
    else:
        return DelayedVarConstructor(index_over, initialize, bounds, variable_dict, variable)


def Expression(expr):
    return expr


def Objective(expr):
    return objective(expr=expr)


def ConcreteModel():
    return block()
