scoreboard players enable @s rpg_panel
scoreboard players add @s rpg_panel 0
execute if entity @s[tag=rpg.h.player_tag1,tag=!rpg.panel.open] run function rpg:panel/open
execute unless entity @s[tag=rpg.h.player_tag1] run tag @s remove rpg.panel.open
execute if score @s rpg_panel matches 1 run function rpg:inquest/career
execute if score @s rpg_panel matches 2 run function rpg:panel/inquest
execute if score @s rpg_panel matches 3 run function rpg:panel/pact
execute if score @s rpg_panel matches 4 run function rpg:panel/squad
execute if score @s rpg_panel matches 5 run function rpg:panel/hud_toggle
execute if score @s rpg_panel matches 6 run function rpg:panel/help
execute if score @s rpg_panel matches 8 run function rpg:panel/open
execute if score @s rpg_panel matches 9 run function rpg:divine/judgment/arm
execute if score @s rpg_panel matches 10 run function rpg:divine/gift
execute if score @s rpg_panel matches 1.. run scoreboard players set @s rpg_panel 0
