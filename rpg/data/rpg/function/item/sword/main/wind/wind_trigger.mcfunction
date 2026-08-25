
# 每位玩家只读自己的蓄力、经验和主手；不再生成靠 @p 猜主人的盔甲架。
execute as @a[scores={wind=50..},level=1..] if items entity @s weapon.mainhand *[minecraft:custom_data~{wind_tag:1b}] run function rpg:item/legacy_advanced/rune/wind_release
execute as @a[scores={wind=50..},level=..0] if items entity @s weapon.mainhand *[minecraft:custom_data~{wind_tag:1b}] run function rpg:item/legacy_advanced/rune/wind_empty
