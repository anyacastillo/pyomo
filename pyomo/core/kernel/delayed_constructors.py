from pyomo.core.expr.numvalue import native_numeric_types


class DelayedConstraintConstructor(object):
    def __init__(self, index_over, rule, container, component):
        self.index_over = index_over
        self.rule = rule
        self.container = container
        self.component = component

    def build(self, m):
        c = self.container()
        for i in self.index_over:
            c[i] = self.component(expr=self.rule(m, i))
        return c


class DelayedVarConstructor(object):
    def __init__(self, index_over, init_rule, bounds_rule, container, component):
        self.index_over = index_over
        self.init_rule = init_rule
        self.bounds_rule = bounds_rule
        self.container = container
        self.component = component

    def build(self, m):
        v = self.container()
        for i in self.index_over:
            if type(self.init_rule) in native_numeric_types or self.init_rule is None:
                val = self.init_rule
            else:
                val = self.init_rule(m, i)
            if type(self.bounds_rule) is tuple:
                lb = self.bounds_rule[0]
                ub = self.bounds_rule[1]
            elif self.bounds_rule is None:
                lb = None
                ub = None
            else:
                lb, ub = self.bounds_rule(m, i)
            v[i] = self.component(lb=lb, ub=ub, value=val)
        return v
