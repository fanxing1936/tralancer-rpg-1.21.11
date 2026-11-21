function rpg:forge/op/gild/scan
execute if score #n rpg_fg matches 0 run item modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents {function:"minecraft:enchant_randomly",only_compatible:true}
execute if score #n rpg_fg matches 0 run function rpg:forge/op/gild/scan
execute if score #n rpg_fg matches 0 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　这件装备附不上任何附魔，镀金箔没有消耗","color":"#C04A3C","bold":false,"italic":false}]
scoreboard players remove #n rpg_fg 1
execute store result storage rpg:forge d.m int 1 run scoreboard players get #n rpg_fg
function rpg:forge/op/gild/pick with storage rpg:forge d
function rpg:forge/op/gild/up with storage rpg:forge pick
data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.gild set value 1b
data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.gk set from storage rpg:forge pick.k
execute store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.gl int 1 run scoreboard players get #gl rpg_fg
function rpg:forge/render
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
playsound minecraft:item.totem.use player @s ~ ~ ~ 0.6 1.6
particle minecraft:wax_on ~ ~1 ~ 0.4 0.6 0.4 0.6 40
