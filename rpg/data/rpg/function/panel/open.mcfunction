tag @s add rpg.panel.open
playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.65 1.25
data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[]}
scoreboard players add @s rpg_ex_lvl 0
execute store result storage rpg:panel v.rpg_ex_lvl int 1 run scoreboard players get @s rpg_ex_lvl
scoreboard players add @s rpg_ex_xp 0
execute store result storage rpg:panel v.rpg_ex_xp int 1 run scoreboard players get @s rpg_ex_xp
scoreboard players add @s rpg_lt_auth 0
execute store result storage rpg:panel v.rpg_lt_auth int 1 run scoreboard players get @s rpg_lt_auth
scoreboard players add @s rpg_taint 0
execute store result storage rpg:panel v.rpg_taint int 1 run scoreboard players get @s rpg_taint
function rpg:panel/pages/panel_open with storage rpg:panel v
function rpg:panel/ui/show with storage rpg:panel ui
