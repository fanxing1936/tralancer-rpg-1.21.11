function rpg:inquest/seal/reindex
data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[]}
scoreboard players add @s rpg_agit 0
execute store result storage rpg:panel v.rpg_agit int 1 run scoreboard players get @s rpg_agit
scoreboard players add @s rpg_case1 0
execute store result storage rpg:panel v.rpg_case1 int 1 run scoreboard players get @s rpg_case1
scoreboard players add @s rpg_case2 0
execute store result storage rpg:panel v.rpg_case2 int 1 run scoreboard players get @s rpg_case2
scoreboard players add @s rpg_case3 0
execute store result storage rpg:panel v.rpg_case3 int 1 run scoreboard players get @s rpg_case3
scoreboard players add @s rpg_case4 0
execute store result storage rpg:panel v.rpg_case4 int 1 run scoreboard players get @s rpg_case4
scoreboard players add @s rpg_case5 0
execute store result storage rpg:panel v.rpg_case5 int 1 run scoreboard players get @s rpg_case5
scoreboard players add @s rpg_case6 0
execute store result storage rpg:panel v.rpg_case6 int 1 run scoreboard players get @s rpg_case6
scoreboard players add @s rpg_case7 0
execute store result storage rpg:panel v.rpg_case7 int 1 run scoreboard players get @s rpg_case7
function rpg:panel/pages/panel_inquest with storage rpg:panel v
function rpg:panel/ui/show with storage rpg:panel ui
