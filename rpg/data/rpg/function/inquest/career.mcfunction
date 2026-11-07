scoreboard players add @s rpg_ex_xp 0
scoreboard players add @s rpg_ex_lvl 0
scoreboard players add @s rpg_ex_path 0
scoreboard players add @s rpg_ex_slots 0
function rpg:inquest/career/sync
data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[]}
scoreboard players add @s rpg_ex_lvl 0
execute store result storage rpg:panel v.rpg_ex_lvl int 1 run scoreboard players get @s rpg_ex_lvl
scoreboard players add @s rpg_ex_slots 0
execute store result storage rpg:panel v.rpg_ex_slots int 1 run scoreboard players get @s rpg_ex_slots
scoreboard players add @s rpg_ex_xp 0
execute store result storage rpg:panel v.rpg_ex_xp int 1 run scoreboard players get @s rpg_ex_xp
function rpg:panel/pages/inquest_career with storage rpg:panel v
function rpg:panel/ui/show with storage rpg:panel ui
