# 贝利尔罪仆每刻入口。任何途径召出的第 6 柱罪仆（手动、仪式二阶段）都在这里换装。
execute if entity @e[tag=rpg.demon.minion.lord6,tag=!rpg.bls,type=!minecraft:illusioner,limit=1] as @e[tag=rpg.demon.minion.lord6,tag=!rpg.bls,type=!minecraft:illusioner] at @s run function rpg:belial_servant/dress
execute if entity @e[tag=rpg.bls,type=!minecraft:item_display,limit=1] as @e[tag=rpg.bls,type=!minecraft:item_display] at @s run function rpg:belial_servant/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.bls.part,predicate=!rpg:belial_servant/riding,limit=1] run function rpg:belial_servant/orphans
