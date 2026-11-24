# 保惠师：12 格内友方生命恢复（美丽阶起 II）；每 10 秒，圣力者生命力再 +1（美丽阶起 +2）
scoreboard players operation #q rpg_fo = #now rpg_fo
scoreboard players operation #q rpg_fo /= #20 rpg_fo
scoreboard players operation #q2 rpg_fo = #q rpg_fo
scoreboard players operation #q rpg_fo %= #2 rpg_fo
scoreboard players operation #q2 rpg_fo %= #10 rpg_fo
execute if score #q rpg_fo matches 0 run particle minecraft:end_rod ~ ~0.3 ~ 5 0.2 5 0 10
execute unless score @s rpg_sef matches 5.. run execute if score #q rpg_fo matches 0 run effect give @a[distance=..12,gamemode=!spectator] minecraft:regeneration 3 0 true
execute unless score @s rpg_sef matches 5.. run execute if score #q2 rpg_fo matches 0 run scoreboard players add @a[distance=..12,scores={rpg_force=1}] rpg_vital 1
execute unless score @s rpg_sef matches 5.. run execute if score #q2 rpg_fo matches 0 run scoreboard players add @a[distance=..12,scores={rpg_force=3}] rpg_vital 1
execute if score @s rpg_sef matches 5.. run execute if score #q rpg_fo matches 0 run effect give @a[distance=..12,gamemode=!spectator] minecraft:regeneration 3 1 true
execute if score @s rpg_sef matches 5.. run execute if score #q2 rpg_fo matches 0 run scoreboard players add @a[distance=..12,scores={rpg_force=1}] rpg_vital 2
execute if score @s rpg_sef matches 5.. run execute if score #q2 rpg_fo matches 0 run scoreboard players add @a[distance=..12,scores={rpg_force=3}] rpg_vital 2
execute if score #q2 rpg_fo matches 0 run scoreboard players set @a[distance=..12,scores={rpg_vital=101..}] rpg_vital 100
