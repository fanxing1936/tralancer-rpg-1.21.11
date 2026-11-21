# 装备养成的每刻入口（#minecraft:tick，排在 rpg:command/tick_end 之前）。
execute as @a[tag=rpg.fg.ui] run function rpg:forge/ui/lock
execute as @a[scores={rpg_fg_do=1..}] at @s run function rpg:forge/ui/do
scoreboard players add #clk rpg_fg 1
scoreboard players operation #c10 rpg_fg = #clk rpg_fg
scoreboard players operation #c10 rpg_fg %= #10 rpg_fg
scoreboard players operation #c40 rpg_fg = #clk rpg_fg
scoreboard players operation #c40 rpg_fg %= #40 rpg_fg
execute as @a at @s run function rpg:forge/player
execute as @e[tag=rpg.hurt] at @s run function rpg:forge/hit/victim
execute as @e[scores={rpg_fg_ec=1..}] at @s run function rpg:forge/rune/echo_tick
execute as @e[scores={rpg_fg_bt=1..}] run function rpg:forge/rune/ember_decay
execute as @e[scores={rpg_fg_mt=1..}] at @s run function rpg:forge/rune/hunt_decay
execute as @e[type=#minecraft:arrows,tag=rpg.fg.meteor] at @s run function rpg:forge/rune/meteor_tick
execute as @e[type=minecraft:marker,tag=rpg.fg.smelt] at @s run function rpg:forge/smelt/tick
execute as @e[type=minecraft:marker,tag=rpg.fg.fire] run function rpg:forge/smelt/fire_tick
execute as @e[type=minecraft:marker,tag=rpg.fg.fx] at @s run function rpg:forge/stone/fx_tick
execute as @a run function rpg:forge/player_late
