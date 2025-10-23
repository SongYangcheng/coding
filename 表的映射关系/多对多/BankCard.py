""" 银行卡类， 一个卡可对多个持有人 """

class BankCard:
    def __init__(self, bank_name, number, password):
        self.bank_name=bank_name
        self.number = number
        self.password = password
        self.card_holders = [] #多个持卡人
    def add_holder(self, holder):
        if holder not in self.card_holders:
            self.card_holders.append(holder)
        
        #自动维护双向关联
        if self not in holder.bank_cards:
            holder.bank_cards.append(self)
    
    def remove_holder(self, holder):
        if holder in self.card_holders:
            self.card_holders.remove(holder)
        if self in holder.bank_cards:
            holder.bank_cards.remove(self)
    
    def get_holder_count(self):
        return len(self.card_holders)
    def is_shared(self):
        return len(self.card_holders) > 1
    
    def get_card_type(self):
        if len(self.card_holders) == 0:
            return '未激活卡'
        elif len(self.card_holders) == 1:
            return '个人卡'
        else:
            return '共享卡'
        
    def __str__(self):
        holders_names = ','.join([h.name for h in self.card_holders])
        return f'{self.bank_name} - {self.number} (持卡人：{holders_names})'
    
    def __repr__(self):
        return f'BankCard(bank={self.bank_name})'