scoreboard players set @s rpg_ub_sk 15
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 142
# 神力超载（as/at 载体）
data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:1b}
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run tp @s ~ ~3 ~
function rpg:prime_enchanter/anim/enter/overcharge
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#F0CF7A","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔘𝔰𝔲𝔯𝔭𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"神力超载","color":"#E6DFCF","bold":false,"italic":false},{"text":"","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 1.4 0.6
playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..48] ~ ~ ~ 0.6 1.6
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~6 ~ ~6 positioned over motion_blocking_no_leaves align xyz run function rpg:usurper_boss/over/altar
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~-7 ~ ~6 positioned over motion_blocking_no_leaves align xyz run function rpg:usurper_boss/over/altar
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~6 ~ ~-7 positioned over motion_blocking_no_leaves align xyz run function rpg:usurper_boss/over/altar
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~-7 ~ ~-7 positioned over motion_blocking_no_leaves align xyz run function rpg:usurper_boss/over/altar
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run function rpg:usurper_boss/over/field
