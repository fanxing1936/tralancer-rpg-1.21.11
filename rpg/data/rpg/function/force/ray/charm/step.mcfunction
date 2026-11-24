execute if score #r rpg_fo matches ..45 run particle minecraft:dust{color:[0.85,0.48,0.85],scale:0.8} ~ ~ ~ 0 0 0 0 1 force
execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[type=#rpg:seal_hostile,tag=!rpg.ally,tag=!rpg.pope,tag=!rpg.mkb,tag=!rpg.jqb,tag=!rpg.lub,tag=!rpg.slb,tag=!rpg.usb,dx=0,dy=0,dz=0,tag=!rpg.fo.hit,limit=1,sort=nearest] at @s run function rpg:force/ray/charm/hit
execute if score #stop rpg_fo matches 1 run return run scoreboard players set #stop rpg_fo 1
scoreboard players remove #r rpg_fo 1
execute unless block ~ ~ ~ #rpg:force/pass run return run scoreboard players set #stop rpg_fo 1
execute if score #r rpg_fo matches ..0 run return run scoreboard players set #stop rpg_fo 1
execute positioned ^ ^ ^0.5 run function rpg:force/ray/charm/step
