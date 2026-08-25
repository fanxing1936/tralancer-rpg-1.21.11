scoreboard players set @s rpg_ex_kind 0
scoreboard players set @s rpg_ex_ransom 0
scoreboard players set @s rpg_ex_counter 220
function rpg:inquest/stability/restore
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[赎金已付] ","color":"#FFD85A","bold":true,"italic":false},{"text":"账目暂平，宣判继续。","color":"gray","italic":false}]
