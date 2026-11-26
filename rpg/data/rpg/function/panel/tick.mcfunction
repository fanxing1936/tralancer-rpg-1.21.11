scoreboard players enable @s rpg_sef_do
scoreboard players enable @s rpg_panel
execute if entity @s[tag=rpg.h.player_tag1] if items entity @s weapon.mainhand minecraft:player_head run function rpg:panel/v2/head_swap
execute if score @s rpg_panel_u matches 1.. run scoreboard players remove @s rpg_panel_u 1
scoreboard players add @s rpg_panel 0
execute unless entity @s[tag=rpg.h.player_tag1] run scoreboard players set @s rpg_panel_h 0
execute if entity @s[tag=rpg.panel.open] run scoreboard players set @s rpg_panel_h 0
execute unless entity @s[tag=rpg.h.player_tag1] run tag @s remove rpg.panel.open
execute if score @s rpg_panel matches 1 run function rpg:inquest/career
execute if score @s rpg_panel matches 2 run function rpg:panel/inquest
execute if score @s rpg_panel matches 3 run function rpg:panel/pact
execute if score @s rpg_panel matches 5 run function rpg:panel/hud_toggle
execute if score @s rpg_panel matches 6 run function rpg:panel/help
execute if score @s rpg_panel matches 8 run function rpg:panel/open
execute if score @s rpg_panel matches 9 run function rpg:divine/judgment/arm
execute if score @s rpg_panel matches 10 run function rpg:divine/gift
execute if score @s rpg_panel matches 12 run function rpg:pl/page
execute if score @s rpg_panel matches 13 run function rpg:pl/enter
execute if score @s rpg_panel matches 14 run function rpg:pl/leave
execute if score @s rpg_panel matches 20 run function rpg:paths/page/list
execute if score @s rpg_panel matches 21 run function rpg:panel/v2/force
execute if score @s rpg_panel matches 22 run function rpg:events/jr/open
execute if score @s rpg_panel matches 23 run function rpg:quest/titles
execute if score @s rpg_panel matches 1.. run scoreboard players set @s rpg_panel 0
