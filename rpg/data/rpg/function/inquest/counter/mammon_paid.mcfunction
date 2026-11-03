scoreboard players set @s rpg_ex_kind 0
scoreboard players set @s rpg_ex_ransom 0
scoreboard players set @s rpg_ex_counter 220
function rpg:inquest/stability/restore
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"〖赎金已付〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"账目暂平，宣判继续。","color":"#9C9A94","italic":false}]
