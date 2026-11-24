scoreboard players set #mw rpg_pl 0
scoreboard players set #moon rpg_pl 180
execute in rpg:paradise_lost positioned 0 83 0 run tellraw @a[distance=0..] ["",{"text":"〖失乐园・血月〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔅𝔩𝔬𝔬𝔡 𝔐𝔬𝔬𝔫","color":"#8F7430","bold":false,"italic":false},{"text":"  天上开始落血。三分钟内怪更多，掉落翻倍。","color":"#9C9A94","bold":false,"italic":false}]
execute in rpg:paradise_lost positioned 0 83 0 run playsound minecraft:ambient.crimson_forest.mood master @a[distance=0..] ~ ~ ~ 2 0.5
