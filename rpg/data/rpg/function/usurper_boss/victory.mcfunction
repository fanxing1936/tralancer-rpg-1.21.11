# 原质：记打过、给阅历（add_sephira.py）
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run function rpg:sephira/boss/usurper
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run particle minecraft:flash{color:16774876} ~ ~2 ~ 0 0 0 0 1 force
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run playsound minecraft:block.beacon.deactivate hostile @a[distance=..48] ~ ~ ~ 1.2 0.8
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run tellraw @a[distance=..48] ["",{"text":"〖约翰福音 10:10〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"盗贼来，无非要偷窃，杀害，毁坏。","color":"#E6DFCF","bold":false,"italic":false}]
# 装备养成：邪念之源与符石
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run loot spawn ~ ~1 ~ loot rpg:forge/boss/malice
function rpg:usurper_boss/clear
