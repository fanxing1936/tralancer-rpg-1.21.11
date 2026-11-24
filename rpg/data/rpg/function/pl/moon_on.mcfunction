scoreboard players remove #moon rpg_pl 1
execute in rpg:paradise_lost positioned 0 83 0 as @a[distance=36..,gamemode=!spectator] at @s run particle minecraft:falling_dust{block_state:{Name:"minecraft:redstone_block"}} ~ ~8 ~ 8 2 8 0 60
scoreboard players operation #q rpg_pl = #moon rpg_pl
scoreboard players set #15 rpg_pl 15
scoreboard players operation #q rpg_pl %= #15 rpg_pl
execute if score #q rpg_pl matches 0 in rpg:paradise_lost positioned 0 83 0 as @a[distance=44..,gamemode=!spectator,gamemode=!creative] at @s run function rpg:pl/moon_wave
execute if score #moon rpg_pl matches 0 in rpg:paradise_lost positioned 0 83 0 run tellraw @a[distance=0..] ["",{"text":"〖失乐园・血月〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔅𝔩𝔬𝔬𝔡 𝔐𝔬𝔬𝔫","color":"#8F7430","bold":false,"italic":false},{"text":"  血停了。","color":"#9C9A94","bold":false,"italic":false}]
