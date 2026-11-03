execute if score @s rpg_dm_lord matches 1 as @p[distance=..20] run function rpg:inquest/give/core1
execute if score @s rpg_dm_lord matches 2 as @p[distance=..20] run function rpg:inquest/give/core2
execute if score @s rpg_dm_lord matches 3 as @p[distance=..20] run function rpg:inquest/give/core3
execute if score @s rpg_dm_lord matches 4 as @p[distance=..20] run function rpg:inquest/give/core4
execute if score @s rpg_dm_lord matches 5 as @p[distance=..20] run function rpg:inquest/give/core5
execute if score @s rpg_dm_lord matches 6 as @p[distance=..20] run function rpg:inquest/give/core6
execute if score @s rpg_dm_lord matches 7 as @p[distance=..20] run function rpg:inquest/give/core7
scoreboard players add @a[distance=..20,gamemode=!spectator] rpg_ex_xp 25
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"〖裁决・消灭〗","color":"#C04A3C","bold":true,"italic":false},{"text":" 𝔄𝔫𝔫𝔦𝔥𝔦𝔩𝔞𝔱𝔢","color":"#7D3027","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"恶魔形体崩解，留下完整武器核心。","color":"#9C9A94","italic":false}]
function rpg:taint/demon_boom
