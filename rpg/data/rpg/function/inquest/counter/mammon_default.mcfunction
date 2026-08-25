scoreboard players set @s rpg_ex_kind 0
scoreboard players set @s rpg_ex_ransom 0
function rpg:inquest/stability/hit25
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[逾期加征] ","color":"dark_red","bold":true,"italic":false},{"text":"无人付账，玛门从法阵本身收取代价。","color":"gray","italic":false}]
