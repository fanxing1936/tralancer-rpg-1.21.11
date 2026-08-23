# 暴怒的毒。走 rpg.hurt + on attacker，与包里其余被动同一形状。
#
# 这一趟**不按人数放大**：它问的是受伤实体的攻击者是不是第五柱，
# 与"哪个玩家在跑这条命令"无关，所以全场一次遍历就够。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.pact,scores={rpg_pact=5}] run function rpg:pact/samael_hit
