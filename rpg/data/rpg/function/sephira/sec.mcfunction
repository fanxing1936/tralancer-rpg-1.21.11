# 每秒一次（as/at 玩家）
scoreboard players enable @s rpg_sef_do
execute unless score @s rpg_sef_mig matches 1 run function rpg:sephira/mig/run
execute unless score @s rpg_sef_day = #day rpg_sef run function rpg:sephira/day
execute unless score @s rpg_force matches 0.. if score @s rpg_ident matches 1.. run function rpg:sephira/force/assign
execute if score #m2 rpg_sef matches 0 run function rpg:sephira/tier/check
execute if score @s rpg_force matches 1.. run function rpg:sephira/force/sec
execute if score @s rpg_sef_lcd matches 1.. run scoreboard players remove @s rpg_sef_lcd 1
# 慈悲柱第 9 阶：6 格内友方抗性 I
execute if score #m2 rpg_sef matches 0 if score @s rpg_pillar matches 2 if score @s rpg_sef matches 9.. run effect give @a[distance=..6,gamemode=!spectator] minecraft:resistance 3 0 true
