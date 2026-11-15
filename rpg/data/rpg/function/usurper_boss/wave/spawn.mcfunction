# 一波（as/at 载体）：场上不足 4 名才召，两侧各一名
function rpg:usurper/anim/enter/enchant
scoreboard players set @s rpg_ub_busy 40
execute store result score #n rpg_ub if entity @e[tag=rpg.usb.unit]
execute if score #n rpg_ub matches ..3 positioned ^3.5 ^ ^1 run function rpg:usurper_boss/wave/one
execute store result score #n rpg_ub if entity @e[tag=rpg.usb.unit]
execute if score #n rpg_ub matches ..3 positioned ^-3.5 ^ ^1 run function rpg:usurper_boss/wave/one
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#B784D6","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"七十二柱召役 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"七十二柱，听候所罗门之名。","color":"#9C9A94","bold":false,"italic":false}]
