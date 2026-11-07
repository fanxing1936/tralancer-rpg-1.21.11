# 倒下（判定体可能已被打穿）。模型留到动作放完。
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] at @s run tp @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] ~ ~ ~
function rpg:pope_fight/heart/weak_off
kill @e[type=minecraft:vindicator,tag=rpg.pf.heart]
tag @a[tag=rpg.pf.tgt] remove rpg.pf.tgt
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.face] at @s run function rpg:arch_visage/internal/clear
kill @e[tag=rpg.pope.fx]
scoreboard players set #stage rpg_pf 5
scoreboard players set #t rpg_pf 0
bossbar set minecraft:pope value 0
bossbar set minecraft:pope name {"text":"","font":"rpg:pope_fx"}
function rpg:pope_fight/heart/clip/death
tellraw @a[distance=..48] ["",{"text":"〖末影之心〗","color":"#A276BE","bold":true,"italic":false},{"text":" ℌ𝔢𝔞𝔯𝔱 𝔬𝔣 𝔈𝔫𝔡𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……结束了……吗……","color":"#9C9A94","bold":false,"italic":false}]
