execute as @a[scores={rpg_q_do=1..}] at @s run function rpg:quest/press
scoreboard players remove @a[scores={rpg_q_st=1..}] rpg_q_st 1
execute as @a[scores={rpg_q_st=0}] run function rpg:quest/sub_off
scoreboard players remove @a[scores={rpg_q_mt=1..}] rpg_q_mt 1
execute as @a[scores={rpg_q_mt=0}] run function rpg:quest/music_off
scoreboard players add #t rpg_q_st 1
execute if score #t rpg_q_st matches 20.. run function rpg:quest/sec
