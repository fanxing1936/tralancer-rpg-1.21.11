# 路西法罪仆每刻入口。任何途径召出的第 1 柱罪仆（手动、仪式二阶段）都在这里换装。
execute if entity @e[tag=rpg.demon.minion.lord1,tag=!rpg.lcs,type=!minecraft:illusioner,limit=1] as @e[tag=rpg.demon.minion.lord1,tag=!rpg.lcs,type=!minecraft:illusioner] at @s run function rpg:lucifer_servant/dress
execute if entity @e[tag=rpg.lcs,type=!minecraft:item_display,limit=1] as @e[tag=rpg.lcs,type=!minecraft:item_display] at @s run function rpg:lucifer_servant/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.lcs.part,predicate=!rpg:lucifer_servant/riding,limit=1] run function rpg:lucifer_servant/orphans
