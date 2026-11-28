scoreboard players operation #t rpg_tw = #px rpg_tw
scoreboard players operation #t rpg_tw -= #r rpg_tw
execute store result storage rpg:town m.xlo int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #px rpg_tw
scoreboard players operation #t rpg_tw += #r rpg_tw
execute store result storage rpg:town m.xhi int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #pz rpg_tw
scoreboard players operation #t rpg_tw -= #r rpg_tw
execute store result storage rpg:town m.zlo int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #pz rpg_tw
scoreboard players operation #t rpg_tw += #r rpg_tw
execute store result storage rpg:town m.zhi int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #r rpg_tw
scoreboard players set #k rpg_tw -3
scoreboard players operation #t rpg_tw *= #k rpg_tw
scoreboard players set #k rpg_tw 3
scoreboard players operation #t rpg_tw /= #k rpg_tw
scoreboard players operation #t rpg_tw += #px rpg_tw
execute store result storage rpg:town m.x0 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #r rpg_tw
scoreboard players set #k rpg_tw -1
scoreboard players operation #t rpg_tw *= #k rpg_tw
scoreboard players set #k rpg_tw 3
scoreboard players operation #t rpg_tw /= #k rpg_tw
scoreboard players operation #t rpg_tw += #px rpg_tw
execute store result storage rpg:town m.x1 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #r rpg_tw
scoreboard players set #k rpg_tw 1
scoreboard players operation #t rpg_tw *= #k rpg_tw
scoreboard players set #k rpg_tw 3
scoreboard players operation #t rpg_tw /= #k rpg_tw
scoreboard players operation #t rpg_tw += #px rpg_tw
execute store result storage rpg:town m.x2 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #r rpg_tw
scoreboard players set #k rpg_tw 3
scoreboard players operation #t rpg_tw *= #k rpg_tw
scoreboard players set #k rpg_tw 3
scoreboard players operation #t rpg_tw /= #k rpg_tw
scoreboard players operation #t rpg_tw += #px rpg_tw
execute store result storage rpg:town m.x3 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #r rpg_tw
scoreboard players set #k rpg_tw -3
scoreboard players operation #t rpg_tw *= #k rpg_tw
scoreboard players set #k rpg_tw 3
scoreboard players operation #t rpg_tw /= #k rpg_tw
scoreboard players operation #t rpg_tw += #pz rpg_tw
execute store result storage rpg:town m.z0 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #r rpg_tw
scoreboard players set #k rpg_tw -1
scoreboard players operation #t rpg_tw *= #k rpg_tw
scoreboard players set #k rpg_tw 3
scoreboard players operation #t rpg_tw /= #k rpg_tw
scoreboard players operation #t rpg_tw += #pz rpg_tw
execute store result storage rpg:town m.z1 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #r rpg_tw
scoreboard players set #k rpg_tw 1
scoreboard players operation #t rpg_tw *= #k rpg_tw
scoreboard players set #k rpg_tw 3
scoreboard players operation #t rpg_tw /= #k rpg_tw
scoreboard players operation #t rpg_tw += #pz rpg_tw
execute store result storage rpg:town m.z2 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #r rpg_tw
scoreboard players set #k rpg_tw 3
scoreboard players operation #t rpg_tw *= #k rpg_tw
scoreboard players set #k rpg_tw 3
scoreboard players operation #t rpg_tw /= #k rpg_tw
scoreboard players operation #t rpg_tw += #pz rpg_tw
execute store result storage rpg:town m.z3 int 1 run scoreboard players get #t rpg_tw
