# 一座河庭打完（at 中心）
scoreboard players set #c2 rpg_pl 3
setblock ~ ~1 ~ minecraft:air
execute as @a[distance=..32,gamemode=!spectator] run loot give @s loot rpg:trial/key
execute as @a[distance=..32,gamemode=!spectator] run scoreboard players add @s rpg_ex_xp 12
execute as @a[distance=..32,gamemode=!spectator] if score @s rpg_pl_best matches ..9 run scoreboard players set @s rpg_pl_best 10
tellraw @a[distance=..48] ["",{"text":"〖失乐园・基训河庭〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔊𝔦𝔥𝔬𝔫","color":"#8F7430","bold":false,"italic":false},{"text":"  五层都过了。宝库在南边，钥匙已经给你。","color":"#9C9A94","bold":false,"italic":false}]
execute as @a[distance=..32,gamemode=!spectator] run function rpg:paths/court
