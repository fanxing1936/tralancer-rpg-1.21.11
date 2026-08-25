execute if score @s rpg_dm_lord matches 1 as @p[distance=..20] run function rpg:inquest/give/core1
execute if score @s rpg_dm_lord matches 2 as @p[distance=..20] run function rpg:inquest/give/core2
execute if score @s rpg_dm_lord matches 3 as @p[distance=..20] run function rpg:inquest/give/core3
execute if score @s rpg_dm_lord matches 4 as @p[distance=..20] run function rpg:inquest/give/core4
execute if score @s rpg_dm_lord matches 5 as @p[distance=..20] run function rpg:inquest/give/core5
execute if score @s rpg_dm_lord matches 6 as @p[distance=..20] run function rpg:inquest/give/core6
execute if score @s rpg_dm_lord matches 7 as @p[distance=..20] run function rpg:inquest/give/core7
scoreboard players add @a[distance=..20,gamemode=!spectator] rpg_ex_xp 25
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[裁决·消灭] ","color":"#FF6B5E","bold":true,"italic":false},{"text":"恶魔形体崩解，留下完整武器核心。","color":"gray","italic":false}]
function rpg:taint/demon_boom
