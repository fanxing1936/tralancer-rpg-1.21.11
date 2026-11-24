scoreboard players set #t rpg_q_st 0
scoreboard players enable @a rpg_q_do
execute as @a[scores={rpg_ob=100,rpg_sef=1..}] unless score @s rpg_q1 matches 1.. run function rpg:quest/start_1
function rpg:quest/egg/sec
