# 加上握持判定：原本没有这一条，攒满任何一块符石都会把三种效果一起放出。

# 每位玩家只读自己的蓄力、经验和主手；不再生成靠 @p 猜主人的盔甲架。
execute as @a[tag=rpg.h.sweep_tag1,scores={sweep=50..}] if items entity @s weapon.mainhand *[minecraft:custom_data~{sweep_tag:1b}] run function rpg:item/legacy_advanced/rune/sweep_release
