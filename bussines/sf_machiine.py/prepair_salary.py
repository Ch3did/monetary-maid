from models.fixed_debits import FixedDebits


class Prepare_salary:
    
    def savings(self):
        porcent_save = self.salary * 0.05
    
    def fixed_debits(self):
        fd = FixedDebits()
    
    
    def run(self, salary):
        self.salary = salary
        self.savings()
