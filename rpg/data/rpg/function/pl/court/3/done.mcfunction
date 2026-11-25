# 一座河庭打完（at 中心）
scoreboard players set #c3 rpg_pl 3
setblock ~ ~2 ~ minecraft:air
execute as @a[distance=..32,gamemode=!spectator] run loot give @s loot rpg:trial/ominous_key
execute as @a[distance=..32,gamemode=!spectator] run scoreboard players add @s rpg_ex_xp 12
execute as @a[distance=..32,gamemode=!spectator] if score @s rpg_pl_best matches ..14 run scoreboard players set @s rpg_pl_best 15
tellraw @a[distance=..48] ["",{"text":"〖失乐园・希底结河庭〗","color":"#E0483C","bold":true,"italic":false},{"text":" ℌ𝔦𝔡𝔡𝔢𝔨𝔢𝔩","color":"#8F7430","bold":false,"italic":false},{"text":"  五层都过了。宝库在南边，钥匙已经给你。","color":"#9C9A94","bold":false,"italic":false}]
