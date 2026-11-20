execute if score @s rpg_sl_t matches 16 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo0] at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/echoes/warn
execute if score @s rpg_sl_t matches 30 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo0] run function rpg:saul_ghost/anim/enter/roll_f
execute if score @s rpg_sl_t matches 30..39 as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo0] at @s run function rpg:saul_boss/echoes/dash
execute if score @s rpg_sl_t matches 40 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo0] at @s run function rpg:saul_boss/echoes/hurt
execute if score @s rpg_sl_t matches 40 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo0] run function rpg:saul_ghost/anim/enter/thrust
execute if score @s rpg_sl_t matches 34 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo1] at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/echoes/warn
execute if score @s rpg_sl_t matches 48 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo1] run function rpg:saul_ghost/anim/enter/roll_f
execute if score @s rpg_sl_t matches 48..57 as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo1] at @s run function rpg:saul_boss/echoes/dash
execute if score @s rpg_sl_t matches 58 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo1] at @s run function rpg:saul_boss/echoes/hurt
execute if score @s rpg_sl_t matches 58 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo1] run function rpg:saul_ghost/anim/enter/thrust
execute if score @s rpg_sl_t matches 52 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo2] at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/echoes/warn
execute if score @s rpg_sl_t matches 66 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo2] run function rpg:saul_ghost/anim/enter/roll_f
execute if score @s rpg_sl_t matches 66..75 as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo2] at @s run function rpg:saul_boss/echoes/dash
execute if score @s rpg_sl_t matches 76 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo2] at @s run function rpg:saul_boss/echoes/hurt
execute if score @s rpg_sl_t matches 76 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo2] run function rpg:saul_ghost/anim/enter/thrust
execute if score @s rpg_sl_t matches 70 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo3] at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/echoes/warn
execute if score @s rpg_sl_t matches 84 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo3] run function rpg:saul_ghost/anim/enter/roll_f
execute if score @s rpg_sl_t matches 84..93 as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo3] at @s run function rpg:saul_boss/echoes/dash
execute if score @s rpg_sl_t matches 94 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo3] at @s run function rpg:saul_boss/echoes/hurt
execute if score @s rpg_sl_t matches 94 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo3] run function rpg:saul_ghost/anim/enter/thrust
execute if score @s rpg_sl_t matches 86 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo] at @s facing entity @e[type=minecraft:marker,tag=rpg.slb.center,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 88 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo] at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/echoes/warn
execute if score @s rpg_sl_t matches 88 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#D8DEE6","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔐𝔞𝔯𝔰𝔥𝔞𝔩","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"一起来！","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl_t matches 108 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo] run function rpg:saul_ghost/anim/enter/roll_f
execute if score @s rpg_sl_t matches 108..117 as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo] at @s run function rpg:saul_boss/echoes/dash
execute if score @s rpg_sl_t matches 118 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo] at @s run function rpg:saul_boss/echoes/hurt
execute if score @s rpg_sl_t matches 118 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo] run function rpg:saul_ghost/anim/enter/final
execute if score @s rpg_sl_t matches 124 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo] at @s run function rpg:saul_boss/echo/fade
execute if score @s rpg_sl_t matches 124 run function rpg:saul_boss/lesson/end
execute if score @s rpg_sl_t matches 126 run function rpg:saul_boss/skill/stagger
