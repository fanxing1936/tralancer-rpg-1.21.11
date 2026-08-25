scoreboard players set @s rpg_ex_kind 0
function rpg:inquest/stability/hit20
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..10]
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[伪名坐实] ","color":"dark_red","bold":true,"italic":false},{"text":"无人宣认真名，法阵承认了谎言。","color":"gray","italic":false}]
