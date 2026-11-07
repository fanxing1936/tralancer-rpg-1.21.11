data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[]}
scoreboard players add @s rpg_lt_auth 0
execute store result storage rpg:panel v.rpg_lt_auth int 1 run scoreboard players get @s rpg_lt_auth
scoreboard players add @s rpg_pact_bond 0
execute store result storage rpg:panel v.rpg_pact_bond int 1 run scoreboard players get @s rpg_pact_bond
scoreboard players add @s rpg_pact_cd 0
execute store result storage rpg:panel v.rpg_pact_cd int 1 run scoreboard players get @s rpg_pact_cd
scoreboard players add @s rpg_taint 0
execute store result storage rpg:panel v.rpg_taint int 1 run scoreboard players get @s rpg_taint
function rpg:panel/pages/panel_pact with storage rpg:panel v
function rpg:panel/ui/show with storage rpg:panel ui
