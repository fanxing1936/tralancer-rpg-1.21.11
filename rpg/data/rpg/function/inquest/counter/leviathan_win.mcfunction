scoreboard players set @s rpg_ex_kind 0
function rpg:inquest/stability/restore
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[妒影击破] ","color":"#3DA9E8","bold":true,"italic":false},{"text":"被复制的力量回流法阵。","color":"gray","italic":false}]
