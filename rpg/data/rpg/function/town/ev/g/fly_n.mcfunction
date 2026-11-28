summon minecraft:silverfish ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.fly"],PersistenceRequired:1b,CustomName:{"text":"蝇群","color":"#B5D957","bold":false,"italic":false}}
particle minecraft:dust{color:[0.2,0.25,0.08],scale:1.2} ~ ~0.5 ~ 0.6 0.4 0.6 0 16
scoreboard players remove #k rpg_te 1
execute if score #k rpg_te matches 1.. run function rpg:town/ev/g/fly_n
