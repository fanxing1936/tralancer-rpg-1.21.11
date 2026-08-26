scoreboard players set @s rpg_ch1_sub 1
scoreboard players set @s rpg_ch1_time 0
tag @s remove rpg.ch1.theory.1
tag @s remove rpg.ch1.theory.2
bossbar set rpg:chapter1 name ["",{"text":"假说审判｜找出并排除两个伪解","color":"#B8A98B","bold":true,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[假说审判] ","color":"#B8A98B","bold":true,"italic":false},{"text":"踏入两个无法同时解释全部证物的伪解；不要把仍需验证的‘暴食寄生’提前排除。","color":"gray","bold":false,"italic":false}]
function rpg:campaign/beelzebub/hypothesis_board/spawn_choices
