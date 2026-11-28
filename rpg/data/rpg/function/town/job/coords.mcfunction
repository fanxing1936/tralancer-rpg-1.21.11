# 宏不能做加减：把候选点四周要用的坐标先算好放进 rpg:town m
execute store result storage rpg:town m.x int 1 run scoreboard players get #px rpg_tw
scoreboard players operation #t rpg_tw = #px rpg_tw
scoreboard players add #t rpg_tw 20
execute store result storage rpg:town m.xp20 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #px rpg_tw
scoreboard players remove #t rpg_tw 20
execute store result storage rpg:town m.xm20 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #px rpg_tw
scoreboard players add #t rpg_tw 40
execute store result storage rpg:town m.xp40 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #px rpg_tw
scoreboard players remove #t rpg_tw 40
execute store result storage rpg:town m.xm40 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #px rpg_tw
scoreboard players add #t rpg_tw 48
execute store result storage rpg:town m.xp48 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #px rpg_tw
scoreboard players remove #t rpg_tw 48
execute store result storage rpg:town m.xm48 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #px rpg_tw
scoreboard players add #t rpg_tw 96
execute store result storage rpg:town m.xp96 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #px rpg_tw
scoreboard players remove #t rpg_tw 96
execute store result storage rpg:town m.xm96 int 1 run scoreboard players get #t rpg_tw
execute store result storage rpg:town m.z int 1 run scoreboard players get #pz rpg_tw
scoreboard players operation #t rpg_tw = #pz rpg_tw
scoreboard players add #t rpg_tw 20
execute store result storage rpg:town m.zp20 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #pz rpg_tw
scoreboard players remove #t rpg_tw 20
execute store result storage rpg:town m.zm20 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #pz rpg_tw
scoreboard players add #t rpg_tw 40
execute store result storage rpg:town m.zp40 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #pz rpg_tw
scoreboard players remove #t rpg_tw 40
execute store result storage rpg:town m.zm40 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #pz rpg_tw
scoreboard players add #t rpg_tw 48
execute store result storage rpg:town m.zp48 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #pz rpg_tw
scoreboard players remove #t rpg_tw 48
execute store result storage rpg:town m.zm48 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #pz rpg_tw
scoreboard players add #t rpg_tw 96
execute store result storage rpg:town m.zp96 int 1 run scoreboard players get #t rpg_tw
scoreboard players operation #t rpg_tw = #pz rpg_tw
scoreboard players remove #t rpg_tw 96
execute store result storage rpg:town m.zm96 int 1 run scoreboard players get #t rpg_tw
