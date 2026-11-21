execute unless score @s rpg_fg_id matches 1.. run function rpg:forge/new_id
# F 键：上一刻主手是带符石的武器、副手不是；这一刻它到了副手 -> 换回来并释放。
scoreboard players set #cast rpg_fg 0
execute if entity @s[tag=rpg.fg.sm,tag=!rpg.fg.so] if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_eq:{}}] unless items entity @s weapon.offhand *[minecraft:custom_data~{rpg_eq:{stone:"none"}}] run function rpg:forge/stone/swap
# 手里的装备 -> 状态标签
execute if entity @s[tag=rpg.fg.m] run function rpg:forge/state/clear
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{}}] run function rpg:forge/state/main
execute if score #c10 rpg_fg matches 0 run function rpg:forge/state/armor
execute if score #c10 rpg_fg matches 5 run function rpg:forge/auto/scan
execute if score #c40 rpg_fg matches 7 run function rpg:forge/conv/scan
execute if score #cast rpg_fg matches 1 run function rpg:forge/stone/try
execute if score @s rpg_fg_kx matches 1.. run function rpg:forge/kill/credit
# 记下这一刻的手，供下一刻判断 F 键
tag @s remove rpg.fg.sm
tag @s remove rpg.fg.so
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{}}] unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{stone:"none"}}] run tag @s add rpg.fg.sm
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_eq:{}}] unless items entity @s weapon.offhand *[minecraft:custom_data~{rpg_eq:{stone:"none"}}] run tag @s add rpg.fg.so
# 窗口计时
scoreboard players remove @s[scores={rpg_fg_rw=1..}] rpg_fg_rw 1
scoreboard players remove @s[scores={rpg_fg_rs=1..}] rpg_fg_rs 1
scoreboard players remove @s[scores={rpg_fg_shd=1..}] rpg_fg_shd 1
scoreboard players remove @s[scores={rpg_fg_bl=1..}] rpg_fg_bl 1
scoreboard players remove @s[scores={rpg_fg_lb=1..}] rpg_fg_lb 1
scoreboard players remove @s[scores={rpg_fg_shot=1..}] rpg_fg_shot 1
# 弓弩射出的箭
execute if score @s rpg_fg_bow matches 1.. run function rpg:forge/arrow/shot
execute if score @s rpg_fg_xbow matches 1.. run function rpg:forge/arrow/shot
scoreboard players reset @s rpg_fg_bow
scoreboard players reset @s rpg_fg_xbow
# 持续效果
execute if score #c10 rpg_fg matches 3 run function rpg:forge/rune/bloodpact_tick
execute if entity @s[tag=rpg.fg.a.stillwater] run function rpg:forge/rune/stillwater
execute if entity @s[tag=rpg.fg.src.malice] run function rpg:forge/src/malice_tick
execute if entity @s[tag=rpg.fg.bl] run particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0 1
tag @s remove rpg.fg.bl
execute if score @s rpg_fg_bl matches 1.. run tag @s add rpg.fg.bl
