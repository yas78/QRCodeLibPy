class ModuleRatio(object):

    def __init__(self) -> None:
        self.pre_light4   = 0
        self.pre_dark1    = 0
        self.pre_light1   = 0
        self.center_dark3 = 0
        self.fol_light1   = 0
        self.fol_dark1    = 0
        self.fol_light4   = 0

    def penalty_imposed(self) -> bool:
        if self.pre_dark1 == 0:
            return False

        if (self.pre_dark1
                == self.pre_light1
                == self.fol_light1
                == self.fol_dark1
                == (self.center_dark3 / 3)):

            return (self.pre_light4 >= self.pre_dark1 * 4 or
                    self.fol_light4 >= self.pre_dark1 * 4)
        else:
            return False
