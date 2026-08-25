
# 玩家状态彼此隔离；达到阈值时只释放自己的技能。
execute as @a[scores={ice_step=45..}] if items entity @s weapon.mainhand *[minecraft:custom_data~{ice_tag:1b}] at @s run function rpg:item/legacy_advanced/epic/ice_release
execute as @a[scores={sea_step=10..}] if items entity @s weapon.mainhand *[minecraft:custom_data~{sea_tag:1b}] at @s run function rpg:item/legacy_advanced/epic/sea_release
