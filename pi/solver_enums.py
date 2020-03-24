from aenum import Enum, NoAlias


class PolyKind(Enum, settings=NoAlias):
    polynomial2 = 2
    polynomial1 = 1


class GameLevel(Enum):
    simple = 1


class MathSymbols(Enum):
    delta = "\Delta"
    radical = "\sqrt"
    fraction = "\over"
    plum_minus = "\pm"
    then = "\Rightarrow "
    start_statement = "\("
    end_statement = "\)"
    start_line = "\["
    end_line = "\]"


class EquationStates(Enum):
    impossible = "غیر ممکن است، پس معادله جواب ندارد"
    trivial = "تساوی بدیهی"


class Poly2States(Enum):
    poly1 = "تبدیل به درجه یک"


class Poly2Delta(Enum, settings=NoAlias):
    name = "دلتا"
    delta_calculation_code = 0
    pre_delta = "محاسبه دلتا"
    negative_delta = "دلتا  منفی است، پس معادله جواب ندارد"
    negative_delta_code = -1
    zero_delta = "دلتا مساوی صفر است، پس معادله ریشه مضاعف دارد"
    zero_delta_code = 1
    positive_delta = "دلتا مثبت است پس معادله دو ریشه دارد"
    positive_delta_code = 2


class Poly2Square(Enum, settings=NoAlias):
    name = "مربع کامل"
    negative_a = "طرفین تساوی را در منفی ضرب می‌کنیم"
    multiple4 = "طرفین را ضرب در ۴ می‌کنیم"
    multiple_a = "طریفین را در ظریب جمله درجه دو ظرب می‌کنیم تا مربع کامل شود"

class Poly2Decompose(Enum, settings=NoAlias):
    name = "تجزیه"
    devide_a = "طرفین را تقسیم بر ضریب جمله درجه دو می کنیم"
    looking = "دو عدد می‌خواهیم که مجموع آنها {} و حاصلضرب آنها {} باشد"
    finding = "آن دو عدد {} و {} هستند"
    zero_equal = "هر دو پرانتز را مساوی سفر قرار می‌دهیم"