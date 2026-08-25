tag @s add rpg.inquest.intro
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[驱魔调查] ","color":"#DAA520","bold":true,"italic":false},{"text":"携带圣器见证五种招式中的任意三种；重复招式不会生成新罪证。","color":"gray","italic":false}]
execute if score @s rpg_dm_lord matches 1 as @a[tag=rpg.name.1,distance=..24,gamemode=!spectator] run function rpg:inquest/reminder/1
execute if score @s rpg_dm_lord matches 2 as @a[tag=rpg.name.2,distance=..24,gamemode=!spectator] run function rpg:inquest/reminder/2
execute if score @s rpg_dm_lord matches 3 as @a[tag=rpg.name.3,distance=..24,gamemode=!spectator] run function rpg:inquest/reminder/3
execute if score @s rpg_dm_lord matches 4 as @a[tag=rpg.name.4,distance=..24,gamemode=!spectator] run function rpg:inquest/reminder/4
execute if score @s rpg_dm_lord matches 5 as @a[tag=rpg.name.5,distance=..24,gamemode=!spectator] run function rpg:inquest/reminder/5
execute if score @s rpg_dm_lord matches 6 as @a[tag=rpg.name.6,distance=..24,gamemode=!spectator] run function rpg:inquest/reminder/6
execute if score @s rpg_dm_lord matches 7 as @a[tag=rpg.name.7,distance=..24,gamemode=!spectator] run function rpg:inquest/reminder/7
