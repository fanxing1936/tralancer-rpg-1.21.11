# 过场：圣器反噬。人倒下了，圣力还在。旋风放完 7 秒才碎；他要是已被一击打穿，直接碎。
scoreboard players set #stage rpg_pf 3
scoreboard players set #t rpg_pf 0
# 还没落下的天罚、光束、圣印到这里全部作废。
kill @e[tag=rpg.pope.fx]
execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1] run function rpg:pope_fight/boss/show
execute unless entity @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1] run scoreboard players set #t rpg_pf 139
execute as @e[type=minecraft:vindicator,tag=rpg.pf.unit] run function rpg:tower_guard/ai/remove
execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1] run data merge entity @s {Invulnerable:1b}
execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1] run function rpg:pope_fight/clip/whirlwind
execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1] at @s run tp @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] ~ ~ ~
bossbar set minecraft:pope name {"text":"","font":"rpg:pope_fx"}
execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1] at @s positioned ~ ~2.4 ~ run function rpg:pope_fight/fx/halo_long
execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1] at @s run function rpg:pope_fight/fx/vortex
bossbar set minecraft:pope value 0
tellraw @a[distance=..48] ["",{"text":"〖教皇〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔓𝔬𝔭𝔢","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣器……在吃我……","color":"#9C9A94","bold":false,"italic":false}]
