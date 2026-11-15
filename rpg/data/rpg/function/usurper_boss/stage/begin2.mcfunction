tag @s remove rpg.usb.morph
tag @s remove rpg.usb.u1
tag @s remove rpg.usb.u2
tag @s remove rpg.usb.last1
data merge entity @s {NoAI:0b,Invulnerable:0b}
scoreboard players set @s rpg_ub 2
scoreboard players set #stage rpg_ub 2
scoreboard players set @s rpg_ub_c 0
scoreboard players set @s rpg_ub_n 0
scoreboard players set @s rpg_ub_k 0
scoreboard players set @s rpg_ub_b 20
scoreboard players set @s rpg_ub_x 0
scoreboard players set @s rpg_ub_sk 0
execute store result score @s rpg_ub_l run data get entity @s Health 10
# 第一件事是授权：召来圣卫
tag @s add rpg.usb.auth
bossbar set rpg:usurper_boss name {"text":"\ue234\ue1f5\ue1f1\ue1f9","font":"rpg:usurper_boss"}
scoreboard players set @s rpg_ub_s 20
function rpg:usurper_boss/music/2
particle minecraft:flash{color:16774876} ~ ~1.5 ~ 0 0 0 0 1 force
playsound minecraft:item.totem.use hostile @a[distance=..48] ~ ~ ~ 1 0.8
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#F0CF7A","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔘𝔰𝔲𝔯𝔭𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"第二阶段 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"权柄在我手里。现在，由我来命名真实。","color":"#9C9A94","bold":false,"italic":false}]
