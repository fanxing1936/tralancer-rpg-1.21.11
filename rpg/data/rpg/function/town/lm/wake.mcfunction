# 每秒：恶魔阵营的人走近孤堡，站岗的醒过来
execute as @e[tag=rpg.lm.guard,tag=!rpg.lm.awake] at @s if entity @a[tag=rpg.dm,distance=..20,gamemode=!spectator] run function rpg:town/lm/wake_one
