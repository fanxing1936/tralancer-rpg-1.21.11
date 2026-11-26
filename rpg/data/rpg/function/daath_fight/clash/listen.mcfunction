execute at @a[tag=rpg.dt.me,limit=1] run tp @e[type=minecraft:interaction,tag=rpg.dt.clk,distance=..20] ~ ~-0.5 ~
scoreboard players set #w rpg_dt 0
execute as @e[type=minecraft:interaction,tag=rpg.dt.clk,distance=..30] if data entity @s attack run scoreboard players set #w rpg_dt 1
execute as @e[type=minecraft:interaction,tag=rpg.dt.clk,distance=..30] if data entity @s interaction run scoreboard players set #w rpg_dt 1
execute if score #w rpg_dt matches 1 run function rpg:daath_fight/clash/win
