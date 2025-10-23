""" 持卡人 一个人可有多张卡 多人多卡 """
class CardHolder:
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        self.bank_cards = []

    def add_card(self, card):
        if card not in self.bank_cards:
            self.bank_cards.append(card)
        
        # 修正：self.card_holders 应为 card.card_holders
        if self not in card.card_holders:
            card.card_holders.append(self)
    
    def remove_card(self, card):
        if card in self.bank_cards:
            self.bank_cards.remove(card)
            # 自动维护反向关联
        if self in card.card_holders:
            card.card_holders.remove(self)
            
    def get_card_count(self):
        return len(self.bank_cards)
    
    def has_shared_cards(self):
        for card in self.bank_cards:
            # 修正：card.card_holder -> card.card_holders
            if len(card.card_holders) > 1:
                return True
        # 修正：缩进错误，应在循环外
        return False
        
    def get_shared_cards(self):
        return [card for card in self.bank_cards if len(card.card_holders) > 1]
        
    def get_personal_cards(self):
        """获取个人持有卡"""
        # 修正：card.card_hoders 拼写错误
        return [card for card in self.bank_cards if len(card.card_holders) == 1]
    
    def __str__(self):
        return f'{self.name}-{self.sex} 有 {len(self.bank_cards)}张卡'
    
    def __repr__(self):
        return f'CardHolder(name={self.name}, sex={self.sex})'  # 修正类名
