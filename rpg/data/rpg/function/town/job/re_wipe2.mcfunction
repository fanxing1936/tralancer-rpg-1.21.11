# 清掉这座镇上的人、骑在他们身上的模型与名牌、道具、锚点（positioned 镇中心）
execute as @e[type=minecraft:villager,tag=rpg.tnpc,distance=..170] on passengers run kill @s
kill @e[type=minecraft:villager,tag=rpg.tnpc,distance=..170]
execute as @e[type=minecraft:villager,tag=rpg.mer.smith,distance=..170] on passengers run kill @s
kill @e[type=minecraft:villager,tag=rpg.mer.smith,distance=..170]
execute as @e[tag=rpg.tw.guard,distance=..170] on passengers run kill @s
kill @e[tag=rpg.tw.guard,distance=..170]
kill @e[type=minecraft:interaction,tag=rpg.tnpc,distance=..170]
kill @e[type=minecraft:text_display,tag=rpg.tnpc.plate,distance=..170]
kill @e[tag=rpg.tw.prop,distance=..170]
kill @e[type=minecraft:marker,tag=rpg.tw.a,distance=..170]
tellraw @a[distance=..200] ["",{"text":"〖城镇〗","color":"#E6DFCF","bold":true,"italic":false},{"text":"  这座镇在重修：林中营地挪去了镇外。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #cur rpg_tw matches 1 run function rpg:town/job/re_clear/1
execute if score #cur rpg_tw matches 2 run function rpg:town/job/re_clear/2
execute if score #cur rpg_tw matches 4 run function rpg:town/job/re_clear/4
execute if score #cur rpg_tw matches 6 run function rpg:town/job/re_clear/6
execute if score #cur rpg_tw matches 7 run function rpg:town/job/re_clear/7
execute if score #cur rpg_tw matches 9 run function rpg:town/job/re_clear/9
execute if score #cur rpg_tw matches 10 run function rpg:town/job/re_clear/10
execute if score #cur rpg_tw matches 12 run function rpg:town/job/re_clear/12
execute if score #cur rpg_tw matches 14 run function rpg:town/job/re_clear/14
execute if score #cur rpg_tw matches 15 run function rpg:town/job/re_clear/15
execute if score #cur rpg_tw matches 17 run function rpg:town/job/re_clear/17
execute if score #cur rpg_tw matches 18 run function rpg:town/job/re_clear/18
execute if score #cur rpg_tw matches 19 run function rpg:town/job/re_clear/19
execute if score #cur rpg_tw matches 20 run function rpg:town/job/re_clear/20
