# 萨麦尔罪仆每刻入口。任何途径召出的第 5 柱罪仆（手动、仪式二阶段）都在这里换装。
execute if entity @e[tag=rpg.demon.minion.lord5,tag=!rpg.sms,type=!minecraft:illusioner,limit=1] as @e[tag=rpg.demon.minion.lord5,tag=!rpg.sms,type=!minecraft:illusioner] at @s run function rpg:samael_servant/dress
execute if entity @e[tag=rpg.sms,type=!minecraft:item_display,limit=1] as @e[tag=rpg.sms,type=!minecraft:item_display] at @s run function rpg:samael_servant/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.sms.part,predicate=!rpg:samael_servant/riding,limit=1] run function rpg:samael_servant/orphans
