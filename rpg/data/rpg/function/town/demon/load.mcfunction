scoreboard objectives add rpg_dm dummy
scoreboard objectives add rpg_dm_do trigger
scoreboard objectives add rpg_dm_rep dummy
scoreboard objectives add rpg_dm_exp dummy
team add rpg_dm
team modify rpg_dm friendlyFire false
team modify rpg_dm color dark_purple
team modify rpg_dm prefix ["",{"text":"魔印 ","color":"#A276BE","bold":true,"italic":false}]
schedule function rpg:town/demon/sec 20t
