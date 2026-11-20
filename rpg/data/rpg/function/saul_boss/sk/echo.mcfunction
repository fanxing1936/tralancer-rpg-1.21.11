execute if score @s rpg_sl_t matches 3 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo] run function rpg:saul_ghost/anim/enter/idle
execute if score @s rpg_sl_t matches 22 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo] run function rpg:saul_ghost/anim/enter/thrust
execute if score @s rpg_sl_t matches 24 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo] at @s run function rpg:saul_boss/echo/strike
execute if score @s rpg_sl_t matches 36 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,tag=rpg.slb.echo] at @s run function rpg:saul_boss/echo/fade
execute if score @s rpg_sl_t matches 48.. run function rpg:saul_boss/sk/end
