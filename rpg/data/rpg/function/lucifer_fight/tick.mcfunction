# 路西法每刻（as 领主 at 领主，由 taint/advent_tick 在 inquest/boss_tick 之后调用）。
scoreboard players add @s rpg_l2_st 0
execute if entity @s[tag=!rpg.lu.phase2,tag=!rpg.lu2f.morph] run function rpg:lucifer_fight/morph/check
execute if entity @s[tag=rpg.lu2f.morph] run return run function rpg:lucifer_fight/morph/tick
execute unless entity @s[tag=rpg.lu.phase2] run return run function rpg:lucifer_fight/p1/tick
execute if entity @s[tag=!rpg.lu2f.big] run function rpg:lucifer_fight/grow
execute unless score @s rpg_l2_id matches 1.. run function rpg:lucifer_fight/new_id
# 自己射出的果核不论处于什么状态都要飞完。
scoreboard players operation #id rpg_l2_id = @s rpg_l2_id
tag @s add rpg.dm.cast
execute as @e[type=minecraft:item_display,tag=rpg.lu2f.dart] if score @s rpg_l2_id = #id rpg_l2_id at @s run function rpg:lucifer_fight/dart/step
tag @s remove rpg.dm.cast
execute if score @s rpg_ex_stage matches 2..4 run return run function rpg:lucifer_fight/bound/tick
execute if entity @s[tag=rpg.lu2f.bound] run function rpg:lucifer_fight/bound/leave
# 忙碌时把出招冷却压在 30 以上：招与招之间至少隔这么久，中间穿插普攻。
execute unless score @s rpg_l2_st matches 2 if score @s rpg_dm_cd matches ..29 run scoreboard players set @s rpg_dm_cd 30
execute if score @s rpg_l2_st matches 3 run return run function rpg:lucifer_fight/skill/tick
execute if score @s rpg_l2_st matches 4 run return run function rpg:lucifer_fight/vuln/tick
scoreboard players set @s rpg_l2_st 2
execute if score @s rpg_l2_mc matches 1.. run scoreboard players remove @s rpg_l2_mc 1
execute if score @s rpg_l2_mc matches ..0 if score @s rpg_dm_ult matches ..0 if entity @a[distance=..6,gamemode=!spectator,gamemode=!creative] run function rpg:lucifer_fight/melee/start
