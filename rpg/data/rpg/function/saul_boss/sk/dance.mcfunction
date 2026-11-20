execute unless entity @e[tag=rpg.unit.f,distance=..48] run return run function rpg:saul_boss/dance/abort
execute if score @s rpg_sl_t matches 16 run execute at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] rotated 0 0 positioned ^ ^ ^7 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
execute if score @s rpg_sl_t matches 16 run execute at @s run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 17 run execute at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/dance/warn
execute if score @s rpg_sl_t matches 17 run function rpg:saul/anim/enter/roll_f
execute if score @s rpg_sl_t matches 23..29 run function rpg:saul_boss/dance/step
execute if score @s rpg_sl_t matches 29 run function rpg:saul/anim/enter/final
execute if score @s rpg_sl_t matches 29 run playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.2 0.80
execute if score @s rpg_sl_t matches 30 run execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 8 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
execute if score @s rpg_sl_t matches 30 run tag @e[tag=rpg.unit] remove rpg.slb.hit
execute if score @s rpg_sl_t matches 30 run execute at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] rotated 60 0 positioned ^ ^ ^7 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
execute if score @s rpg_sl_t matches 30 run execute at @s run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 31 run execute at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/dance/warn
execute if score @s rpg_sl_t matches 31 run function rpg:saul/anim/enter/roll_f
execute if score @s rpg_sl_t matches 37..43 run function rpg:saul_boss/dance/step
execute if score @s rpg_sl_t matches 43 run function rpg:saul/anim/enter/final
execute if score @s rpg_sl_t matches 43 run playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.2 0.92
execute if score @s rpg_sl_t matches 44 run execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 8 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
execute if score @s rpg_sl_t matches 44 run tag @e[tag=rpg.unit] remove rpg.slb.hit
execute if score @s rpg_sl_t matches 44 run execute at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] rotated 120 0 positioned ^ ^ ^7 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
execute if score @s rpg_sl_t matches 44 run execute at @s run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 45 run execute at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/dance/warn
execute if score @s rpg_sl_t matches 45 run function rpg:saul/anim/enter/roll_f
execute if score @s rpg_sl_t matches 51..57 run function rpg:saul_boss/dance/step
execute if score @s rpg_sl_t matches 57 run function rpg:saul/anim/enter/final
execute if score @s rpg_sl_t matches 57 run playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.2 1.04
execute if score @s rpg_sl_t matches 58 run execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 8 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
execute if score @s rpg_sl_t matches 58 run tag @e[tag=rpg.unit] remove rpg.slb.hit
execute if score @s rpg_sl_t matches 58 run execute at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] rotated 180 0 positioned ^ ^ ^7 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
execute if score @s rpg_sl_t matches 58 run execute at @s run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 59 run execute at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/dance/warn
execute if score @s rpg_sl_t matches 59 run function rpg:saul/anim/enter/roll_f
execute if score @s rpg_sl_t matches 65..71 run function rpg:saul_boss/dance/step
execute if score @s rpg_sl_t matches 71 run function rpg:saul/anim/enter/final
execute if score @s rpg_sl_t matches 71 run playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.2 1.16
execute if score @s rpg_sl_t matches 72 run execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 8 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
execute if score @s rpg_sl_t matches 72 run tag @e[tag=rpg.unit] remove rpg.slb.hit
execute if score @s rpg_sl_t matches 72 run execute at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] rotated 240 0 positioned ^ ^ ^7 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
execute if score @s rpg_sl_t matches 72 run execute at @s run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 73 run execute at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/dance/warn
execute if score @s rpg_sl_t matches 73 run function rpg:saul/anim/enter/roll_f
execute if score @s rpg_sl_t matches 79..85 run function rpg:saul_boss/dance/step
execute if score @s rpg_sl_t matches 85 run function rpg:saul/anim/enter/final
execute if score @s rpg_sl_t matches 85 run playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.2 1.28
execute if score @s rpg_sl_t matches 86 run execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 8 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
execute if score @s rpg_sl_t matches 86 run tag @e[tag=rpg.unit] remove rpg.slb.hit
execute if score @s rpg_sl_t matches 86 run execute at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] rotated 300 0 positioned ^ ^ ^7 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
execute if score @s rpg_sl_t matches 86 run execute at @s run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 87 run execute at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/dance/warn
execute if score @s rpg_sl_t matches 87 run function rpg:saul/anim/enter/roll_f
execute if score @s rpg_sl_t matches 93..99 run function rpg:saul_boss/dance/step
execute if score @s rpg_sl_t matches 99 run function rpg:saul/anim/enter/final
execute if score @s rpg_sl_t matches 99 run playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.2 1.40
execute if score @s rpg_sl_t matches 100 run execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 8 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
execute if score @s rpg_sl_t matches 100 run tag @e[tag=rpg.unit] remove rpg.slb.hit
execute if score @s rpg_sl_t matches 98 run function rpg:saul_boss/dance/glow
execute if score @s rpg_sl_t matches 98 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……斩！","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl_t matches 110 run function rpg:saul_boss/dance/burst
execute if score @s rpg_sl_t matches 111 run execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 16 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
execute if score @s rpg_sl_t matches 111 run tag @e[tag=rpg.unit] remove rpg.slb.hit
execute if score @s rpg_sl_t matches 114 run data merge entity @s {Invulnerable:0b}
execute if score @s rpg_sl_t matches 114 run function rpg:saul/anim/enter/kneel
execute if score @s rpg_sl_t matches 114 run attribute @s minecraft:armor base set 0
execute if score @s rpg_sl_t matches 114 run tag @s add rpg.slb.weak
execute if score @s rpg_sl_t matches 116 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……哈。哈哈……真是，老了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl_t matches 180.. run function rpg:saul_boss/sk/end
