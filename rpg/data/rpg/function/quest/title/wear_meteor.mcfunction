execute unless entity @s[tag=rpg.t.meteor] run return run tellraw @s ["",{"text":"[称号]","color":"#FFD85A","bold":true,"italic":false},{"text":"　还没得到这个称号。","color":"gray","bold":false,"italic":false}]
team join rpg_t_meteor @s
playsound minecraft:item.armor.equip_gold player @s ~ ~ ~ 1 1.2
