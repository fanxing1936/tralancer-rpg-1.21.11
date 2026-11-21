execute unless data storage rpg:forge e{kind:"melee"} run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　[寒潮]只能镶在近战武器上","color":"#C04A3C","bold":false,"italic":false}]
execute if items entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents *[minecraft:custom_data~{jachin_tag:1b}] run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　双子武器靠换手作战，不开符石槽","color":"#C04A3C","bold":false,"italic":false}]
execute if items entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents *[minecraft:custom_data~{boaz_tag:1b}] run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　双子武器靠换手作战，不开符石槽","color":"#C04A3C","bold":false,"italic":false}]
execute if data storage rpg:forge e{stone:"frost"} run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　已经镶着这枚符石了","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set @s rpg_fg_op 6
scoreboard players set @s rpg_fg_arg 1
data modify storage rpg:forge d.cur set value "空"
execute if data storage rpg:forge e{stone:"rift"} run data modify storage rpg:forge d.cur set value "[裂地]（退回背包）"
execute if data storage rpg:forge e{stone:"frost"} run data modify storage rpg:forge d.cur set value "[寒潮]（退回背包）"
execute if data storage rpg:forge e{stone:"shadow"} run data modify storage rpg:forge d.cur set value "[影步]（退回背包）"
execute if data storage rpg:forge e{stone:"blood"} run data modify storage rpg:forge d.cur set value "[血祭]（退回背包）"
execute if data storage rpg:forge e{stone:"gale"} run data modify storage rpg:forge d.cur set value "[风墙]（退回背包）"
execute if data storage rpg:forge e{stone:"volley"} run data modify storage rpg:forge d.cur set value "[箭雨]（退回背包）"
execute if data storage rpg:forge e{stone:"banner"} run data modify storage rpg:forge d.cur set value "[战旗]（退回背包）"
function rpg:forge/op/stone/show_frost with storage rpg:forge d
