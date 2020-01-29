from aenum import Enum, NoAlias


class SolverKind(Enum, settings=NoAlias):
    polynomial2 = 2
    polynomial1 = 1


class Steps(Enum, settings=NoAlias):
    delta_calculation_code = 0
    pre_delta = "محاسبه دلتا"
    negative_delta = "دلتا  منفی است، پس معادله جواب ندارد"
    negative_delta_code = -1
    zero_delta = "دلتا مساوی صفر است، پس معادله ریشه مضاعف دارد"
    zero_delta_code = 1
    positive_delta = "دلتا مثبت است پس معادله دو ریشه دارد"
    positive_delta_code = 2
