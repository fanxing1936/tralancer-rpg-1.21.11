# 洗炼钻在抽的时候就消耗；结果先挂在装备上，等你二选一。
execute store result score #pq rpg_fg run random value -10..15
execute store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.pq int 1 run scoreboard players get #pq rpg_fg
function rpg:forge/wb/save_off
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.2
