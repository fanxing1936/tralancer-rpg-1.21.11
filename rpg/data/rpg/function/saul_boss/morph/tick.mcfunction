scoreboard players add @s rpg_sl_c 1
scoreboard players operation #c rpg_sl = @s rpg_sl_c
execute if score @s rpg_sl_c matches 1..16 as @e[tag=rpg.slb.shard,distance=..8] run function rpg:saul_boss/morph/shard
execute if score @s rpg_sl_c matches 1..30 run particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~ ~1.6 ~ 0.4 0.5 0.4 0 2
execute if score @s rpg_sl_c matches 16 run playsound minecraft:block.anvil.land hostile @a[distance=..32] ~ ~ ~ 0.8 0.7
execute if score @s rpg_sl_c matches 20 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔐𝔞𝔡 𝔎𝔦𝔫𝔤","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl_c matches 40 run function rpg:saul/anim/enter/hero
execute if score @s rpg_sl_c matches 40 run function rpg:saul_boss/vfx/rise
execute if score @s rpg_sl_c matches 44 run playsound rpg:saul.laugh hostile @a[distance=..40] ~ ~ ~ 1.4 0.7
execute if score @s rpg_sl_c matches 44 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔐𝔞𝔡 𝔎𝔦𝔫𝔤","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"第二阶段 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"斯塔福德……你又来了？哈哈哈……那就再来！","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl_c matches 86 run function rpg:saul_boss/stage/begin2
