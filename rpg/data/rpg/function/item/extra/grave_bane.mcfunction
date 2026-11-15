# 坟墓克星［三段连斩］的每刻结算。由 rpg:item/extra/skills 守卫调用。
execute as @a[scores={rpg_gb_dmg=1..}] if items entity @s weapon.mainhand *[minecraft:custom_data~{grave_bane_tag:1b}] at @s run function rpg:item/extra/grave_bane_hit
scoreboard players reset * rpg_gb_dmg
