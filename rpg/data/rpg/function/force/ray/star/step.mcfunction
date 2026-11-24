execute if score #r rpg_fo matches ..57 run particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1 force
execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[type=#rpg:seal_hostile,tag=!rpg.ally,dx=0,dy=0,dz=0,tag=!rpg.fo.hit,limit=1,sort=nearest] at @s run function rpg:force/ray/star/hit
execute if score #stop rpg_fo matches 1 run return run function rpg:force/ray/star/end
scoreboard players remove #r rpg_fo 1
execute unless block ~ ~ ~ #rpg:force/pass run return run function rpg:force/ray/star/end
execute if score #r rpg_fo matches ..0 run return run function rpg:force/ray/star/end
execute positioned ^ ^ ^0.5 run function rpg:force/ray/star/step
