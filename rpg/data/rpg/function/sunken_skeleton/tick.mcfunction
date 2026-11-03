# 沉没罪仆每刻入口。任何途径召出的利维坦罪仆（手动、仪式二阶段）都在这里换装。
execute if entity @e[tag=rpg.demon.minion.lord2,tag=!rpg.sk,type=!minecraft:illusioner,limit=1] as @e[tag=rpg.demon.minion.lord2,tag=!rpg.sk,type=!minecraft:illusioner] at @s run function rpg:sunken_skeleton/dress
execute if entity @e[tag=rpg.sk,type=!minecraft:item_display,limit=1] as @e[tag=rpg.sk,type=!minecraft:item_display] at @s run function rpg:sunken_skeleton/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.sk.part,predicate=!rpg:sunken_skeleton/riding,limit=1] run function rpg:sunken_skeleton/orphans
