class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        result = False
        if(self.check_funds(amount)):
            if(amount > 0):
                amount *= -1
            self.ledger.append({'amount': amount, 'description': description})
            result = True
        return result

    def get_balance(self):
        balance = 0
        for i in self.ledger:
            balance += i['amount']
        return balance

    def transfer(self, amount, budget):
        result = False
        if(self.check_funds(amount)):
            self.withdraw(amount, f'Transfer to {budget.name}')
            budget.deposit(amount, f'Transfer from {self.name}')
            result = True
        return result

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def get_spent(self):
        spent = 0
        for i in self.ledger:
            if(i['amount'] < 0):
                spent += i['amount']
        return spent

    def __str__(self) -> str:
        result = []
        result.append('{0:*^30}'.format(self.name))
        for item in self.ledger:
            line = '{0: <23}{1:>7.2f}'.format(item['description'][:23], item['amount'])
            result.append(line)
        result.append('Total: {0:>.2f}'.format(self.get_balance()))
        return '\n'.join(result)


def create_spend_chart(categories):
    result = []
    result.append('Percentage spent by category')
    category_names = []
    total_spent = 0
    for category in categories:
        total_spent += category.get_spent()
        category_names.append(list(category.name))

    for i in sorted(range(0, 101, 10), reverse=True):
        line = '{0: >3}|'.format(i)
        for category in categories:
            if(int(abs(category.get_spent()/total_spent)*100) >= i):
                line += ' {0} '.format('o')
            else:
                line += ' {0} '.format(' ')
        result.append(line+' ')
    result.append('{0}{1}'.format(' '*4, '-'*10))

    max_len_category_name = max([ len(x) for x in category_names ])
    for i in range(max_len_category_name):
        line = '{0}'.format(' '*4)
        for category in category_names:
            if(len(category) > i):
                line += ' {0} '.format(category[i])
            else:
                line += ' {0} '.format(' ')
        result.append(line+' ')

    return '\n'.join(result)        