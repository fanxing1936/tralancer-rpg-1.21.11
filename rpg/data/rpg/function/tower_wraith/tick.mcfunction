# 幽魂罪仆每刻入口。任何途径召出的亚巴顿罪仆（手动、仪式二阶段）都在这里换装。
execute if entity @e[tag=rpg.demon.minion.lord3,tag=!rpg.tw,type=!minecraft:illusioner,limit=1] as @e[tag=rpg.demon.minion.lord3,tag=!rpg.tw,type=!minecraft:illusioner] at @s run function rpg:tower_wraith/dress
execute if entity @e[tag=rpg.tw,type=!minecraft:item_display,limit=1] as @e[tag=rpg.tw,type=!minecraft:item_display] at @s run function rpg:tower_wraith/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tw.part,predicate=!rpg:tower_wraith/riding,limit=1] run function rpg:tower_wraith/orphans
