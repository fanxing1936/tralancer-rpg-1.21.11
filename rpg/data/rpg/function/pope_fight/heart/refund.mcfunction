scoreboard players operation #lost rpg_pf *= #keep rpg_pf
scoreboard players operation #lost rpg_pf /= #ten rpg_pf
scoreboard players operation #hp rpg_pf += #lost rpg_pf
execute store result entity @s Health float 1 run scoreboard players get #hp rpg_pf
# 血量涨回来不是挨打：对齐受伤基准，否则下一刻 rpg.hurt 又触发一次裁决。
scoreboard players operation @s damage_timing = #hp rpg_pf
scoreboard players operation @s damage_action = #hp rpg_pf
