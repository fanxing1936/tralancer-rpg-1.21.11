# 一缕绿烟：从洞底的路西法身上升起，穿过洞口往上飘，最后钻进裂缝
particle minecraft:dust{color:[0.37,0.84,0.55],scale:1.8} ~ ~ ~ 0.15 0.15 0.15 0 6 force
particle minecraft:dust{color:[0.85,1.0,0.9],scale:0.9} ~ ~ ~ 0.05 0.05 0.05 0 2 force
particle minecraft:campfire_cosy_smoke ~ ~ ~ 0.05 0.05 0.05 0.005 1 force
execute unless entity @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=..2] run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.pr.smokev","rpg.pr.ent"],billboard:"center",teleport_duration:1,brightness:{sky:15,block:15},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:prologue_fx/smoke_0"}},item_display:"fixed",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.6f,1.6f,1.6f]}}
tp @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=..2,limit=1,sort=nearest] ~ ~ ~
execute if entity @s[y=80,dy=12] facing 0 87.5 -9 run tp @s ^ ^ ^0.45
execute unless entity @s[y=80,dy=12] run tp @s ~0.01 ~0.65 ~-0.02
