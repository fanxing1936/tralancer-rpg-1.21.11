# 右键法阵（as 法阵；@p 是右键的人）
execute if score #totem rpg_te matches 1 run return 0
execute unless items entity @p[tag=rpg.tw.in,distance=..6] weapon.mainhand minecraft:totem_of_undying run return run tellraw @p ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  拿着驱魔图腾右键法阵。","color":"#9C9A94","bold":false,"italic":false}]
item modify entity @p[tag=rpg.tw.in,distance=..6] weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
scoreboard players set #totem rpg_te 1
execute at @s run summon minecraft:item_display ~ ~1 ~ {Tags:["rpg.tw.ev"],item:{id:"minecraft:totem_of_undying",count:1},billboard:"vertical"}
execute at @s run playsound minecraft:block.wood.place player @a[distance=..16] ~ ~ ~ 1 0.8
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  图腾立起来了。现在扔驱魔圣水点燃它。","color":"#9C9A94","bold":false,"italic":false}]
