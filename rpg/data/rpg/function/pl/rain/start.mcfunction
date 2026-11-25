# 下血雨（管理员也可以直接执行）
scoreboard players set #rt rpg_pl 0
scoreboard players set #rain rpg_pl 240
execute in rpg:paradise_lost positioned 0 83 0 run tellraw @a[distance=0..] ["",{"text":"〖失乐园・血雨〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔅𝔩𝔬𝔬𝔡 ℜ𝔞𝔦𝔫","color":"#8F7430","bold":false,"italic":false},{"text":"  血从天上落下来。四分钟里怪物更强，精英更多，掉落更好。","color":"#9C9A94","bold":false,"italic":false}]
execute in rpg:paradise_lost positioned 0 83 0 as @a[distance=0..] at @s run playsound minecraft:entity.lightning_bolt.thunder weather @s ~ ~ ~ 0.7 0.6
