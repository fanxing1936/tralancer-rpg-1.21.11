# 二阶段打完：倒地（原作死亡动作），王冠碎裂，权柄归还，约 6 秒后胜利。
function rpg:usurper_boss/refill
tag @s add rpg.usb.end
scoreboard players set @s rpg_ub_c 0
scoreboard players set @s rpg_ub_sk 0
data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}
function rpg:usurper_boss/altar_clear
kill @e[tag=rpg.usb.fx]
execute as @e[tag=rpg.usb.guard] run function rpg:holy_guard/remove
tag @s remove rpg.usb.exposed
tag @s remove rpg.usb.guarded
tag @s remove rpg.usb.auth
tag @s remove rpg.usb.reauth
tag @e[tag=rpg.unit] remove rpg.usb.shit
tag @e[tag=rpg.unit] remove rpg.usb.dhit
execute if entity @s[tag=rpg.usb.s2] run function rpg:prime_enchanter/anim/enter/death
playsound minecraft:entity.evoker.death hostile @a[distance=..48] ~ ~ ~ 1.2 0.6
playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..48] ~ ~ ~ 0.8 0.7
bossbar set rpg:usurper_boss value 0
bossbar set rpg:usurper_boss name {"text":"\ue220\ue1f5\ue1f1\ue1f9","font":"rpg:usurper_boss"}
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#F0CF7A","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔘𝔰𝔲𝔯𝔭𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……权柄，从来就不是能偷来的东西。","color":"#9C9A94","bold":false,"italic":false}]
