scoreboard players add @s rpg_dt_t 1
execute if score @s rpg_dt_q matches 1 run return run function rpg:daath_fight/end/sever
execute if score @s rpg_dt_q matches 2 run return run function rpg:daath_fight/end/accept
execute if score @s rpg_dt_t matches ..20 run return 0
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ~ ~0.8 ~ 0.4 0.6 0.4 0 1
execute as @e[type=minecraft:interaction,tag=rpg.dt.touch,distance=..4,limit=1] if data entity @s attack run scoreboard players set @e[type=minecraft:vindicator,tag=rpg.dtb,tag=rpg.dt.it] rpg_dt_q 1
execute as @e[type=minecraft:interaction,tag=rpg.dt.touch,distance=..4,limit=1] if data entity @s interaction run scoreboard players set @e[type=minecraft:vindicator,tag=rpg.dtb,tag=rpg.dt.it] rpg_dt_q 2
execute if score @s rpg_dt_t matches 1200.. run scoreboard players set @s rpg_dt_q 2
execute if score @s rpg_dt_q matches 1.. run function rpg:daath_fight/end/pick
