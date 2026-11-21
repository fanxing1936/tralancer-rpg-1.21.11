execute if data storage rpg:forge e{kind:"armor"} run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　源只能给武器","color":"#C04A3C","bold":false,"italic":false}]
execute if items entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents *[minecraft:custom_data~{holy_weapon_tag:1b}] run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　神圣武器接不住傲慢之源","color":"#C04A3C","bold":false,"italic":false}]
execute if data storage rpg:forge e{src:"pride"} run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　已经是这个源了","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set @s rpg_fg_op 4
scoreboard players set @s rpg_fg_arg 5
data modify storage rpg:forge d.cur set value "无"
execute if data storage rpg:forge e{src:"faith"} run data modify storage rpg:forge d.cur set value "[信念]"
execute if data storage rpg:forge e{src:"hope"} run data modify storage rpg:forge d.cur set value "[希望]"
execute if data storage rpg:forge e{src:"resolve"} run data modify storage rpg:forge d.cur set value "[不屈]"
execute if data storage rpg:forge e{src:"malice"} run data modify storage rpg:forge d.cur set value "[邪念]"
execute if data storage rpg:forge e{src:"hatred"} run data modify storage rpg:forge d.cur set value "[仇恨]"
execute if data storage rpg:forge e{src:"pride"} run data modify storage rpg:forge d.cur set value "[傲慢]"
function rpg:forge/op/src/show_pride with storage rpg:forge d
