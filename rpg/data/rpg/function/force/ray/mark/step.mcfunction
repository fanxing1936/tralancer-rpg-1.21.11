execute if score #r rpg_fo matches ..37 run particle minecraft:dust{color:[1.0,0.85,0.35],scale:1.0} ~ ~ ~ 0.02 0.02 0.02 0 1 force
execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[type=#rpg:seal_hostile,tag=!rpg.ally,dx=0,dy=0,dz=0,tag=!rpg.fo.hit,limit=1,sort=nearest] at @s run function rpg:force/ray/mark/hit
execute if score #stop rpg_fo matches 1 run return run scoreboard players set #stop rpg_fo 1
scoreboard players remove #r rpg_fo 1
execute unless block ~ ~ ~ #rpg:force/pass run return run scoreboard players set #stop rpg_fo 1
execute if score #r rpg_fo matches ..0 run return run scoreboard players set #stop rpg_fo 1
execute positioned ^ ^ ^0.5 run function rpg:force/ray/mark/step
