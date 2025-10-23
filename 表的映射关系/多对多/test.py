from BankCard import BankCard
from CardHolder import CardHolder

# 创建持卡人
holder1 = CardHolder("张三", "男")
holder2 = CardHolder("李四", "男")
holder3 = CardHolder("王五", "女")

# 创建银行卡
card1 = BankCard("建设银行", "6222 0000 1111 2222", "123456")
card2 = BankCard("工商银行", "6222 3333 4444 5555", "234567")
card3 = BankCard("农业银行", "6222 6666 7777 8888", "345678")

# 测试关联关系建立
print("=== 测试添加持卡人 ===")
# card1.add_holder(holder1)  # 张三持有建设银行卡
card1.add_holder(holder2)  # 李四也持有建设银行卡（共享卡）
card2.add_holder(holder2)  # 李四持有工商银行卡
card3.add_holder(holder3)  # 王五持有农业银行卡
#张三有三张卡
holder1.add_card(card1)
holder1.add_card(card2)
holder1.add_card(card3)


# 打印所有银行卡信息{hoder.name:<10}打印hoder.name的10个字符宽度
print("\n=== 所有银行卡信息 ===")
cards = [card1, card2, card3]
for card in cards:
    print(f"{card} - 类型：{card.get_card_type()}")

# 打印所有持卡人信息
print("\n=== 所有持卡人信息 ===")
holders = [holder1, holder2, holder3]
for holder in holders:
    print(holder)
    print(f"  持有的银行卡: {[str(card) for card in holder.bank_cards]}")
    print(f"  是否有共享卡: {holder.has_shared_cards()}")
    print(f"  共享卡列表: {[str(card) for card in holder.get_shared_cards()]}")
    print(f"  个人卡列表: {[str(card) for card in holder.get_personal_cards()]}")
    print()

# 测试解除关联
print("=== 测试移除持卡人 ===")
print(f"移除前卡1的持卡人数: {card1.get_holder_count()}")
card1.remove_holder(holder1)
print(f"移除后卡1的持卡人数: {card1.get_holder_count()}")
print(f"卡1现在是{card1.get_card_type()}")

# 测试从持卡人移除卡
print("\n=== 测试移除银行卡 ===")
print(f"移除前李四的银行卡数: {holder2.get_card_count()}")
holder2.remove_card(card2)
print(f"移除后李四的银行卡数: {holder2.get_card_count()}")