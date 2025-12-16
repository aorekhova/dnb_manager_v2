import stat



class CheckPoint:
    def __init__(self, phase, inf=None):
        self.stat  = stat.Stat(phase)
        self.result = None

        self.setting_acceptInput = {"select parties": True, "match data to dnb": False, "generate reports": False}

        self.acceptInput = self.setting_acceptInput[phase]
        try:
            if self.acceptInput:
                self.give_new_stat(inf)
        except TypeError:
            self.result = TypeError


    def give_new_stat(self, inf):
        self.stat.take_new_inf(inf)



    def determine_risk_flag(self):
        if self.result is TypeError:
            return "red flag"
        return "red flag"