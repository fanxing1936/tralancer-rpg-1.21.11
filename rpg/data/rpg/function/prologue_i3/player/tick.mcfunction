# 序章里的玩家每刻（as/at）
execute if score @s rpg_pr_cd1 matches 1.. run scoreboard players remove @s rpg_pr_cd1 1
execute if score @s rpg_pr_cd2 matches 1.. run scoreboard players remove @s rpg_pr_cd2 1
execute if score @s rpg_pr_av matches 1.. run scoreboard players remove @s rpg_pr_av 1
execute if score @s rpg_pr_av matches 0 run function rpg:prologue_i3/role/avatar_off
execute if score @s rpg_pr_down matches 1.. run function rpg:prologue_i3/player/down
execute unless entity @s[gamemode=adventure] run return 0
scoreboard players operation #m rpg_pr_i3 = #t rpg_pr_i3
scoreboard players set #k rpg_pr_i3 5
scoreboard players operation #m rpg_pr_i3 %= #k rpg_pr_i3
execute if score #m rpg_pr_i3 matches 0 run function rpg:prologue_i3/player/hud
execute if entity @s[tag=rpg.pr.mh] if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_pr_w:1b}] unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_pr_w:1b}] run function rpg:prologue_i3/role/f
tag @s remove rpg.pr.mh
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_pr_w:1b}] run tag @s add rpg.pr.mh
execute unless items entity @s weapon.offhand *[minecraft:custom_data~{rpg_pr_guard:1b}] unless items entity @s weapon.offhand *[minecraft:custom_data~{rpg_pr_w:1b}] run item replace entity @s weapon.offhand with minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty",minecraft:custom_data={rpg_pr_guard:1b}]
execute in rpg:armageddon_3 positioned 0 81 0 unless entity @s[distance=..70] run function rpg:prologue_i3/player/to_west
