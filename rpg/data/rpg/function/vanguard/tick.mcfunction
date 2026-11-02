# 先锋罪仆每刻入口。任何途径召出的别西卜罪仆（手动、仪式二阶段）都在这里换装。
execute if entity @e[tag=rpg.demon.minion.lord4,tag=!rpg.vg,type=!minecraft:illusioner,limit=1] as @e[tag=rpg.demon.minion.lord4,tag=!rpg.vg,type=!minecraft:illusioner] at @s run function rpg:vanguard/dress
execute if entity @e[tag=rpg.vg,type=!minecraft:item_display,limit=1] as @e[tag=rpg.vg,type=!minecraft:item_display] at @s run function rpg:vanguard/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.vg.part,predicate=!rpg:vanguard/riding,limit=1] run function rpg:vanguard/orphans
