# 找到了。标记目标，全队转入交战。
execute as @e[distance=..0.7,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1,sort=nearest] run function rpg:squad/mark_one
execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players set @s rpg_sq_mode 2
particle crit ~ ~ ~ 0.3 0.3 0.3 0.2 20
playsound minecraft:entity.husk.ambient hostile @a[distance=..20] ~ ~ ~ 1 0.7
