# 玛门罪仆每刻入口。任何途径召出的第 7 柱罪仆（手动、仪式二阶段）都在这里换装。
execute if entity @e[tag=rpg.demon.minion.lord7,tag=!rpg.mms,type=!minecraft:illusioner,limit=1] as @e[tag=rpg.demon.minion.lord7,tag=!rpg.mms,type=!minecraft:illusioner] at @s run function rpg:mammon_servant/dress
execute if entity @e[tag=rpg.mms,type=!minecraft:item_display,limit=1] as @e[tag=rpg.mms,type=!minecraft:item_display] at @s run function rpg:mammon_servant/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.mms.part,predicate=!rpg:mammon_servant/riding,limit=1] run function rpg:mammon_servant/orphans
